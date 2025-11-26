"""Encryption service for credentials."""
import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from app.config import settings


class EncryptionService:
    """Service for encrypting and decrypting credentials."""
    
    @staticmethod
    def encrypt(plaintext: str, master_key: bytes | None = None) -> tuple[str, str, str]:
        """
        Encrypt plaintext using AES-256-GCM.
        
        Args:
            plaintext: Text to encrypt
            master_key: Master encryption key (defaults to settings)
            
        Returns:
            Tuple of (encrypted_hex, salt_hex, nonce_hex)
        """
        if master_key is None:
            master_key = settings.MASTER_ENCRYPTION_KEY.encode()
        
        # Generate salt
        salt = os.urandom(32)
        
        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(master_key)
        
        # Encrypt with AES-GCM
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
        
        return ciphertext.hex(), salt.hex(), nonce.hex()
    
    @staticmethod
    def decrypt(encrypted_hex: str, salt_hex: str, nonce_hex: str, master_key: bytes | None = None) -> str:
        """
        Decrypt encrypted text.
        
        Args:
            encrypted_hex: Encrypted data as hex string
            salt_hex: Salt as hex string
            nonce_hex: Nonce as hex string
            master_key: Master encryption key (defaults to settings)
            
        Returns:
            Decrypted plaintext
        """
        if master_key is None:
            master_key = settings.MASTER_ENCRYPTION_KEY.encode()
        
        # Decode hex
        ciphertext = bytes.fromhex(encrypted_hex)
        salt = bytes.fromhex(salt_hex)
        nonce = bytes.fromhex(nonce_hex)
        
        # Derive key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(master_key)
        
        # Decrypt
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        return plaintext.decode()
    
    @staticmethod
    def encrypt_oauth_tokens(access_token: str, refresh_token: str = None, master_key: bytes | None = None) -> tuple[str, str, str]:
        """
        Encrypt OAuth tokens (access_token and refresh_token).
        
        Args:
            access_token: OAuth access token
            refresh_token: OAuth refresh token (optional)
            master_key: Master encryption key (defaults to settings)
            
        Returns:
            Tuple of (ciphertext_hex, salt_hex, nonce_hex)
        """
        import json
        tokens_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        tokens_json = json.dumps(tokens_data)
        return EncryptionService.encrypt(tokens_json, master_key)
    
    @staticmethod
    def decrypt_oauth_tokens(ciphertext_hex: str, salt_hex: str, nonce_hex: str, master_key: bytes | None = None) -> dict:
        """
        Decrypt OAuth tokens.
        
        Args:
            ciphertext_hex: Encrypted tokens (hex)
            salt_hex: Salt (hex)
            nonce_hex: Nonce (hex)
            master_key: Master encryption key (defaults to settings)
            
        Returns:
            Dictionary with access_token and refresh_token
        """
        import json
        plaintext = EncryptionService.decrypt(ciphertext_hex, salt_hex, nonce_hex, master_key)
        return json.loads(plaintext)

