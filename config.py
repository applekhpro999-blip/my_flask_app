import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_DIR = os.path.join(BASE_DIR, "profiles_data")

if not os.path.exists(PROFILES_DIR):
    os.makedirs(PROFILES_DIR)

PROFILES = [
    {
        "id": 1,
        "name": "Profile_1",
        "profile_path": os.path.join(PROFILES_DIR, "profile_1"),
        "width": 371, "height": 322, "pos_x": 0, "pos_y": 0,
        "lang": "en-US", "timezone": "UTC", "theme": "light",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.61.110",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 2,
        "name": "Profile_2",
        "profile_path": os.path.join(PROFILES_DIR, "profile_2"),
        "width": 372, "height": 325, "pos_x": 500, "pos_y": 0,
        "lang": "en-US", "timezone": "UTC", "theme": "dark",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.60.113",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 3,
        "name": "Profile_3",
        "profile_path": os.path.join(PROFILES_DIR, "profile_3"),
        "width": 373, "height": 330, "pos_x": 1000, "pos_y": 0,
        "lang": "en-US", "timezone": "UTC", "theme": "light",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.63.105",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 4,
        "name": "Profile_4",
        "profile_path": os.path.join(PROFILES_DIR, "profile_4"),
        "width": 374, "height": 331, "pos_x": 1500, "pos_y": 0,
        "lang": "en-US", "timezone": "UTC", "theme": "dark",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.57.111",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 5,
        "name": "Profile_5",
        "profile_path": os.path.join(PROFILES_DIR, "profile_5"),
        "width": 375, "height": 335, "pos_x": 2000, "pos_y": 0,
        "lang": "en-US", "timezone": "UTC", "theme": "light",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.64.127",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 6,
        "name": "Profile_6",
        "profile_path": os.path.join(PROFILES_DIR, "profile_6"),
        "width": 370, "height": 327, "pos_x": 0, "pos_y":335,
        "lang": "en-US", "timezone": "UTC", "theme": "dark",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.58.148",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 7,
        "name": "Profile_7",
        "profile_path": os.path.join(PROFILES_DIR, "profile_7"),
        "width": 371, "height": 329, "pos_x": 500, "pos_y": 335,
        "lang": "en-US", "timezone": "UTC", "theme": "light",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.62.108",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 8,
        "name": "Profile_8",
        "profile_path": os.path.join(PROFILES_DIR, "profile_8"),
        "width": 372, "height": 333, "pos_x": 1000, "pos_y": 335,
        "lang": "en-US", "timezone": "UTC", "theme": "dark",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.59.127",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 9,
        "name": "Profile_9",
        "profile_path": os.path.join(PROFILES_DIR, "profile_9"),
        "width": 373, "height": 337, "pos_x": 1500, "pos_y": 335,
        "lang": "en-US", "timezone": "UTC", "theme": "light",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.64.146",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 10,
        "name": "Profile_10",
        "profile_path": os.path.join(PROFILES_DIR, "profile_10"),
        "width": 374, "height": 339, "pos_x": 2000, "pos_y": 335,
        "lang": "en-US", "timezone": "UTC", "theme": "dark",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.59.142",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 11,
        "name": "Profile_11",
        "profile_path": os.path.join(PROFILES_DIR, "profile_11"),
        "width": 375, "height": 342, "pos_x": 0, "pos_y": 700,
        "lang": "en-US", "timezone": "UTC", "theme": "light",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.59.146",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 12,
        "name": "Profile_12",
        "profile_path": os.path.join(PROFILES_DIR, "profile_12"),
        "width": 370, "height": 322, "pos_x": 500, "pos_y": 700,
        "lang": "en-US", "timezone": "UTC", "theme": "dark",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.56.105",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 13,
        "name": "Profile_13",
        "profile_path": os.path.join(PROFILES_DIR, "profile_13"),
        "width": 371, "height": 329, "pos_x": 1000, "pos_y": 700,
        "lang": "en-US", "timezone": "UTC", "theme": "light",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.64.129",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 14,
        "name": "Profile_14",
        "profile_path": os.path.join(PROFILES_DIR, "profile_14"),
        "width": 372, "height": 325, "pos_x": 1500, "pos_y": 700,
        "lang": "en-US", "timezone": "UTC", "theme": "dark",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.58.143",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 15,
        "name": "Profile_15",
        "profile_path": os.path.join(PROFILES_DIR, "profile_15"),
        "width": 373, "height": 328, "pos_x": 2000, "pos_y": 700,
        "lang": "en-US", "timezone": "UTC", "theme": "light",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.55.148",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 16,
        "name": "Profile_16",
        "profile_path": os.path.join(PROFILES_DIR, "profile_16"),
        "width": 374, "height": 333, "pos_x": 0, "pos_y": 700,
        "lang": "en-US", "timezone": "UTC", "theme": "dark",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.56.115",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 17,
        "name": "Profile_17",
        "profile_path": os.path.join(PROFILES_DIR, "profile_17"),
        "width": 375, "height": 322, "pos_x": 500, "pos_y": 1050,
        "lang": "en-US", "timezone": "UTC", "theme": "light",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.55.117",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 18,
        "name": "Profile_18",
        "profile_path": os.path.join(PROFILES_DIR, "profile_18"),
        "width": 370, "height": 326, "pos_x": 1000, "pos_y": 1050,
        "lang": "en-US", "timezone": "UTC", "theme": "dark",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.62.137",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 19,
        "name": "Profile_19",
        "profile_path": os.path.join(PROFILES_DIR, "profile_19"),
        "width": 371, "height": 329, "pos_x": 1500, "pos_y": 1050,
        "lang": "en-US", "timezone": "UTC", "theme": "light",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.62.133",
        "browser_type": "brave",
        "proxy": ""
    },
    {
        "id": 20,
        "name": "Profile_20",
        "profile_path": os.path.join(PROFILES_DIR, "profile_20"),
        "width": 372, "height": 335, "pos_x": 2000, "pos_y": 1050,
        "lang": "en-US", "timezone": "UTC", "theme": "dark",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Brave/1.61.144",
        "browser_type": "brave",
        "proxy": ""
    },
]
