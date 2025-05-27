import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def get_number(text, default=0):
    try:
        return int(re.sub(r"\D", "", text))
    except Exception as e:
        return default
    
def update_url_param(url, param_name, param_value):
    base_url, fragment = url.split('#', 1) if '#' in url else (url, '')

    pattern = rf'([?&]){re.escape(param_name)}=[^&]*'
    if re.search(pattern, base_url):
        base_url = re.sub(pattern, rf'\1{param_name}={param_value}', base_url)
    else:
        if '?' in base_url:
            base_url = base_url + f'&{param_name}={param_value}'
        else:
            base_url = base_url + f'?{param_name}={param_value}'

    return base_url + ('#' + fragment if fragment else '')

def get_url_param(url, param_name, default=None):
    pattern = rf'([?&]){re.escape(param_name)}=([^&]*)'
    match = re.search(pattern, url)
    if match:
        return match.group(2)
    else:
        return default