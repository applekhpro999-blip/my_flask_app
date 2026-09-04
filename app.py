from datetime import datetime, timedelta
import sqlite3
from flask import Flask, render_template, request, redirect, jsonify, url_for, session, flash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import subprocess
import time
import random
import os
import psutil
import yt_dlp
import threading
import pyautogui
import numpy as np
import requests
import json
import websocket
import shutil

from config import PROFILES

# Consolidated Global Pools
USER_AGENTS_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
]

SCREEN_RESOLUTIONS = [
    {"width": 1366, "height": 768},
    {"width": 1920, "height": 1080},
    {"width": 1536, "height": 864},
    {"width": 1440, "height": 900}
]

WEBGL_RENDERERS_POOL = [
    {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)"},
    {"vendor": "Google Inc. (AMD)", "renderer": "ANGLE (AMD, AMD Radeon RX 6700 XT Direct3D11 vs_5_0 ps_5_0)"},
    {"vendor": "Google Inc. (Intel)", "renderer": "ANGLE (Intel, Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0)"},
    {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 SUPER Direct3D11 vs_5_0 ps_5_0)"}
]

pyautogui.FAILSAFE = True

app = Flask(__name__)
app.secret_key = 'super_secret_key_random_string_here'  

from database import init_db, generate_key_code
init_db()

is_running = False
status_lock = threading.Lock()
run_counter = 0
counter_lock = threading.Lock()
search_history_cache = {}
history_lock = threading.Lock()

limiter = Limiter(
    key_func=get_remote_address,  
    app=app,
    default_limits=["200 per day", "50 per hour"],  
    storage_uri="memory://"  
)

def get_video_info_via_ytdlp(url):
    default_duration = 3600  
    try:
        selected_user_agent = PROFILES[0]['user_agent'] if PROFILES else USER_AGENTS_POOL[0]
        
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'socket_timeout': 5,
            'http_headers': {
                'User-Agent': selected_user_agent
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', None)
            duration = info.get('duration', default_duration)
            
            if title:
                return title, duration
    except Exception as e:
        print(f"yt_dlp មិនអាចទាញយក Title បានទេ: {e}")

    try:
        oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
        response = requests.get(oembed_url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            title = data.get('title', '')
            if title:
                return title, default_duration
    except Exception as ex:
        print(f"oembed fallback error: {ex}")

    return "", default_duration

@app.route('/')
def index():
    return render_template('index.html', profiles=PROFILES)

def clear_browser_sessions(profile_path):
    try:
        session_folders = [
            "Default/Sessions", "Default/Session Storage", 
            "Default/Cookies", "Default/Network Persistent State"
        ]
        for folder in session_folders:
            folder_path = os.path.join(profile_path, folder)
            if os.path.exists(folder_path):
                if os.path.isdir(folder_path):
                    shutil.rmtree(folder_path, ignore_errors=True)
                else:
                    os.remove(folder_path)
    except Exception as e:
        print(f"បញ្ហាក្នុងការសម្អាត Session: {e}")

def human_like_move(target_x, target_y):
    start_x, start_y = pyautogui.position()
    distance = ((target_x - start_x)**2 + (target_y - start_y)**2)**0.5
    curve_offset = max(distance * 0.5, 150) 
    
    sign = random.choice([-1, 1])
    control_x = (start_x + target_x) / 2 + sign * random.randint(int(curve_offset * 0.7), int(curve_offset))
    control_y = (start_y + target_y) / 2 - sign * random.randint(int(curve_offset * 0.7), int(curve_offset))
    
    steps = int(max(40, min(distance / 10, 90)))
    
    for i in range(steps + 1):
        t = i / float(steps)
        x = (1 - t)**2 * start_x + 2 * (1 - t) * t * control_x + t**2 * target_x
        y = (1 - t)**2 * start_y + 2 * (1 - t) * t * control_y + t**2 * target_y
        
        pyautogui.moveTo(x, y)
        time.sleep(random.uniform(0.008, 0.02))

def apply_stealth_spoofing(ws, profile):
    vendor = profile.get('webgl_vendor', 'Google Inc. (NVIDIA)')
    renderer = profile.get('webgl_renderer', 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)')
    lat = profile.get('latitude', 11.5564)
    lng = profile.get('longitude', 104.9282)
    
    stealth_script = f"""
    try {{
        Object.defineProperty(navigator, 'webdriver', {{
            get: () => undefined
        }});

        Object.defineProperty(navigator, 'plugins', {{
            get: () => [1, 2, 3, 4, 5]
        }});

        Object.defineProperty(navigator, 'languages', {{
            get: () => ['km-KH', 'km', 'en-US', 'en']
        }});

        if (!window.chrome) {{
            window.chrome = {{
                runtime: {{}}
            }};
        }}

        const overrideWebGL = (contextProto) => {{
            if (!contextProto) return;
            const getParameterOriginal = contextProto.prototype.getParameter;
            contextProto.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) return "{vendor}";
                if (parameter === 37446) return "{renderer}";
                return getParameterOriginal.apply(this, arguments);
            }};
        }};
        overrideWebGL(WebGLRenderingContext);
        if (typeof WebGL2RenderingContext !== 'undefined') {{
            overrideWebGL(WebGL2RenderingContext);
        }}

        if (navigator.geolocation) {{
            navigator.geolocation.getCurrentPosition = function(success) {{
                success({{
                    coords: {{
                        latitude: {lat},
                        longitude: {lng},
                        accuracy: 20
                    }},
                    timestamp: new Date().getTime()
                }});
            }};
        }}

        const statiqueRtc = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
        if (statiqueRtc) {{
            window.RTCPeerConnection = function(...args) {{
                const pc = new statiqueRtc(...args);
                pc.createDataChannel = () => {{}};
                return pc;
            }};
        }}

        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({{ state: 'denied' }}) :
                originalQuery(parameters)
        );
    }} catch(e) {{}}
    """
    
    payload = {
        "id": random.randint(1000, 9999),
        "method": "Page.addScriptToEvaluateOnNewDocument",
        "params": {"source": stealth_script}
    }
    
    try:
        ws.send(json.dumps(payload))
        ws.recv()
    except Exception as e:
        print(f"Error applying stealth spoofing: {e}")

def perform_human_engagement(profile):
    ws = None
    try:
        port = 9222 + profile['id']
        res = requests.get(f"http://127.0.0.1:{port}/json", timeout=3)
        if res.status_code != 200:
            return
            
        tabs = res.json()
        target_tab = None
        for tab in tabs:
            if 'youtube.com' in tab.get('url', '').lower():
                target_tab = tab
                break
        
        if not target_tab and tabs:
            target_tab = tabs[0]
                
        if not target_tab or 'webSocketDebuggerUrl' not in target_tab:
            return

        ws = websocket.create_connection(target_tab['webSocketDebuggerUrl'], timeout=3)
        apply_stealth_spoofing(ws, profile)

        def execute_js(js_code):
            payload = {
                "id": random.randint(100, 999),
                "method": "Runtime.evaluate",
                "params": {"expression": js_code, "returnByValue": True}
            }
            ws.send(json.dumps(payload))
            try:
                ws.recv()
            except:
                pass

        auto_click_video_js = """
        (function() {
            if (window.location.href.includes('/results')) {
                let firstVideo = document.querySelector('ytd-video-renderer #video-title, ytd-rich-item-renderer #video-title');
                if (firstVideo) {
                    firstVideo.click();
                    return "clicked_search_video";
                }
            }
            return "already_on_watch";
        })();
        """
        execute_js(auto_click_video_js)
        
        time.sleep(random.uniform(2, 5))
        speed_modifier = random.uniform(0.8, 1.2)

        scale_factor = 0.75
        browser_x = profile['pos_x'] * scale_factor
        browser_y = profile['pos_y'] * scale_factor
        browser_w = profile['width'] * scale_factor
        browser_h = profile['height'] * scale_factor

        random_right_positions = [
            (random.randint(int(browser_w * 0.70), int(browser_w * 0.90)), random.randint(int(browser_h * 0.35), int(browser_h * 0.85))),
            (random.randint(int(browser_w * 0.75), int(browser_w * 0.93)), random.randint(int(browser_h * 0.45), int(browser_h * 0.90))),
            (random.randint(int(browser_w * 0.65), int(browser_w * 0.88)), random.randint(int(browser_h * 0.40), int(browser_h * 0.80))),
            (random.randint(int(browser_w * 0.72), int(browser_w * 0.91)), random.randint(int(browser_h * 0.30), int(browser_h * 0.75)))
        ]
        
        chosen_pos = random.choice(random_right_positions)
        target_x = browser_x + chosen_pos[0]
        target_y = browser_y + chosen_pos[1]

        human_like_move(target_x, target_y)

        for _ in range(random.randint(2, 4)):
            jx = target_x + random.randint(-15, 15)
            jy = target_y + random.randint(-15, 15)
            pyautogui.moveTo(jx, jy, duration=random.uniform(0.1, 0.3))
            time.sleep(random.uniform(0.1, 0.3))

        scroll_steps = random.randint(1, 2)
        for _ in range(scroll_steps):
            random_scroll_amount = random.randint(300, 600)
            step_js = f"""
            (function() {{
                window.scrollBy({{ top: {random_scroll_amount}, behavior: 'smooth' }});
                let video = document.querySelector('video');
                if (video && video.paused) {{
                    video.play();
                }}
            }})();
            """
            execute_js(step_js)
            time.sleep(random.uniform(5.0, 8.5))

        read_comment_time = random.uniform(4, 8) * speed_modifier
        check_video_playing_js = """
        (function() {
            let video = document.querySelector('video');
            if (video && video.paused) {
                video.play();
            }
        })();
        """
        
        waited = 0
        while waited < read_comment_time:
            time.sleep(1)
            waited += 1
            execute_js(check_video_playing_js)

        scroll_up_js = """
        (function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            let video = document.querySelector('video');
            if (video && video.paused) {
                video.play();
            }
        })();
        """
        execute_js(scroll_up_js)
        time.sleep(1.5)

    except Exception as e:
        print(f"Engagement error on {profile['name']}: {e}")
    finally:
        if ws:
            try:
                ws.close()
            except:
                pass

def deep_clean_browser_profile(profile_path):
    try:
        cache_folders = [
            "Cache", "Code Cache", "GPUCache",
            "Network Persistent State", "Service Worker", "Session Storage"
        ]
        for folder in cache_folders:
            folder_path = os.path.join(profile_path, folder)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path, ignore_errors=True)
    except Exception as e:
        print(f"បញ្ហាក្នុងការសម្អាត Cache: {e}")

def run_single_profile_full_process(profile, youtube_url, duration):
    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    
    try:
        deep_clean_browser_profile(profile['profile_path'])
        
        pool_websites = [
            "https://www.google.com", "https://en.wikipedia.org/wiki/Main_Page",
            "https://github.com", "https://news.google.com", "https://www.reddit.com",
            "https://stackoverflow.com", "https://medium.com", "https://www.bbc.com",
            "https://x.com", "https://www.imdb.com"
        ]

        num_sites_to_visit = random.randint(1, 2)
        selected_sites = random.sample(pool_websites, num_sites_to_visit)

        for site in selected_sites:
            warmup_cmd = [
                brave_path,
                f"--user-data-dir={profile['profile_path']}",
                f"--window-size={profile['width']},{profile['height']}",
                f"--window-position={profile['pos_x']},{profile['pos_y']}",
                f"--user-agent={profile['user_agent']}",
                "--force-device-scale-factor=0.75",
                f"--lang={profile['lang']}",
                f"--timezone={profile['timezone']}",
                "--disable-blink-features=AutomationControlled",
                "--no-restore-state", 
                "--test-type",
                "--disable-notifications",
                "--disable-popup-blocking",
                site
            ]
            if profile.get("proxy"):
                warmup_cmd.append(f"--proxy-server={profile['proxy']}")

            warmup_proc = subprocess.Popen(warmup_cmd)
            time.sleep(random.uniform(15, 25))
            
            try:
                warmup_proc.terminate()
                warmup_proc.wait(timeout=3)
            except:
                try:
                    warmup_proc.kill()
                except:
                    pass
            time.sleep(1)

        clear_browser_sessions(profile['profile_path'])

        cmd = [
            brave_path,
            f"--user-data-dir={profile['profile_path']}",
            f"--window-size={profile['width']},{profile['height']}",
            f"--window-position={profile['pos_x']},{profile['pos_y']}",
            f"--user-agent={profile['user_agent']}",
            "--force-device-scale-factor=0.75",
            "--enable-features=NetworkService",
            f"--lang={profile['lang']}",
            f"--timezone={profile['timezone']}",
            f"--remote-debugging-port={9222 + profile['id']}",
            "--remote-allow-origins=*",
            "--hide-crash-restore-bubble",
            "--disable-session-crashed-bubble",
            "--autoplay-policy=no-user-gesture-required",
            "--disable-features=BraveShields,CanvasDataImageReadout",
            "--disable-blink-features=AutomationControlled",
            "--exclude-switches=enable-automation",
            "--disable-extensions",
            "--no-default-browser-check",
            "--disable-default-apps",
            "--disable-hang-monitor",
            "--disable-popup-blocking",
            "--disable-prompt-on-repost",
            "--disable-sync",
            "--disable-translate",
            "--metrics-recording-only",
            "--no-first-run",
            "--safebrowsing-disable-auto-update",
            "--disable-infobars",
            "--overscroll-history-navigation=0",
            "--disk-cache-dir=nul",
            "--no-restore-state",
            "--test-type",
            "--disable-notifications"
        ]

        hardware_spoof_args = [
            "--disable-component-update",
            "--disable-client-side-phishing-detection",
            f"--hardware-concurrency={random.choice([4, 6, 8, 12])}",
            "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
            "--disable-features=WebRtcHideLocalIpsWithMdns",
            "--use-gl=angle",
            "--use-angle=d3d11",
            "--disable-software-rasterizer"
        ]
        
        for arg in hardware_spoof_args:
            if arg not in cmd:
                cmd.append(arg)
          
        if profile.get("proxy"):
            cmd.append(f"--proxy-server={profile['proxy']}")
        if profile.get("theme") == "dark":
            cmd.append("--force-dark-mode")
            cmd.append("--enable-features=WebUIDarkMode")
        else:
            cmd.append("--disable-features=WebUIDarkMode")
            
        cmd.append(youtube_url)
        
        process = subprocess.Popen(cmd)
        time.sleep(random.uniform(2, 3))

        actual_duration = max(10, duration)
        random_percentage = random.uniform(0.80, 0.92)

        sleep_duration = actual_duration * random_percentage
        elapsed_time = 0
        next_action_time = random.randint(600, 720)

        while elapsed_time < sleep_duration:
            time.sleep(5)
            elapsed_time += 5
            
            if elapsed_time >= next_action_time:
                perform_human_engagement(profile)
                next_action_time = elapsed_time + random.randint(300, 600)
        
        try:
            process.terminate()
            process.wait(timeout=3)
        except:
            pass

        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'brave' in proc.info['name'].lower():
                    cmdline = proc.info['cmdline']
                    if cmdline and any(profile['profile_path'] in arg for arg in cmdline):
                        proc.kill()
            except:
                pass
                
    except Exception as e:
        print(f"បញ្ហាលើ {profile['name']}: {e}")

@app.route('/run', methods=['POST'])
@limiter.limit("5 per minute")
def run_automation():
    global is_running, run_counter
    
    try:
        requested_count = int(request.form.get('num_profiles', 10))
    except ValueError:
        requested_count = 10

    if not session.get('is_premium') and requested_count > 5:
        return """
        <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
            <h2 style="color: #f44336;">🚫 ដែនកំណត់លើសចំនួន!</h2>
            <p>Free User អាចបើកបានត្រឹមតែ ៥ Profiles ប៉ុណ្ណោះ។</p>
            <p>សូម <a href='/buy-premium'>ទិញគម្រោង Premium</a> ដើម្បីប្រើប្រាស់បានច្រើនជាងនេះ។</p>
            <br>
            <a href='/' style="padding: 10px 20px; background: #2196F3; color: white; text-decoration: none; border-radius: 5px;">ត្រឡប់ក្រោយ</a>
        </div>
        """
    
    with status_lock:
        if is_running:
            return f"<h3>ប្រព័ន្ធកំពុងដំណើរការរួចហើយ! សូមរង់ចាំរហូតទាល់តែចប់សិន។</h3><a href='/'>ត្រឡប់ក្រោយ</a>"
        is_running = True
    
    input_url = request.form.get('query', '').strip()
    
    with history_lock:
        if input_url:
            current_count = search_history_cache.get(input_url, 0)
            if current_count >= 2:
                with status_lock:
                    is_running = False
                return f"""
                <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
                    <h2 style="color: #f44336; font-size: 24px;">🚫 Link នេះត្រូវបាន Block ជាស្ថាពរ!</h2>
                    <p style="font-size: 16px;">Link នេះត្រូវបានយកមក Search ចំនួន <b>2 ដង</b> រួចហើយ។ អ្នកមិនអាចប្រើប្រាស់ Link នេះជាថ្មីទៀតបានទេ។</p>
                    <a href='/' style="padding: 10px 20px; background: #2196F3; color: white; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px;">ត្រឡប់ក្រោយ</a>
                </div>
                """
            search_history_cache[input_url] = current_count + 1
    
    def background_task():
        global is_running, run_counter
        try:
            max_limit = min(requested_count, len(PROFILES))
            profiles_to_run = PROFILES[:max_limit]

            with counter_lock:
                run_counter += 1
                current_count = run_counter

            if current_count >= 10:
                for profile in profiles_to_run:
                    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                        try:
                            if proc.info['name'] and 'brave' in proc.info['name'].lower():
                                cmdline = proc.info['cmdline']
                                if cmdline and any(profile['profile_path'] in arg for arg in cmdline):
                                    proc.kill()
                        except:
                            pass
                with counter_lock:
                    run_counter = 0
                time.sleep(3)

            raw_title = input_url
            duration = 3600  
            
            if "youtube.com" in input_url or "youtu.be" in input_url:
                try:
                    fetched_title, real_duration = get_video_info_via_ytdlp(input_url)
                    if fetched_title:
                        raw_title = fetched_title
                    if real_duration:
                        duration = min(real_duration, 3600) 
                except Exception as e:
                    print(f"⚠️ មិនអាចទាញយកតាម yt_dlp បាន: {e}")
            
            for i, profile in enumerate(profiles_to_run):
                with status_lock:
                    if not is_running:
                        break

                words = raw_title.split()
                if len(words) > 1:
                    percentage = random.uniform(0.90, 0.95)
                    selected_length = max(1, int(len(words) * percentage))
                    profile_query = " ".join(words[:selected_length])
                else:
                    profile_query = raw_title

                encoded_query = profile_query.replace(' ', '+')
                profile_youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}&autoplay=1"

                def profile_video_session(p, initial_url):
                    target_watch_time = random.randint(3000, 3300) 
                    
                    t_proc = threading.Thread(target=run_single_profile_full_process, args=(p, initial_url, target_watch_time))
                    t_proc.daemon = True
                    t_proc.start()
                    
                    elapsed = 0
                    while elapsed < target_watch_time:
                        time.sleep(5)
                        elapsed += 5
                        with status_lock:
                            if not is_running:
                                break
                    
                    if is_running:
                        try:
                            port = 9222 + p['id']
                            res = requests.get(f"http://127.0.0.1:{port}/json", timeout=2)
                            if res.status_code == 200:
                                tabs = res.json()
                                if tabs:
                                    alt_queries = ["Khmer Song", "Relaxing Music", "Lo-Fi Beats", "Technology News", "Vlog Cambodia"]
                                    new_query = random.choice(alt_queries).replace(' ', '+')
                                    new_youtube_url = f"https://www.youtube.com/results?search_query={new_query}&autoplay=1"
                                    
                                    ws_url = tabs[0].get('webSocketDebuggerUrl')
                                    if ws_url:
                                        ws = websocket.create_connection(ws_url, timeout=3)
                                        navigate_js = f"""
                                        (function() {{
                                            window.location.href = "{new_youtube_url}";
                                        }})();
                                        """
                                        payload = {
                                            "id": 1,
                                            "method": "Runtime.evaluate",
                                            "params": {"expression": navigate_js}
                                        }
                                        ws.send(json.dumps(payload))
                                        ws.close()
                        except Exception as ex:
                            print(f"Error switching video for {p['name']}: {ex}")

                pt = threading.Thread(target=profile_video_session, args=(profile, profile_youtube_url))
                pt.daemon = True
                pt.start()
                
                if i < len(profiles_to_run) - 1:
                    time.sleep(random.uniform(10, 15))

        except Exception as e:
            print(f"❌ Error in background_task: {e}")
        finally:
            with status_lock:
                is_running = False

    main_thread = threading.Thread(target=background_task)
    main_thread.daemon = True
    main_thread.start()
    
    return redirect('/')

@app.route('/stop', methods=['POST'])
@limiter.limit("10 per minute")
def stop_process():
    global is_running
    try:
        with status_lock:
            is_running = False  
        
        max_limit = min(20, len(PROFILES))
        profiles_to_close = PROFILES[:max_limit]
        
        for profile in profiles_to_close:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and 'brave' in proc.info['name'].lower():
                        cmdline = proc.info['cmdline']
                        if cmdline and any(profile['profile_path'] in arg for arg in cmdline):
                            proc.kill()
                except:
                    pass

        return redirect('/')
    except Exception as e:
        return redirect('/')

@app.route('/close', methods=['POST'])
@limiter.limit("5 per minute")
def close_profiles():
    try:
        max_limit = min(20, len(PROFILES))
        profiles_to_close = PROFILES[:max_limit]
        
        for profile in profiles_to_close:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and 'brave' in proc.info['name'].lower():
                        cmdline = proc.info['cmdline']
                        if cmdline and any(profile['profile_path'] in arg for arg in cmdline):
                            proc.kill()
                except:
                    pass
            
        return redirect('/')
    except Exception as e:
        return f"<h3>មានបញ្ហាក្នុងការបិទ: {e}</h3><a href='/'>ត្រឡប់ក្រោយ</a>"

@app.route('/admin')
def admin_panel():
    return render_template('admin.html')    

if __name__ == '__main__':
    app.run(debug=True)