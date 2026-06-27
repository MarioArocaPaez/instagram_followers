from django.shortcuts import render
from django.http import HttpResponse
import json
from datetime import datetime
from django.template.loader import render_to_string
from xhtml2pdf import pisa


def index(request):
    return render(request, 'index.html')


def _get_username(entry):
    """
    Extrae el username soportando varios formatos de exportación de Instagram:
    - following nuevo: entry['title']
    - followers clásico/nuevo: entry['string_list_data'][0]['value']
    - fallback desde href
    """
    if not isinstance(entry, dict):
        return ''

    username = (entry.get('title') or '').strip()
    if username:
        return username

    string_data = entry.get('string_list_data') or []
    if string_data and isinstance(string_data[0], dict):
        username = (string_data[0].get('value') or '').strip()
        if username:
            return username

        href = (string_data[0].get('href') or '').strip().rstrip('/')
        if href:
            return href.split('/')[-1]

    return ''


def _get_first_string_data(entry):
    string_data = entry.get('string_list_data') or []
    if string_data and isinstance(string_data[0], dict):
        return string_data[0]
    return {}


def _format_timestamp(timestamp):
    if not timestamp:
        return 'Fecha no disponible'

    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    except (TypeError, ValueError, OSError):
        return 'Fecha no disponible'


def upload_files(request):
    error_message = None

    if request.method == 'POST' and 'following_file' in request.FILES and 'followers_file' in request.FILES:
        following_file = request.FILES['following_file']
        followers_file = request.FILES['followers_file']

        try:
            following_data = json.load(following_file)
            followers_data = json.load(followers_file)

            if not isinstance(following_data, dict) or not isinstance(following_data.get('relationships_following'), list):
                raise ValueError('El archivo following.json no tiene la estructura esperada')

            if isinstance(followers_data, dict):
                followers_entries = (
                    followers_data.get('relationships_followers')
                    or followers_data.get('followers')
                    or []
                )
            elif isinstance(followers_data, list):
                followers_entries = followers_data
            else:
                raise ValueError('El archivo followers_1.json no tiene la estructura esperada')

            following_entries = following_data['relationships_following']

            following_details = {}
            for entry in following_entries:
                username = _get_username(entry)
                if not username:
                    continue

                data = _get_first_string_data(entry)
                key = username.lower()

                following_details[key] = {
                    'username': username,
                    'href': data.get('href') or f'https://www.instagram.com/{username}',
                    'timestamp': data.get('timestamp')
                }

            followers_usernames = set()
            for entry in followers_entries:
                username = _get_username(entry)
                if username:
                    followers_usernames.add(username.lower())

            not_following_back_details = []

            for key, details in following_details.items():
                if key not in followers_usernames:
                    not_following_back_details.append({
                        'username': details['username'],
                        'href': details['href'],
                        'timestamp': details['timestamp'],
                        'follow_date': _format_timestamp(details['timestamp'])
                    })

            # Orden por fecha de seguimiento, más recientes primero
            not_following_back_details.sort(
                key=lambda user: user.get('timestamp') or 0,
                reverse=True
            )

            not_following_back_count = len(not_following_back_details)

            request.session['not_following_back_details'] = not_following_back_details

            return render(request, 'result.html', {
                'not_following_back_details': not_following_back_details,
                'not_following_back_count': not_following_back_count
            })

        except json.JSONDecodeError:
            error_message = 'Error: alguno de los archivos no es un JSON válido'
        except Exception as e:
            error_message = f'Error procesando archivos: {str(e)}'

    return render(request, 'index.html', {'error_message': error_message})


def download_pdf(request):
    not_following_back_details = request.session.get('not_following_back_details', [])
    not_following_back_count = len(not_following_back_details)

    context = {
        'not_following_back_details': not_following_back_details,
        'not_following_back_count': not_following_back_count
    }

    html = render_to_string('pdf_template.html', context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="users_not_following_back.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response