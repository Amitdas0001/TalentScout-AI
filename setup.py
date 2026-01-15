"""
Setup Script for TalentScout Hiring Assistant
==============================================
Automated setup and configuration
"""

import os
import sys
from pathlib import Path


def create_directories():
    """Create necessary directories"""
    directories = [
        "candidate_data",
        "candidate_data/json",
        "candidate_data/exports",
        ".streamlit"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")


def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists(".env"):
        with open(".env.example", "r") as example:
            content = example.read()
        
        with open(".env", "w") as env_file:
            env_file.write(content)
        
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env and add your HUGGINGFACE_API_KEY")
    else:
        print("ℹ️  .env file already exists")


def create_streamlit_config():
    """Create Streamlit configuration"""
    config_content = """# Streamlit Configuration

[theme]
primaryColor = "#667eea"
backgroundColor = "#f0f2f6"
secondaryBackgroundColor = "#ffffff"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 5

[browser]
gatherUsageStats = false
"""
    
    config_path = Path(".streamlit/config.toml")
    with open(config_path, "w") as f:
        f.write(config_content)
    
    print("✅ Created Streamlit configuration")


def check_dependencies():
    """Check if dependencies are installed"""
    try:
        import streamlit
        import huggingface_hub
        import dotenv
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e.name}")
        print("Run: pip install -r requirements.txt")
        return False


def main():
    """Main setup function"""
    print("=" * 50)
    print("TalentScout Hiring Assistant - Setup")
    print("=" * 50)
    print()
    
    # Create directories
    print("Creating directories...")
    create_directories()
    print()
    
    # Create .env file
    print("Setting up environment variables...")
    create_env_file()
    print()
    
    # Create Streamlit config
    print("Creating Streamlit configuration...")
    create_streamlit_config()
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    if check_dependencies():
        print()
        print("=" * 50)
        print("✅ Setup complete!")
        print("=" * 50)
        print()
        print("Next steps:")
        print("1. Edit .env and add your HUGGINGFACE_API_KEY")
        print("2. Run: streamlit run app.py")
        print()
    else:
        print()
        print("⚠️  Please install dependencies first:")
        print("pip install -r requirements.txt")


if __name__ == "__main__":
    main()
