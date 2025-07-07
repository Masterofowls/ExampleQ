#!/usr/bin/env python3
"""
Simple database viewer to show current data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Admin, Group, Post

def show_database_content():
    """Display all data in the database"""
    
    app = create_app()
    
    with app.app_context():
        print("📊 Current Database Content")
        print("=" * 50)
        
        # Show all groups
        print("\n🏫 Groups:")
        groups = Group.query.all()
        for group in groups:
            print(f"  ID: {group.id}, Name: {group.name}, Course: {group.course}, City: {group.city}")
        
        # Show all admins
        print("\n👨‍💼 Admins:")
        admins = Admin.query.all()
        for admin in admins:
            print(f"  ID: {admin.id}, Login: {admin.login}, Created: {admin.created_at}")
        
        # Show all students
        print("\n👨‍🎓 Students:")
        print("  Студенты теперь не сохраняются в базе данных")
        print("  Они входят через выбор группы и хранятся только в сессии")
        
        # Show all posts
        print("\n📝 Posts:")
        posts = Post.query.all()
        if posts:
            for post in posts:
                print(f"  ID: {post.id}, Title: {post.title}, Status: {post.status}, Admin: {post.admin.login}")
        else:
            print("  No posts yet")
        
        print("\n✅ Database query completed successfully!")

if __name__ == "__main__":
    show_database_content()
