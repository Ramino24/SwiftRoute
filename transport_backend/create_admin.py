import os
import django

# This must match the folder name where your settings.py lives
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transport_backend.settings') 
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
email = 'admin@example.com' # Use this to log in
password = 'YourSecurePassword123'

if not User.objects.filter(email=email).exists():
    # Since your admin.py uses 'email' as the primary identifier
    User.objects.create_superuser(
        email=email, 
        password=password,
        first_name="System",
        last_name="Admin",
        role="park_admin" # Matches your role_display logic and frontend check
    )
    print("Superuser created successfully.")
else:
    print("Superuser already exists.")