from django.shortcuts import render
from django.http import JsonResponse
import json
from datetime import datetime

def index(request):
    return render(request, 'index.html')

def upload_files(request):
    if request.method == 'POST' and 'following_file' in request.FILES and 'followers_file' in request.FILES:
        following_file = request.FILES['following_file']
        followers_file = request.FILES['followers_file']
        
        # Load JSON data from files
        following_data = json.load(following_file)["relationships_following"]
        followers_data = json.load(followers_file)

        following_details = {
            entry['string_list_data'][0]['value']: {
                'href': entry['string_list_data'][0]['href'],
                'timestamp': entry['string_list_data'][0]['timestamp']
            } 
            for entry in following_data if entry['string_list_data']
        }
        followers_usernames = {entry['string_list_data'][0]['value'] for entry in followers_data if entry['string_list_data']}

        not_following_back_details = [
            {
                'username': username,
                'href': details['href'],
                'follow_date': datetime.fromtimestamp(details['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            }
            for username, details in following_details.items() if username not in followers_usernames
        ]

        return render(request, 'result.html', {'not_following_back_details': not_following_back_details})
    
    return JsonResponse({'error': 'Invalid request method or missing files'})
