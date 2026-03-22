from django.conf import settings

def google_maps_key(request):
    """
    Returns the Google Maps API key from settings to be used in templates.
    """
    return {
        'GOOGLE_CLIENT_ID': getattr(settings, 'GOOGLE_CLIENT_ID', '')
    }
