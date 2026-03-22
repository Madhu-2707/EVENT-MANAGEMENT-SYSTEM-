
import os
import django
import requests
from django.core.files.base import ContentFile

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from core.models import Service

# Clear existing services to avoid confusion with the new package structure
# or just update them. The user wants a specific structure.
# Let's clear and rebuild for a clean package-based experience.

PACKAGE_SERVICES = [
    # BUDGET PACKAGE
    {
        'name': 'Basic Catering',
        'package_type': 'Budget',
        'description': 'Essential buffet with standard dishes, perfect for intimate gatherings and budget-friendly events.',
        'price': 10000,
        'url': 'https://images.unsplash.com/photo-1555244162-803834f70033?w=800&q=80'
    },
    {
        'name': 'Simple Decoration',
        'package_type': 'Budget',
        'description': 'Elegant yet minimal decor featuring seasonal flowers and basic lighting for a warm atmosphere.',
        'price': 5000,
        'url': 'https://images.unsplash.com/photo-1513151233558-d860c5398176?w=800&q=80'
    },
    {
        'name': 'Basic Photography',
        'package_type': 'Budget',
        'description': 'Professional coverage of your main event moments with high-quality digital delivery.',
        'price': 8000,
        'url': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&q=80'
    },
    {
        'name': 'Basic Lighting',
        'package_type': 'Budget',
        'description': 'Standard ambient lighting to ensure your venue is bright and welcoming.',
        'price': 3000,
        'url': 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&q=80'
    },
    {
        'name': 'Basic Sound Setup',
        'package_type': 'Budget',
        'description': 'Essential audio equipment for clear speeches and ambient background music.',
        'price': 4000,
        'url': 'https://images.unsplash.com/photo-1551701444-2274f2313217?w=800&q=80'
    },

    # STANDARD PACKAGE
    {
        'name': 'Standard Catering',
        'package_type': 'Standard',
        'description': 'A wide variety of cuisines and appetizers, served by professional staff for a complete dining experience.',
        'price': 25000,
        'url': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80'
    },
    {
        'name': 'Stage Decoration',
        'package_type': 'Standard',
        'description': 'Designer stage setups with thematic backdrops and floral arrangements that stand out.',
        'price': 20000,
        'url': 'https://images.unsplash.com/photo-1505236858219-8359eb29e329?w=800&q=80'
    },
    {
        'name': 'Professional Photography',
        'package_type': 'Standard',
        'description': 'Comprehensive photo coverage including candid shots and a professionally edited digital album.',
        'price': 25000,
        'url': 'https://images.unsplash.com/photo-1452626038306-9aae5e071dd3?w=800&q=80'
    },
    {
        'name': 'DJ / Music',
        'package_type': 'Standard',
        'description': 'Professional DJ with a high-quality sound system and a curated playlist for your event.',
        'price': 15000,
        'url': 'https://images.unsplash.com/photo-1571266028243-e4733b0f0bb1?w=800&q=80'
    },
    {
        'name': 'Decorative Lighting',
        'package_type': 'Standard',
        'description': 'Dynamic mood lighting and spotlights to enhance the visual appeal of your venue.',
        'price': 10000,
        'url': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800&q=80'
    },
    {
        'name': 'Standard Sound System',
        'package_type': 'Standard',
        'description': 'High-fidelity audio coverage for small to medium-sized event spaces.',
        'price': 12000,
        'url': 'https://images.unsplash.com/photo-1598387181032-a3103a2db5b3?w=800&q=80'
    },

    # LUXURY PACKAGE
    {
        'name': 'Premium Catering',
        'package_type': 'Luxury',
        'description': 'Gourmet multi-course experience featuring international cuisines and elite table service.',
        'price': 75000,
        'url': 'https://images.unsplash.com/photo-1519741497674-611481863552?w=800&q=80'
    },
    {
        'name': 'Luxury Decoration',
        'package_type': 'Luxury',
        'description': 'Exquisite, high-end thematic designs with premium materials and grand floral structures.',
        'price': 100000,
        'url': 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=800&q=80'
    },
    {
        'name': 'Cinematic Photo/Videography',
        'package_type': 'Luxury',
        'description': 'Full cinematic production including drone shots, 4K videography, and premium physical albums.',
        'price': 150000,
        'url': 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800&q=80'
    },
    {
        'name': 'Professional DJ & Sound System',
        'package_type': 'Luxury',
        'description': 'Top-tier DJ and professional grade sound reinforcement for a concert-like experience.',
        'price': 50000,
        'url': 'https://images.unsplash.com/photo-1598387181032-a3103a2db5b3?w=800&q=80'
    },
    {
        'name': 'Advanced Lighting',
        'package_type': 'Luxury',
        'description': 'Computer-controlled intelligent lighting, laser effects, and smoke machines for a grand show.',
        'price': 40000,
        'url': 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&q=80'
    },
    {
        'name': 'Makeup Artist',
        'package_type': 'Luxury',
        'description': 'Elite bridal and party makeup by celebrity artists for a flawless, high-definition look.',
        'price': 25000,
        'url': 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=800&q=80'
    },
    {
        'name': 'Event Host / Anchor',
        'package_type': 'Luxury',
        'description': 'Professional MC or anchor to manage the event flow and keep your guests entertained.',
        'price': 20000,
        'url': 'https://images.unsplash.com/photo-1475721027187-4322f4bb57d8?w=800&q=80'
    },
]

def populate():
    print("Clearing existing services...")
    Service.objects.all().delete()
    
    print("Populating tiered package services...")
    for data in PACKAGE_SERVICES:
        try:
            service = Service.objects.create(
                name=data['name'],
                package_type=data['package_type'],
                description=data['description'],
                price=data['price']
            )
            
            print(f"Downloading image for {data['name']}...")
            response = requests.get(data['url'], timeout=15)
            if response.status_code == 200:
                img_name = f"{data['name'].lower().replace(' ', '_').replace('/', '_')}.jpg"
                service.image.save(img_name, ContentFile(response.content), save=True)
                print(f"✅ Created: {data['name']}")
            else:
                print(f"❌ Failed to download image for {data['name']}")
                service.save()
        except Exception as e:
            print(f"🛑 Error creating {data['name']}: {e}")

    print("Population complete!")

if __name__ == '__main__':
    populate()
