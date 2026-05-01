# airquality.py — 12-hour AQI forecast for Lecco, Italy (Open-Meteo)
#010526 Chnage to a chart of next 2 days

import socket, ssl, json, gc
import wifi_mgr

HOST = "air-quality-api.open-meteo.com"
PATH = ("/v1/air-quality?latitude=45.85&longitude=9.4"
        "&current=european_aqi"
        "&hourly=european_aqi"
        "&forecast_days=2")

def _https_get(host, path):
    addr = socket.getaddrinfo(host, 443)[0][-1]
    s = socket.socket()
    s.settimeout(15)
    s.connect(addr)
    s = ssl.wrap_socket(s, server_hostname=host)
    s.write((
        f"GET {path} HTTP/1.0\r\n"
        f"Host: {host}\r\n"
        "\r\n"
    ).encode())
    chunks = []
    try:
        while True:
            chunk = s.read(512)
            if not chunk:
                break
            chunks.append(bytes(chunk))
    finally:
        s.close()
    raw = b''.join(chunks)
    sep = raw.find(b"\r\n\r\n")
    if sep < 0:
        raise ValueError("Bad HTTP response")
    if b" 200 " not in raw[:raw.find(b"\r\n")]:
        raise ValueError(raw[:60].decode())
    return raw[sep + 4:]

tft.fill(0x0000)
term = _TFTTerminal(tft, None, font=mono13)

def mprint(*args, **kwargs):
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    term.write(sep.join(str(a) for a in args) + end)

mprint("AQI Chart - Lecco")
mprint("Connecting...")

if not wifi_mgr.is_connected():
    wifi_mgr.load_creds()
    if wifi_mgr._creds:
        c = wifi_mgr._creds[0]
        wifi_mgr.connect(c['ssid'], c['pass'])

if not wifi_mgr.is_connected():
    mprint("No WiFi connection")
else:
    try:
        gc.collect()
        body = _https_get(HOST, PATH)
        data = json.loads(body)
        gc.collect()

        cur_time = data['current']['time']
        h_times = data['hourly']['time']
        h_aqis  = data['hourly']['european_aqi']

        try:
            start_idx = h_times.index(cur_time) + 1
        except ValueError:
            start_idx = 0

        # Collect the next 12 hours of data
        aqi_list = []
        time_list = []
        for i in range(start_idx, start_idx + 12):
            if i < len(h_times):
                time_list.append(h_times[i][-5:]) # "HH:MM"
                aqi_list.append(h_aqis[i])

        tft.fill(0x0000)
        term = _TFTTerminal(tft, None, font=mono13)
        mprint("Lecco AQI (Next 12h)")

        # Draw the Y-axis and chart data (0-100 scale, step 10)
        for lvl in range(100, -1, -10):
            row = f"{lvl:3}|"
            for aqi in aqi_list:
                if aqi is None:
                    row += "   "
                else:
                    # Cap visual values at 100
                    display_aqi = min(aqi, 100)
                    # Round to the nearest 10-point interval
                    nearest = round(display_aqi / 10) * 10
                    if nearest == lvl:
                        row += " # "
                    else:
                        row += "   "
            mprint(row)

        # Draw the X-axis
        mprint("   +" + "-" * 36)
        
        # Draw the X-axis hour labels (extracting 'HH' from 'HH:MM')
        labels = "    "
        for t in time_list:
            labels += f"{t[:2]:>2} "
        mprint(labels)

    except Exception as e:
        mprint(f"Error: {e}")