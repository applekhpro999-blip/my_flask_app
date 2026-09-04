import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import sys
import time

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request_method()

    def do_POST(self):
        self.handle_request_method()

    def handle_request_method(self):
        try:
            req_url = self.path
            if not req_url.startswith('http'):
                req_url = f"http://{self.headers.get('Host', 'localhost')}{self.path}"

            content_length = int(self.headers.get('Content-Length', 0)) if 'Content-Length' in self.headers else 0
            body_data = self.rfile.read(content_length) if content_length > 0 else None
            
            req = urllib.request.Request(req_url, data=body_data, headers=dict(self.headers))
            
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for header, value in response.headers.items():
                    if header.lower() not in ['transfer-encoding', 'content-encoding']:
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
        except Exception as e:
            self.send_error(500, str(e))

    def log_message(self, format, *args):
        # បិទការ Log ច្រើនហួសហេតុក្នុង Console ឱ្យស្អាត
        return

def start_server(port):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, ProxyHandler)
    httpd.serve_forever()

def update_config_with_proxies(num_profiles=20):
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")
    
    # អាន config.py ចាស់មកកែសម្រួល
    import config
    profiles = config.PROFILES

    config_content = '''import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_DIR = os.path.join(BASE_DIR, "profiles_data")

if not os.path.exists(PROFILES_DIR):
    os.makedirs(PROFILES_DIR)

PROFILES = [\n'''

    for i in range(num_profiles):
        p_id = i + 1
        port = 8079 + p_id  # เริ่มจาก Port 8080 ถึง 8099
        proxy_url = f"http://127.0.0.1:{port}"
        
        # ទាញយកទិន្នន័យចាស់មកប្រើបន្ត (ถ้ามี)
        existing_profile = next((p for p in profiles if p['id'] == p_id), None)
        
        width = existing_profile['width'] if existing_profile else 370
        height = existing_profile['height'] if existing_profile else 320
        pos_x = existing_profile['pos_x'] if existing_profile else (i % 5) * 500
        pos_y = existing_profile['pos_y'] if existing_profile else (i // 5) * 1000
        lang = existing_profile['lang'] if existing_profile else "en-US"
        timezone = existing_profile['timezone'] if existing_profile else "UTC"
        theme = existing_profile['theme'] if existing_profile else ("dark" if i % 2 == 0 else "light")
        user_agent = existing_profile['user_agent'] if existing_profile else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.61.110"
        browser_type = "brave"

        config_content += f"""    {{
        "id": {p_id},
        "name": "Profile_{p_id}",
        "profile_path": os.path.join(PROFILES_DIR, "profile_{p_id}"),
        "width": {width}, "height": {height}, "pos_x": {pos_x}, "pos_y": {pos_y},
        "lang": "{lang}", "timezone": "{timezone}", "theme": "{theme}",
        "user_agent": "{user_agent}",
        "browser_type": "{browser_type}",
        "proxy": "{proxy_url}"
    }},\n"""

    config_content += "]\n"

    with open(config_file_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("✅ បានធ្វើបច្ចុប្បន្នភាព Proxy ទាំង ២០ ចូលក្នុង config.py រួចរាល់!")

if __name__ == '__main__':
    NUM_PROXIES = 20
    BASE_PORT = 8080

    print(f"🚀 กำลังចាប់ផ្តើមបង្កើត Local Proxy ចំនួន {NUM_PROXIES}...")
    
    # ធ្វើបច្ចុប្បន្នភាព File config.py ដោយស្វ័យប្រវត្តិ
    update_config_with_proxies(NUM_PROXIES)

    # បើក Server ទាំង ២០ ក្នុង Background Threads
    for i in range(NUM_PROXIES):
        port = BASE_PORT + i
        t = threading.Thread(target=start_server, args=(port,))
        t.daemon = True
        t.start()
        print(f"   -> Proxy Server ដំណើរការលើ Port: {port}")

    print("\n✨ Proxy ទាំងអស់កំពុងដំណើរការ! អ្នកអាចបើកដំណើរការ app.py របស់អ្នកបានปกติ។")
    
    # ទប់កុំឱ្យ Terminal បិទ
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 កំពុងបិទ Proxy Servers...")