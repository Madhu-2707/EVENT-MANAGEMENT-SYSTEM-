import os
import requests

def download_image(url, folder, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            os.makedirs(folder, exist_ok=True)
            path = os.path.join(folder, filename)
            with open(path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {path}")
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

categories = {
    'wedding': [
        'https://i.pinimg.com/1200x/80/2b/e5/802be59a47603d04fc8985c55956d1d4.jpg',
        'https://i.pinimg.com/1200x/03/d3/c6/03d3c6aacf3410dd8f4936b46e3208d5.jpg',
        'https://i.pinimg.com/1200x/60/1a/75/601a75dbce444176f0bb258041dd420f.jpg',
        'https://i.pinimg.com/736x/07/fd/3d/07fd3d0461bc4a16e7679b5b8f86be08.jpg',
        'https://i.pinimg.com/1200x/c5/7a/6d/c57a6d423e213f2dd29a423bb03eabb1.jpg'
    ],
    'birthday': [
        'https://i.pinimg.com/1200x/24/9f/08/249f082ab13d270eb012e79b9facde5b.jpg',
        'https://i.pinimg.com/736x/0b/7a/24/0b7a24b7486e223b68cbef0d9be41750.jpg',
        'https://i.pinimg.com/1200x/59/58/a6/5958a66d5048b0f0a818dc8e21c72a86.jpg',
        'https://i.pinimg.com/736x/35/2a/12/352a122de2ea0dc6cbf144215c5b6e9d.jpg',
        'https://images.unsplash.com/photo-1533294160022-4187eac57fe2?q=80&w=800&auto=format&fit=crop'
    ],
    'corporate': [
        'https://images.unsplash.com/photo-1511578314322-379afb476865?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1475721027185-404ebc77d337?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1505373877841-8d25f7d46678?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1551818255-e6e10975bc17?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1540575861501-7ce0e1d529c3?q=80&w=800&auto=format&fit=crop'
    ],
    'engagement': [
        'https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1520854221256-17451cc331bf?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1529636798458-92182e662485?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1537633552985-df8429e8048b?q=80&w=800&auto=format&fit=crop'
    ],
    'babyshower': [
        'https://images.unsplash.com/photo-1559461678-834ff5a88aa1?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1519225421980-715cb0215aed?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1510253687831-0f982d7862fc?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1555244162-803834f70033?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1522204523234-8729aa6e3d5f?q=80&w=800&auto=format&fit=crop'
    ],
    'collegefest': [
        'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1514525253361-b83f83ef908c?q=80&w=800&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1517457373958-b7bdd4587205?q=80&w=800&auto=format&fit=crop'
    ]
}

base_media_path = 'media/gallery'

for cat, urls in categories.items():
    folder = os.path.join(base_media_path, cat)
    for i, url in enumerate(urls):
        filename = f"{cat}_{i+1}.jpg"
        download_image(url, folder, filename)
