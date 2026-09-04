import time
import random
import subprocess
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from config import PROFILES

class BraveAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brave Multi-Profile Automation Suite")
        self.root.geometry("750x550")
        self.root.minsize(700, 500)
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.bg_color = "#f4f6f9"
        self.primary_color = "#2563eb" 
        self.success_color = "#16a34a" 
        self.text_color = "#1f2937"
        
        self.root.configure(bg=self.bg_color)
        
        self.is_running = False
        self.processes = []
        
        self.create_widgets()
        
    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=70)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🚀 Brave Multi-Profile YouTube Launcher", 
            font=("Segoe UI", 16, "bold"), 
            bg=self.primary_color, 
            fg="white"
        )
        title_label.pack(pady=18)
        
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        input_frame = tk.LabelFrame(
            main_container, 
            text=" Configuration ", 
            font=("Segoe UI", 10, "bold"), 
            bg=self.bg_color, 
            fg=self.text_color,
            bd=2, relief=tk.GROOVE
        )
        input_frame.pack(fill=tk.X, padx=0, pady=(0, 15), ipadx=10, ipady=10)
        
        lbl_url = tk.Label(input_frame, text="YouTube URL:", font=("Segoe UI", 10), bg=self.bg_color, fg=self.text_color)
        lbl_url.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.url_entry = tk.Entry(input_frame, font=("Segoe UI", 10), width=45, bd=1, relief=tk.SOLID)
        self.url_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        self.url_entry.insert(0, "https://www.youtube.com/watch?v=...")
        
        self.start_btn = tk.Button(
            input_frame, 
            text="Start Profiles", 
            font=("Segoe UI", 10, "bold"), 
            bg=self.success_color, 
            fg="white", 
            activebackground="#15803d",
            activeforeground="white",
            relief=tk.FLAT,
            padx=15, pady=5,
            command=self.start_automation_thread
        )
        self.start_btn.grid(row=0, column=2, padx=10, pady=5)
        
        info_frame = tk.LabelFrame(
            main_container, 
            text=f" Loaded Profiles ({len(PROFILES)} available) ", 
            font=("Segoe UI", 10, "bold"), 
            bg=self.bg_color, 
            fg=self.text_color,
            bd=2, relief=tk.GROOVE
        )
        info_frame.pack(fill=tk.X, padx=0, pady=(0, 15), ipadx=10, ipady=5)
        
        profile_names = ", ".join([p.get('name', f'Profile {i+1}') for i, p in enumerate(PROFILES)])
        lbl_profiles = tk.Label(
            info_frame, 
            text=f"Profiles: {profile_names}", 
            font=("Segoe UI", 9), 
            bg=self.bg_color, 
            fg="#4b5563",
            wraplength=650,
            justify=tk.LEFT
        )
        lbl_profiles.pack(anchor=tk.W, padx=5, pady=5)
        
        log_frame = tk.LabelFrame(
            main_container, 
            text=" Live Logs & Status ", 
            font=("Segoe UI", 10, "bold"), 
            bg=self.bg_color, 
            fg=self.text_color,
            bd=2, relief=tk.GROOVE
        )
        log_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        self.log_area = scrolledtext.ScrolledText(
            log_frame, 
            font=("Consolas", 9), 
            bg="#0f172a", 
            fg="#38bdf8", 
            insertbackground="white",
            state=tk.DISABLED
        )
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        self.log("ប្រព័ន្ធបានរៀបចំរួចរាល់។ សូមបញ្ចូលលីង YouTube រួចចុច Start Profiles។")

    def log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"> {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def start_automation_thread(self):
        if self.is_running:
            messagebox.showwarning("កំពុងដំណើរការ", "កម្មវិធីកំពុងរត់រួចហើយ!")
            return
            
        url = self.url_entry.get().strip()
        if not url or "watch?v=..." in url:
            messagebox.showerror("កំហុស", "សូមបញ្ចូលលីង YouTube ឱ្យបានត្រឹមត្រូវ!")
            return
            
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED, bg="#9ca3af")
        
        threading.Thread(target=self.run_automation, args=(url,), daemon=True).start()

    def run_automation(self, youtube_url):
        self.log(f"ចាប់ផ្តើមបើក YouTube URL: {youtube_url}")
        brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        
        if not os.path.exists(brave_path):
            self.log("រកមិនឃើញ Brave Browser តាម Path កំណត់ទេ!")
            messagebox.showerror("Error", f"រកមិនឃើញ Brave Browser ទីនេះទេ:\n{brave_path}")
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL, bg=self.success_color)
            return

        for i, profile in enumerate(PROFILES):
            p_name = profile.get('name', f'Profile {i+1}')
            self.log(f"កំពុងបើក Profile ទី {i+1}: {p_name} ({profile.get('theme', 'light')} mode)...")
            
            cmd = [
                brave_path,
                f"--user-data-dir={profile['profile_path']}",
                f"--lang={profile['lang']}",
                f"--window-size={profile['width']},{profile['height']}",
                f"--window-position={profile['pos_x']},{profile['pos_y']}"
            ]
            
            if profile.get("theme") == "dark":
                cmd.append("--force-dark-mode")
                cmd.append("--enable-features=WebUIDarkMode")
            else:
                cmd.append("--disable-features=WebUIDarkMode")
                cmd.append("--blink-settings=darkModeEnabled=false")
                
            cmd.append(youtube_url)
            
            try:
                proc = subprocess.Popen(cmd)
                self.processes.append(proc)
                self.log(f"Profile {i+1} ({p_name}) បានបើកជោគជ័យ!")
            except Exception as e:
                self.log(f"កំហុសក្នុងការបើក Profile {i+1}: {e}")
            
            if i < len(PROFILES) - 1:
                wait_time = random.uniform(5, 10)
                self.log(f"រង់ចាំ {wait_time:.1f} វិនាទី មុនបើក Profile បន្ទាប់...")
                time.sleep(wait_time)

        self.log("🎉 បានបើកដំណើរការគ្រប់ Profiles ទាំងអស់ដោយជោគជ័យពេញលេញ!")
        messagebox.showinfo("ជោគជ័យ", "កម្មវិធីបានបើក Profiles ទាំងអស់រួចរាល់ហើយ!")
        
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL, bg=self.success_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = BraveAutomationApp(root)
    root.mainloop()