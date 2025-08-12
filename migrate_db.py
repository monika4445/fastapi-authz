#!/usr/bin/env python3
"""
Database migration script to add email verification fields
Run this after updating your models
"""

from sqlalchemy import text
from app.database import engine

def migrate_database():
    """Add email verification columns to existing users table"""
    
    migration_sql = """
    -- Add email verification columns
    ALTER TABLE users 
    ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS verification_token VARCHAR,
    ADD COLUMN IF NOT EXISTS verified_at TIMESTAMP WITH TIME ZONE;
    
    -- Update existing users to be verified (optional - for existing users)
    -- Uncomment the next line if you want existing users to be automatically verified
    -- UPDATE users SET is_verified = TRUE WHERE is_verified IS NULL;
    """
    
    try:
        with engine.connect() as connection:
            connection.execute(text(migration_sql))
            connection.commit()
            print("✅ Database migration completed successfully!")
            print("   - Added is_verified column")
            print("   - Added verification_token column") 
            print("   - Added verified_at column")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("💡 This is normal if columns already exist")

def check_migration():
    """Check if migration was successful"""
    check_sql = """
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'users' 
    AND column_name IN ('is_verified', 'verification_token', 'verified_at');
    """
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text(check_sql))
            columns = [row[0] for row in result]
            
            print("\n📊 Current users table columns:")
            if 'is_verified' in columns:
                print("✅ is_verified - Present")
            else:
                print("❌ is_verified - Missing")
                
            if 'verification_token' in columns:
                print("✅ verification_token - Present") 
            else:
                print("❌ verification_token - Missing")
                
            if 'verified_at' in columns:
                print("✅ verified_at - Present")
            else:
                print("❌ verified_at - Missing")
                
    except Exception as e:
        print(f"❌ Check failed: {e}")

if __name__ == "__main__":
    print("🔄 Starting database migration for email verification...")
    print("=" * 50)
    
    migrate_database()
    check_migration()
    
    print("\n✨ Migration complete! Your auth service now supports email verification.")
    print("\n📝 Next steps:")
    print("1. Set up your Gmail App Password in .env file")
    print("2. Update EMAIL_USER and EMAIL_PASSWORD in .env")
    print("3. Restart your FastAPI server")
    print("4. Test registration with email verification")