from cryptography.fernet import Fernet
from app.config import settings
import base64
import hashlib


class EncryptionService:
    """Service for encrypting/decrypting sensitive data using Fernet"""
    
    def __init__(self):
        # Derive a valid Fernet key from the encryption key in settings
        key_bytes = settings.encryption_key.encode()
        # Hash to ensure we have 32 bytes, then base64 encode for Fernet
        hashed = hashlib.sha256(key_bytes).digest()
        self.key = base64.urlsafe_b64encode(hashed)
        self.cipher = Fernet(self.key)
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext string"""
        if not plaintext:
            return ""
        encrypted_bytes = self.cipher.encrypt(plaintext.encode())
        return encrypted_bytes.decode()
    
    def decrypt(self, encrypted_text: str) -> str:
        """Decrypt encrypted string"""
        if not encrypted_text:
            return ""
        decrypted_bytes = self.cipher.decrypt(encrypted_text.encode())
        return decrypted_bytes.decode()
    
    def mask_api_key(self, api_key: str, visible_chars: int = 4) -> str:
        """Mask API key for display (e.g., 'sk-...xxxx')"""
        if not api_key or len(api_key) <= visible_chars:
            return "***"
        return f"{api_key[:3]}...{api_key[-visible_chars:]}"


# Singleton instance
encryption_service = EncryptionService()
