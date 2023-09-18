from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


base_url = 'https://api.spotify.com/'

class MusicView(APIView):
    def get(self, request, *args, artist_id, **kwargs):
        r = requests.get(url=f'{base_url}v1/artists/{artist_id}',
                         headers={
                             'Authorization': 'Bearer'
                         })
        green_day = r.json()
        print(args, artist_id)
        return Response(green_day['genres'])
    
    def post(self, request):
        return Response(request.data)

