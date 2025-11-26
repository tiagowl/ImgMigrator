"""
Vercel serverless entry point.
This file is required for Vercel to properly handle the FastAPI app.
"""
from app.main import app

# Export app for Vercel
__all__ = ["app"]






