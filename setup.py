#!/usr/bin/env python3
"""
Setup script for Google Trends Pine Seeds Repository
Helps users test the data fetching and validation locally.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr.strip() if e.stderr else str(e)}")
        return False

def check_python_version():
    """Check if Python version is adequate."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install required Python packages."""
    requirements = [
        "pytrends>=4.9.0",
        "pandas>=1.5.0", 
        "requests>=2.28.0"
    ]
    
    print("\n📦 Installing dependencies...")
    for package in requirements:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            return False
    return True

def test_data_fetch():
    """Test the data fetching functionality."""
    print("\n🧪 Testing data fetch functionality...")
    
    # Create a simple test script
    test_script = """
import sys
sys.path.append('scripts')
from fetch_trends import GoogleTrendsFetcher

# Test with a single keyword
fetcher = GoogleTrendsFetcher()
data = fetcher.fetch_trends_data('bitcoin', 'today 3-m')

if data:
    print(f"✅ Successfully fetched {len(data)} data points for Bitcoin")
    print(f"Latest data point: {data[-1][1]} (timestamp: {data[-1][0]})")
else:
    print("❌ No data fetched")
"""
    
    try:
        exec(test_script)
        return True
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def validate_structure():
    """Validate the repository structure."""
    print("\n🔍 Validating repository structure...")
    
    required_files = [
        "README.md",
        "requirements.txt",
        "scripts/fetch_trends.py",
        "scripts/validate_data.py",
        ".github/workflows/update_data.yml",
        "examples/google_trends_indicator.pine"
    ]
    
    required_dirs = [
        "data",
        "scripts",
        ".github/workflows",
        "examples"
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_files or missing_dirs:
        print("❌ Repository structure incomplete:")
        for file in missing_files:
            print(f"  Missing file: {file}")
        for dir in missing_dirs:
            print(f"  Missing directory: {dir}")
        return False
    
    print("✅ Repository structure is complete")
    return True

def create_github_repository():
    """Provide instructions for GitHub repository creation."""
    print("\n🌐 GitHub Repository Setup Instructions:")
    print("=" * 50)
    print("1. Create a new GitHub repository with the naming format:")
    print("   'seed_<your_username>_google_trends'")
    print("")
    print("2. Initialize and push this repository:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit: Google Trends Pine Seeds repository'")
    print("   git branch -M main")
    print("   git remote add origin https://github.com/<username>/<repo-name>.git")
    print("   git push -u origin main")
    print("")
    print("3. Enable GitHub Actions in your repository settings")
    print("")
    print("4. The workflow will run automatically daily at 10:00 UTC")
    print("   You can also trigger it manually from the Actions tab")
    print("")
    print("5. In TradingView Pine Script, use:")
    print("   request.seed('<your_github_username>', 'GOOGL_TRENDS_BITCOIN', 'close')")

def main():
    """Main setup function."""
    print("🚀 Google Trends Pine Seeds Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Validate repository structure
    if not validate_structure():
        print("\n⚠️  Some files may be missing. Please ensure all files are present.")
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies. Please install manually:")
        print("pip install pytrends pandas requests")
        sys.exit(1)
    
    # Test data fetching
    print("\n⚠️  Testing data fetch (this may take a moment)...")
    if test_data_fetch():
        print("✅ Data fetching test passed")
    else:
        print("⚠️  Data fetching test failed. Check your internet connection.")
    
    # Test validation
    if run_command("python scripts/validate_data.py", "Testing data validation"):
        print("✅ Data validation working correctly")
    
    # GitHub setup instructions
    create_github_repository()
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Follow the GitHub repository setup instructions above")
    print("2. Wait for the first automated data update (or trigger manually)")
    print("3. Use the Pine Script example in examples/google_trends_indicator.pine")
    print("4. Replace 'YOUR_GITHUB_USERNAME' with your actual GitHub username")

if __name__ == "__main__":
    main() 