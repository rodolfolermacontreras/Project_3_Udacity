"""
Test script to verify all modules are working correctly
This can be run before testing with actual audio files
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing module imports...")
    
    try:
        import openai
        print("  ✓ openai")
    except ImportError:
        print("  ✗ openai - Run: pip install openai")
        return False
    
    try:
        import requests
        print("  ✓ requests")
    except ImportError:
        print("  ✗ requests - Run: pip install requests")
        return False
    
    try:
        from PIL import Image
        print("  ✓ Pillow (PIL)")
    except ImportError:
        print("  ✗ Pillow - Run: pip install pillow")
        return False
    
    try:
        import config
        print("  ✓ config.py")
    except ImportError:
        print("  ✗ config.py not found")
        return False
    
    try:
        from whisper import transcribe_audio
        print("  ✓ whisper.py")
    except Exception as e:
        print(f"  ✗ whisper.py - {e}")
        return False
    
    try:
        from dalle import generate_image
        print("  ✓ dalle.py")
    except Exception as e:
        print(f"  ✗ dalle.py - {e}")
        return False
    
    try:
        from vision import describe_image
        print("  ✓ vision.py")
    except Exception as e:
        print(f"  ✗ vision.py - {e}")
        return False
    
    try:
        from gpt import classify_with_gpt
        print("  ✓ gpt.py")
    except Exception as e:
        print(f"  ✗ gpt.py - {e}")
        return False
    
    print("\n✅ All modules imported successfully!")
    return True


def test_config():
    """Test that configuration is set up correctly"""
    print("\nTesting configuration...")
    
    try:
        import config
        
        # Check API keys
        if config.AZURE_OPENAI_API_KEY and len(config.AZURE_OPENAI_API_KEY) > 10:
            print("  ✓ AZURE_OPENAI_API_KEY is set")
        else:
            print("  ✗ AZURE_OPENAI_API_KEY is not properly configured")
            return False
        
        if config.DALLE_API_KEY and len(config.DALLE_API_KEY) > 10:
            print("  ✓ DALLE_API_KEY is set")
        else:
            print("  ✗ DALLE_API_KEY is not properly configured")
            return False
        
        # Check endpoints
        if config.AZURE_OPENAI_ENDPOINT and config.AZURE_OPENAI_ENDPOINT.startswith("https://"):
            print("  ✓ AZURE_OPENAI_ENDPOINT is set")
        else:
            print("  ✗ AZURE_OPENAI_ENDPOINT is not properly configured")
            return False
        
        # Check deployments
        if config.WHISPER_DEPLOYMENT:
            print(f"  ✓ Whisper deployment: {config.WHISPER_DEPLOYMENT}")
        
        if config.DALLE_DEPLOYMENT:
            print(f"  ✓ DALL-E deployment: {config.DALLE_DEPLOYMENT}")
        
        if config.GPT4O_DEPLOYMENT:
            print(f"  ✓ GPT-4o deployment: {config.GPT4O_DEPLOYMENT}")
        
        print("\n✅ Configuration looks good!")
        return True
    
    except Exception as e:
        print(f"\n✗ Configuration error: {e}")
        return False


def test_directories():
    """Test that required directories exist"""
    print("\nTesting directory structure...")
    
    required_dirs = ['audio', 'output']
    all_exist = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            print(f"  ✓ {dir_name}/ directory exists")
        else:
            print(f"  ✗ {dir_name}/ directory not found")
            all_exist = False
    
    if os.path.exists('categories.json'):
        print("  ✓ categories.json exists")
    else:
        print("  ✗ categories.json not found")
        all_exist = False
    
    if all_exist:
        print("\n✅ All required directories and files exist!")
    
    return all_exist


def test_audio_files():
    """Check if there are audio files to process"""
    print("\nChecking for audio files...")
    
    audio_extensions = ['.mp3', '.wav', '.m4a', '.ogg']
    audio_files = []
    
    if os.path.exists('audio'):
        for file in os.listdir('audio'):
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                audio_files.append(file)
    
    if audio_files:
        print(f"  ✓ Found {len(audio_files)} audio file(s):")
        for file in audio_files:
            print(f"    - {file}")
        return True
    else:
        print("  ⚠ No audio files found in audio/ directory")
        print("    Add an audio file (.mp3, .wav, .m4a, or .ogg) to test the system")
        return False


def main():
    """Run all tests"""
    print("=" * 70)
    print("  CUSTOMER COMPLAINT CLASSIFICATION SYSTEM - VERIFICATION TEST")
    print("=" * 70)
    print()
    
    results = {
        "imports": test_imports(),
        "config": test_config(),
        "directories": test_directories(),
        "audio": test_audio_files()
    }
    
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL" if test_name != "audio" else "⚠️  WARN"
        print(f"  {test_name.capitalize()}: {status}")
    
    all_critical_passed = results["imports"] and results["config"] and results["directories"]
    
    print("\n" + "=" * 70)
    
    if all_critical_passed:
        if results["audio"]:
            print("✅ SYSTEM READY! You can run: python main.py")
        else:
            print("✅ SYSTEM CONFIGURED! Add an audio file to audio/ and run: python main.py")
    else:
        print("❌ SYSTEM NOT READY - Fix the issues above before running")
    
    print("=" * 70)
    print()
    
    return all_critical_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
