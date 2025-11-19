"""
Setup MySQL Database - Create tables and insert sample data
Run this script to set up your database
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def read_sql_file(filename):
    """Read SQL file"""
    filepath = os.path.join('database', filename)
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def execute_sql_file(connection, filename, description):
    """Execute SQL file"""
    print(f"\n{'='*60}")
    print(f"Executing: {description}")
    print(f"{'='*60}")
    
    sql_content = read_sql_file(filename)
    if not sql_content:
        return False
    
    cursor = connection.cursor()
    
    # Split by semicolon and execute each statement
    # Remove comments and empty lines
    lines = sql_content.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('--'):
            cleaned_lines.append(line)
    
    # Join and split by semicolon
    full_text = ' '.join(cleaned_lines)
    statements = [s.strip() for s in full_text.split(';') if s.strip()]
    
    success_count = 0
    error_count = 0
    
    for i, statement in enumerate(statements, 1):
        try:
            if statement:
                cursor.execute(statement)
                success_count += 1
                print(f"[OK] Statement {i}/{len(statements)} executed")
        except Error as e:
            error_count += 1
            print(f"[ERROR] Error in statement {i}: {str(e)[:100]}")
            print(f"      Statement: {statement[:50]}...")
    
    connection.commit()
    cursor.close()
    
    print(f"\nResults: {success_count} successful, {error_count} errors")
    return error_count == 0

def setup_database():
    """Main setup function"""
    print("=" * 60)
    print("Project Recommendation System - MySQL Database Setup")
    print("=" * 60)
    
    # Database configuration
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', '@yush2004'),
    }
    
    print(f"\nConnecting to MySQL...")
    print(f"  Host: {db_config['host']}")
    print(f"  Port: {db_config['port']}")
    print(f"  User: {db_config['user']}")
    
    try:
        # First connect without database to create it
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password']
        )
        
        print("[OK] Connected to MySQL server!\n")
        
        # Create database if not exists
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS project_recommender")
        cursor.execute("USE project_recommender")
        cursor.close()
        connection.close()
        
        print("[OK] Database 'project_recommender' created/selected\n")
        
        # Reconnect with database
        db_config['database'] = 'project_recommender'
        connection = mysql.connector.connect(**db_config)
        
        # Execute schema
        schema_success = execute_sql_file(connection, 'mysql_schema.sql', 'Database Schema (5 Tables)')
        
        if schema_success:
            # Execute sample data
            execute_sql_file(connection, 'mysql_sample_data.sql', 'Sample Data')
        
        connection.close()
        
        print("\n" + "=" * 60)
        print("[OK] Database setup completed!")
        print("=" * 60)
        print("\nCreated 5 tables:")
        print("  1. STUDENTS")
        print("  2. SKILLS")
        print("  3. STUDENT_SKILLS")
        print("  4. PROJECTS")
        print("  5. PROJECT_SKILLS")
        print("\nNext steps:")
        print("  1. Update backend/.env with your credentials")
        print("  2. Start backend: python app.py")
        print("  3. Test API: curl http://localhost:5000/api/health")
        
        return True
        
    except Error as e:
        print(f"\n[ERROR] Error: {str(e)}")
        print("\nPlease check:")
        print("  1. MySQL is running")
        print("  2. Credentials are correct")
        print("  3. You have necessary permissions")
        return False

if __name__ == '__main__':
    setup_database()

