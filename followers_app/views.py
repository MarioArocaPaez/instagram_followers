from django.shortcuts import render
from django.http import JsonResponse
import json
from datetime import datetime

def index(request):
    return render(request, 'index.html')

def upload_files(request):
    error_message = None
    if request.method == 'POST' and 'following_file' in request.FILES and 'followers_file' in request.FILES:
        following_file = request.FILES['following_file']
        followers_file = request.FILES['followers_file']
        
        try:
            # Attempt to load JSON data from files
            following_data = json.load(following_file)
            followers_data = json.load(followers_file)

            # Check if the JSON structure matches the expected format
            if "relationships_following" not in following_data or not isinstance(following_data["relationships_following"], list):
                raise ValueError("Invalid following.json structure")
            if not isinstance(followers_data, list):
                raise ValueError("Invalid followers_1.json structure")

            # Extract data
            following_details = {
                entry['string_list_data'][0]['value']: {
                    'href': entry['string_list_data'][0]['href'],
                    'timestamp': entry['string_list_data'][0]['timestamp']
                } 
                for entry in following_data["relationships_following"] if entry['string_list_data']
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

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Set an error message if JSON is invalid or the structure is incorrect
            error_message = str(e)

    # Render the index page with an error message if something goes wrong
    return render(request, 'index.html', {'error_message': error_message})

