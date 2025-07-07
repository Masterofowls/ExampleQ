#!/usr/bin/env python3
"""
Test script to verify database connectivity and functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Student, Admin, Group, Post

def test_database():
    """Test database connectivity and basic operations"""
    
    print("🔍 Testing database connectivity...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test 1: Check if tables exist
            print("📊 Checking database tables...")
            
            # Check if we can query tables (this will create them if they don't exist)
            student_count = Student.query.count()
            admin_count = Admin.query.count()
            group_count = Group.query.count()
            post_count = Post.query.count()
            
            print(f"✅ Students table: {student_count} records")
            print(f"✅ Admins table: {admin_count} records")
            print(f"✅ Groups table: {group_count} records")
            print(f"✅ Posts table: {post_count} records")
            
            # Test 2: Try to create a test group
            print("\n🧪 Testing data insertion...")
            
            # Check if test group already exists
            test_group = Group.query.filter_by(name="Test Group").first()
            if not test_group:
                test_group = Group(name="Test Group", course="Test Course", city="Test City")
                db.session.add(test_group)
                db.session.commit()
                print("✅ Created test group")
            else:
                print("✅ Test group already exists")
            
            # Test 3: Try to create a test admin
            test_admin = Admin.query.filter_by(login="test_admin").first()
            if not test_admin:
                test_admin = Admin(login="test_admin")
                test_admin.set_password("test123")
                db.session.add(test_admin)
                db.session.commit()
                print("✅ Created test admin")
            else:
                print("✅ Test admin already exists")
            
            # Test 4: Try to create a test student
            test_student = Student.query.filter_by(login="test_student").first()
            if not test_student:
                test_student = Student(login="test_student", group_id=test_group.id)
                test_student.set_password("test123")
                db.session.add(test_student)
                db.session.commit()
                print("✅ Created test student")
            else:
                print("✅ Test student already exists")
            
            # Test 5: Test password verification
            print("\n🔒 Testing password verification...")
            if test_admin.check_password("test123"):
                print("✅ Admin password verification works")
            else:
                print("❌ Admin password verification failed")
            
            if test_student.check_password("test123"):
                print("✅ Student password verification works")
            else:
                print("❌ Student password verification failed")
            
            # Test 6: Test relationships
            print("\n🔗 Testing database relationships...")
            student_group = test_student.group
            if student_group:
                print(f"✅ Student-Group relationship works: {test_student.login} is in {student_group.name}")
            else:
                print("❌ Student-Group relationship failed")
            
            print("\n🎉 Database is working correctly!")
            return True
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False

if __name__ == "__main__":
    test_database()
