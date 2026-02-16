from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.platform_account import PlatformAccount
from app.models.usage_log import UsageLog
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse, AccountVerifyResponse, QuotaInfo
from app.routers.auth import get_current_user
from app.services.encryption import encryption_service
from app.services.quota_tracker import quota_tracker
from datetime import datetime

router = APIRouter(prefix="/api/accounts", tags=["Accounts"])


@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Register a new platform account"""
    # Verify platform exists
    platform_info = quota_tracker.get_platform_info(account_data.platform_id)
    if not platform_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown platform: {account_data.platform_id}"
        )
    
    # Encrypt API key
    encrypted_key = encryption_service.encrypt(account_data.api_key)
    
    # Create account
    new_account = PlatformAccount(
        user_id=current_user.id,
        platform_id=account_data.platform_id,
        account_identifier=account_data.account_identifier,
        encrypted_api_key=encrypted_key
    )
    
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    
    # Initialize quotas
    await quota_tracker.initialize_quotas(db, new_account.id, account_data.platform_id)
    
    # Log action
    log = UsageLog(
        user_id=current_user.id,
        account_id=new_account.id,
        action="account_created",
        details=f"Added {account_data.platform_id} account"
    )
    db.add(log)
    await db.commit()
    
    # Get quotas for response
    quotas = await quota_tracker.get_quota_status(db, new_account.id)
    quota_responses = [QuotaInfo(**q) for q in quotas]
    
    return AccountResponse(
        id=new_account.id,
        platform_id=new_account.platform_id,
        account_identifier=new_account.account_identifier,
        api_key_preview=encryption_service.mask_api_key(account_data.api_key),
        is_verified=new_account.is_verified,
        last_verified_at=new_account.last_verified_at,
        created_at=new_account.created_at,
        quotas=quota_responses
    )


@router.get("", response_model=List[AccountResponse])
async def list_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all user's platform accounts"""
    result = await db.execute(
        select(PlatformAccount).where(PlatformAccount.user_id == current_user.id)
    )
    accounts = result.scalars().all()
    
    response = []
    for account in accounts:
        # Decrypt to get preview (we only show masked version)
        decrypted_key = encryption_service.decrypt(account.encrypted_api_key)
        api_key_preview = encryption_service.mask_api_key(decrypted_key)
        
        # Get quotas
        quotas = await quota_tracker.get_quota_status(db, account.id)
        quota_responses = [QuotaInfo(**q) for q in quotas]
        
        response.append(AccountResponse(
            id=account.id,
            platform_id=account.platform_id,
            account_identifier=account.account_identifier,
            api_key_preview=api_key_preview,
            is_verified=account.is_verified,
            last_verified_at=account.last_verified_at,
            created_at=account.created_at,
            quotas=quota_responses
        ))
    
    return response


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get account details with quota information"""
    result = await db.execute(
        select(PlatformAccount).where(
            PlatformAccount.id == account_id,
            PlatformAccount.user_id == current_user.id
        )
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Decrypt to get preview
    decrypted_key = encryption_service.decrypt(account.encrypted_api_key)
    api_key_preview = encryption_service.mask_api_key(decrypted_key)
    
    # Get quotas
    quotas = await quota_tracker.get_quota_status(db, account.id)
    quota_responses = [QuotaInfo(**q) for q in quotas]
    
    return AccountResponse(
        id=account.id,
        platform_id=account.platform_id,
        account_identifier=account.account_identifier,
        api_key_preview=api_key_preview,
        is_verified=account.is_verified,
        last_verified_at=account.last_verified_at,
        created_at=account.created_at,
        quotas=quota_responses
    )


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete platform account (disconnect)"""
    result = await db.execute(
        select(PlatformAccount).where(
            PlatformAccount.id == account_id,
            PlatformAccount.user_id == current_user.id
        )
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Log action before deletion
    log = UsageLog(
        user_id=current_user.id,
        action="account_deleted",
        details=f"Deleted {account.platform_id} account"
    )
    db.add(log)
    
    # Delete account (cascades to quotas and logs)
    await db.delete(account)
    await db.commit()
    
    return None


@router.post("/{account_id}/verify", response_model=AccountVerifyResponse)
async def verify_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Verify platform account connection"""
    result = await db.execute(
        select(PlatformAccount).where(
            PlatformAccount.id == account_id,
            PlatformAccount.user_id == current_user.id
        )
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # For MVP, we'll do a simple verification
    # In production, this would test actual API calls to each platform
    try:
        # Decrypt API key to verify it's accessible
        decrypted_key = encryption_service.decrypt(account.encrypted_api_key)
        
        if not decrypted_key:
            return AccountVerifyResponse(
                success=False,
                message="API key is empty or invalid",
                details=None
            )
        
        # Update verification status
        account.is_verified = True
        account.last_verified_at = datetime.utcnow()
        await db.commit()
        
        # Log action
        log = UsageLog(
            user_id=current_user.id,
            account_id=account.id,
            action="account_verified",
            details=f"Verified {account.platform_id} account"
        )
        db.add(log)
        await db.commit()
        
        return AccountVerifyResponse(
            success=True,
            message="Account verified successfully",
            details={"platform_id": account.platform_id}
        )
    
    except Exception as e:
        return AccountVerifyResponse(
            success=False,
            message=f"Verification failed: {str(e)}",
            details=None
        )
