#!/usr/bin/env python
"""
Run this script after migrations to set up initial data.
Usage: python setup_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ethics_project.settings')
django.setup()

from blog.models import Category
from django.contrib.auth.models import User

CATEGORIES = [
    ('Films',                 'films'),
    ('Theatre Plays',         'theatre-plays'),
    ('Literary Texts',        'literary-texts'),
    ('Clinical Ethics Cases', 'clinical-ethics-cases'),
    ('Ethics News',           'ethics-news'),
]

print("Creating categories...")
for name, slug in CATEGORIES:
    obj, created = Category.objects.get_or_create(slug=slug, defaults={'name': name})
    print(f"  {'Created' if created else 'Exists'}: {name}")

print("\nCreating editor account...")
if not User.objects.filter(username='editor').exists():
    editor = User.objects.create_user('editor', 'editor@medethics.com', 'editor1234')
    editor.is_staff = True
    editor.save()
    print("  Editor account created!")
    print("  Username : editor")
    print("  Password : editor1234")
else:
    print("  Editor account already exists.")

print("\nDone! Run: python manage.py runserver")
