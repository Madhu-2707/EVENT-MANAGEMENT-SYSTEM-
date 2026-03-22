
import os
import django
import requests
from django.core.files.base import ContentFile

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from core.models import Service

# Precise mapping with vetted high-quality Unsplash images
SERVICE_DATA = {
    'Catering': {
        'url': 'https://images.unsplash.com/photo-1555244162-803834f70033?w=1200&q=80',
    },
    'Photography': {
        'url': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=1200&q=80', # Camera lens
    },
    'Wedding Events': {
        'url': 'https://images.unsplash.com/photo-1519741497674-611481863552?w=1200&q=80', # Wedding flowers
    },
    'Birthday Parties': {
        'url': 'https://images.unsplash.com/photo-1530103862676-fa8c9d34b3b7?w=1200&q=80', # Party balloons
    },
    'Corporate Events': {
        'url': 'https://images.unsplash.com/photo-1511578314322-379afb476865?w=1200&q=80', # Corporate hall
    },
    'Engagement Functions': {
        'url': 'https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=1200&q=80', # Engagement ring/flowers
    },
    'Baby Shower': {
        'url': 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200&q=80', # Pastel decor/flowers
    },
    'College Fest': {
        'url': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=1200&q=80', # Crowd/Festival
    },
    'Anniversary Celebration': {
        'url': 'https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=1200&q=80', # Romantic outdoor setup
    },
    'House Warming Ceremony': {
        'url': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=1200&q=80', # Traditional warm interior
    },
    'Product Launch Event': {
        'url': 'https://images.unsplash.com/photo-1505373877841-8d25f7d46678?w=1200&q=80', # Tech stage/presentation
    },
    'Cultural Events': {
        'url': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=1200&q=80', # Celebration/Festival
    },
    'Music Concert Events': {
        'url': 'https://images.unsplash.com/photo-1459749411177-042180ce673c?w=1200&q=80', # Concert stage
    },
    'Premium Wedding Package': {
        'url': 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=1200&q=80', # Grand wedding hall
    },
    'Corporate Annual Gala': {
        'url': 'https://images.unsplash.com/photo-1461280360983-bd93eaa5ec61?w=1200&q=80', # Red carpet gala
    },
    'Photo/Videography': {
        'url': 'https://images.unsplash.com/photo-1452626038306-9aae5e071dd3?w=1200&q=80', # Photographer with camera
    },
    'Sound System': {
        'url': 'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=1200&q=80', # Audio mixer/faders
    },
    'Stage Decoration': {
        'url': 'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=1200&q=80', # Event stage
    },
    'DJ': {
        'url': 'https://images.unsplash.com/photo-1598387181032-a3103a2db5b3?w=1200&q=80', # DJ controller
    },
    'Lighting': {
        'url': 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=1200&q=80', # Fairy lights/lighting
    },
    'Makeup': {
        'url': 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=1200&q=80', # Makeup palette/brushes
    }
}

def update_images():
    print("Correcting service images with curated photography...")
    for name, data in SERVICE_DATA.items():
        try:
            service = Service.objects.filter(name=name).first()
            if service:
                print(f"Updating {name}...")
                response = requests.get(data['url'], timeout=15)
                if response.status_code == 200:
                    img_name = f"{name.lower().replace(' ', '_').replace('/', '_')}_v2.jpg"
                    service.image.save(img_name, ContentFile(response.content), save=True)
                    print(f"✅ Success: {name}")
                else:
                    print(f"❌ Failed: {name} (Status: {response.status_code})")
            else:
                print(f"⚠️ Service '{name}' not found in database.")
        except Exception as e:
            print(f"🛑 Error for {name}: {e}")

    print("Correction complete!")

if __name__ == '__main__':
    update_images()
