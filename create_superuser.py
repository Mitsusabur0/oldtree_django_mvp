# create_superuser.py

import os
import django
from django.contrib.auth import get_user_model

# This is required to set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oldtree_project.settings')
django.setup()

User = get_user_model()

# Get the superuser credentials from environment variables
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

# Create the superuser only if the credentials are provided AND the user does not already exist
if username and email and password and not User.objects.filter(username=username).exists():
    print(f"Creating superuser: {username}")
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully.")
else:
    print("Superuser already exists or environment variables are not set. Skipping creation.")