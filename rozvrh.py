#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import datetime
import base64

# --- CONFIGURATION ---
OS_CISLO = "F220000" 
USERNAME = "your_stag_login "
PASSWORD = "your_stag_password."
# ---------------------

def get_today_schedule():
    # Get today's exact date in the DD.MM.YYYY format that STAG expects
    today_str = datetime.datetime.now().strftime("%d.%m.%Y")
    
    # By using datumOd and datumDo, STAG ignores the generic semester template 
    # and returns the ACTUAL live calendar for today!
    url = f"https://ws.ujep.cz/ws/services/rest2/rozvrhy/getRozvrhByStudent?osCislo={OS_CISLO}&datumOd={today_str}&datumDo={today_str}&outputFormat=JSON"
    
    # Create the Base64 encoded authentication header
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

    # If the API returns nothing at all for this date
    if 'rozvrhovaAkce' not in data or not data['rozvrhovaAkce']:
        return "No classes today!"

    events = data['rozvrhovaAkce']

    # Sort events by starting time
    events.sort(key=lambda x: x.get('hodinaSkutOd', {}).get('value', x.get('hodinaSkutOd', '00:00')))

    output = ""
    for e in events:
        # Filter out classes that were explicitly marked as cancelled in STAG
        if e.get('zruseno') == 'A':
            continue 
            
        start = e.get('hodinaSkutOd', '')
        end = e.get('hodinaSkutDo', '')
        if isinstance(start, dict): start = start.get('value', '')
        if isinstance(end, dict): end = end.get('value', '')
        
        subj = e.get('predmet', '???')
        room = e.get('mistnost', '???')
        typ = e.get('typAkceZkr', '')

        output += f"{start}-{end} | {subj} ({typ}) | {room}\n"
    
    # Just in case all classes were cancelled
    if not output:
        return "No classes today!"
        
    return output.strip()

if __name__ == "__main__":
    print(get_today_schedule())