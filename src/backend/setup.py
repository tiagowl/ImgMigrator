"""Setup script for the backend."""
import os
import sys

def setup():
    """Setup the backend environment."""
    print("Setting up Cloud Migrate Backend...")
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("Creating .env from env.example...")
        if os.path.exists("env.example"):
            with open("env.example", "r") as f:
                content = f.read()
            with open(".env", "w") as f:
                f.write(content)
            print("✓ .env created. Please edit it with your configuration.")
        else:
            print("⚠ env.example not found. Please create .env manually.")
    
    # Initialize database
    print("\nInitializing database...")
    try:
        from app.database import init_db
        init_db()
        print("✓ Database initialized successfully!")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        sys.exit(1)
    
    print("\n✓ Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env with your configuration")
    print("2. Run: uvicorn app.main:app --reload")
    print("3. Access API docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    setup()



