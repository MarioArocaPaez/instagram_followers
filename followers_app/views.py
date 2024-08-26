from django.shortcuts import render
from django.http import JsonResponse
import json

def index(request):
    return render(request, 'index.html')

def upload_files(request):
    if request.method == 'POST' and 'following_file' in request.FILES and 'followers_file' in request.FILES:
        following_file = request.FILES['following_file']
        followers_file = request.FILES['followers_file']
        
        # Load JSON data from files
        following_data = json.load(following_file)["relationships_following"]
        followers_data = json.load(followers_file)

        following_usernames = {entry['string_list_data'][0]['value'] for entry in following_data if entry['string_list_data']}
        followers_usernames = {entry['string_list_data'][0]['value'] for entry in followers_data if entry['string_list_data']}

        not_following_back = following_usernames - followers_usernames

        return JsonResponse({'not_following_back': list(not_following_back)})
    
    return JsonResponse({'error': 'Invalid request method or missing files'})
