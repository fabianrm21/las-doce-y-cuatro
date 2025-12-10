from urllib.parse import urlencode
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, serializers
from django.conf import settings
import base64
import requests
from .models import SpotifyAuth, LinkedDevice, GlobalPlaybackSchedule
from .utils import get_valid_token, play_dtmf_api_call


class LinkSpotifyAccount(APIView):
    def post(self, request):
        device_id = request.data.get("device_id")

        device = LinkedDevice.objects.filter(id=device_id).exists()
        existing = device and (device.spotify_account is not None)
        if existing:
            return Response({"message": "Account already linked"}, status=status.HTTP_200_OK)
        
        client_id = settings.SPOTIFY_CLIENT_ID
        redirect_uri = f"{settings.CALLBACK_URL}/spotify/callback/"
        scope = "user-read-private user-read-email user-top-read"

        query_params = urlencode({
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": device_id,
        })

        auth_url = f"https://accounts.spotify.com/authorize?{query_params}"
        return Response({"auth_url": auth_url}, status=status.HTTP_200_OK)
    


class SpotifyCallback(APIView):

    def get(self, request):
        code = request.GET.get("code")
        device_id = request.GET.get("state")

        redirect_uri = f"{settings.CALLBACK_URL}/spotify/callback/"
        token_url = "https://accounts.spotify.com/api/token"

        client_id = settings.SPOTIFY_CLIENT_ID
        client_secret = settings.SPOTIFY_CLIENT_SECRET

        auth_str = f"{client_id}:{client_secret}"
        b64_auth_str = base64.b64encode(auth_str.encode()).decode()

        headers = {"Authorization": f"Basic {b64_auth_str}"}
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        try:
            response = requests.post(token_url, headers=headers, data=data)
            tokens = response.json()
        except:
            print("this is happening")
            return Response({"error": "Error during callback"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")

        get_user_id = requests.get("https://api.spotify.com/v1/me",
                                   headers={"Authorization": f"Bearer {access_token}"})
        
        spotify_user_id = get_user_id.json().get("id")
        print("we have not made it here")
        user = SpotifyAuth.objects.create(spotify_user_id=spotify_user_id,
                                   refresh_token=refresh_token)
        
        print("this is what fucked it up")
        
        LinkedDevice.objects.create(id=device_id,
                                    spotify_account=user)
        print("we've made it here")     
        return redirect(f"{settings.FRONTEND_HOST_URL}/spotify-connected/")
    

class GetPlaybackTime(APIView):

    def get(self, request):
        playback_time = GlobalPlaybackSchedule.objects.get(id=1).playback_time
        return Response({"playback_time": str(playback_time)},
                        status=status.HTTP_200_OK)
    

class PlayDTMF(APIView):

    def post(self, request):
        secret = request.data.get("secret")
        if not secret or secret != settings.DTMF_ENDPOINT_KEY:
            return Response({"error": "Incorrect or missing secret key"},
                            status=status.HTTP_403_FORBIDDEN)
        
        users = SpotifyAuth.objects.all()
        for user in users:
            access_token = get_valid_token(user.refresh_token)
            play_dtmf_api_call(user=user, access_token=access_token)
        return Response({"message": "Vamo a vel si es veldad"},
                        status=status.HTTP_200_OK)