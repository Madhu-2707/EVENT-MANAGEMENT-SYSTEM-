
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from core.models import Gallery

gallery_count = Gallery.objects.count()
print(f"Total Gallery Items: {gallery_count}")

for i in Gallery.objects.all():
    print(f"Category: {i.category}")
    print(f"  Image: {i.image.name if i.image else 'NONE'}")
    if i.image:
        print(f"  URL: {i.image.url}")
        print(f"  Path Exists: {os.path.exists(i.image.path)}")
