#!/usr/bin/env python3
"""
Simple MongoDB connection test script
"""
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from pymongo import MongoClient
    import pymongo
    
    print("Testing MongoDB connection...")
    
    # Try to connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    
    # Test the connection
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
    
    # List databases
    databases = client.list_database_names()
    print(f"Available databases: {databases}")
    
    # Test creating a test database and collection
    db = client["test_db"]
    collection = db["test_collection"]
    
    # Insert a test document
    test_doc = {"test": "connection", "timestamp": "2024-01-01"}
    result = collection.insert_one(test_doc)
    print(f"✅ Test document inserted with ID: {result.inserted_id}")
    
    # Find the document
    found_doc = collection.find_one({"test": "connection"})
    print(f"✅ Test document found: {found_doc}")
    
    # Clean up
    collection.drop()
    client.drop_database("test_db")
    print("✅ Test database cleaned up")
    
    client.close()
    print("✅ MongoDB connection test completed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Installing required packages...")
    os.system("pip install pymongo")
    
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("Make sure MongoDB is running on localhost:27017")
    sys.exit(1)
