#!/usr/bin/env python3
"""
Test script to verify Flask app can start without errors
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all imports work correctly"""
    try:
        print("Testing imports...")
        
        # Test basic Flask imports
        from flask import Flask
        print("✓ Flask imported successfully")
        
        # Test our app imports
        from src.main import app
        print("✓ Main app imported successfully")
        
        # Test configuration
        from src.config import get_config
        config = get_config()
        print("✓ Configuration loaded successfully")
        
        # Test database
        from src.database import init_database
        print("✓ Database module imported successfully")
        
        # Test services
        from src.services.ai_service import AIService
        from src.services.communication_service import CommunicationService
        from src.services.social_service import SocialService
        from src.services.crm_service import CRMService
        from src.services.content_service import ContentService
        from src.services.automation_service import AutomationService
        from src.services.analytics_service import AnalyticsService
        print("✓ All services imported successfully")
        
        # Test models
        from src.models.user import User, Tenant
        from src.models.content import Content
        from src.models.crm import Customer
        print("✓ All models imported successfully")
        
        print("\n🎉 All imports successful! The app should start without issues.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_app_startup():
    """Test that the app can be created without errors"""
    try:
        print("\nTesting app startup...")
        
        from src.main import app
        
        # Test that the app has the expected attributes
        assert hasattr(app, 'config'), "App should have config"
        assert hasattr(app, 'route'), "App should have route decorator"
        
        print("✓ App created successfully")
        print("✓ App has expected attributes")
        
        # Test health endpoint
        with app.test_client() as client:
            response = client.get('/health')
            print(f"✓ Health endpoint responds with status: {response.status_code}")
        
        print("\n🎉 App startup test successful!")
        return True
        
    except Exception as e:
        print(f"❌ App startup error: {e}")
        return False

if __name__ == '__main__':
    print("CloudBoost AI - Flask App Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test app startup
        startup_ok = test_app_startup()
        
        if startup_ok:
            print("\n✅ All tests passed! The Flask app is ready for deployment.")
            sys.exit(0)
        else:
            print("\n❌ App startup test failed.")
            sys.exit(1)
    else:
        print("\n❌ Import test failed.")
        sys.exit(1) 