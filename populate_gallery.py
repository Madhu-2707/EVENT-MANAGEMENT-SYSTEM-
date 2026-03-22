
import os
import django
import requests
from django.core.files.base import ContentFile
import time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from core.models import Gallery

# Define categories and reliable search terms for LoremFlickr (more stable for scripts)
GALLERY_DATA = {
    'Wedding': [
        'wedding,stage',
        'wedding,ceremony',
        'wedding,mandap',
        'wedding,hall',
        'indian,wedding',
        'wedding,flower'
    ],
    'Birthday Party': [
        'birthday,party,decoration',
        'birthday,cake',
        'balloon,party',
        'birthday,celebration',
        'kids,birthday',
        'birthday,lighting'
    ],
    'Engagement': [
        'engagement,ceremony',
        'engagement,ring',
        'engagement,stage',
        'engagement,party',
        'engagement,couple'
    ],
    'Baby Shower': [
        'baby,shower,decor',
        'baby,shower,cake',
        'baby,shower,party',
        'baby,shower,balloon',
        'baby,shower,celebration'
    ],
    'Corporate Event': [
        'conference,hall',
        'product,launch',
        'corporate,event',
        'business,meeting',
        'corporate,gala',
        'seminar,stage'
    ],
    'Cultural Event': [
        'cultural,dance',
        'traditional,festival',
        'cultural,show',
        'folk,dance',
        'traditional,performance'
    ],
    'Music Concert': [
        'concert,stage',
        'live,band',
        'music,crowd',
        'rock,concert',
        'music,festival'
    ]
}

def download_image(query):
    # Using LoremFlickr which is very stable for programmatic access
    url = f"https://loremflickr.com/800/600/{query}"
    try:
        response = requests.get(url, timeout=20, allow_redirects=True)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print(f"  Error downloading {query}: {e}")
    return None

def populate():
    print("Clearing existing gallery images...")
    Gallery.objects.all().delete()
    
    print("Populating high-quality event images...")
    for category, queries in GALLERY_DATA.items():
        print(f"\nProcessing category: {category}")
        success_count = 0
        for i, query in enumerate(queries):
            print(f"  Downloading image {i+1}/{len(queries)} for: {query}")
            img_data = download_image(query)
            if img_data:
                img_name = f"{category.lower().replace(' ', '_')}_{i+1}.jpg"
                gallery_item = Gallery(category=category)
                gallery_item.image.save(img_name, ContentFile(img_data), save=True)
                print(f"  ✅ Saved: {img_name}")
                success_count += 1
                time.sleep(1) # Be nice to the server
            else:
                print(f"  ❌ Failed to download: {query}")
        
        print(f"Finished {category}: {success_count} images saved.")

    print("\nGallery population complete!")

if __name__ == '__main__':
    populate()
