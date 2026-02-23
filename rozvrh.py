#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import datetime
import base64

# --- CONFIGURATION ---
OS_CISLO = "F"
USERNAME = "st"
PASSWORD = "???"
HIGHLIGHT_COLOR = "${color #ff0000}"
# ---------------------

def get_today_schedule():
    now = datetime.datetime.now().time()

    today_str = datetime.datetime.now().strftime("%d.%m.%Y")
    
    url = f"https://ws.ujep.cz/ws/services/rest2/rozvrhy/getRozvrhByStudent?osCislo={OS_CISLO}&datumOd={today_str}&datumDo={today_str}&outputFormat=JSON"
    
    auth_str = f"{USERNAME}:{PASSWORD}"
    b64_auth_str = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    
    headers = {
        'Authorization': f'Basic {b64_auth_str}'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return "Auth Error: Wrong STAG username or password!"
        elif e.code == 403:
            return "Forbidden: No permission for this schedule!"
        else:
            return f"HTTP Error: {e.code}"
    except Exception as e:
        return "Error connecting to STAG / Network offline"

    if 'rozvrhovaAkce' not in data or not data['rozvrhovaAkce']:
        return "No classes today!"

    events = data['rozvrhovaAkce']

    events.sort(key=lambda x: x.get('hodinaSkutOd', {}).get('value', x.get('hodinaSkutOd', '00:00')))

    output = ""
    for e in events:
        if e.get('zruseno') == 'A':
            continue 
            
        start = e.get('hodinaSkutOd', '')
        end = e.get('hodinaSkutDo', '')
        if isinstance(start, dict): start = start.get('value', '')
        if isinstance(end, dict): end = end.get('value', '')

        is_now = False
        try:
            start_time = datetime.datetime.strptime(start, "%H:%M").time()
            end_time = datetime.datetime.strptime(end, "%H:%M").time()
            
            if start_time <= now <= end_time:
                is_now = True
        except ValueError:
            pass
        
        department = e.get('katedra', '???')
        subj = e.get('predmet', '???')
        building = e.get('budova', '???')
        room = e.get('mistnost', '???')
        typ = e.get('typAkceZkr', '')

        line = f"{start}-{end} | {department}/{subj} ({typ}) | {building}-{room}"
        
        if is_now:
            output += f"{HIGHLIGHT_COLOR}{line}${{color}}\n"
        else:
            output += f"{line}\n"

    if not output:
        return "No classes today!"
        
    return output.strip()

if __name__ == "__main__":
    print(get_today_schedule())