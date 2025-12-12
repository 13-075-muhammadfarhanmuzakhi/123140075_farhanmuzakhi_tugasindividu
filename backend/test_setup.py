import sys

def test_imports():
    """Test all required imports"""
    print("=" * 50)
    print("Testing Imports...")
    print("=" * 50)
    
    try:
        import pyramid
        print("✓ Pyramid imported successfully")
    except ImportError as e:
        print(f"✗ Pyramid import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✓ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"✗ SQLAlchemy import failed: {e}")
        return False
    
    try:
        import psycopg2
        print("✓ psycopg2 imported successfully")
    except ImportError as e:
        print(f"✗ psycopg2 import failed: {e}")
        return False
    
    try:
        from transformers import pipeline
        print("✓ Transformers imported successfully")
    except ImportError as e:
        print(f"✗ Transformers import failed: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✓ Google Generative AI imported successfully")
    except ImportError as e:
        print(f"✗ Google Generative AI import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ python-dotenv import failed: {e}")
        return False
    
    return True

def test_env_file():
    """Test .env file exists and has required keys"""
    print("\n" + "=" * 50)
    print("Testing .env Configuration...")
    print("=" * 50)
    
    import os
    from dotenv import load_dotenv
    
    if not os.path.exists('.env'):
        print("✗ .env file not found!")
        print("  Create .env file with:")
        print("  DATABASE_URL=postgresql://review_user:password@localhost/product_reviews")
        print("  HUGGINGFACE_API_KEY=your_key_here")
        print("  GEMINI_API_KEY=your_key_here")
        return False
    
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    hf_key = os.getenv('HUGGINGFACE_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not database_url:
        print("✗ DATABASE_URL not set in .env")
        return False
    print(f"✓ DATABASE_URL found: {database_url[:30]}...")
    
    if not hf_key:
        print("⚠ HUGGINGFACE_API_KEY not set (optional but recommended)")
    else:
        print(f"✓ HUGGINGFACE_API_KEY found: {hf_key[:10]}...")
    
    if not gemini_key:
        print("✗ GEMINI_API_KEY not set in .env")
        return False
    print(f"✓ GEMINI_API_KEY found: {gemini_key[:10]}...")
    
    return True

def test_database():
    """Test database connection"""
    print("\n" + "=" * 50)
    print("Testing Database Connection...")
    print("=" * 50)
    
    try:
        from sqlalchemy import create_engine
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        database_url = os.getenv('DATABASE_URL')
        
        engine = create_engine(database_url)
        connection = engine.connect()
        connection.close()
        print("✓ Database connection successful!")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check database credentials in .env")
        print("3. Try: psql -U review_user -d product_reviews")
        return False

def test_models():
    """Test model initialization"""
    print("\n" + "=" * 50)
    print("Testing Model Initialization...")
    print("=" * 50)
    
    try:
        from transformers import pipeline
        print("Loading sentiment analysis model...")
        analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        print("✓ Sentiment analysis model loaded")
        
        # Test prediction
        result = analyzer("This is a test")[0]
        print(f"✓ Model test successful: {result}")
        return True
    except Exception as e:
        print(f"✗ Model initialization failed: {e}")
        return False

if __name__ == '__main__':
    print("\n🔍 Product Review Analyzer - Setup Test\n")
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
        print("\n❌ Import test failed. Install missing packages:")
        print("pip install pyramid waitress sqlalchemy psycopg2-binary transformers torch google-generativeai python-dotenv")
        sys.exit(1)
    
    if not test_env_file():
        all_passed = False
    
    if not test_database():
        all_passed = False
    
    if not test_models():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed! You can run the app now.")
        print("Run: python app.py")
    else:
        print("❌ Some tests failed. Fix the issues above.")
    print("=" * 50 + "\n")
