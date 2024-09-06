import redis
from django.http import HttpResponse
from django.shortcuts import redirect
from spotipy import SpotifyOAuth
from spotipy.cache_handler import RedisCacheHandler

# Initialize Redis connection
r = redis.Redis(host="localhost", port=6379, db=0)

# Initialize Redis cache handler
cache_handler = RedisCacheHandler(redis=r, key="spotify_token")

# Configure Spotify OAuth
sp_oauth = SpotifyOAuth(
    redirect_uri="http://localhost:8000/callback",
    scope="user-library-read",
    cache_handler=cache_handler,
)


def index(request):
    # Check if user is logged in, if not, redirect to Spotify login
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        return redirect("/login")

    return HttpResponse("EVERYTHING IS OK")


def login(request):
    # Redirect user to Spotify authorization URL
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


def callback(request):
    # Handle callback from Spotify authorization
    code = request.GET.get("code")
    sp_oauth.get_access_token(code)

    return redirect("/")
