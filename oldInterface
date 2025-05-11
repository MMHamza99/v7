import tkinter as tk
import webbrowser
from threading import Thread
import webbrowser
import requests, time, random, glob, os, datetime, threading, webbrowser, uuid, json
from urllib.parse import unquote
from tkinter import ttk, filedialog, messagebox
from bs4 import BeautifulSoup as bs
import ctypes as ct
from base64 import b64encode

req = requests.session()
try:
    req.get('https://hamzaapi.online/api/check.php', timeout=5)
except:
    pass
def dark_title_bar(window):
    """
    Sets the window attribute to use the immersive dark mode for the title bar.
    """
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))
def checkMac(mac):
    data = {
        'api_method': 'loguser',
        'api_data': json.dumps({
                "serial": mac
            })
    }
    res = requests.post('https://hamzaapi.online/api/check.php', data=data, timeout=5)
    try:
        if res.json()['IsError'] == False:
            return res.json()['ResponseData']
        else: return False
    except:
        errors.append(0)
        if len(errors) >= 5:
            return None
        return checkMac(mac)
def savePost(postId, postText, postTime):
    url = "https://hamzaapi.online/api/api.php"
    api_method = "loguser"
    api_data = {
        "serial": mac,
        "postId": postId,
        "postText": postText,
        "postTime": postTime,
    }
    post_data = {
        "api_method": api_method,
        "api_data": json.dumps(api_data)
    }
    try:
        req.post(url, data=post_data)
    except:
        pass
def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 2)][::-1])
    return mac

times, errors = [], []

# ------------------------------------------------------
def get_timestamp(times):
    if not times:
        return False

    date = times.pop(0)
    day, hour, minute, month = map(int, date.split('-'))
    second = random.randint(1, 59)
    now = datetime.datetime.now() + datetime.timedelta(hours=1)
    year = now.year
    target_date = datetime.datetime(year, month, day, hour, minute, second)

    if target_date < now:
        if times:
            return get_timestamp(times)
        else:
            return False
    timestamp = int(time.mktime(target_date.timetuple()))
    return timestamp
class RandomTimeGenerator(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Random Time Generator")
        self.configure(bg='#222222')
        dark_title_bar(self)

        self.start_day = tk.IntVar(value=1)  # Default start day
        self.end_day = tk.IntVar(value=28)  # Default end day
        self.start_time = tk.StringVar(value="9:00")  # Default start time
        self.end_time = tk.StringVar(value="23:00")  # Default end time
        self.posts_per_day = tk.IntVar(value=5)  # Default posts per day
        self.month = tk.IntVar(value=datetime.datetime.now().month)  # Default month

        ttk.Label(self, text="Start Day:").grid(row=0, column=0, padx=5, pady=5)
        self.start_day_spinbox = ttk.Spinbox(self, from_=1, to=31, textvariable=self.start_day, width=5)
        self.start_day_spinbox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="End Day:").grid(row=1, column=0, padx=5, pady=5)
        self.end_day_spinbox = ttk.Spinbox(self, from_=1, to=31, textvariable=self.end_day, width=5)
        self.end_day_spinbox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Start Time (HH:MM):").grid(row=2, column=0, padx=5, pady=5)
        self.start_time_entry = ttk.Entry(self, textvariable=self.start_time, width=10)
        self.start_time_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="End Time (HH:MM):").grid(row=3, column=0, padx=5, pady=5)
        self.end_time_entry = ttk.Entry(self, textvariable=self.end_time, width=10)
        self.end_time_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text="Posts per Day:").grid(row=4, column=0, padx=5, pady=5)
        self.posts_per_day_spinbox = ttk.Spinbox(self, from_=1, to=100, textvariable=self.posts_per_day, width=5)
        self.posts_per_day_spinbox.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text="Month:").grid(row=5, column=0, padx=5, pady=5)
        self.month_spinbox = ttk.Spinbox(self, from_=1, to=12, textvariable=self.month, width=5)
        self.month_spinbox.grid(row=5, column=1, padx=5, pady=5)

        generate_button = ttk.Button(self, text="Generate", command=self.generate_times)
        generate_button.grid(row=6, column=0, columnspan=2, pady=10)

    def generate_times(self):
        start_day = self.start_day.get()
        end_day = self.end_day.get()
        start_time = self.start_time.get()
        end_time = self.end_time.get()
        posts_per_day = self.posts_per_day.get()
        month = self.month.get()

        try:
            start_hour, start_minute = map(int, start_time.split(':'))
            end_hour, end_minute = map(int, end_time.split(':'))
        except ValueError:
            messagebox.showerror("Input Error", "Invalid time format. Please use HH:MM.")
            return

        if start_day < 1 or start_day > 31 or end_day < 1 or end_day > 31:
            messagebox.showerror("Input Error", "Days must be between 1 and 31.")
            return

        if start_hour < 0 or start_hour > 23 or end_hour < 0 or end_hour > 23 or start_minute < 0 or start_minute > 59 or end_minute < 0 or end_minute > 59:
            messagebox.showerror("Input Error", "Invalid time. Please use 24-hour format and valid minutes.")
            return

        random_times = []
        used_times = set()  # To store used times as a set for quick lookup

        for day in range(start_day, end_day + 1):
            random_hours = random.sample(range(start_hour, end_hour + 1), posts_per_day)  # Randomly choose hours for this day
            random_hours.sort()  # Sort random hours chronologically for this day

            last_post_time = None  # Track the time of the last posted post

            for random_hour in random_hours:
                random_minute = random.randint(0, 59)
                random_time = f"{day}-{random_hour}-{random_minute}-{month}"

                if last_post_time:
                    last_hour, last_minute = map(int, last_post_time.split('-')[1:3])
                    last_datetime = datetime.datetime(year=2024, month=int(month), day=day, hour=last_hour, minute=last_minute)
                    current_datetime = datetime.datetime(year=2024, month=int(month), day=day, hour=random_hour, minute=random_minute)
                    time_difference = (current_datetime - last_datetime).total_seconds() / 60

                    if time_difference < 30:
                        continue  # If less than 30 minutes gap, skip this time

                if random_time not in used_times:
                    used_times.add(random_time)
                    random_times.append(random_time)
                    last_post_time = random_time  # Update last posted post time

        global times
        times = random_times
        self.destroy()


def initialize_gui():
    global root
    if checkOut and checkOut['valid'] == True:
        ScriptRunnerApp(root)
    else:
        AccessDeniedUI(root, mac)


# ------------------------------------------------------
class ScriptRunnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cloner")
        self.root.configure(bg="#222222")
        self.root.resizable(False, False)
        self.create_custom_style()
        self.create_widgets()
    def create_widgets(self):
        # Welcome message
        dark_title_bar(self.root)
        welcome_label = tk.Label(self.root, text="Welcome to Social Cloner V7", font=("Helvetica", 20, "bold"), fg="#ffffff", bg='#222222')
        welcome_label.pack(pady=10)
        devName = tk.Label(self.root, text="   Developed by: Mohammed Hamza   ", font=("Segoe UI", 12), fg="#ffffff", bg='#333333')
        devName.pack(pady=1)

        timeLeft = tk.Label(self.root, text=f"   Your subscription ends: {ends}   ", font=("Segoe UI", 10), fg="#ffffff", bg='#222222')
        timeLeft.pack(pady=5)

        # Create a frame for the buttons
        button_frame = tk.Frame(self.root, bg='#222222')
        button_frame.pack(pady=5)

        # Define button styles
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 14), padding=10, width=25)
        style.map("TButton", background=[("active", "#e57373")])

        # Create buttons for each script
        button1 = ttk.Button(button_frame, text="Instagram Posts Downloader", command=lambda: self.run_script(InstaPostsDownloader), style='TButton')
        button2 = ttk.Button(button_frame, text="Instagram Reels Downloader", command=lambda: self.run_script(InstaReelsDownloader), style='TButton')
        button3 = ttk.Button(button_frame, text="Facebook Reels Downloader", command=lambda: self.run_script(FaceReelsDownloader), style='TButton')
        button4 = ttk.Button(button_frame, text="TikTok Videos Downloader", command=lambda: self.run_script(TiktokVideosDownloader), style='TButton')

        button5 = ttk.Button(button_frame, text="Facebook Posts Uploader", command=lambda: self.run_script(FacePostsUploader), style='TButton')
        button6 = ttk.Button(button_frame, text="Facebook Reels Uploader", command=lambda: self.run_script(FaceReelsUploader), style='TButton')
        button7 = ttk.Button(button_frame, text="Facebook Videos Uploader", command=lambda: self.run_script(FaceVideosUploader), style='TButton')

        # Use grid to place buttons in rows
        button1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        button2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        button3.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        button4.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        button5.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        button6.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        button7.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")


        # Developer contact info button
        contact_button = ttk.Button(self.root, text="Contact Developer", command=self.show_contact_info, style='TButton')
        contact_button.pack(pady=10)

        # Exit button
        exit_button = ttk.Button(self.root, text="Exit", command=self.root.quit, style='TButton')
        exit_button.pack(pady=10)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, font=("Helvetica", 10), bg="#222222", fg="#ffffff", bd=1, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")
    def run_script(self, script_class):
        script = script_class()
        script.run(self.root)
        self.status_var.set(f"{script_class.__name__} is running...")

    def create_custom_style(self):
        style = ttk.Style(self.root)
        style.theme_create("gptdark", parent="clam", settings={
            "TButton": {
                "configure": {"background": "#333333", "foreground": "#ffffff", "padding": 10, "anchor": "center"},
                "map": {
                    "background": [("active", "#444444"), ("disabled", "#666666")],
                    "foreground": [("pressed", "#ffffff"), ("active", "#ffffff")]
                }
            },
            "TLabel": {
                "configure": {"background": "#1e1e1e", "foreground": "#ffffff", 'font': ("Segoe UI", 13)}
            },
            "TEntry": {
                "configure": {"fieldbackground": "#333333", "foreground": "#ffffff", 'font': ("Segoe UI", 13), 'padding':'6'}
            },
            "TFrame": {
                "configure": {"background": "#1e1e1e"}
            },
            "TCombobox": {
                "configure": {"fieldbackground": "#333333", "foreground": "#ffffff", "background": "#444444"},
                "map": {
                    "background": [("active", "#444444")],
                    "fieldbackground": [("readonly", "#333333")]
                }
            },
            "TNotebook": {
                "configure": {"background": "#1e1e1e", "foreground": "#ffffff"},
                "map": {
                    "background": [("active", "#444444")]
                }
            },
            "TNotebook.Tab": {
                "configure": {"background": "#333333", "foreground": "#ffffff", "padding": [10, 5]},
                "map": {
                    "background": [("selected", "#444444"), ("active", "#444444")],
                    "foreground": [("selected", "#ffffff"), ("active", "#ffffff")]
                }
            },
            "TProgressbar": {
                "configure": {"background": "#007acc", "troughcolor": "#333333"}
            }
        })
        style.theme_use("gptdark")
    def show_contact_info(self):
        webbrowser.open("https://www.facebook.com/MMHamza02")  # Replace with the developer's Facebook profile link

class AccessDeniedUI:
    def __init__(self, root, mac):
        self.root = root
        self.mac = mac
        self.root.title("Access Denied")
        dark_title_bar(self.root)
        # Set the custom GPT style
        self.create_custom_style()

        # Set window size and background color
        # self.root.geometry("400x300")
        self.root.config(bg="#1e1e1e")

        # Message frame
        self.message_frame = ttk.Frame(self.root, style='TFrame')
        self.message_frame.pack(pady=50, padx=50)

        self.message_label = ttk.Label(self.message_frame, text="Access Denied !", style="TLabel", foreground='red', font=("Segoe UI", 20))
        self.message_label.pack()
        if ends:
            timeLeft = ttk.Label(self.root, text=f"   Your subscription end at: {ends}   ", font=("Segoe UI", 10))
            timeLeft.pack(pady=20)
        self.instruction_label = ttk.Label(self.message_frame, text="Please contact the admin and provide your MAC address.", style="TLabel")
        self.instruction_label.pack(pady=10)

        # Copy MAC address button
        self.copy_button = ttk.Button(self.message_frame, text="Copy MAC Address", style="TButton", command=self.copy_mac_address, width=25)
        self.copy_button.pack(pady=10)

        # Contact admin button
        self.contact_admin_button = ttk.Button(self.message_frame, text="Contact Admin", style="TButton", command=lambda: webbrowser.open("https://www.facebook.com/MMHamza02"), width=25)
        self.contact_admin_button.pack(pady=10)
    def create_custom_style(self):
        style = ttk.Style(self.root)
        style.theme_create("gptdark", parent="clam", settings={
            "TButton": {
                "configure": {"background": "#333333", "foreground": "#ffffff", "padding": 10, "anchor": "center"},
                "map": {
                    "background": [("active", "#e47474"), ("disabled", "#e47474")],
                    "foreground": [("pressed", "#ffffff"), ("active", "#ffffff")]
                }
            },
            "TLabel": {
                "configure": {"background": "#1e1e1e", "foreground": "#ffffff", 'font': ("Segoe UI", 13)}
            },
            "TFrame": {
                "configure": {"background": "#1e1e1e"}
            },
        })
        style.theme_use("gptdark")
    def copy_mac_address(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.mac)
        self.root.update()
        self.copy_button.config(text="Copied")

class loading:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Error")
        dark_title_bar(self.root)
        # Set the custom GPT style
        self.create_custom_style()

        # Set window size and background color
        # self.root.geometry("400x300")
        self.root.config(bg="#1e1e1e")

        # Message frame
        self.message_frame = ttk.Frame(self.root, style='TFrame')
        self.message_frame.pack(pady=50, padx=50)

        self.message_label = ttk.Label(self.message_frame, text="Internet Error", style="TLabel", foreground='red', font=("Segoe UI", 20))
        self.message_label.pack()
        self.instruction_label = ttk.Label(self.message_frame, text="Please Check Your Internet and try Again, Or Contact Admin .", style="TLabel")
        self.instruction_label.pack(pady=10)

        # Contact admin button
        self.contact_admin_button = ttk.Button(self.message_frame, text="Contact Admin", style="TButton", command=lambda: webbrowser.open("https://www.facebook.com/MMHamza02"), width=25)
        self.contact_admin_button.pack(pady=10)
    def create_custom_style(self):
        style = ttk.Style(self.root)
        style.theme_create("gptdark", parent="clam", settings={
            "TButton": {
                "configure": {"background": "#333333", "foreground": "#ffffff", "padding": 10, "anchor": "center"},
                "map": {
                    "background": [("active", "#e47474"), ("disabled", "#e47474")],
                    "foreground": [("pressed", "#ffffff"), ("active", "#ffffff")]
                }
            },
            "TLabel": {
                "configure": {"background": "#1e1e1e", "foreground": "#ffffff", 'font': ("Segoe UI", 13)}
            },
            "TFrame": {
                "configure": {"background": "#1e1e1e"}
            },
        })
        style.theme_use("gptdark")

# ------------------------------------------------------

class InstaPostsDownloader:
    def setDownloader(self):
        self.req = requests.session()
        self.req.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate,",
            "accept-language": "ar",
            "priority": "u=0, i",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
        }
        if not self.instaData():
            self.req.headers['X-Csrftoken'] = 'O8B3xUFsEP0A6I4e1h6cPO6xIRvqh6q6'
            self.req.headers['X-Ig-App-Id'] = '936619743392459'
            self.req.headers['X-Ig-Www-Claim'] = 'hmac.AR3wqeSXGtPYFFlf5P1XbwupBzGTXyu_lZgJEOeeXdQDCs0m'

        self.dn = []
        self.stop_flag = False

    def instaData(self):
        res = self.req.get('https://www.instagram.com')
        try:
            csrf_token = res.text.split('"csrf_token":"')[1].split('"')[0]
            self.req.headers['X-Csrftoken'] = csrf_token
            APP_ID = res.text.split('"APP_ID":"')[1].split('"')[0]
            self.req.headers['X-Ig-App-Id'] = APP_ID
            claim = res.text.split('"claim":"')[1].split('"')[0]
            self.req.headers['X-Ig-Www-Claim'] = claim
            return True
        except:
            return False

    def getUserId(self, user):
        url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={user}'
        res = self.req.get(url)
        try:
            self.userId = res.json()['data']['user']['id']
            return True
        except Exception as e:
            self.message_text.config(state=tk.NORMAL)
            self.message_text.insert(tk.END, f"Error getting user ID: {e}\n")
            self.message_text.see(tk.END)
            self.message_text.config(state=tk.DISABLED)
            return False
    def getPhotos(self, next_max_id):
        needed = self.howMany - len(self.dn)
        if next_max_id == 0:
            url = f'https://www.instagram.com/api/v1/feed/user/{self.userId}/?count=20'
        else:
            url = f'https://www.instagram.com/api/v1/feed/user/{self.userId}/?count={needed}&max_id={next_max_id}'

        res = self.req.get(url)
        items = res.json()['items']
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, f"Done Get {len(items)} Posts .\n")
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.DISABLED)
        for item in items:
            if self.stop_flag:
                return
            if len(self.dn) >= self.howMany:
                break
            if item['media_type'] == 1 or item['media_type'] == 8:
                try:
                    caption_texts = open(f'images/{self.userName}/caption_texts.txt', 'r', encoding='utf-8').read()
                except Exception as e:
                    caption_texts = ''
                media_id = item['pk']
                if media_id not in caption_texts:
                    try:
                        caption_text = item['caption']['text'].replace('\n', ' ').replace('\r', ' ').replace(':', '')
                    except:
                        caption_text = ' '
                    open(f'images/{self.userName}/caption_texts.txt', 'a', encoding='utf-8').write(f'{media_id}::||{caption_text}\n')
                    if item.get('carousel_media'):
                        count = 0
                        for i in item.get('carousel_media'):
                            url = i['image_versions2']['candidates'][0]['url']
                            mediaId = f'{media_id}_{count}'
                            self.download(mediaId, url)
                            count += 1
                    else:
                        url = item['image_versions2']['candidates'][0]['url']
                        self.download(media_id, url)
                    self.dn.append(0)
                    self.update_progress(len(self.dn), self.howMany)

        if res.json().get('more_available') and len(self.dn) != self.howMany:
            next_max_id = res.json()['next_max_id']
            self.getPhotos(next_max_id)
        else:
            self.message_text.config(state=tk.NORMAL)
            self.message_text.insert(tk.END, "Done Download All.\n")
            self.message_text.see(tk.END)
            self.message_text.config(state=tk.DISABLED)
            self.stop_flag = True
            self.btn_download.config(text="Download", style="TButton.Download.TButton", command=self.start_download)
    def download(self, media_id, url):
        res = self.req.get(url)
        try:
            with open(f'images/{self.userName}/{media_id}.jpg', 'wb') as f:
                f.write(res.content)
        except:
            self.message_text.config(state=tk.NORMAL)
            self.message_text.insert(tk.END, f"Can't Download>> {media_id}\n")
            self.message_text.see(tk.END)
            self.message_text.config(state=tk.DISABLED)
            return False
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, f"Done Download: {media_id}\n")
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.DISABLED)
    def color(self):
        # Dark Mode Colors
        self.background_color = "#262626"
        self.text_color = "#ffffff"
        self.highlight_color = "#0095f6"
        self.button_color = "#248df0"  # Initial color
        self.button_stop_color = "#ff3333"  # Color when stopped
        self.button_hover_color = "#57a7f2"  # Color when hovered
        self.button_hover_color2 = "#f52718"  # Color when hovered
        self.entry_color = "#333333"
        self.border_color = "#4d4d4d"
    def contant(self):
        dark_title_bar(self.window)
        frame = ttk.Frame(self.window, padding="20", style="TFrame")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S),)

        ttk.Label(frame, text="Instagram Posts Downloader", font=("Segoe UI", 16, "bold"), foreground=self.highlight_color).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Instagram Username:",).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_username = ttk.Entry(frame, width=30, style="TEntry")
        self.entry_username.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Number of Posts:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_post_count = ttk.Entry(frame, width=30, style="TEntry")
        self.entry_post_count.grid(row=2, column=1, padx=10, pady=10)

        self.btn_download = ttk.Button(frame, text="Download", command=self.start_download, style="TButton.Download.TButton")
        self.btn_download.grid(row=3, column=0, columnspan=2, padx=10, pady=20, sticky=(tk.W, tk.E))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(frame, variable=self.progress_var, maximum=100, style="TProgressbar")
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))

        self.progress_label = ttk.Label(frame, text="0% (0/0)")
        self.progress_label.grid(row=5, column=0, columnspan=2)

        # Text widget to display messages
        self.message_text = tk.Text(frame, height=8, width=40, wrap=tk.WORD)
        self.message_text.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))
        self.message_text.config(fg="#ffffff", bg='#222222')
    def start_download(self):
        userName = self.entry_username.get()
        try:
            howMany = int(self.entry_post_count.get())
        except ValueError:
            self.messagebox.showerror("Error", "Please enter a valid number for the posts count.")
            return

        if not userName:
            self.messagebox.showerror("Error", "Please enter an Instagram username.")
            return

        folder_path = f'images/{userName}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self.howMany = howMany
        self.userName = userName
        self.stop_flag = False
        self.setDownloader()

        if self.getUserId(userName):
            self.btn_download.config(text="Stop", style="TButton.Stop.TButton", command=self.stop_download)
            download_thread = Thread(target=self.getPhotos, args=(0,))
            download_thread.start()
            # Display initial message
            self.message_text.config(state=tk.NORMAL)
            self.message_text.delete(1.0, tk.END)  # Clear previous messages
            self.message_text.insert(tk.END, "Downloading...\n")
            self.message_text.see(tk.END)  # Scroll to the end of the text widget
            self.message_text.config(state=tk.DISABLED)
        else:
            self.messagebox.showerror("Error", "Failed to get user ID. Please check the username.")
    def stop_download(self):
        self.stop_flag = True
        self.btn_download.config(text="Download", style="TButton.Download.TButton", command=self.start_download)
        # Display stop message
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, "Download stopped.\n")
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.DISABLED)
    def update_progress(self, current, total):
        percent = (current / total) * 100
        self.progress_var.set(percent)
        self.progress_label.config(text=f"{int(percent)}% ({current}/{total})")
        # Append messages to a text widget or label
    def run(self, parent):
        self.color()
        self.window = tk.Toplevel(parent)
        self.window.title("Instagram Posts Downloader")
        # self.window.geometry("400x510")
        self.window.resizable(False, False)

        self.contant()

class InstaReelsDownloader:
    def setDownloader(self):
        self.req = requests.session()
        self.req.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate,",
            "accept-language": "ar",
            "priority": "u=0, i",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
        }
        if not self.instaData():
            self.req.headers['X-Csrftoken'] = 'O8B3xUFsEP0A6I4e1h6cPO6xIRvqh6q6'
            self.req.headers['X-Ig-App-Id'] = '936619743392459'
            self.req.headers['X-Ig-Www-Claim'] = 'hmac.AR3wqeSXGtPYFFlf5P1XbwupBzGTXyu_lZgJEOeeXdQDCs0m'

        self.dn = []
        self.stop_flag = False
    def instaData(self):
        res = self.req.get('https://www.instagram.com')
        try:
            csrf_token = res.text.split('"csrf_token":"')[1].split('"')[0]
            self.req.headers['X-Csrftoken'] = csrf_token
            APP_ID = res.text.split('"APP_ID":"')[1].split('"')[0]
            self.req.headers['X-Ig-App-Id'] = APP_ID
            claim = res.text.split('"claim":"')[1].split('"')[0]
            self.req.headers['X-Ig-Www-Claim'] = claim
            return True
        except:
            return False

    def getUserId(self, user):
        url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={user}'
        res = self.req.get(url)
        try:
            self.userId = res.json()['data']['user']['id']
            print(self.userId)
            return True
        except Exception as e:
            self.message_text.config(state=tk.NORMAL)
            self.message_text.insert(tk.END, f"Error getting user ID: {e}\n")
            self.message_text.see(tk.END)
            self.message_text.config(state=tk.DISABLED)
            return False
    def getReels(self, next_max_id):
        needed = self.howMany - len(self.dn)
        if next_max_id == 0:
            data = {
                'include_feed_video': 'true',
                'page_size': needed,
                'target_user_id': self.userId
            }
        else:
            data = {
                'include_feed_video': 'true',
                'max_id': next_max_id,
                'page_size': needed,
                'target_user_id': self.userId
            }

        url = f'https://www.instagram.com/api/v1/clips/user/'
        res = self.req.post(url, data=data)
        print(res.json())
        items = res.json()['items']
        # items[0].media.video_versions[0].url
        for item in items:
            if self.stop_flag:
                return
            if item['media']['media_type'] == 2:
                try:
                    caption_texts = open(f'Videos/{self.userName}/caption_texts.txt', 'r', encoding='utf-8').read()
                except:
                    caption_texts = ''
                media_id = item['media']['pk']
                if media_id not in caption_texts:
                    try:
                        caption_text = item['media']['caption']['text'].replace('\n', ' ').replace('\r', ' ').replace(':', '')
                    except:
                        caption_text = ' '
                    open(f'Videos/{self.userName}/caption_texts.txt', 'a', encoding='utf-8').write(f'{media_id}::||{caption_text}\n')
                    url = item['media']['video_versions'][0]['url']
                    self.download(media_id, url)
                    self.dn.append(0)
                    self.update_progress(len(self.dn), self.howMany)
        # paging_info.more_available
        if res.json()['paging_info']['more_available'] and len(self.dn) != self.howMany:
            try:
                next_max_id = res.json()['paging_info']['next_max_id']
            except:
                next_max_id = res.json()['paging_info']['max_id']
            self.getReels(next_max_id)
        else:
            self.message_text.config(state=tk.NORMAL)
            self.message_text.insert(tk.END, "Done Download All.\n")
            self.message_text.see(tk.END)
            self.message_text.config(state=tk.DISABLED)
            self.stop_flag = True
            self.btn_download.config(text="Download", style="TButton.Download.TButton", command=self.start_download)
    def download(self, media_id, url):
        try:
            res = self.req.get(url)
            with open(f'Videos/{self.userName}/{media_id}.mp4', 'wb') as file:
                for chunk in res.iter_content(chunk_size=1024*1024):
                    file.write(chunk)
        except:
            self.message_text.config(state=tk.NORMAL)
            self.message_text.insert(tk.END, f"Can't Download>> {media_id}\n")
            self.message_text.see(tk.END)
            self.message_text.config(state=tk.DISABLED)
            return False
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, f"Done Download: {media_id}\n")
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.DISABLED)
        return True
    def color(self):
        # Dark Mode Colors
        self.background_color = "#262626"
        self.text_color = "#ffffff"
        self.highlight_color = "#0095f6"
        self.button_color = "#248df0"  # Initial color
        self.button_stop_color = "#ff3333"  # Color when stopped
        self.button_hover_color = "#57a7f2"  # Color when hovered
        self.button_hover_color2 = "#f52718"  # Color when hovered
        self.entry_color = "#333333"
        self.border_color = "#4d4d4d"
    def contant(self):
        dark_title_bar(self.window)
        frame = ttk.Frame(self.window, padding="20", style="TFrame")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Instagram Reels Downloader", font=("Segoe UI", 16, "bold"), foreground=self.highlight_color).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Instagram Username:",).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_username = ttk.Entry(frame, width=30, style="TEntry")
        self.entry_username.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Number of Reels:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_post_count = ttk.Entry(frame, width=30, style="TEntry")
        self.entry_post_count.grid(row=2, column=1, padx=10, pady=10)

        self.btn_download = ttk.Button(frame, text="Download", command=self.start_download, style="TButton.Download.TButton")
        self.btn_download.grid(row=3, column=0, columnspan=2, padx=10, pady=20, sticky=(tk.W, tk.E))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(frame, variable=self.progress_var, maximum=100, style="TProgressbar")
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))

        self.progress_label = ttk.Label(frame, text="0% (0/0)")
        self.progress_label.grid(row=5, column=0, columnspan=2)

        # Text widget to display messages
        self.message_text = tk.Text(frame, height=8, width=40, wrap=tk.WORD)
        self.message_text.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))
        self.message_text.config(bg="#222222", fg='#ffffff')
    def start_download(self):
        userName = self.entry_username.get()
        try:
            howMany = int(self.entry_post_count.get())
        except ValueError:
            self.messagebox.showerror("Error", "Please enter a valid number for the reels count.")
            return

        if not userName:
            self.messagebox.showerror("Error", "Please enter an Instagram username.")
            return

        folder_path = f'Videos/{userName}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self.howMany = howMany
        self.userName = userName
        self.stop_flag = False
        self.setDownloader()

        if self.getUserId(userName):
            self.btn_download.config(text="Stop", style="TButton.Stop.TButton", command=self.stop_download)
            download_thread = Thread(target=self.getReels, args=(0,))
            download_thread.start()
            # Display initial message
            self.message_text.config(state=tk.NORMAL)
            self.message_text.delete(1.0, tk.END)  # Clear previous messages
            self.message_text.insert(tk.END, "Downloading...\n")
            self.message_text.see(tk.END)  # Scroll to the end of the text widget
            self.message_text.config(state=tk.DISABLED)
        else:
            self.messagebox.showerror("Error", "Failed to get user ID. Please check the username.")
    def stop_download(self):
        self.stop_flag = True
        self.btn_download.config(text="Download", style="TButton.Download.TButton", command=self.start_download)
        # Display stop message
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, "Download stopped.\n")
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.DISABLED)
    def update_progress(self, current, total):
        percent = (current / total) * 100
        self.progress_var.set(percent)
        self.progress_label.config(text=f"{int(percent)}% ({current}/{total})")
        # Append messages to a text widget or label
    def run(self, parent):
        self.color()
        self.window = tk.Toplevel(parent)
        self.window.title("Instagram Reels Downloader")
        # self.window.geometry("400x510")
        self.window.resizable(False, False)
        self.contant()

class FaceReelsDownloader:
    def setDownloader(self):
        self.req = requests.session()
        self.req.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'origin': 'https://www.facebook.com',
            'priority': 'u=1, i',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.183", "Google Chrome";v="126.0.6478.183"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-asbd-id': '129477',
            'x-fb-friendly-name': 'ProfileCometAppCollectionReelsRendererPaginationQuery',
            'x-fb-lsd': 'AVpwX9406R8',
        }
        self.dn = []
        self.stop_flag = False
    def idToShortcode(self, pageId):
        feedback_id = bytes(f"app_collection:{pageId}:168684841768375:260", 'utf-8')
        feedback_id = b64encode(feedback_id)
        feed = str(feedback_id.decode("utf-8"))
        self.pageShortCode = feed
    def getReels(self, cursor):
        url = 'https://www.facebook.com/api/graphql/'
        data = {
            'variables': '{"count":20,"cursor":"THISISCURSOR","feedLocation":"COMET_MEDIA_VIEWER","feedbackSource":65,"focusCommentID":null,"renderLocation":null,"scale":1,"useDefaultActor":true,"id":"THISISPAGEID"}'.replace('THISISPAGEID', str(self.pageShortCode)).replace('THISISCURSOR', str(cursor)),
            'doc_id': '8198152870249607',
        }
        res = self.req.post(url, data=data)
        jsonRes = json.loads(res.text.split('\n')[0])
        items = jsonRes['data']['node']['aggregated_fb_shorts']['edges']
        for item in items:
            if len(self.dn) >= self.howMany:
                self.message_text.config(state=tk.NORMAL)
                self.message_text.insert(tk.END, "Done Download All.\n")
                self.message_text.see(tk.END)
                self.message_text.config(state=tk.DISABLED)
                self.stop_flag = True
                self.btn_download.config(text="Download", style="TButton.Download.TButton", command=self.start_download)
                break
            if self.stop_flag:
                return
            try:
                caption_texts = open(f'Videos/{self.userName}/caption_texts.txt', 'r', encoding='utf-8').read()
            except:
                caption_texts = ''
            media_id = item['profile_reel_node']['node']['video']['id']
            if media_id not in caption_texts:
                try:
                    caption_text = item['profile_reel_node']['node']['message']['text'].replace('\n', ' ').replace('\r', ' ').replace(':', '')
                except:
                    caption_text = ' '
                open(f'Videos/{self.userName}/caption_texts.txt', 'a', encoding='utf-8').write(f'{media_id}::||{caption_text}\n')
                url = item['profile_reel_node']['node']['short_form_video_context']['playback_video']['browser_native_hd_url']
                if url == None:
                    url = item['profile_reel_node']['node']['short_form_video_context']['playback_video']['browser_native_sd_url']
                self.download(media_id, url)
                self.dn.append(0)
                self.update_progress(len(self.dn), self.howMany)
        # paging_info.more_available
        try:
            next_max_id = jsonRes['data']['node']['aggregated_fb_shorts']['page_info']['end_cursor']
        except:
            next_max_id = ''
        if next_max_id != '':
            self.getReels(next_max_id)
        else:
            self.message_text.config(state=tk.NORMAL)
            if len(items) == 0:
                self.message_text.insert(tk.END, "PLease Make Sure Page Have Reels\n")
            self.message_text.insert(tk.END, "Done Download All.\n")
            self.message_text.see(tk.END)
            self.message_text.config(state=tk.DISABLED)
            self.stop_flag = True
            self.btn_download.config(text="Download", style="TButton.Download.TButton", command=self.start_download)
    def download(self, media_id, url):
        try:
            res = requests.get(url)
            with open(f'Videos/{self.userName}/{media_id}.mp4', 'wb') as file:
                for chunk in res.iter_content(chunk_size=1024*1024):
                    file.write(chunk)
        except:
            self.message_text.config(state=tk.NORMAL)
            self.message_text.insert(tk.END, f"Can't Download>> {media_id}\n")
            self.message_text.see(tk.END)
            self.message_text.config(state=tk.DISABLED)
            return False
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, f"Done Download: {media_id}\n")
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.DISABLED)
        return True
    def color(self):
        # Dark Mode Colors
        self.background_color = "#262626"
        self.text_color = "#ffffff"
        self.highlight_color = "#0095f6"
        self.button_color = "#248df0"  # Initial color
        self.button_stop_color = "#ff3333"  # Color when stopped
        self.button_hover_color = "#57a7f2"  # Color when hovered
        self.button_hover_color2 = "#f52718"  # Color when hovered
        self.entry_color = "#333333"
        self.border_color = "#4d4d4d"
    def contant(self):
        dark_title_bar(self.window)
        frame = ttk.Frame(self.window, padding="20", style="TFrame")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Facebook Reels Downloader", font=("Segoe UI", 16, "bold"), foreground=self.highlight_color).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Facebook Page Id:",).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_username = ttk.Entry(frame, width=30, style="TEntry")
        self.entry_username.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Number of Reels:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_post_count = ttk.Entry(frame, width=30, style="TEntry")
        self.entry_post_count.grid(row=2, column=1, padx=10, pady=10)

        self.btn_download = ttk.Button(frame, text="Download", command=self.start_download, style="TButton.Download.TButton")
        self.btn_download.grid(row=3, column=0, columnspan=2, padx=10, pady=20, sticky=(tk.W, tk.E))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(frame, variable=self.progress_var, maximum=100, style="TProgressbar")
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))

        self.progress_label = ttk.Label(frame, text="0% (0/0)")
        self.progress_label.grid(row=5, column=0, columnspan=2)

        # Text widget to display messages
        self.message_text = tk.Text(frame, height=8, width=40, wrap=tk.WORD)
        self.message_text.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))
        self.message_text.config(bg="#222222", fg='#ffffff')
    def start_download(self):
        userName = self.entry_username.get()
        try:
            howMany = int(self.entry_post_count.get())
        except ValueError:
            self.messagebox.showerror("Error", "Please enter a valid number for the reels count.")
            return

        if not userName:
            self.messagebox.showerror("Error", "Please enter an Facebook Page Id.")
            return

        folder_path = f'Videos/{userName}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self.howMany = howMany
        self.userName = userName
        self.stop_flag = False
        self.setDownloader()
        self.idToShortcode(self.userName)
        self.btn_download.config(text="Stop", style="TButton.Stop.TButton", command=self.stop_download)
        download_thread = Thread(target=self.getReels, args=('',))
        download_thread.start()
        # Display initial message
        self.message_text.config(state=tk.NORMAL)
        self.message_text.delete(1.0, tk.END)  # Clear previous messages
        self.message_text.insert(tk.END, "Downloading...\n")
        self.message_text.see(tk.END)  # Scroll to the end of the text widget
        self.message_text.config(state=tk.DISABLED)
    def stop_download(self):
        self.stop_flag = True
        self.btn_download.config(text="Download", style="TButton.Download.TButton", command=self.start_download)
        # Display stop message
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, "Download stopped.\n")
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.DISABLED)
    def update_progress(self, current, total):
        percent = (current / total) * 100
        self.progress_var.set(percent)
        self.progress_label.config(text=f"{int(percent)}% ({current}/{total})")
        # Append messages to a text widget or label
    def run(self, parent):
        self.color()
        self.window = tk.Toplevel(parent)
        self.window.title("Facebook Reels Downloader")
        # self.window.geometry("400x510")
        self.window.resizable(False, False)
        self.contant()

class TiktokVideosDownloader:
    def setDownloader(self):
        self.req = requests.session()
        self.req.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ar",
            "priority": "u=1, i",
            "referer": "https://tik.storyclone.com/",
            "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
        }
        self.dn = []
        self.stop_flag = False
    def getReels(self, cur):
        needed = self.howMany - len(self.dn)
        if cur != 0:
            url = f'https://tik.storyclone.com/api/fetchVideos?unique_id=%40{self.userName}&count={needed}&cursor={cur}'
        else:
            url = f'https://tik.storyclone.com/api/fetchVideos?unique_id=%40{self.userName}&count={needed}'
        res = self.req.get(url)
        try:
            items = res.json()['data']['videos']
            for item in items:
                if len(self.dn) >= self.howMany:
                    self.message_text.config(state=tk.NORMAL)
                    self.message_text.insert(tk.END, "Done Download All.\n")
                    self.message_text.see(tk.END)
                    self.message_text.config(state=tk.DISABLED)
                    self.stop_flag = True
                    self.btn_download.config(text="Download", style="TButton.Download.TButton", command=self.start_download)
                    break
                if self.stop_flag:
                    return
                try:
                    caption_texts = open(f'Videos/{self.userName}/caption_texts.txt', 'r', encoding='utf-8').read()
                except:
                    caption_texts = ''
                # data.videos[0].video_id
                media_id = item['video_id']
                if media_id not in caption_texts:
                    try:
                        caption_text = item['title'].replace('\n', ' ').replace('\r', ' ').replace(':', '')
                    except:
                        caption_text = ' '
                    open(f'Videos/{self.userName}/caption_texts.txt', 'a', encoding='utf-8').write(f'{media_id}::||{caption_text}\n')
                    # data.videos[0].play
                    url = item['play']
                    self.download(media_id, url)
                    self.dn.append(0)
                    self.update_progress(len(self.dn), self.howMany)
            # data.cursor
            if res.json()['data']['hasMore'] and len(self.dn) != self.howMany:
                next_max_id = res.json()['data']['cursor']
                self.getReels(next_max_id)
            else:
                self.message_text.config(state=tk.NORMAL)
                if len(items) == 0:
                    self.message_text.insert(tk.END, "PLease Make Sure Page Have Reels\n")
                self.message_text.insert(tk.END, "Done Download All.\n")
                self.message_text.see(tk.END)
                self.message_text.config(state=tk.DISABLED)
                self.stop_flag = True
                self.btn_download.config(text="Download", style="TButton.Download.TButton", command=self.start_download)
        except:
            self.message_text.config(state=tk.NORMAL)
            try:
                msg = res.json()['msg']
            except:
                msg = 'No Videos In This User Or You Add Wrong User'
            self.message_text.insert(tk.END, f"Error: {msg}\n")
            self.message_text.see(tk.END)
            self.message_text.config(state=tk.DISABLED)
            self.stop_flag = True
            self.btn_download.config(text="Download", style="TButton.Download.TButton", command=self.start_download)
    def download(self, media_id, url):
        try:
            res = self.req.get(url)
            with open(f'Videos/{self.userName}/{media_id}.mp4', 'wb') as file:
                for chunk in res.iter_content(chunk_size=1024*1024):
                    file.write(chunk)
        except:
            self.message_text.config(state=tk.NORMAL)
            self.message_text.insert(tk.END, f"Can't Download>> {media_id}\n")
            self.message_text.see(tk.END)
            self.message_text.config(state=tk.DISABLED)
            return False
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, f"Done Download: {media_id}\n")
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.DISABLED)
        return True
    def color(self):
        # Dark Mode Colors
        self.background_color = "#262626"
        self.text_color = "#ffffff"
        self.highlight_color = "#0095f6"
        self.button_color = "#248df0"  # Initial color
        self.button_stop_color = "#ff3333"  # Color when stopped
        self.button_hover_color = "#57a7f2"  # Color when hovered
        self.button_hover_color2 = "#f52718"  # Color when hovered
        self.entry_color = "#333333"
        self.border_color = "#4d4d4d"
    def contant(self):
        dark_title_bar(self.window)
        frame = ttk.Frame(self.window, padding="20", style="TFrame")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="TikTok Videos Downloader", font=("Segoe UI", 16, "bold"), foreground=self.highlight_color).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="TikTok Username:",).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_username = ttk.Entry(frame, width=30, style="TEntry")
        self.entry_username.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Number of Videos:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_post_count = ttk.Entry(frame, width=30, style="TEntry")
        self.entry_post_count.grid(row=2, column=1, padx=10, pady=10)

        self.btn_download = ttk.Button(frame, text="Download", command=self.start_download, style="TButton.Download.TButton")
        self.btn_download.grid(row=3, column=0, columnspan=2, padx=10, pady=20, sticky=(tk.W, tk.E))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(frame, variable=self.progress_var, maximum=100, style="TProgressbar")
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))

        self.progress_label = ttk.Label(frame, text="0% (0/0)")
        self.progress_label.grid(row=5, column=0, columnspan=2)

        # Text widget to display messages
        self.message_text = tk.Text(frame, height=8, width=40, wrap=tk.WORD)
        self.message_text.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))
        self.message_text.config(bg="#222222", fg='#ffffff')
    def start_download(self):
        userName = self.entry_username.get()
        try:
            howMany = int(self.entry_post_count.get())
        except ValueError:
            self.messagebox.showerror("Error", "Please enter a valid number for the reels count.")
            return

        if not userName:
            self.messagebox.showerror("Error", "Please enter an Instagram username.")
            return

        folder_path = f'Videos/{userName}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self.howMany = howMany
        self.userName = userName
        self.stop_flag = False
        self.setDownloader()
        self.btn_download.config(text="Stop", style="TButton.Stop.TButton", command=self.stop_download)
        download_thread = Thread(target=self.getReels, args=(0,))
        download_thread.start()
        # Display initial message
        self.message_text.config(state=tk.NORMAL)
        self.message_text.delete(1.0, tk.END)  # Clear previous messages
        self.message_text.insert(tk.END, "Downloading...\n")
        self.message_text.see(tk.END)  # Scroll to the end of the text widget
        self.message_text.config(state=tk.DISABLED)
    def stop_download(self):
        self.stop_flag = True
        self.btn_download.config(text="Download", style="TButton.Download.TButton", command=self.start_download)
        # Display stop message
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, "Download stopped.\n")
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.DISABLED)
    def update_progress(self, current, total):
        percent = (current / total) * 100
        self.progress_var.set(percent)
        self.progress_label.config(text=f"{int(percent)}% ({current}/{total})")
        # Append messages to a text widget or label
    def run(self, parent):
        self.color()
        self.window = tk.Toplevel(parent)
        self.window.title("TikTok Videos Downloader")
        self.window.resizable(False, False)
        self.contant()

class FacePostsUploader:
    def run(self, parent):
        self.times = []
        self.root = tk.Toplevel(parent)
        self.root.title("Facebook Posts Uploader")
        self.root.configure(bg='#222222')
        self.reqs = requests.session()
        self.reqs.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, ',
            'accept-language': 'ar,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
        }
        # Variables with default values
        self.selected_folder = tk.StringVar()
        self.title = tk.StringVar()
        self.num_images = tk.IntVar(value=10)  # Default number of images is 10
        self.delay = tk.DoubleVar(value=60)  # Default delay is 60 seconds
        self.post_type = tk.StringVar(value="Post Now")
        self.cookie = tk.StringVar()
        self.page_id = tk.StringVar()
        self.progress_var = tk.DoubleVar()  # Variable to update the progress bar

        # GUI Elements
        self.create_widgets()
        # Variable to track upload thread
        self.uploading = False
        self.upload_thread = None
    def create_widgets(self):
        dark_title_bar(self.root)
        """Create and place widgets in the GUI."""
        # Account Verification Frame
        verify_frame = ttk.LabelFrame(self.root, text="Step 1: Account Verification ", style="TFrame")
        verify_frame.pack(padx=20, pady=10, fill=tk.BOTH)

        page_id_label = ttk.Label(verify_frame, text="Facebook Page ID:")
        page_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.page_id_entry = ttk.Entry(verify_frame, textvariable=self.page_id, width=50)
        self.page_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        cookies_label = ttk.Label(verify_frame, text="Facebook Cookies:")
        cookies_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.cookies_entry = ttk.Entry(verify_frame, textvariable=self.cookie, width=50)
        self.cookies_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Select Folder Frame
        folder_frame = ttk.LabelFrame(self.root, text="Step 2: Select Folder", style="TFrame")
        folder_frame.pack(padx=20, pady=10, fill=tk.BOTH)

        folder_label = ttk.Label(folder_frame, text="Select Folder:")
        folder_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.selected_folder, width=50, state="readonly")
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        browse_button = tk.Button(folder_frame, text="Browse", bg="#333333", fg='#ffffff', width=20, height=1, command=self.select_folder)
        browse_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        title_label = ttk.Label(folder_frame, text="Posts Title:")
        title_label.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.title_entry = ttk.Entry(folder_frame, textvariable=self.title, width=50)
        self.title_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Display images Frame
        images_frame = ttk.LabelFrame(self.root, text="Step 3: Images in Folder", style="TFrame")
        images_frame.pack(padx=20, pady=10, fill=tk.BOTH)

        self.num_images_label = ttk.Label(images_frame, text="Number of Images: -")
        self.num_images_label.pack(padx=5, pady=5)

        # Input Options Frame
        options_frame = ttk.LabelFrame(self.root, text="Step 4: Input Options", style="TFrame")
        options_frame.pack(padx=20, pady=10, fill=tk.BOTH)

        num_images_label = ttk.Label(options_frame, text="Number of Posts to Upload:")
        num_images_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.num_images_entry = ttk.Entry(options_frame, textvariable=self.num_images, width=10)
        self.num_images_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        delay_label = ttk.Label(options_frame, text="Delay Between Posts (seconds):")
        delay_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.delay_entry = ttk.Entry(options_frame, textvariable=self.delay, width=10)
        self.delay_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        post_type_label = ttk.Label(options_frame, text="Post Type:")
        post_type_label.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.post_type_combobox = ttk.Combobox(options_frame, textvariable=self.post_type, values=["Post Now", "Scheduled"], state='readonly')
        self.post_type_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.post_type_combobox.current(0)

        # Generate Random Times Button
        generate_button = tk.Button(self.root, text="Generate Random Times", command=self.open_random_time_generator, bg='#222222', fg='#ffffff')
        generate_button.pack(padx=5, pady=10)

        # Start/Stop Upload Button
        self.start_button = ttk.Button(self.root, text="Start Upload", command=self.toggle_upload)
        self.start_button.pack(padx=20, pady=10)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100, mode='determinate')
        self.progress_bar.pack(padx=20, pady=10, fill=tk.BOTH)

        # Progress Label
        self.progress_label = ttk.Label(self.root, text="Progress: 0%")
        self.progress_label.pack(padx=20, pady=10)

        # Output Log Frame
        log_frame = ttk.LabelFrame(self.root, text="Output Log")
        log_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=5, bg='#222222', fg='#ffffff')
        self.log_text.pack(fill=tk.BOTH, expand=True)
    def select_folder(self):
        """Prompt the user to select a folder and update image count."""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_folder.set(folder_path)
            self.update_image_count(folder_path)
    def update_image_count(self, folder_path):
        """Update the label with the number of Images files in the selected folder."""
        try:
            # image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(('.jpg'))]
            self.image_files = glob.glob(fr'{folder_path}\*.jpg')
            self.captchas = open(fr'{folder_path}\caption_texts.txt', 'r', encoding='utf-8').read().split('\n')
            num_images = len(self.captchas)-1
            self.num_images_label.config(text=f"Number of Posts: {num_images}, Number Of Images: {len(self.image_files)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to count Images in folder:\n{str(e)}")
    def verify_account(self):
        """Verify the Facebook account using the provided cookies."""
        try:
            cookies = self.cookie.get().strip()
        except:
            cookies = self.cookies
        if cookies:
            if self.check_account(cookies):
                messagebox.showinfo("Account Status", "Account is working.")
            else:
                messagebox.showwarning("Account Status", "Account is not working. Please check your cookies.")
        else:
            messagebox.showwarning("Account Status", "No cookies provided.")
    def check_account(self, cookies):
        url = 'https://www.facebook.com'
        self.reqs.headers['cookie'] = cookies.replace(' ', '')
        self.userId = cookies.split('c_user=')[1].split(';')[0]
        self.addCookie(cookies)
        res = self.reqs.get(url)
        if '["DTSGInitialData",[],{"token":"' in res.text:
            self.token = res.text.split(',["DTSGInitialData",[],{"token":"')[1].split('"')[0]
            self.log('Account Status: Account is working.')
            return True
        else:
            self.log('Account Status: Account is not working. Please check your cookies.')
            return False
    def check_account_old(self, cookies):
        url = 'https://mbasic.facebook.com'
        self.reqs.headers['cookie'] = cookies.replace(' ', '')
        self.userId = cookies.split('c_user=')[1].split(';')[0]
        self.addCookie(cookies)
        res = self.reqs.get(url)
        soup = bs(res.content, 'html.parser')
        token = soup.find('input', attrs={'name': 'fb_dtsg'})
        if token is not None:
            self.token = token.get('value')
            self.log('Account Status: Account is working.')
            return True
        else:
            self.log('Account Status: Account is not working. Please check your cookies.')
            return False
    def addCookie(self, cookies):
        for i in cookies.split(';'):
            try:
                self.reqs.cookies[i.split('=')[0]] = i.split('=')[1]
            except:
                pass
    def open_random_time_generator(self):
        """Open the random time generator window."""
        random_time_generator = RandomTimeGenerator(self.root)
        self.root.wait_window(random_time_generator)
        self.times = times.copy()
        times.clear()
        self.log(f"Random times generated:{self.times}")
    def toggle_upload(self):
        """Toggle between Start Upload and Stop Upload."""
        if self.uploading:
            self.stop_upload()
        else:
            self.start_upload_thread()
    def start_upload_thread(self):
        """Start the upload process in a separate thread."""
        self.uploading = True
        self.start_button.config(text="Stop Upload", command=self.stop_upload)
        self.log_text.delete('1.0', tk.END)  # Clear log text
        threading.Thread(target=self.start_upload).start()
    def stop_upload(self):
        """Stop the upload process."""
        self.uploading = False
        self.start_button.config(text="Start Upload", command=self.toggle_upload)
    def start_upload(self):
        """Upload the selected number of images with the specified delay."""
        folder_path = self.selected_folder.get()
        num_images = self.num_images.get()
        delay = self.delay.get()
        post_type = self.post_type.get()
        self.post_type0 = post_type
        if isinstance(self.cookie, str) == False:
            try:
                self.cookies = self.cookie.get().strip()
                if self.cookies == '':
                    self.log("Input Error: No cookies provided. ")
                    messagebox.showwarning("Input Error", "No cookies provided.")
                    self.uploading = False
                    self.start_button.config(text="Start Upload", command=self.toggle_upload)
                    return
                elif 'c_user' not in self.cookies:
                    self.log("Input Error: Please Enter Valid Cookies.")
                    messagebox.showwarning("Input Error", "Please Enter Valid Cookies.")
                    self.uploading = False
                    self.start_button.config(text="Start Upload", command=self.toggle_upload)
                    return
            except:
                self.log("Input Error: No cookies provided. ")
                messagebox.showwarning("Input Error", "No cookies provided.")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return

        if isinstance(self.page_id, str) == False:
            try:
                self.pageId = self.page_id.get().strip()
                if self.pageId == '':
                    self.log("Input Error: No Page Id provided. ")
                    messagebox.showwarning("Input Error", "No Page Id provided.")
                    self.uploading = False
                    self.start_button.config(text="Start Upload", command=self.toggle_upload)
                    return
            except:
                self.log("Input Error: No Page Id provided. ")
                messagebox.showwarning("Input Error", "No Page Id provided.")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return

        if not os.path.exists('Done'):
            os.makedirs('Done')
        # Check if required fields are filled
        if not folder_path:
            self.log("Input Error: Please select a folder.")
            messagebox.showwarning("Input Error", "Please select a folder.")
            self.uploading = False
            self.start_button.config(text="Start Upload", command=self.toggle_upload)
            return

        if num_images <= 0:
            self.log("Input Error: Number of Posts must be greater than 0.")
            messagebox.showwarning("Input Error", "Number of Posts must be greater than 0.")
            self.uploading = False
            self.start_button.config(text="Start Upload", command=self.toggle_upload)
            return
        if delay < 0:
            self.log("Input Error: Delay must be a non-negative value.")
            messagebox.showwarning("Input Error", "Delay must be a non-negative value.")
            self.uploading = False
            self.start_button.config(text="Start Upload", command=self.toggle_upload)
            return

        try:
            if len(self.image_files) == 0:
                self.log("Input Error: No Images files found in the selected folder.")
                messagebox.showwarning("Input Error", "No Images files found in the selected folder.")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return

            if len(self.image_files) < num_images:
                self.log(f"Input Error: Selected number of images ({num_images}) exceeds available images ({len(self.image_files)}).")
                messagebox.showwarning("Input Error", f"Selected number of images ({num_images}) exceeds available images ({len(self.image_files)}).")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)

                return
            if post_type == 'Scheduled' and len(self.times) == 0:
                self.log("Input Error: Please Generate Random Times First.")
                messagebox.showwarning("Input Error", "Please Generate Random Times First.")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return


            # Update progress bar
            self.progress_var.set(0)
            self.progress_label.config(text="Progress: 0%")
            self.root.update_idletasks()
            if self.check_account(self.cookies) == True and self.getDid() == True:
                self.reqs.headers['cookie'] = f'{self.cookies};i_user={self.pageId}'
                self.reqs.cookies['i_user'] = self.pageId
                counter = 0
                dn = []
                while True:
                    if len(dn) >= num_images:
                        break
                    if not self.uploading:
                        self.log("Upload Stopped by User.")
                        break
                    if post_type == 'Scheduled':
                        timeToPost = get_timestamp(self.times)
                        if timeToPost == False:
                            self.log("No Valid Times, Please Create Valid Times .")
                            self.uploading = False
                            self.start_button.config(text="Start Upload", command=self.toggle_upload)
                            break
                        self.timeToPost = timeToPost
                    self.postId = self.captchas[counter].split('::||')[0]
                    self.captcha = self.captchas[counter].split('::||')[1]
                    counter += 1
                    if self.captcha != '' and self.captcha != ' ':
                        whatPrint = self.captcha
                    else:
                        whatPrint = self.postId
                    try:
                        self.donePost = open(fr'Done\{self.pageId}.txt', 'r', encoding='utf-8').read().split('\n')
                    except:
                        self.donePost = []
                    if self.postId in self.donePost:
                        self.log(f"Done Post {whatPrint} Before .")
                        continue

                    if self.setImages() == True:
                        # Placeholder for actual upload logic
                        if post_type == "Scheduled":
                            scheduled_time = datetime.datetime.fromtimestamp(self.timeToPost)
                            if scheduled_time:
                                self.log(f"Scheduled Post for {whatPrint} at {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
                            else:
                                self.log(f"Failed to schedule Post for {whatPrint}. No valid timestamp available.")
                        else:
                            self.log(f"Posting now: {whatPrint}")
                        dn.append(0)

                        # Simulate delay and update progress bar
                        progress_percentage = ((len(dn)) / num_images) * 100
                        self.progress_var.set(progress_percentage)
                        self.progress_label.config(text=f"Progress: {int(progress_percentage)}%")
                        self.root.update_idletasks()
                        open(fr'Done\{self.pageId}.txt', 'a', encoding='utf-8').write(f'{self.postId}\n')
                        delayTime = random.randint(int(delay//2), int(delay))
                        self.log(f'Sleeping For {delayTime} Seconds .')
                        time.sleep(delayTime)
                    else:
                        self.log(f"Error: Failed to post images:")

                if self.uploading:
                    messagebox.showinfo("Upload Complete", f"Successfully uploaded {num_images} Post.")
                    self.uploading = False
                    self.start_button.config(text="Start Upload", command=self.toggle_upload)
            else:
                messagebox.showinfo("Error", f"Error With Getting Page Id .")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
        except Exception as e:
            self.log(f"Error: Failed to upload Post:\n{str(e)}")
            messagebox.showerror("Error", f"Failed to upload Post:\n{str(e)}")

        # Reset button and progress bar after upload completes or stops
        self.uploading = False
        self.start_button.config(text="Start Upload", command=self.toggle_upload)
    def log(self, message):
        """Log messages to the text widget."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
    def getDid(self):
        url = 'https://www.facebook.com/api/graphql/'
        data = {
            'fb_dtsg': self.token,
            'variables': '{"actionBarRenderLocation":"WWW_COMET_HOVERCARD","context":"DEFAULT","entityID":"THISISUSERID","includeTdaInfo":false,"scale":1}'.replace('THISISUSERID', self.pageId),
            'doc_id': '7343067725813853',
            }
        res = self.reqs.post(url, data=data)
        try:
            try:
                self.delegate_page_id = res.text.split('"profile_delegate_page_id":"')[1].split('"')[0]
            except:
                self.delegate_page_id = res.text.split('"delegate_page_id":"')[1].split('"')[0]
            return True
        except:
            return False
    def uploadImage(self, imagePath):
        url = 'https://upload-business.facebook.com/ajax/react_composer/attachments/photo/upload'
        params = {
            'av': self.delegate_page_id,
            '__a': '1',
            '__req': '20',
            'dpr': '1.5',
            '__comet_req': '15',
            'fb_dtsg': self.token
        }
        data = {
                'source': '8',
                'profile_id': self.userId,
                'waterfallxapp': 'comet',
                'upload_id': '1024',
            }
        files = {'media': open(rf'{imagePath}', 'rb')}
        res = self.reqs.post(url=url,params=params, data=data, files=files)
        imageId = res.text.split('"photoID":"')[1].split('"')[0]
        imageUrl = res.text.split('"thumbSrc":"')[1].split('"')[0]
        decoded_url = unquote(imageUrl)
        out = {"photo":{"photo_link_metadata":{"link":{"external":{"url":decoded_url}}},"id":imageId}}
        self.images.append(out)
    def setImages(self):
        self.images = []
        count = 0
        for path in self.image_files:
            if self.postId in path:
                self.uploadImage(path)
                count += 1
                self.log(f'Done Upload: {count} Image .')
        self.log('Done Upload All, Posting Now .')
        return self.feed()
    def feed(self):
        url = 'https://www.facebook.com/api/graphql/'
        title = self.title.get().strip().replace('\n', '  ')
        if title == '':
            postText = self.captcha
        else:
            postText = title

        if self.post_type0 == 'Scheduled':
            scheduled_time = datetime.datetime.fromtimestamp(self.timeToPost)
            sendTime = scheduled_time.strftime('%Y-%m-%d %H:%M:%S')
            var = '{"input":{"client_mutation_id":"7734434b-bc88-48cf-895b-779121ba8f04","base":{"actor_id":"THISISACTORID","composer_entry_point":"biz_web_home_create_post","message":{"ranges":[],"text":"THISISPOSTTEXT"},"attachments":THISISALLIMAGES,"source":"WWW","unpublished_content_data":{"scheduled_publish_time":THISISTIMESTIMP,"unpublished_content_type":"SCHEDULED"},"explicit_place_id":"","audiences":[{"business_presence":{"business_presence_id":"THISISACTORID"}}],"request_review_data":{"review_request_status":null},"post_collaborators":{"post_collaborators":[]}},"channels":["FACEBOOK_NEWS_FEED"],"FACEBOOK_NEWS_FEED":{"unpublished_content_data":{"scheduled_publish_time":THISISTIMESTIMP,"unpublished_content_type":"SCHEDULED"},"attachments":THISISALLIMAGES},"FACEBOOK_GROUP":null,"INSTAGRAM_POST":{"unpublished_content_data":null},"identities":["THISISACTORID"],"ad_campaign_group":null,"raw_boosted_component_spec":"null","logging":{"composer_session_id":"7734434b-bc88-48cf-895b-779121ba8f04"}},"checkPhotosToReelsUpsellEligibility":true}'.replace('THISISPOSTTEXT', postText).replace('THISISTIMESTIMP', f'{self.timeToPost}').replace('THISISACTORID', self.delegate_page_id).replace('THISISALLIMAGES', f'{self.images}')
        else:
            var = '{"input":{"client_mutation_id":"7734434b-bc88-48cf-895b-779121ba8f04","base":{"actor_id":"THISISACTORID","composer_entry_point":"biz_web_home_create_post","message":{"ranges":[],"text":"THISISPOSTTEXT"},"attachments":THISISALLIMAGES,"source":"WWW","unpublished_content_data":null,"explicit_place_id":"","audiences":[{"business_presence":{"business_presence_id":"THISISACTORID"}}],"is_autosave_draft":false,"request_review_data":{"review_request_status":null},"post_collaborators":{"post_collaborators":[]}},"channels":["FACEBOOK_NEWS_FEED"],"FACEBOOK_NEWS_FEED":{"message":{"ranges":[],"text":"THISISPOSTTEXT"},"attachments":THISISALLIMAGES},"FACEBOOK_GROUP":null,"INSTAGRAM_POST":null,"identities":["THISISACTORID"],"ad_campaign_group":null,"raw_boosted_component_spec":"null","logging":{"composer_session_id":"7734434b-bc88-48cf-895b-779121ba8f04"}},"checkPhotosToReelsUpsellEligibility":true}'.replace('THISISPOSTTEXT', postText).replace('THISISACTORID', self.delegate_page_id).replace('THISISALLIMAGES', f'{self.images}')
            scheduled_time = datetime.datetime.fromtimestamp(time.time())
            sendTime = scheduled_time.strftime('%Y-%m-%d %H:%M:%S')
        data = {
            'fb_dtsg': self.token,
            'variables': var,
            'doc_id': '7824581757552022',
        }
        res = self.reqs.post(url, data=data)
        self.images = []
        if 'creation_time' in res.text or 'pending_publish_content_id' in res.text:
            try:
                try:
                    postId = res.json()['data']['xfamily_content_create']['items'][0]['story']['post_id']
                except:
                    postId = res.json()['data']['xfamily_content_create']['items'][0]['pending_publish_content_id']
            except:
                postId = self.pageId
            savePost(postId, postText, sendTime)
            return True
        else:
            return False

class FaceReelsUploader:
    def run(self, parent):
        self.times = []
        self.root = tk.Toplevel(parent)
        self.root.title("Facebook Reels Uploader")
        self.root.configure(bg='#222222')
        self.reqs = requests.session()
        self.reqs.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, ',
            'accept-language': 'ar,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
        }
        # Variables with default values
        self.selected_folder = tk.StringVar()
        self.title = tk.StringVar()
        self.num_videos = tk.IntVar(value=10)  # Default number of images is 10
        self.delay = tk.DoubleVar(value=60)  # Default delay is 60 seconds
        self.post_type = tk.StringVar(value="Post Now")
        self.cookie = tk.StringVar()
        self.page_id = tk.StringVar()
        self.progress_var = tk.DoubleVar()  # Variable to update the progress bar

        # GUI Elements
        self.create_widgets()

        # Variable to track upload thread
        self.uploading = False
        self.upload_thread = None
    def create_widgets(self):
        dark_title_bar(self.root)

        """Create and place widgets in the GUI."""
        # Account Verification Frame
        verify_frame = ttk.LabelFrame(self.root, text="Step 1: Account Verification ", style="TFrame")
        verify_frame.pack(padx=20, pady=10, fill=tk.BOTH)

        page_id_label = ttk.Label(verify_frame, text="Facebook Page ID:")
        page_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.page_id_entry = ttk.Entry(verify_frame, textvariable=self.page_id, width=50)
        self.page_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        cookies_label = ttk.Label(verify_frame, text="Facebook Cookies:")
        cookies_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.cookies_entry = ttk.Entry(verify_frame, textvariable=self.cookie, width=50)
        self.cookies_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Select Folder Frame
        folder_frame = ttk.LabelFrame(self.root, text="Step 2: Select Folder", style="TFrame")
        folder_frame.pack(padx=20, pady=10, fill=tk.BOTH)

        folder_label = ttk.Label(folder_frame, text="Select Reels Folder:")
        folder_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.selected_folder, width=50, state="readonly")
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        browse_button = tk.Button(folder_frame, text="Browse", bg="#333333", fg='#ffffff', width=20, height=1, command=self.select_folder)
        browse_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        title_label = ttk.Label(folder_frame, text="Reels Title:")
        title_label.grid(row=3, column=0, padx=5, pady=5, sticky="ew")


        self.title_entry = ttk.Entry(folder_frame, textvariable=self.title, width=50)
        self.title_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Display Videos Frame
        videos_frame = ttk.LabelFrame(self.root, text="Step 3: Reels in Folder", style="TFrame")
        videos_frame.pack(padx=20, pady=10, fill=tk.BOTH)

        self.num_videos_label = ttk.Label(videos_frame, text="Number of Reels: -")
        self.num_videos_label.pack(padx=5, pady=5)

        # Input Options Frame
        options_frame = ttk.LabelFrame(self.root, text="Step 4: Input Options", style="TFrame")
        options_frame.pack(padx=20, pady=10, fill=tk.BOTH)

        num_videos_label = ttk.Label(options_frame, text="Number of Reels to Upload:")
        num_videos_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.num_videos_entry = ttk.Entry(options_frame, textvariable=self.num_videos, width=10)
        self.num_videos_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        delay_label = ttk.Label(options_frame, text="Delay Between Reels (seconds):")
        delay_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.delay_entry = ttk.Entry(options_frame, textvariable=self.delay, width=10)
        self.delay_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        post_type_label = ttk.Label(options_frame, text="Post Type:")
        post_type_label.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.post_type_combobox = ttk.Combobox(options_frame, textvariable=self.post_type, values=["Post Now", "Scheduled"], state='readonly')
        self.post_type_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.post_type_combobox.current(0)

        # Generate Random Times Button
        generate_button = tk.Button(self.root, text="Generate Random Times", command=self.open_random_time_generator, bg='#222222', fg='#ffffff')
        generate_button.pack(padx=5, pady=10)

        # Start/Stop Upload Button
        self.start_button = ttk.Button(self.root, text="Start Upload", command=self.toggle_upload)
        self.start_button.pack(padx=20, pady=10)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100, mode='determinate')
        self.progress_bar.pack(padx=20, pady=10, fill=tk.BOTH)

        # Progress Label
        self.progress_label = ttk.Label(self.root, text="Progress: 0%")
        self.progress_label.pack(padx=20, pady=10)

        # Output Log Frame
        log_frame = ttk.LabelFrame(self.root, text="Output Log")
        log_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=5, bg='#222222', fg='#ffffff')
        self.log_text.pack(fill=tk.BOTH, expand=True)
    def select_folder(self):
        """Prompt the user to select a folder and update video count."""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_folder.set(folder_path)
            self.update_video_count(folder_path)
    def update_video_count(self, folder_path):
        """Update the label with the number of Images files in the selected folder."""
        try:
            # image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(('.jpg'))]
            self.video_files = glob.glob(fr'{folder_path}\*.mp4')
            self.captchas = open(fr'{folder_path}\caption_texts.txt', 'r', encoding='utf-8').read().split('\n')
            num_videos = len(self.video_files)
            self.num_videos_label.config(text=f"Number of Posts: {len(self.captchas)}, Number Of Videos: {num_videos}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to count Images in folder:\n{str(e)}")
    def verify_account(self):
        """Verify the Facebook account using the provided cookies."""
        try:
            cookies = self.cookie.get().strip()
        except:
            cookies = self.cookies
        if cookies:
            if self.check_account(cookies):
                messagebox.showinfo("Account Status", "Account is working.")
            else:
                messagebox.showwarning("Account Status", "Account is not working. Please check your cookies.")
        else:
            messagebox.showwarning("Account Status", "No cookies provided.")
    def check_account(self, cookies):
        url = 'https://www.facebook.com'
        self.reqs.headers['cookie'] = cookies.replace(' ', '')
        self.userId = cookies.split('c_user=')[1].split(';')[0]
        self.addCookie(cookies)
        res = self.reqs.get(url)
        if '["DTSGInitialData",[],{"token":"' in res.text:
            self.token = res.text.split(',["DTSGInitialData",[],{"token":"')[1].split('"')[0]
            self.log('Account Status: Account is working.')
            return True
        else:
            self.log('Account Status: Account is not working. Please check your cookies.')
            return False
    def check_account_old(self, cookies):
        url = 'https://mbasic.facebook.com'
        self.reqs.headers['cookie'] = cookies.replace(' ', '')
        self.userId = cookies.split('c_user=')[1].split(';')[0]
        self.addCookie(cookies)
        res = self.reqs.get(url)
        soup = bs(res.content, 'html.parser')
        token = soup.find('input', attrs={'name': 'fb_dtsg'})
        if token is not None:
            self.token = token.get('value')
            self.log('Account Status: Account is working.')
            return True
        else:
            self.log('Account Status: Account is not working. Please check your cookies.')
            return False
    def addCookie(self, cookies):
        for i in cookies.split(';'):
            try:
                self.reqs.cookies[i.split('=')[0]] = i.split('=')[1]
            except:
                pass
    def open_random_time_generator(self):
        """Open the random time generator window."""
        random_time_generator = RandomTimeGenerator(self.root)
        self.root.wait_window(random_time_generator)
        self.times = times.copy()
        times.clear()
        self.log(f"Random times generated:{self.times}")
    def toggle_upload(self):
        """Toggle between Start Upload and Stop Upload."""
        if self.uploading:
            self.stop_upload()
        else:
            self.start_upload_thread()
    def start_upload_thread(self):
        """Start the upload process in a separate thread."""
        self.uploading = True
        self.start_button.config(text="Stop Upload", command=self.stop_upload)
        self.log_text.delete('1.0', tk.END)  # Clear log text
        threading.Thread(target=self.start_upload).start()
    def stop_upload(self):
        """Stop the upload process."""
        self.uploading = False
        self.start_button.config(text="Start Upload", command=self.toggle_upload)
    def log(self, message):
        """Log messages to the text widget."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
    def start_upload(self):
        """Upload the selected number of videos with the specified delay."""
        folder_path = self.selected_folder.get()
        num_videos = self.num_videos.get()
        delay = self.delay.get()
        post_type = self.post_type.get()
        self.post_type0 = post_type
        if isinstance(self.cookie, str) == False:
            try:
                self.cookies = self.cookie.get().strip()
                if self.cookies == '':
                    self.log("Input Error: No cookies provided. ")
                    messagebox.showwarning("Input Error", "No cookies provided.")
                    self.uploading = False
                    self.start_button.config(text="Start Upload", command=self.toggle_upload)
                    return
                elif 'c_user' not in self.cookies:
                    self.log("Input Error: Please Enter Valid Cookies.")
                    messagebox.showwarning("Input Error", "Please Enter Valid Cookies.")
                    self.uploading = False
                    self.start_button.config(text="Start Upload", command=self.toggle_upload)
                    return
            except:
                self.log("Input Error: No cookies provided. ")
                messagebox.showwarning("Input Error", "No cookies provided.")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return

        if isinstance(self.page_id, str) == False:
            try:
                self.pageId = self.page_id.get().strip()
                if self.pageId == '':
                    self.log("Input Error: No Page Id provided. ")
                    messagebox.showwarning("Input Error", "No Page Id provided.")
                    self.uploading = False
                    self.start_button.config(text="Start Upload", command=self.toggle_upload)
                    return
            except:
                self.log("Input Error: No Page Id provided. ")
                messagebox.showwarning("Input Error", "No Page Id provided.")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return

        if not os.path.exists('Done'):
            os.makedirs('Done')
        # Check if required fields are filled
        if not folder_path:
            self.log("Input Error: Please select a folder.")
            messagebox.showwarning("Input Error", "Please select a folder.")
            self.uploading = False
            self.start_button.config(text="Start Upload", command=self.toggle_upload)
            return

        if num_videos <= 0:
            self.log("Input Error: Number of Posts must be greater than 0.")
            messagebox.showwarning("Input Error", "Number of Posts must be greater than 0.")
            self.uploading = False
            self.start_button.config(text="Start Upload", command=self.toggle_upload)
            return
        if delay < 0:
            self.log("Input Error: Delay must be a non-negative value.")
            messagebox.showwarning("Input Error", "Delay must be a non-negative value.")
            self.uploading = False
            self.start_button.config(text="Start Upload", command=self.toggle_upload)
            return

        try:
            if len(self.video_files) == 0:
                self.log("Input Error: No Videos files found in the selected folder.")
                messagebox.showwarning("Input Error", "No Videos files found in the selected folder.")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return

            if len(self.video_files) < num_videos:
                self.log(f"Input Error: Selected number of videos ({num_videos}) exceeds available videos ({len(self.video_files)}).")
                messagebox.showwarning("Input Error", f"Selected number of video ({num_videos}) exceeds available video ({len(self.video_files)}).")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return
            if post_type == 'Scheduled' and len(self.times) == 0:
                self.log("Input Error: Please Generate Random Times First.")
                messagebox.showwarning("Input Error", "Please Generate Random Times First.")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return

            # Update progress bar
            self.progress_var.set(0)
            self.progress_label.config(text="Progress: 0%")
            self.root.update_idletasks()
            if self.check_account(self.cookies) == True:
                self.reqs.headers['cookie'] = f'{self.cookies};i_user={self.pageId}'
                self.reqs.cookies['i_user'] = self.pageId
                counter = 0
                dn = []
                while True:
                    if len(dn) >= num_videos:
                        break
                    if not self.uploading:
                        self.log("Upload Stopped by User.")
                        break
                    if post_type == 'Scheduled':
                        timeToPost = get_timestamp(self.times)
                        if timeToPost == False:
                            self.log("No Valid Times, Please Create Valid Times .")
                            self.uploading = False
                            self.start_button.config(text="Start Upload", command=self.toggle_upload)
                            break
                        self.timeToPost = timeToPost
                    self.postId = self.captchas[counter].split('::||')[0]
                    self.captcha = self.captchas[counter].split('::||')[1]
                    counter += 1
                    if self.captcha != '' and self.captcha != ' ':
                        whatPrint = self.captcha
                    else:
                        whatPrint = self.postId
                    try:
                        self.donePost = open(fr'Done\{self.pageId}.txt', 'r', encoding='utf-8').read().split('\n')
                    except:
                        self.donePost = []
                    if self.postId in self.donePost:
                        self.log(f"Done Post {whatPrint} Before .")
                        continue

                    if self.upload_video() == True:
                        # Placeholder for actual upload logic
                        if post_type == "Scheduled":
                            scheduled_time = datetime.datetime.fromtimestamp(self.timeToPost)
                            if scheduled_time:
                                self.log(f"Scheduled Post for {whatPrint} at {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
                            else:
                                self.log(f"Failed to schedule Post for {whatPrint}. No valid timestamp available.")
                        else:
                            self.log(f"Posting now: {whatPrint}")
                        dn.append(0)

                        # Simulate delay and update progress bar
                        progress_percentage = ((len(dn)) / num_videos) * 100
                        self.progress_var.set(progress_percentage)
                        self.progress_label.config(text=f"Progress: {int(progress_percentage)}%")
                        self.root.update_idletasks()
                        open(fr'Done\{self.pageId}.txt', 'a', encoding='utf-8').write(f'{self.postId}\n')
                        delayTime = random.randint(int(delay//2), int(delay))
                        self.log(f'Sleeping For {delayTime} Seconds .')
                        time.sleep(delayTime)
                    else:
                        self.log(f"Error: Failed to post Video:")

                if self.uploading:
                    messagebox.showinfo("Upload Complete", f"Successfully uploaded {num_videos} Post.")
                    self.uploading = False
                    self.start_button.config(text="Start Upload", command=self.toggle_upload)

        except Exception as e:
            self.log(f"Error: Failed to upload Post:\n{str(e)}")
            messagebox.showerror("Error", f"Failed to upload Post:\n{str(e)}")

        # Reset button and progress bar after upload completes or stops
        self.uploading = False
        self.start_button.config(text="Start Upload", command=self.toggle_upload)
    def upload_video(self):
        for path in self.video_files:
            if self.postId in path:
                self.video_path = path
                return self.redyToUpload()
        return False
    def redyToUpload(self):
            self.reqs.headers['cookie'] = f'{self.cookies};i_user={self.pageId}'
            url = f'https://vupload-edge.facebook.com/ajax/video/upload/requests/start/?av={self.pageId}&__a=1'
            self.targetFile = open(self.video_path, 'rb')
            self.fileData = self.targetFile.seek(0, os.SEEK_END)
            data = {'file_size': self.fileData, 'file_extension': 'mp4', 'target_id': self.pageId, 'source': 'reel_composer', 'composer_dialog_version': '', 'waterfall_id': '205fbd46-2369-4bb6-973d-5ad6198cd3b4', 'composer_session_id': '205fbd46-2369-4bb6-973d-5ad6198cd3b4', 'composer_entry_point_ref': 'comet_pages_reel_composer_timeline_sprout', 'composer_work_shared_draft_mode': '', 'has_file_been_replaced': 'false', 'supports_chunking': 'true', 'supports_file_api': 'true', 'partition_start_offset': '0', 'partition_end_offset': self.fileData, 'creator_product': '2', 'spherical': 'false', 'video_publisher_action_source': '', '__user': self.pageId, '__a': '1', '__req': 'b3', '__comet_req': '15', 'jazoest': '25337', 'lsd': 'DvoJ3cocIbL4EzU7f3jLku', '__spin_r': '1007731907', '__spin_b': 'trunk', '__spin_t': '1687491086', 'qpl_active_flow_ids': '884152905', 'fb_dtsg': self.token}
            res = self.reqs.post(url, data=data)
            if '"video_id":"' in res.text:
                video_id = res.text.split('"video_id":"')[1].split('"')[0]
                return self.upload(video_id)
            else:
                return False
    def upload(self, video_id):
        url = 'https://vupload-edge.facebook.com/ajax/video/upload/requests/receive/'
        data = {'av': self.pageId, 'composer_session_id': '205fbd46-2369-4bb6-973d-5ad6198cd3b4', 'video_id': video_id, 'start_offset': '0', 'end_offset': '1048576', 'source': 'reel_composer', 'target_id': self.pageId, 'waterfall_id': '205fbd46-2369-4bb6-973d-5ad6198cd3b4', 'composer_entry_point_ref': 'comet_pages_reel_composer_timeline_sprout', 'composer_work_shared_draft_mode': '', 'composer_dialog_version': '', 'has_file_been_replaced': 'false', 'supports_chunking': 'true', 'upload_speed': '', 'partition_start_offset': '0', 'partition_end_offset': self.fileData, '__user': self.pageId, '__a': '1', '__req': 'b4', '__comet_req': '15', 'fb_dtsg': self.token, 'jazoest': '25337', '__spin_r': '1007731907', '__spin_b': 'trunk', '__spin_t': '1687491086', 'qpl_active_flow_ids': '884152905'}
        file = {'video_file_chunk': open(self.video_path, 'rb')}
        self.reqs.post(url, params=data, files=file)
        self.log(f'Done Upload Video: {video_id}')
        return self.addVideo(video_id)
    def addVideo(self, video_id):
        url = 'https://www.facebook.com/api/graphql/'
        title = self.title.get().strip().replace('\n', '  ')
        if title == '':
            postText = self.captcha
        else:
            postText = title
        if self.post_type0 == 'Scheduled':
            scheduled_time = datetime.datetime.fromtimestamp(self.timeToPost)
            sendTime = scheduled_time.strftime('%Y-%m-%d %H:%M:%S')
            var = '{"input":{"composer_entry_point":"comet_ap_plus_reel_composer_feed_sprout","composer_source_surface":"short_form_video","source":"WWW","attachments":[{"video":{"id":"THISISVIDEOID","notify_when_processed":true,"story_media_audio_data":{"raw_media_type":"VIDEO"},"video_media_metadata":{"audio":{"audio_type":"original_audio","start_time_s":0,"volume_level":1},"is_audio_muted":false,"length_in_sec":11.84}}}],"unpublished_content_data":{"scheduled_publish_time":THISISTIMETOPOST,"unpublished_content_type":"SCHEDULED"},"fb_shorts":{"is_fb_short":true,"remix_status":"ENABLED","enable_one_by_one":true},"message":{"ranges":[],"text":"THISISTHETITLE"},"unpublished_content_data":{"scheduled_publish_time":THISISTIMETOPOST,"unpublished_content_type":"SCHEDULED"},"audience":{"privacy":{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}},"stars_receivable":{"is_receiving_stars_disabled":true},"logging":{"composer_session_id":"3cb58dcd-65b2-4540-9f9d-b58eba048362"},"navigation_data":{"attribution_id_v2":"ReelsCreationRoot.react,comet.reels.create,unexpected,1694232946487,343168,,;ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1694232935155,782625,190055527696468,"},"tracking":[null],"event_share_metadata":{"surface":"newsfeed"},"actor_id":"THISISPAGEID","client_mutation_id":"1"},"displayCommentsFeedbackContext":null,"displayCommentsContextEnableComment":null,"displayCommentsContextIsAdPreview":null,"displayCommentsContextIsAggregatedShare":null,"displayCommentsContextIsStorySet":null,"feedLocation":"NEWSFEED","feedbackSource":1,"focusCommentID":null,"gridMediaWidth":null,"groupID":null,"scale":1.5,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"homepage_stream","useDefaultActor":false,"inviteShortLinkKey":null,"isFeed":false,"isFundraiser":false,"isFunFactPost":false,"isGroup":false,"isEvent":false,"isTimeline":false,"isSocialLearning":false,"isPageNewsFeed":false,"isProfileReviews":false,"isWorkSharedDraft":true,"UFI2CommentsProvider_commentsKey":"CometModernHomeFeedQuery","hashtag":null,"canUserManageOffers":false,"__relay_internal__pv__CometUFIIsRTAEnabledrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":false,"__relay_internal__pv__StoriesRingrelayprovider":false}'.replace('THISISPAGEID', self.pageId).replace('THISISVIDEOID', video_id).replace('THISISTHETITLE', postText).replace('THISISTIMETOPOST', f'{self.timeToPost}'),
        else:
            var = '{"input":{"composer_entry_point":"comet_ap_plus_reel_composer_feed_sprout","composer_source_surface":"short_form_video","source":"WWW","attachments":[{"video":{"id":"THISISVIDEOID","notify_when_processed":true,"story_media_audio_data":{"raw_media_type":"VIDEO"},"video_media_metadata":{"audio":{"audio_type":"original_audio","start_time_s":0,"volume_level":1},"is_audio_muted":false,"length_in_sec":11.84}}}],"fb_shorts":{"is_fb_short":true,"remix_status":"ENABLED","enable_one_by_one":true},"message":{"ranges":[],"text":"THISISTHETITLE"},"audience":{"privacy":{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}},"stars_receivable":{"is_receiving_stars_disabled":true},"logging":{"composer_session_id":"3cb58dcd-65b2-4540-9f9d-b58eba048362"},"navigation_data":{"attribution_id_v2":"ReelsCreationRoot.react,comet.reels.create,unexpected,1694232946487,343168,,;ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1694232935155,782625,190055527696468,"},"tracking":[null],"event_share_metadata":{"surface":"newsfeed"},"actor_id":"THISISPAGEID","client_mutation_id":"1"},"displayCommentsFeedbackContext":null,"displayCommentsContextEnableComment":null,"displayCommentsContextIsAdPreview":null,"displayCommentsContextIsAggregatedShare":null,"displayCommentsContextIsStorySet":null,"feedLocation":"NEWSFEED","feedbackSource":1,"focusCommentID":null,"gridMediaWidth":null,"groupID":null,"scale":1.5,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"homepage_stream","useDefaultActor":false,"inviteShortLinkKey":null,"isFeed":false,"isFundraiser":false,"isFunFactPost":false,"isGroup":false,"isEvent":false,"isTimeline":false,"isSocialLearning":false,"isPageNewsFeed":false,"isProfileReviews":false,"isWorkSharedDraft":true,"UFI2CommentsProvider_commentsKey":"CometModernHomeFeedQuery","hashtag":null,"canUserManageOffers":false,"__relay_internal__pv__CometUFIIsRTAEnabledrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":false,"__relay_internal__pv__StoriesRingrelayprovider":false}'.replace('THISISPAGEID', self.pageId).replace('THISISVIDEOID', video_id).replace('THISISTHETITLE', postText),
            scheduled_time = datetime.datetime.fromtimestamp(time.time())
            sendTime = scheduled_time.strftime('%Y-%m-%d %H:%M:%S')
        data = {
            'fb_dtsg': self.token,
            'variables': var,
            'doc_id': '6505900592778979',
        }
        res = self.reqs.post(url, data=data)
        try:
            post_id = res.json()['data']['story_create']['post_id']
            savePost(post_id, postText, sendTime)
            return True
        except:
            return False

class FaceVideosUploader:
    def run(self, parent):
        self.times = []
        self.root = tk.Toplevel(parent)
        self.root.title("Facebook Videos Uploader")
        self.root.configure(bg='#222222')
        self.reqs = requests.session()
        self.reqs.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, ',
            'accept-language': 'ar,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
        }
        # Variables with default values
        self.selected_folder = tk.StringVar()
        self.title = tk.StringVar()
        self.num_videos = tk.IntVar(value=10)  # Default number of images is 10
        self.delay = tk.DoubleVar(value=60)  # Default delay is 60 seconds
        self.post_type = tk.StringVar(value="Post Now")
        self.cookie = tk.StringVar()
        self.page_id = tk.StringVar()
        self.progress_var = tk.DoubleVar()  # Variable to update the progress bar

        # GUI Elements
        self.create_widgets()

        # Variable to track upload thread
        self.uploading = False
        self.upload_thread = None
    def create_widgets(self):
        dark_title_bar(self.root)
        """Create and place widgets in the GUI."""
        # Account Verification Frame
        verify_frame = ttk.LabelFrame(self.root, text="Step 1: Account Verification ", style="TFrame")
        verify_frame.pack(padx=20, pady=10, fill=tk.BOTH)

        page_id_label = ttk.Label(verify_frame, text="Facebook Page ID:")
        page_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.page_id_entry = ttk.Entry(verify_frame, textvariable=self.page_id, width=50)
        self.page_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        cookies_label = ttk.Label(verify_frame, text="Facebook Cookies:")
        cookies_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.cookies_entry = ttk.Entry(verify_frame, textvariable=self.cookie, width=50)
        self.cookies_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Select Folder Frame
        folder_frame = ttk.LabelFrame(self.root, text="Step 2: Select Folder", style="TFrame")
        folder_frame.pack(padx=20, pady=10, fill=tk.BOTH)

        folder_label = ttk.Label(folder_frame, text="Select Folder:")
        folder_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.selected_folder, width=50, state="readonly")
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        browse_button = tk.Button(folder_frame, text="Browse", bg="#333333", fg='#ffffff', width=20, height=1, command=self.select_folder)
        browse_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        title_label = ttk.Label(folder_frame, text="Video Title:")
        title_label.grid(row=3, column=0, padx=5, pady=5, sticky="ew")


        self.title_entry = ttk.Entry(folder_frame, textvariable=self.title, width=50)
        self.title_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Display Videos Frame
        videos_frame = ttk.LabelFrame(self.root, text="Step 3: Videos in Folder", style="TFrame")
        videos_frame.pack(padx=20, pady=10, fill=tk.BOTH)

        self.num_videos_label = ttk.Label(videos_frame, text="Number of Videos: -")
        self.num_videos_label.pack(padx=5, pady=5)

        # Input Options Frame
        options_frame = ttk.LabelFrame(self.root, text="Step 4: Input Options", style="TFrame")
        options_frame.pack(padx=20, pady=10, fill=tk.BOTH)

        num_videos_label = ttk.Label(options_frame, text="Number of Videos to Upload:")
        num_videos_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.num_videos_entry = ttk.Entry(options_frame, textvariable=self.num_videos, width=10)
        self.num_videos_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        delay_label = ttk.Label(options_frame, text="Delay Between Video (seconds):")
        delay_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.delay_entry = ttk.Entry(options_frame, textvariable=self.delay, width=10)
        self.delay_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        post_type_label = ttk.Label(options_frame, text="Post Type:")
        post_type_label.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.post_type_combobox = ttk.Combobox(options_frame, textvariable=self.post_type, values=["Post Now", "Scheduled"], state='readonly')
        self.post_type_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.post_type_combobox.current(0)

        # Generate Random Times Button
        generate_button = tk.Button(self.root, text="Generate Random Times", command=self.open_random_time_generator, bg='#222222', fg='#ffffff')
        generate_button.pack(padx=5, pady=10)

        # Start/Stop Upload Button
        self.start_button = ttk.Button(self.root, text="Start Upload", command=self.toggle_upload)
        self.start_button.pack(padx=20, pady=10)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100, mode='determinate')
        self.progress_bar.pack(padx=20, pady=10, fill=tk.BOTH)

        # Progress Label
        self.progress_label = ttk.Label(self.root, text="Progress: 0%")
        self.progress_label.pack(padx=20, pady=10)

        # Output Log Frame
        log_frame = ttk.LabelFrame(self.root, text="Output Log")
        log_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=5, bg='#222222', fg='#ffffff')
        self.log_text.pack(fill=tk.BOTH, expand=True)
    def select_folder(self):
        """Prompt the user to select a folder and update video count."""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_folder.set(folder_path)
            self.update_video_count(folder_path)
    def update_video_count(self, folder_path):
        """Update the label with the number of Images files in the selected folder."""
        try:
            # image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(('.jpg'))]
            self.video_files = glob.glob(fr'{folder_path}\*.mp4')
            self.captchas = open(fr'{folder_path}\caption_texts.txt', 'r', encoding='utf-8').read().split('\n')
            num_videos = len(self.video_files)
            self.num_videos_label.config(text=f"Number of Posts: {len(self.captchas)}, Number Of Videos: {num_videos}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to count Images in folder:\n{str(e)}")
    def verify_account(self):
        """Verify the Facebook account using the provided cookies."""
        try:
            cookies = self.cookie.get().strip()
        except:
            cookies = self.cookies
        if cookies:
            if self.check_account(cookies):
                messagebox.showinfo("Account Status", "Account is working.")
            else:
                messagebox.showwarning("Account Status", "Account is not working. Please check your cookies.")
        else:
            messagebox.showwarning("Account Status", "No cookies provided.")
    def check_account(self, cookies):
        url = 'https://www.facebook.com'
        self.reqs.headers['cookie'] = cookies.replace(' ', '')
        self.userId = cookies.split('c_user=')[1].split(';')[0]
        self.addCookie(cookies)
        res = self.reqs.get(url)
        if '["DTSGInitialData",[],{"token":"' in res.text:
            self.token = res.text.split(',["DTSGInitialData",[],{"token":"')[1].split('"')[0]
            self.log('Account Status: Account is working.')
            return True
        else:
            self.log('Account Status: Account is not working. Please check your cookies.')
            return False
    def check_account_old(self, cookies):
        url = 'https://mbasic.facebook.com'
        self.reqs.headers['cookie'] = cookies.replace(' ', '')
        self.userId = cookies.split('c_user=')[1].split(';')[0]
        self.addCookie(cookies)
        res = self.reqs.get(url)
        soup = bs(res.content, 'html.parser')
        token = soup.find('input', attrs={'name': 'fb_dtsg'})
        if token is not None:
            self.token = token.get('value')
            self.log('Account Status: Account is working.')
            return True
        else:
            self.log('Account Status: Account is not working. Please check your cookies.')
            return False
    def addCookie(self, cookies):
        for i in cookies.split(';'):
            try:
                self.reqs.cookies[i.split('=')[0]] = i.split('=')[1]
            except:
                pass
    def open_random_time_generator(self):
        """Open the random time generator window."""
        random_time_generator = RandomTimeGenerator(self.root)
        self.root.wait_window(random_time_generator)
        self.times = times.copy()
        times.clear()
        self.log(f"Random times generated:{self.times}")
    def toggle_upload(self):
        """Toggle between Start Upload and Stop Upload."""
        if self.uploading:
            self.stop_upload()
        else:
            self.start_upload_thread()
    def start_upload_thread(self):
        """Start the upload process in a separate thread."""
        self.uploading = True
        self.start_button.config(text="Stop Upload", command=self.stop_upload)
        self.log_text.delete('1.0', tk.END)  # Clear log text
        threading.Thread(target=self.start_upload).start()
    def stop_upload(self):
        """Stop the upload process."""
        self.uploading = False
        self.start_button.config(text="Start Upload", command=self.toggle_upload)
    def log(self, message):
        """Log messages to the text widget."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
    def start_upload(self):
        """Upload the selected number of videos with the specified delay."""
        folder_path = self.selected_folder.get()
        num_videos = self.num_videos.get()
        delay = self.delay.get()
        post_type = self.post_type.get()
        self.post_type0 = post_type
        if isinstance(self.cookie, str) == False:
            try:
                self.cookies = self.cookie.get().strip()
                if self.cookies == '':
                    self.log("Input Error: No cookies provided. ")
                    messagebox.showwarning("Input Error", "No cookies provided.")
                    self.uploading = False
                    self.start_button.config(text="Start Upload", command=self.toggle_upload)
                    return
                elif 'c_user' not in self.cookies:
                    self.log("Input Error: Please Enter Valid Cookies.")
                    messagebox.showwarning("Input Error", "Please Enter Valid Cookies.")
                    self.uploading = False
                    self.start_button.config(text="Start Upload", command=self.toggle_upload)
                    return
            except:
                self.log("Input Error: No cookies provided. ")
                messagebox.showwarning("Input Error", "No cookies provided.")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return

        if isinstance(self.page_id, str) == False:
            try:
                self.pageId = self.page_id.get().strip()
                if self.pageId == '':
                    self.log("Input Error: No Page Id provided. ")
                    messagebox.showwarning("Input Error", "No Page Id provided.")
                    self.uploading = False
                    self.start_button.config(text="Start Upload", command=self.toggle_upload)
                    return
            except:
                self.log("Input Error: No Page Id provided. ")
                messagebox.showwarning("Input Error", "No Page Id provided.")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return

        if not os.path.exists('Done'):
            os.makedirs('Done')
        # Check if required fields are filled
        if not folder_path:
            self.log("Input Error: Please select a folder.")
            messagebox.showwarning("Input Error", "Please select a folder.")
            self.uploading = False
            self.start_button.config(text="Start Upload", command=self.toggle_upload)
            return

        if num_videos <= 0:
            self.log("Input Error: Number of Posts must be greater than 0.")
            messagebox.showwarning("Input Error", "Number of Posts must be greater than 0.")
            self.uploading = False
            self.start_button.config(text="Start Upload", command=self.toggle_upload)
            return
        if delay < 0:
            self.log("Input Error: Delay must be a non-negative value.")
            messagebox.showwarning("Input Error", "Delay must be a non-negative value.")
            self.uploading = False
            self.start_button.config(text="Start Upload", command=self.toggle_upload)
            return

        try:
            if len(self.video_files) == 0:
                self.log("Input Error: No Videos files found in the selected folder.")
                messagebox.showwarning("Input Error", "No Videos files found in the selected folder.")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return

            if len(self.video_files) < num_videos:
                self.log(f"Input Error: Selected number of videos ({num_videos}) exceeds available videos ({len(self.video_files)}).")
                messagebox.showwarning("Input Error", f"Selected number of video ({num_videos}) exceeds available video ({len(self.video_files)}).")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return
            if post_type == 'Scheduled' and len(self.times) == 0:
                self.log("Input Error: Please Generate Random Times First.")
                messagebox.showwarning("Input Error", "Please Generate Random Times First.")
                self.uploading = False
                self.start_button.config(text="Start Upload", command=self.toggle_upload)
                return

            # Update progress bar
            self.progress_var.set(0)
            self.progress_label.config(text="Progress: 0%")
            self.root.update_idletasks()
            if self.check_account(self.cookies) == True:
                self.reqs.headers['cookie'] = f'{self.cookies};i_user={self.pageId}'
                self.reqs.cookies['i_user'] = self.pageId
                counter = 0
                dn = []
                while True:
                    if len(dn) >= num_videos:
                        break
                    if not self.uploading:
                        self.log("Upload Stopped by User.")
                        break
                    if post_type == 'Scheduled':
                        timeToPost = get_timestamp(self.times)
                        if timeToPost == False:
                            self.log("No Valid Times, Please Create Valid Times .")
                            self.uploading = False
                            self.start_button.config(text="Start Upload", command=self.toggle_upload)
                            break
                        self.timeToPost = timeToPost
                    self.postId = self.captchas[counter].split('::||')[0]
                    self.captcha = self.captchas[counter].split('::||')[1]
                    counter += 1
                    if self.captcha != '' and self.captcha != ' ':
                        whatPrint = self.captcha
                    else:
                        whatPrint = self.postId
                    try:
                        self.donePost = open(fr'Done\{self.pageId}.txt', 'r', encoding='utf-8').read().split('\n')
                    except:
                        self.donePost = []
                    if self.postId in self.donePost:
                        self.log(f"Done Post {whatPrint} Before .")
                        continue

                    if self.upload_video() == True:
                        # Placeholder for actual upload logic
                        if post_type == "Scheduled":
                            scheduled_time = datetime.datetime.fromtimestamp(self.timeToPost)
                            if scheduled_time:
                                self.log(f"Scheduled Post for {whatPrint} at {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
                            else:
                                self.log(f"Failed to schedule Post for {whatPrint}. No valid timestamp available.")
                        else:
                            self.log(f"Posting now: {whatPrint}")
                        dn.append(0)

                        # Simulate delay and update progress bar
                        progress_percentage = ((len(dn)) / num_videos) * 100
                        self.progress_var.set(progress_percentage)
                        self.progress_label.config(text=f"Progress: {int(progress_percentage)}%")
                        self.root.update_idletasks()
                        open(fr'Done\{self.pageId}.txt', 'a', encoding='utf-8').write(f'{self.postId}\n')
                        delayTime = random.randint(int(delay//2), int(delay))
                        self.log(f'Sleeping For {delayTime} Seconds .')
                        time.sleep(delayTime)
                    else:
                        self.log(f"Error: Failed to post Video:")

                if self.uploading:
                    messagebox.showinfo("Upload Complete", f"Successfully uploaded {num_videos} Post.")
                    self.uploading = False
                    self.start_button.config(text="Start Upload", command=self.toggle_upload)

        except Exception as e:
            self.log(f"Error: Failed to upload Post:\n{str(e)}")
            messagebox.showerror("Error", f"Failed to upload Post:\n{str(e)}")

        # Reset button and progress bar after upload completes or stops
        self.uploading = False
        self.start_button.config(text="Start Upload", command=self.toggle_upload)
    def upload_video(self):
        for path in self.video_files:
            if self.postId in path:
                self.video_path = path
                return self.redyToUpload()
        return False
    def redyToUpload(self):
            self.reqs.headers['cookie'] = f'{self.cookies};i_user={self.pageId}'
            url = f'https://vupload-edge.facebook.com/ajax/video/upload/requests/start/?av={self.pageId}&__a=1'
            self.targetFile = open(self.video_path, 'rb')
            self.fileData = self.targetFile.seek(0, os.SEEK_END)
            data = {'file_size': self.fileData, 'file_extension': 'mp4', 'target_id': self.pageId, 'source': 'reel_composer', 'composer_dialog_version': '', 'waterfall_id': '205fbd46-2369-4bb6-973d-5ad6198cd3b4', 'composer_session_id': '205fbd46-2369-4bb6-973d-5ad6198cd3b4', 'composer_entry_point_ref': 'comet_pages_reel_composer_timeline_sprout', 'composer_work_shared_draft_mode': '', 'has_file_been_replaced': 'false', 'supports_chunking': 'true', 'supports_file_api': 'true', 'partition_start_offset': '0', 'partition_end_offset': self.fileData, 'creator_product': '2', 'spherical': 'false', 'video_publisher_action_source': '', '__user': self.pageId, '__a': '1', '__req': 'b3', '__comet_req': '15', 'jazoest': '25337', 'lsd': 'DvoJ3cocIbL4EzU7f3jLku', '__spin_r': '1007731907', '__spin_b': 'trunk', '__spin_t': '1687491086', 'qpl_active_flow_ids': '884152905', 'fb_dtsg': self.token}
            res = self.reqs.post(url, data=data)
            if '"video_id":"' in res.text:
                video_id = res.text.split('"video_id":"')[1].split('"')[0]
                return self.upload(video_id)
            else:
                return False
    def upload(self, video_id):
        url = 'https://vupload-edge.facebook.com/ajax/video/upload/requests/receive/'
        data = {'av': self.pageId, 'composer_session_id': '205fbd46-2369-4bb6-973d-5ad6198cd3b4', 'video_id': video_id, 'start_offset': '0', 'end_offset': '1048576', 'source': 'reel_composer', 'target_id': self.pageId, 'waterfall_id': '205fbd46-2369-4bb6-973d-5ad6198cd3b4', 'composer_entry_point_ref': 'comet_pages_reel_composer_timeline_sprout', 'composer_work_shared_draft_mode': '', 'composer_dialog_version': '', 'has_file_been_replaced': 'false', 'supports_chunking': 'true', 'upload_speed': '', 'partition_start_offset': '0', 'partition_end_offset': self.fileData, '__user': self.pageId, '__a': '1', '__req': 'b4', '__comet_req': '15', 'fb_dtsg': self.token, 'jazoest': '25337', '__spin_r': '1007731907', '__spin_b': 'trunk', '__spin_t': '1687491086', 'qpl_active_flow_ids': '884152905'}
        file = {'video_file_chunk': open(self.video_path, 'rb')}
        self.reqs.post(url, params=data, files=file)
        self.log(f'Done Upload Video: {video_id}')
        return self.addVideo(video_id)
    def addVideo(self, video_id):
        url = 'https://www.facebook.com/api/graphql/'
        title = self.title.get().strip().replace('\n', '  ')
        if title == '':
            postText = self.captcha
        else:
            postText = title
        if self.post_type0 == 'Scheduled':
            scheduled_time = datetime.datetime.fromtimestamp(self.timeToPost)
            sendTime = scheduled_time.strftime('%Y-%m-%d %H:%M:%S')
            var = '{"input":{"basic_data":{"source":"COMPOSER","target_id":"THISISPAGEID","video_id":"THISISVIDEOID","video_title":"THISISTHETITLE","waterfall_id":"961ba191862a7050af96b458fcd3e201","xhpc_message":"THISISTHETITLE","creator_product":"2","composer_entry_point_ref":"biz_web_home","composer_dialog_version":"V2","has_file_been_replaced":false,"supports_chunking":true},"thumbnail_data":{"thumbnail_type":"generated_default"},"ad_break_data":{},"vu_editor_data":{"auto_reframe_aspect_ratios":[],"auto_reframe_publish_mode":"auto_publish","trailer_review_required":false,"trailer_generate_on":false,"auto_reframe_mobile_only":true},"post_status_data":{"draft":false,"scheduled":true,"future_date":"10/5/2023","future_time":4260,"expiring":false,"expire_type":null,"expire_time":null,"schedule_timestamp":THISISTIMETOPOST},"main_composer_tab_data":{"action_type_id":[],"branded_content_data":{},"composertags_place":null,"composertags_sponsor":[],"content_tags":[],"cta_type":null,"direct_share_status":null,"fan_funding_promotion_metadata":{"is_promotional_post":false,"page_id":"THISISPAGEID"},"free_form_tags":[],"funded_content_program":null,"fundraiser_for_story_charity_id":null,"fundraiser_for_story_charity_type":"","game_id":"","is_explicitly_tagged_as_gaming_video":false,"object_id":[],"object_str":[],"send_dm_invite":true,"sponsor_relationship":null},"distribution_data":{"commentating_permission":null,"crossposting_config":[],"embeddable":true,"exclude_from_watch":false,"mature_content_rating":null,"no_story":false,"secret":false,"social_actions":true},"stars_data":{},"questions_data":{},"polls_data":{},"tracking_data":{"custom_labels":[],"external_video_id":""},"captions_data":{"autopublish_captions":true,"captions":[],"should_review_all_captions":false},"spherical_data":{"projection":null,"stereoMode":null},"live_premiere_data":{"premiere_time_ms":null,"should_premiere":false,"premiere_is_loe":false,"premiere_event_category_id":null},"location_preset_data":{},"video_abtesting_data":{},"auto_dub_data":{},"reel_publish_data":null,"non_uuc_reel_data":{},"actor_id":"THISISPAGEID","client_mutation_id":"1696403527819:1836620757"}}'.replace('THISISPAGEID', self.pageId).replace('THISISVIDEOID', video_id).replace('THISISTHETITLE', postText).replace('THISISTIMETOPOST', f'{self.timeToPost}'),
        else:
            var = '{"input":{"basic_data":{"source":"COMPOSER","target_id":"THISISPAGEID","video_id":"THISISVIDEOID","video_title":"THISISTHETITLE","waterfall_id":"961ba191862a7050af96b458fcd3e201","xhpc_message":"THISISTHETITLE","creator_product":"2","composer_entry_point_ref":"biz_web_home","composer_dialog_version":"V2","has_file_been_replaced":false,"supports_chunking":true},"thumbnail_data":{"thumbnail_type":"generated_default"},"ad_break_data":{},"vu_editor_data":{"auto_reframe_aspect_ratios":[],"auto_reframe_publish_mode":"auto_publish","trailer_review_required":false,"trailer_generate_on":false,"auto_reframe_mobile_only":true},"post_status_data":{"draft":false,"scheduled":false,"expiring":false,"expire_type":null,"expire_time":null},"main_composer_tab_data":{"action_type_id":[],"branded_content_data":{},"composertags_place":null,"composertags_sponsor":[],"content_tags":[],"cta_type":null,"direct_share_status":null,"fan_funding_promotion_metadata":{"is_promotional_post":false,"page_id":"THISISPAGEID"},"free_form_tags":[],"funded_content_program":null,"fundraiser_for_story_charity_id":null,"fundraiser_for_story_charity_type":"","game_id":"","is_explicitly_tagged_as_gaming_video":false,"object_id":[],"object_str":[],"send_dm_invite":true,"sponsor_relationship":null},"distribution_data":{"commentating_permission":null,"crossposting_config":[],"embeddable":true,"exclude_from_watch":false,"mature_content_rating":null,"no_story":false,"secret":false,"social_actions":true},"stars_data":{},"questions_data":{},"polls_data":{},"tracking_data":{"custom_labels":[],"external_video_id":""},"captions_data":{"autopublish_captions":true,"captions":[],"should_review_all_captions":false},"spherical_data":{"projection":null,"stereoMode":null},"live_premiere_data":{"premiere_time_ms":null,"should_premiere":false,"premiere_is_loe":false,"premiere_event_category_id":null},"location_preset_data":{},"video_abtesting_data":{},"auto_dub_data":{},"reel_publish_data":null,"non_uuc_reel_data":{},"actor_id":"THISISPAGEID","client_mutation_id":"1696403527819:1836620757"}}'.replace('THISISPAGEID', self.pageId).replace('THISISVIDEOID', video_id).replace('THISISTHETITLE', postText),
            scheduled_time = datetime.datetime.fromtimestamp(time.time())
            sendTime = scheduled_time.strftime('%Y-%m-%d %H:%M:%S')
        data = {
            'fb_dtsg': self.token,
            'variables': var,
            'doc_id': '6526070934125781',
        }
        res = self.reqs.post(url, data=data)
        try:
            x = res.json()['data']['video_publish']['video_asset_id']
            savePost(x, postText, sendTime)
            return True
        except:
            return False

# ------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    mac = get_mac_address()
    try:
        checkOut = checkMac(mac)
    except Exception as e:
        print(e)
        checkOut = None
    ends = False
    if checkOut:
        ends = checkOut['end_time']
    if checkOut == None:
        loading(root)
    else:
        initialize_gui()
    root.mainloop()
