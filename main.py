import time
import random
import subprocess
from config import PROFILES

def open_brave_profile(profile_data, youtube_url, index):
    print(f"កំពុងបើក Profile ទី {index + 1}: {profile_data['name']} ({profile_data['theme']} mode)...")
    
    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    
    cmd = [
        brave_path,
        f"--user-data-dir={profile_data['profile_path']}",
        f"--lang={profile_data['lang']}",
        f"--window-size={profile_data['width']},{profile_data['height']}",
        f"--window-position={profile_data['pos_x']},{profile_data['pos_y']}"
    ]
    
    # កំណត់ Theme ពណ៌របស់ Browser (Dark ឬ Light Mode)
    # កំណត់ Theme ពណ៌របស់ Browser ឱ្យដាច់ពីគ្នាខ្លាំង
    if profile_data.get("theme") == "dark":
        cmd.append("--force-dark-mode")
        cmd.append("--enable-features=WebUIDarkMode")
    else:
        cmd.append("--disable-features=WebUIDarkMode")
        cmd.append("--blink-settings=darkModeEnabled=false")
        
    cmd.append(youtube_url)
    
    try:
        process = subprocess.Popen(cmd)
        print(f"Profile {index + 1} បានបើកដោយជោគជ័យ!")
        return process
    except Exception as e:
        print(f"មានបញ្ហាក្នុងការបើក Profile {index + 1}: {e}")
        return None

def main():
    youtube_url = input("សូម Paste លីង YouTube ទីនេះ: ").strip()
    
    if not youtube_url:
        print("សូមបញ្ចូលលីងឱ្យបានត្រឹមត្រូវ!")
        return

    processes = []
    
    for i, profile in enumerate(PROFILES):
        proc = open_brave_profile(profile, youtube_url, i)
        if proc:
            processes.append(proc)
        
        # ចន្លោះពេល Random ពី ៥ ដល់ ១២ វិនាទី ដើម្បីកុំឱ្យបើកព្រមគ្នាកកស្ទះ
        if i < len(PROFILES) - 1:
            wait_time = random.uniform(5, 12)
            print(f"រង់ចាំ {wait_time:.1f} វិនាទី មុននឹងបើក Profile បន្ទាប់...\n")
            time.sleep(wait_time)

    print("\nបានបើកដំណើរការគ្រប់ Profiles ទាំងអស់ដោយភាពខុសគ្នា (Resolution & Theme) យ៉ាងល្អឥតខ្ចោះ!")
    print("សូមចុច Enter នៅលើ Keyboard នេះ ដើម្បីបញ្ចប់កម្មវិធី...")
    input()

if __name__ == "__main__":
    main()