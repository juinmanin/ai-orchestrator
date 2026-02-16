from fastapi import APIRouter
from typing import List, Dict
from app.services.quota_tracker import quota_tracker

router = APIRouter(prefix="/api/guides", tags=["Guides"])


def get_platform_guide(platform_id: str) -> Dict:
    """Generate detailed guide for a platform"""
    platform_info = quota_tracker.get_platform_info(platform_id)
    
    if not platform_info:
        return {}
    
    # Generate step-by-step guide
    guide = {
        "platform_id": platform_id,
        "platform_name": platform_info["name"],
        "description": platform_info.get("description", ""),
        "icon": platform_info.get("icon", ""),
        "signup_url": platform_info.get("signup_url", ""),
        "api_docs_url": platform_info.get("api_docs_url", ""),
        "quotas": platform_info.get("quotas", []),
        "steps": []
    }
    
    # Common steps for all platforms
    guide["steps"] = [
        {
            "step": 1,
            "title": "Visit the Platform",
            "description": f"Go to {platform_info.get('signup_url', '')}",
            "tips": ["Use a dedicated email for AI platforms", "Consider using email aliases (e.g., yourname+ai@gmail.com)"]
        },
        {
            "step": 2,
            "title": "Create Account",
            "description": "Sign up with your email address",
            "tips": ["Use a strong, unique password", "Enable 2FA if available"]
        },
        {
            "step": 3,
            "title": "Verify Email",
            "description": "Check your inbox and verify your email address",
            "tips": ["Check spam folder if you don't see the email", "Make sure to complete verification"]
        },
        {
            "step": 4,
            "title": "Get API Key",
            "description": "Navigate to API settings and generate your API key",
            "tips": [
                "Store your API key securely",
                "Never share your API key publicly",
                "Copy the key immediately - some platforms only show it once"
            ]
        },
        {
            "step": 5,
            "title": "Connect to Open Crow",
            "description": "Return to Open Crow and add your account with the API key",
            "tips": [
                "Your API key is encrypted and stored securely",
                "You can disconnect anytime from the Accounts page"
            ]
        }
    ]
    
    # Platform-specific tips
    platform_tips = {
        "openai_free": [
            "ChatGPT Free has a 3-hour rolling window for quotas",
            "GPT-4o access is limited but powerful",
            "Use for complex reasoning tasks"
        ],
        "gemini_free": [
            "Gemini has both per-minute and daily limits",
            "Great for high-volume tasks within limits",
            "Google account required"
        ],
        "claude_free": [
            "Claude excels at long-form content",
            "30 messages per day - use wisely",
            "Great for writing and analysis"
        ],
        "leonardo_free": [
            "Focused on image generation",
            "150 tokens resets daily",
            "Each generation costs different token amounts"
        ],
        "huggingface_free": [
            "Access to thousands of open-source models",
            "Free tier has rate limits",
            "Great for experimentation"
        ],
        "cohere_free": [
            "Strong text generation and embeddings",
            "1000 calls per month",
            "Good for semantic search and classification"
        ]
    }
    
    guide["platform_tips"] = platform_tips.get(platform_id, [])
    
    return guide


@router.get("", response_model=List[Dict])
async def list_guides():
    """Get list of all platform guides"""
    platforms = quota_tracker.platform_data.get("platforms", [])
    
    guides = []
    for platform in platforms:
        guides.append({
            "platform_id": platform["id"],
            "platform_name": platform["name"],
            "description": platform.get("description", ""),
            "icon": platform.get("icon", ""),
            "signup_url": platform.get("signup_url", "")
        })
    
    return guides


@router.get("/{platform_id}", response_model=Dict)
async def get_guide(platform_id: str):
    """Get detailed guide for a specific platform"""
    guide = get_platform_guide(platform_id)
    
    if not guide:
        return {"error": "Platform not found"}
    
    return guide
