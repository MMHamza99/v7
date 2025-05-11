import sys
import os
import logging

from PyQt6.QtGui import QFont, QMouseEvent, QIcon, QIntValidator
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtGui import QPixmap, QPainter  # Ensure these are imported at the top
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout,
    QHBoxLayout, QComboBox, QStackedWidget, QProgressBar, QButtonGroup, QSizePolicy,
    QFileDialog, QListWidget, QListWidgetItem
)


from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout,
    QHBoxLayout, QComboBox, QStackedWidget, QProgressBar, QButtonGroup, QSizePolicy,
    QFileDialog, QListWidget, QListWidgetItem
)

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox,
    QScrollArea, QGridLayout, QPushButton
)

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox,
    QScrollArea, QGridLayout, QPushButton
)

import os
from PyQt6.QtCore import QSize, Qt, QUrl
from PyQt6.QtGui import QPixmap, QPainter, QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox
# Import multimedia classes for video playback
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

# =======================
# External Stylesheet Loader
# =======================
def load_stylesheet(app, path="styles.qss"):
    # (unchanged)
    if os.path.exists(path):
        try:
            with open(path, "r") as file:
                app.setStyleSheet(file.read())
        except Exception as e:
            print(f"Failed to load stylesheet: {e}")
    else:
        print("Stylesheet not found; using inline defaults.")

# =======================
# Logging to QTextEdit Handler
# =======================
class QTextEditLogger(logging.Handler):
    # (unchanged)
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record):
        msg = self.format(record)
        self.text_edit.append(msg)

# --------------------
# Custom widget for each post
# --------------------------

class PostItemWidget(QWidget):
    def __init__(self, key, file_path, thumbnail_size, caption, parent=None):
        super().__init__(parent)
        self.key = key  # Unique identifier for saving
        self.file_path = file_path
        self.media_player = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        if file_path:
            lower_file = file_path.lower()
            if lower_file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.display_widget = QLabel()
                self.display_widget.setFixedSize(thumbnail_size, thumbnail_size)
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(thumbnail_size, thumbnail_size,
                                           Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
                else:
                    pixmap = QPixmap(thumbnail_size, thumbnail_size)
                    pixmap.fill(Qt.GlobalColor.darkGray)
                self.display_widget.setPixmap(pixmap)
            elif lower_file.endswith(('.mp4', '.avi', '.mov')):
                self.display_widget = QVideoWidget()
                self.display_widget.setFixedSize(thumbnail_size, thumbnail_size)
                self.media_player = QMediaPlayer(self)
                self.audio_output = QAudioOutput(self)
                self.media_player.setAudioOutput(self.audio_output)
                self.media_player.setVideoOutput(self.display_widget)
                self.media_player.setSource(QUrl.fromLocalFile(file_path))
                self.audio_output.setVolume(0)
                self.media_player.play()
                
            else:
                self.display_widget = QLabel("Unsupported file")
                self.display_widget.setFixedSize(thumbnail_size, thumbnail_size)
                self.display_widget.setStyleSheet("background-color: gray; color: white;")
        else:
            self.display_widget = QLabel("No File")
            self.display_widget.setFixedSize(thumbnail_size, thumbnail_size)
            self.display_widget.setStyleSheet("background-color: #2E2E33; color: white;")

        layout.addWidget(self.display_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.caption_edit = QLineEdit(caption)
        self.caption_edit.setStyleSheet("""
            color: white;
            background-color: #2E2E33;
            border-radius: 5px;
            padding: 3px;
        """)
        layout.addWidget(self.caption_edit, alignment=Qt.AlignmentFlag.AlignCenter)

        self.checkbox = QCheckBox("Select")
        self.checkbox.setStyleSheet("color: white;")
        self.checkbox.setChecked(True)
        layout.addWidget(self.checkbox, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)



# =======================
# Download Thread with Progress (Modified)
# =======================
class DownloadThread(QThread):
    """
    Simulates a download process by updating progress and logs.
    Now accepts a starting progress value so that it can resume.
    """
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()

    def __init__(self, start_value=1, parent=None):
        super().__init__(parent)
        self.start_value = start_value

    def run(self):
        self.log_signal.emit("🟢 Download started...")
        # Continue the loop from self.start_value to 100
        for i in range(self.start_value, 101):
            if self.isInterruptionRequested():
                self.log_signal.emit("⛔ Download paused!")
                # When interrupted, exit the thread so that it can later resume from progress i
                return
            self.progress_signal.emit(i)
            QThread.msleep(30)  # Simulate work (30ms per percent)
        self.log_signal.emit("✅ Download completed!")
        self.finished_signal.emit()


# =======================
# Animated Button for Start/Stop Actions
# =======================
class AnimatedButton(QPushButton):
    """
    A QPushButton subclass with hover effects.
    """
    def __init__(self, text, color, hover_color, parent=None):
        super().__init__(text, parent)
        self.color = color
        self.hover_color = hover_color
        self.setStyleSheet(self.get_style(self.color))

    def enterEvent(self, event):
        self.setStyleSheet(self.get_style(self.hover_color))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.get_style(self.color))
        super().leaveEvent(event)

    def get_style(self, color):
        return f"""
            background-color: {color};
            color: white;
            font-weight: bold;
            padding: 12px;
            border-radius: 8px;
            border: none;
        """

# =======================
# Animated Header Button with Hover Geometry Animation
# =======================
class AnimatedHeaderButton(QPushButton):
    """
    A QPushButton subclass that animates its geometry when hovered.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.initial_geometry = None
        self.hover_geometry = None

    def set_geometries(self, initial: QRect, hover: QRect):
        """
        Set the initial and hover geometries.
        """
        self.initial_geometry = initial
        self.hover_geometry = hover
        self.setGeometry(initial)

    def enterEvent(self, event):
        if self.initial_geometry and self.hover_geometry:
            self.animation.stop()
            self.animation.setStartValue(self.geometry())
            self.animation.setEndValue(self.hover_geometry)
            self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.initial_geometry and self.hover_geometry:
            self.animation.stop()
            self.animation.setStartValue(self.geometry())
            self.animation.setEndValue(self.initial_geometry)
            self.animation.start()
        super().leaveEvent(event)

# =======================
# Sidebar Widget with Animated Indicator
# =======================
class SidebarWidget(QWidget):
    """
    A custom sidebar with checkable buttons and an animated active indicator.
    The sidebar buttons display only an icon, with the full text available as a tooltip.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Set a narrow fixed width since we'll only display icons
        self.setFixedWidth(50)
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E33;
            }
            QPushButton#SidebarButton {
                background-color: transparent;
                color: white;
                font-size: 18px;
                padding: 10px;
                border: none;
            }
            QPushButton#SidebarButton:hover {
                background-color: #3A3A3F;
                border-radius: 8px;
            }
            QPushButton#SidebarButton:checked {
                background-color: #505058;
                border-radius: 8px;
            }
        """)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 10, 5, 10)
        self.layout.setSpacing(20)

        # Create a button group for exclusive selection
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        # Create sidebar buttons with icons and tooltips
        self.download_btn = self.create_button("Download", "📥")
        # New Upload button added after Download
        self.upload_btn = self.create_button("Upload", "📤")
        self.settings_btn = self.create_button("Settings", "⚙️")
        self.about_btn = self.create_button("About", "ℹ️")

        # Add buttons to layout in order
        self.layout.addWidget(self.download_btn)
        self.layout.addWidget(self.upload_btn)
        self.layout.addWidget(self.settings_btn)
        self.layout.addWidget(self.about_btn)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

        # Active indicator widget (yellow)
        self.indicator = QWidget(self)
        self.indicator.setStyleSheet("background-color: #FFD700; border-radius: 4px;")
        self.indicator.setFixedSize(4, 40)
        self.indicator.raise_()

        # Set default active button and update indicator position
        self.download_btn.setChecked(True)
        self.update_indicator(self.download_btn)

        # Connect button group signal to update the indicator when a new button is clicked
        self.button_group.buttonClicked.connect(self.on_button_clicked)

    def create_button(self, text, icon_text):
        """
        Create a checkable sidebar button that shows only an icon.
        The full label is set as a tooltip.
        """
        btn = QPushButton(icon_text)
        btn.setObjectName("SidebarButton")
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setToolTip(text)
        self.button_group.addButton(btn)
        return btn

    def on_button_clicked(self, button):
        """
        Animate the indicator to the newly clicked button.
        """
        self.update_indicator(button)

    def update_indicator(self, button):
        """
        Move the indicator widget to align with the given button.
        """
        pos = button.pos()
        target_y = pos.y() + (button.height() - self.indicator.height()) // 2
        anim = QPropertyAnimation(self.indicator, b"geometry")
        anim.setDuration(200)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.setStartValue(self.indicator.geometry())
        anim.setEndValue(QRect(0, target_y, self.indicator.width(), self.indicator.height()))
        anim.start()
        # Keep a reference to the animation to prevent garbage collection
        self.current_animation = anim

    def showEvent(self, event):
        """
        When the sidebar is shown, update the indicator to the currently active button.
        """
        super().showEvent(event)
        active = None
        for btn in self.button_group.buttons():
            if btn.isChecked():
                active = btn
                break
        # If no active button is found, default to download_btn.
        if active is None:
            active = self.download_btn
        self.update_indicator(active)

# =======================
# Upload Thread with Progress
# =======================
class UploadThread(QThread):
    """
    Simulates an upload process by updating progress and logs.
    Accepts a starting progress value so that it can resume.
    """
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()

    def __init__(self, start_value=1, parent=None):
        super().__init__(parent)
        self.start_value = start_value

    def run(self):
        self.log_signal.emit("🟢 Upload started...")
        for i in range(self.start_value, 101):
            if self.isInterruptionRequested():
                self.log_signal.emit("⛔ Upload paused!")
                return
            self.progress_signal.emit(i)
            QThread.msleep(30)  # Simulate work (30ms per percent)
        self.log_signal.emit("✅ Upload completed!")
        self.finished_signal.emit()

# =======================
# Main Application Window (Upload-related Methods)
# =======================
class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 580)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.is_dragging = False

        # Download-related variables:
        self.thread = None
        self.paused = False
        self.current_progress = 0
        self.last_source = ""
        self.last_user = ""


        # Posts page and manual posts variables:
        self.saved_posts_data = {}
        self.last_posts_folder = None
        self.manual_post_counter = 0

        # Upload-specific variables:
        self.upload_thread = None
        self.upload_paused = False
        self.upload_current_progress = 0
        self.upload_last_platform = ""
        self.upload_last_folder = ""
        self.posts_page = None

        # For upload resume comparisons:
        self.upload_last_platform = ""
        self.upload_last_account = ""
        self.upload_last_page = ""
        self.upload_last_folder = ""
        self.upload_current_progress = 0
        self.upload_paused = False
        self.downloader_map = {
            "  📱 Facebook Reels": FaceReelsDownloader,
            "  🎥 Facebook Videos": FaceReelsDownloader,
            "  📜 Facebook Posts (All)": FaceReelsDownloader,
            "  🎬 Instagram Reels": InstaReelsDownloader,
            "  📽 Instagram Videos": InstaReelsDownloader,
            "  📝 Instagram Posts (All)": InstaPostsDownloader,
            # "  🐦 Twitter Posts": TwitterPostsDownloader,
            # "  🍿 YouTube Shorts": YouTubeShortsDownloader,
            # "  📹 YouTube Videos": YouTubeVideosDownloader,
            "  🎵 TikTok Videos": TiktokVideosDownloader
        }
        # Existing accounts data for each platform:
        self.platform_accounts = {
            "Facebook": ["fb_account1", "fb_account2"],
            "Instagram": ["ig_account1"],
            "Twitter": [],  # No accounts available yet
            "YouTube": ["yt_account1", "yt_account2"]
        }
        # New: Facebook pages per account
        self.facebook_pages = {
            "fb_account1": ["FB Page A", "FB Page B"],
            "fb_account2": ["FB Page C"]
        }

        self.init_ui()

    def init_ui(self):
        # (unchanged layout code; see your full code above)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.header = QLabel("📥 Download Manager")
        self.header.setFixedHeight(50)
        self.header.setObjectName("HeaderLabel")
        self.header.setStyleSheet("""
            background-color: rgba(45, 45, 50, 0.8);
            color: white;
            font-weight: bold;
            font-size: 14px;
            padding-left: 15px;
            border-top-left-radius: 25px;
            border-top-right-radius: 25px;
        """)

        content_container = QWidget()
        content_container.setStyleSheet("""
            background-color: #202225;
            border-bottom-left-radius: 25px;
            border-bottom-right-radius: 25px;
            border: 1px solid #333;
        """)
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = SidebarWidget(self)
        # (Sidebar connections remain; note the download page is index 0.)
        self.sidebar.download_btn.clicked.connect(lambda: self.change_page(0))
        self.sidebar.upload_btn.clicked.connect(lambda: self.change_page(1))
        self.sidebar.settings_btn.clicked.connect(lambda: self.change_page(2))
        self.sidebar.about_btn.clicked.connect(lambda: self.change_page(3))
        content_layout.addWidget(self.sidebar)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #202225;")
        content_layout.addWidget(self.stacked_widget)

        main_layout.addWidget(self.header)
        main_layout.addWidget(content_container)

        # Header buttons (Minimize and Close) remain unchanged...
        self.minimize_btn = AnimatedHeaderButton("–", self)
        self.minimize_btn.setStyleSheet("""
            background-color: #F1FAEE;
            color: black;
            border-radius: 15px;
            font-weight: bold;
            border: none;
        """)
        initial_minimize_geom = QRect(520, 10, 30, 30)
        hover_minimize_geom   = QRect(517, 7, 36, 36)
        self.minimize_btn.set_geometries(initial_minimize_geom, hover_minimize_geom)
        self.minimize_btn.clicked.connect(self.showMinimized)

        self.close_btn = AnimatedHeaderButton("✖", self)
        self.close_btn.setStyleSheet("""
            background-color: #E63946;
            color: white;
            border-radius: 15px;
            font-weight: bold;
            border: none;
        """)
        initial_close_geom = QRect(560, 10, 30, 30)
        hover_close_geom   = QRect(557, 7, 36, 36)
        self.close_btn.set_geometries(initial_close_geom, hover_close_geom)
        self.close_btn.clicked.connect(self.close)

        # Initialize pages (Download page now includes the modified logic)
        self.init_download_page()
        self.init_upload_page()
        self.init_settings_page()
        self.init_about_page()

    def init_download_page(self):
        """
        Build the Download page with input fields, buttons, progress bar, and logs.
        """
        download_page = QWidget()
        layout = QVBoxLayout(download_page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        # Source dropdown label
        source_label = QLabel("From")
        source_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        source_label.setStyleSheet("color: #BBBBBB; border: none;")

        self.source_dropdown = QComboBox()
        self.source_dropdown.setStyleSheet("""
            background-color: #2E2E33;
            color: white;
            border-radius: 8px;
            padding: 8px;
            font-size: 16px;
        """)
        self.source_dropdown.clear()

        # --- Facebook Group ---
        self.source_dropdown.addItem("Facebook")
        index = self.source_dropdown.count() - 1
        item = self.source_dropdown.model().item(index)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)  # Make group header non-selectable
        self.source_dropdown.addItem("  📱 Facebook Reels")
        self.source_dropdown.addItem("  🎥 Facebook Videos")
        self.source_dropdown.addItem("  📜 Facebook Posts (All)")

        # --- Instagram Group ---
        self.source_dropdown.addItem("Instagram")
        index = self.source_dropdown.count() - 1
        item = self.source_dropdown.model().item(index)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
        self.source_dropdown.addItem("  🎬 Instagram Reels")
        self.source_dropdown.addItem("  📽 Instagram Videos")
        self.source_dropdown.addItem("  📝 Instagram Posts (All)")

        # --- Twitter Group ---
        self.source_dropdown.addItem("Twitter")
        index = self.source_dropdown.count() - 1
        item = self.source_dropdown.model().item(index)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
        self.source_dropdown.addItem("  🐦 Twitter Posts")

        # --- YouTube Group ---
        self.source_dropdown.addItem("YouTube")
        index = self.source_dropdown.count() - 1
        item = self.source_dropdown.model().item(index)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
        self.source_dropdown.addItem("  🍿 YouTube Shorts")
        self.source_dropdown.addItem("  📹 YouTube Videos")


        user_label = QLabel("User, Id, Url")
        user_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        user_label.setStyleSheet("color: #BBBBBB; border: none;")

        self.user_input = QLineEdit()
        self.user_input.setStyleSheet("""
            background-color: #2E2E33;
            color: white;
            border-radius: 8px;
            padding: 8px;
        """)

        number_label = QLabel("Number")
        number_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        number_label.setStyleSheet("color: #BBBBBB; border: none;")

        self.number_input = QLineEdit("20")
        self.number_input.setValidator(QIntValidator(1, 1000, self))
        self.number_input.setStyleSheet("""
            background-color: #2E2E33;
            color: white;
            border-radius: 8px;
            padding: 8px;
        """)

        # --- Buttons: Start and Stop (with pause/resume behavior) ---
        self.start_btn = AnimatedButton("Start", "#4CAF50", "#5ECF60")
        self.start_btn.clicked.connect(self.start_download)
        # Initially, the Stop button has red colors.
        self.stop_btn = AnimatedButton("Stop", "#D62828", "#E83B3B")
        self.stop_btn.clicked.connect(self.stop_download)
        self.stop_btn.setEnabled(False)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #333;
                border-radius: 8px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 8px;
            }
        """)

        logs_label = QLabel("Logs")
        logs_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        logs_label.setStyleSheet("color: #BBBBBB; border: none;")
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setStyleSheet("""
            background-color: #18191C;
            color: white;
            border-radius: 8px;
            padding: 8px;
        """)

        # Arrange widgets in layout
        layout.addWidget(source_label)
        layout.addWidget(self.source_dropdown)
        layout.addWidget(user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(number_label)
        layout.addWidget(self.number_input)
        layout.addLayout(btn_layout)
        layout.addWidget(self.progress_bar)
        layout.addWidget(logs_label)
        layout.addWidget(self.logs)

        self.stacked_widget.addWidget(download_page)
        self.setup_logging()
    # ------------------------------
    # Modified Upload Page (Index 1)
    # ------------------------------

    def init_upload_page(self):
        """
        Build the Upload page with platform, account, and page dropdowns,
        as well as folder selection and upload controls.
        """
        upload_page = QWidget()
        layout = QVBoxLayout(upload_page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Title: Upload Manager
        title_label = QLabel("Upload Manager")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #BBBBBB; border: none;")
        layout.addWidget(title_label)

        # --- Platform Dropdown ---
        platform_label = QLabel("Choose Platform")
        platform_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        platform_label.setStyleSheet("color: #BBBBBB; border: none;")
        layout.addWidget(platform_label)

        self.upload_platform_dropdown = QComboBox()
        self.upload_platform_dropdown.setStyleSheet("""
            background-color: #2E2E33;
            color: white;
            border-radius: 8px;
            padding: 8px;
            font-size: 16px;
        """)
        self.upload_platform_dropdown.addItem("Facebook")
        self.upload_platform_dropdown.addItem("Instagram")
        self.upload_platform_dropdown.addItem("Twitter")
        self.upload_platform_dropdown.addItem("YouTube")
        layout.addWidget(self.upload_platform_dropdown)

        # --- Account and Page Dropdowns in one horizontal layout ---
        account_page_layout = QHBoxLayout()
        account_page_layout.setSpacing(10)

        # Left: Account dropdown with label
        account_layout = QVBoxLayout()
        account_label = QLabel("Choose Account")
        account_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        account_label.setStyleSheet("color: #BBBBBB; border: none;")
        account_layout.addWidget(account_label)
        self.account_dropdown = QComboBox()
        self.account_dropdown.setStyleSheet("""
            background-color: #2E2E33;
            color: white;
            border-radius: 8px;
            padding: 8px;
            font-size: 16px;
        """)
        account_layout.addWidget(self.account_dropdown)
        account_page_layout.addLayout(account_layout)

        # Right: Page dropdown with label wrapped in its own widget container
        self.page_widget = QWidget()  # Container for page dropdown and its label
        page_layout = QVBoxLayout(self.page_widget)
        page_layout.setContentsMargins(0, 0, 0, 0)
        self.page_label = QLabel("Choose Page")
        self.page_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.page_label.setStyleSheet("color: #BBBBBB; border: none;")
        page_layout.addWidget(self.page_label)
        self.page_dropdown = QComboBox()
        self.page_dropdown.setStyleSheet("""
            background-color: #2E2E33;
            color: white;
            border-radius: 8px;
            padding: 8px;
            font-size: 16px;
        """)
        page_layout.addWidget(self.page_dropdown)
        account_page_layout.addWidget(self.page_widget)
        layout.addLayout(account_page_layout)

        # Connect dropdown signals to update functions:
        self.upload_platform_dropdown.currentIndexChanged.connect(self.update_account_dropdown)
        self.account_dropdown.currentIndexChanged.connect(self.update_page_dropdown)
        # Initialize the account (and page) dropdowns.
        self.update_account_dropdown()

        # --- Posts Folder Selection (if applicable) ---
        folder_label = QLabel("Select Posts Folder")
        folder_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        folder_label.setStyleSheet("color: #BBBBBB; border: none;")
        layout.addWidget(folder_label)

        folder_layout = QHBoxLayout()
        self.folder_path_input = QLineEdit()
        self.folder_path_input.setReadOnly(True)
        self.folder_path_input.setStyleSheet("""
            background-color: #2E2E33;
            color: white;
            border-radius: 8px;
            padding: 8px;
        """)
        browse_btn = AnimatedButton("Browse", "#4CAF50", "#5ECF60")
        browse_btn.clicked.connect(self.browse_folder)
        edit_btn = AnimatedButton("Edit", "#4CAF50", "#5ECF60")
        edit_btn.clicked.connect(self.open_posts_page)
        folder_layout.addWidget(self.folder_path_input)
        folder_layout.addWidget(browse_btn)
        folder_layout.addWidget(edit_btn)
        layout.addLayout(folder_layout)

        # --- Upload Progress Bar ---
        self.upload_progress_bar = QProgressBar()
        self.upload_progress_bar.setRange(0, 100)
        self.upload_progress_bar.setValue(0)
        self.upload_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #333;
                border-radius: 8px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.upload_progress_bar)

        # --- Start and Stop Buttons for Upload ---
        btn_layout = QHBoxLayout()
        self.upload_start_btn = AnimatedButton("Start", "#4CAF50", "#5ECF60")
        self.upload_start_btn.clicked.connect(self.start_upload)
        self.upload_stop_btn = AnimatedButton("Stop", "#D62828", "#E83B3B")
        self.upload_stop_btn.clicked.connect(self.stop_upload)
        self.upload_stop_btn.setEnabled(False)
        btn_layout.addWidget(self.upload_start_btn)
        btn_layout.addWidget(self.upload_stop_btn)
        layout.addLayout(btn_layout)

        # --- Upload Logs ---
        upload_logs_label = QLabel("Upload Logs")
        upload_logs_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        upload_logs_label.setStyleSheet("color: #BBBBBB; border: none;")
        layout.addWidget(upload_logs_label)
        self.upload_logs = QTextEdit()
        self.upload_logs.setReadOnly(True)
        self.upload_logs.setStyleSheet("""
            background-color: #18191C;
            color: white;
            border-radius: 8px;
            padding: 8px;
        """)
        layout.addWidget(self.upload_logs)

        self.stacked_widget.addWidget(upload_page)


    def update_account_dropdown(self):
        """Update the account dropdown based on the selected platform."""
        platform = self.upload_platform_dropdown.currentText().strip()
        accounts = self.platform_accounts.get(platform, [])
        self.account_dropdown.clear()
        if accounts:
            for account in accounts:
                self.account_dropdown.addItem(account)
            self.account_dropdown.setEnabled(True)
            if platform == "Facebook":
                # Show the page widget and update pages accordingly.
                self.page_widget.setVisible(True)
                self.update_page_dropdown()
            else:
                # Hide the page widget for non-Facebook platforms.
                self.page_widget.setVisible(False)
        else:
            self.account_dropdown.addItem("No account available, add account first")
            self.account_dropdown.setEnabled(False)
            self.page_widget.setVisible(False)

    def update_page_dropdown(self):
        """Update the page dropdown based on the selected Facebook account.
           This method is only meaningful if the platform is Facebook."""
        platform = self.upload_platform_dropdown.currentText().strip()
        if platform != "Facebook":
            self.page_dropdown.clear()
            self.page_dropdown.addItem("Not applicable")
            self.page_dropdown.setEnabled(False)
            return

        account = self.account_dropdown.currentText().strip()
        pages = self.facebook_pages.get(account, [])
        self.page_dropdown.clear()

        # Add an empty option as the first entry.
        # This represents "no page" so the upload will occur on the account directly.
        self.page_dropdown.addItem("")  # Blank item

        # Then add the pages for the account, if any.
        if pages:
            for page in pages:
                self.page_dropdown.addItem(page)

        self.page_dropdown.setEnabled(True)

    # ------------------------------
    # Folder Browser for Upload Page
    # ------------------------------
    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Posts Folder")
        if folder_path:
            self.folder_path_input.setText(folder_path)

    # ------------------------------
    # Open Posts Page to Edit/Review Folder Contents
    # ------------------------------
    def open_posts_page(self):
        folder = self.folder_path_input.text().strip()
        self.init_posts_page(folder)
        self.stacked_widget.setCurrentWidget(self.posts_page)


    def init_posts_page(self, folder):
        if self.posts_page is not None:
            self.stacked_widget.removeWidget(self.posts_page)
            self.posts_page.deleteLater()

        if self.last_posts_folder != folder:
            self.saved_posts_data = {}
            self.last_posts_folder = folder

        self.posts_page = QWidget()
        main_layout = QVBoxLayout(self.posts_page)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        title = QLabel("Posts in Folder")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #BBBBBB;")
        main_layout.addWidget(title)

        controls_layout = QHBoxLayout()
        self.select_all_button = QPushButton("Unselect All")
        self.select_all_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                color: white;
            }
            QPushButton:hover {
                background-color: #43a047;
            }
        """)
        self.select_all_button.clicked.connect(self.toggle_select_all)
        controls_layout.addWidget(self.select_all_button)
        controls_layout.addStretch(1)
        main_layout.addLayout(controls_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollBar:vertical {
                background: #2E2E33;
                width: 12px;
                margin: 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #4CAF50;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        container = QWidget()
        self.posts_grid = QGridLayout(container)
        self.posts_grid.setSpacing(10)

        thumbnail_size = 150
        valid_ext = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.mp4', '.avi', '.mov')
        row, col = 0, 0
        self.post_widgets = []

        # Load captions from 'caption_texts.txt'
        captions_dict = {}
        if folder and os.path.isdir(folder):
            caption_file = os.path.join(folder, 'caption_texts.txt')
            if os.path.exists(caption_file):
                try:
                    with open(caption_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            parts = line.strip().split('::||')
                            if len(parts) == 2:
                                file_name, caption = parts
                                captions_dict[file_name] = caption
                                # print(captions_dict)
                    self.upload_logs.append(f"Loaded captions for {len(captions_dict)} files.")
                except Exception as e:
                    self.upload_logs.append(f"Error reading caption file: {e}")
            else:
                self.upload_logs.append("No 'caption_texts.txt' found; using file names as captions.")

        folder_files = []
        if folder and os.path.isdir(folder):
            try:
                for file in os.listdir(folder):
                    lower_file = file.lower()
                    if lower_file.endswith(valid_ext):
                        folder_files.append(os.path.join(folder, file))
            except Exception as e:
                self.upload_logs.append(f"Error listing folder: {e}")

        # Process folder files with captions
        for full_path in folder_files:
            key = full_path
            # file_name = os.path.basename(full_path)
            file_name = os.path.splitext(os.path.basename(full_path))[0]
            # print(file_name)
            default_caption = captions_dict.get(file_name, os.path.splitext(file_name)[0])
            # print('--')
            # print(default_caption)
            if full_path in self.saved_posts_data:
                data = self.saved_posts_data[full_path]
                caption = data.get("caption", default_caption)
                selected = data.get("selected", True)
            else:
                caption = default_caption
                selected = True
            post_widget = PostItemWidget(key, full_path, thumbnail_size, caption)
            post_widget.checkbox.setChecked(selected)
            self.posts_grid.addWidget(post_widget, row, col)
            self.post_widgets.append(post_widget)
            col += 1
            if col >= 2:
                col = 0
                row += 1

        # Process manual posts
        for key, data in self.saved_posts_data.items():
            if key not in folder_files:
                if os.path.exists(key):
                    file_path = key
                    caption = data.get("caption", os.path.splitext(os.path.basename(key))[0])
                else:
                    file_path = ""
                    caption = data.get("caption", "")
                post_widget = PostItemWidget(key, file_path, thumbnail_size, caption)
                post_widget.checkbox.setChecked(data.get("selected", True))
                self.posts_grid.addWidget(post_widget, row, col)
                self.post_widgets.append(post_widget)
                col += 1
                if col >= 2:
                    col = 0
                    row += 1

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)

        add_post_btn = QPushButton("Add Post")
        add_post_btn.setStyleSheet("""
            QPushButton {
                background-color: #61dafb;
                border: none;
                border-radius: 10px;
                padding: 16px 24px;
                font-size: 16px;
                font-weight: bold;
                color: #1e1e1e;
            }
            QPushButton:hover {
                background-color: #52c7e8;
            }
        """)
        add_post_btn.clicked.connect(self.init_add_post_page)
        bottom_layout.addWidget(add_post_btn)

        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                border-radius: 10px;
                padding: 16px 24px;
                font-size: 16px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #43a047;
            }
        """)
        save_btn.clicked.connect(self.save_post_selection)
        bottom_layout.addWidget(save_btn)

        main_layout.addLayout(bottom_layout)

        self.stacked_widget.addWidget(self.posts_page)
        self.stacked_widget.setCurrentWidget(self.posts_page)

    def save_post_selection(self):
        for widget in self.post_widgets:
            self.saved_posts_data[widget.key] = {
                "caption": widget.caption_edit.text().strip(),
                "selected": widget.checkbox.isChecked()
            }
        self.upload_logs.append("Selected posts and captions saved:")
        for key, data in self.saved_posts_data.items():
            self.upload_logs.append(f" - {os.path.basename(key) if key else 'Manual Post'}: {data.get('caption')} (Selected: {data.get('selected')})")
        self.upload_logs.append("✅ Selections saved.")
        self.stacked_widget.setCurrentIndex(1)

    # ---------------------------------------------------
    # Toggle Select/Unselect All
    # ---------------------------------------------------
    def toggle_select_all(self):
        # Check if all post widgets are selected.
        all_selected = all(widget.checkbox.isChecked() for widget in self.post_widgets)

        if all_selected:
            # Unselect all
            for widget in self.post_widgets:
                widget.checkbox.setChecked(False)
            self.select_all_button.setText("Select All")
        else:
            # Select all
            for widget in self.post_widgets:
                widget.checkbox.setChecked(True)
            self.select_all_button.setText("Unselect All")


    # ---------------------------------------------------
    # NEW: Add Post Workflow
    # ---------------------------------------------------
    def init_add_post_page(self):
        add_page = QWidget()
        add_page.setStyleSheet("background-color: #1e1e1e;")
        layout = QVBoxLayout(add_page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Add New Post")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #61dafb;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        file_layout = QHBoxLayout()
        self.new_post_file_input = QLineEdit()
        self.new_post_file_input.setPlaceholderText("Select file (optional)")
        self.new_post_file_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                padding: 12px;
                color: #ffffff;
                font-size: 16px;
            }
        """)
        file_layout.addWidget(self.new_post_file_input)
        browse_btn = QPushButton("Browse")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #61dafb;
                border: none;
                border-radius: 8px;
                padding: 10px;
                color: #1e1e1e;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #52c7e8;
            }
        """)
        browse_btn.clicked.connect(self.browse_new_post_file)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)

        self.new_post_text_input = QTextEdit()
        self.new_post_text_input.setPlaceholderText("Enter text (optional)")
        self.new_post_text_input.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                padding: 12px;
                color: #ffffff;
                font-size: 16px;
            }
        """)
        self.new_post_text_input.setMinimumHeight(100)
        layout.addWidget(self.new_post_text_input)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Post")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #61dafb;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
                color: #1e1e1e;
            }
            QPushButton:hover {
                background-color: #52c7e8;
            }
        """)
        add_btn.clicked.connect(self.handle_add_post)
        btn_layout.addWidget(add_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e53935;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        cancel_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.posts_page))
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.stacked_widget.addWidget(add_page)
        self.stacked_widget.setCurrentWidget(add_page)

    def browse_new_post_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "Images and Videos (*.png *.jpg *.jpeg *.gif *.bmp *.mp4 *.avi *.mov)"
        )
        if file_path:
            self.new_post_file_input.setText(file_path)

    def handle_add_post(self):
        file_path = self.new_post_file_input.text().strip()
        text_content = self.new_post_text_input.toPlainText().strip()  # Use toPlainText() for QTextEdit
        if not file_path and not text_content:
            QMessageBox.warning(self, "Invalid Post", "Please provide a file or text for the post.")
            return
        # Use file_path as key if provided; otherwise generate a manual key.
        if file_path:
            key = file_path
        else:
            self.manual_post_counter += 1
            key = f"manual_post_{self.manual_post_counter}"
        # Save the new post data.
        self.saved_posts_data[key] = {"caption": text_content, "selected": True}
        # Rebuild the posts page (using the previously loaded folder).
        self.init_posts_page(self.last_posts_folder)
        # Return to the posts page.
        self.stacked_widget.setCurrentWidget(self.posts_page)


    # ------------------------------
    # Upload Start/Stop/Resume Logic (Similar to Download)
    # ------------------------------
    def start_upload(self):

        # Retrieve current platform.
        current_platform = self.upload_platform_dropdown.currentText().strip()

        # Determine the posts source:
        # - If a valid folder is selected, use that.
        # - Otherwise, if there are manually added posts, treat the posts as coming from "Manual posts".
        current_folder = self.folder_path_input.text().strip()
        if current_folder and os.path.isdir(current_folder):
            posts_available = True
            folder_used = current_folder
        elif self.saved_posts_data:
            posts_available = True
            folder_used = "Manual posts"
        else:
            posts_available = False

        if not posts_available:
            self.upload_logs.append("⚠️ No posts available! Please select a valid posts folder or add posts manually.")
            return

        # Check that an account is available.
        if not self.account_dropdown.isEnabled():
            self.upload_logs.append(f"⚠️ No account available for {current_platform}. Please add an account first!")
            return

        # Retrieve current account.
        current_account = self.account_dropdown.currentText().strip() if self.account_dropdown.isEnabled() else ""

        # Retrieve current page if the platform is Facebook.
        current_page = ""
        if current_platform == "Facebook" and self.page_dropdown.isEnabled():
            current_page = self.page_dropdown.currentText().strip()

        # ---------------------------
        # Now handle the resume logic.
        # ---------------------------
        if self.upload_paused:
            # Compare all parameters with the last used ones.
            if (current_platform == self.upload_last_platform and
                current_account == self.upload_last_account and
                current_page == self.upload_last_page and
                folder_used == self.upload_last_folder):
                # All parameters are identical: resume the upload.
                self.upload_logs.append(f"🟢 Resuming upload from {self.upload_current_progress}%")
                self.upload_thread = UploadThread(start_value=self.upload_current_progress)
                self.upload_thread.log_signal.connect(self.upload_logs.append)
                self.upload_thread.progress_signal.connect(self.upload_progress_bar.setValue)
                self.upload_thread.finished_signal.connect(self.upload_finished)
                self.upload_thread.start()
                self.upload_paused = False
            else:
                # Parameters have changed: start a new upload.
                self.upload_logs.append("Parameters changed – starting a new upload.")
                # Save the new parameters.
                self.upload_last_platform = current_platform
                self.upload_last_account = current_account
                self.upload_last_page = current_page
                self.upload_last_folder = folder_used

                self.upload_progress_bar.setValue(0)
                self.upload_current_progress = 1
                self.upload_thread = UploadThread(start_value=1)
                self.upload_thread.log_signal.connect(self.upload_logs.append)
                self.upload_thread.progress_signal.connect(self.upload_progress_bar.setValue)
                self.upload_thread.finished_signal.connect(self.upload_finished)
                self.upload_thread.start()
                self.upload_paused = False
        else:
            # Not paused: always start a new upload.
            self.upload_logs.append("🟢 Starting new upload.")
            # Save the current parameters.
            self.upload_last_platform = current_platform
            self.upload_last_account = current_account
            self.upload_last_page = current_page
            self.upload_last_folder = folder_used

            self.upload_progress_bar.setValue(0)
            self.upload_current_progress = 1
            self.upload_thread = UploadThread(start_value=1)
            self.upload_thread.log_signal.connect(self.upload_logs.append)
            self.upload_thread.progress_signal.connect(self.upload_progress_bar.setValue)
            self.upload_thread.finished_signal.connect(self.upload_finished)
            self.upload_thread.start()
            self.upload_paused = False

        self.upload_start_btn.setEnabled(False)
        self.upload_stop_btn.setEnabled(True)

    def stop_upload(self):
        """
        When the Stop button is clicked:
         - Request interruption of the running upload thread,
         - Save the current progress,
         - Mark the upload as paused,
         - Re-enable the Start button to allow resumption.
        """
        if self.upload_thread and self.upload_thread.isRunning():
            self.upload_current_progress = self.upload_progress_bar.value()
            self.upload_thread.requestInterruption()
            self.upload_paused = True
            self.upload_logs.append(f"⛔ Upload paused at {self.upload_current_progress}%")
            self.upload_start_btn.setEnabled(True)
            self.upload_stop_btn.setEnabled(False)

    def upload_finished(self):
        """
        Reset UI elements once upload is finished.
        """
        self.upload_start_btn.setEnabled(True)
        self.upload_stop_btn.setEnabled(False)
        self.upload_progress_bar.setValue(100)
        self.upload_paused = False

    # (Draggable window implementation and other methods remain unchanged.)
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.offset = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_dragging:
            self.move(event.globalPosition().toPoint() - self.offset)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False

    def init_settings_page(self):
        # (Unchanged)
        settings_page = QWidget()
        layout = QVBoxLayout(settings_page)
        layout.setContentsMargins(20, 20, 20, 20)
        settings_label = QLabel("Settings")
        settings_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        settings_label.setStyleSheet("color: #BBBBBB; border: none;")
        layout.addWidget(settings_label)
        self.stacked_widget.addWidget(settings_page)

    def init_about_page(self):
        # (Unchanged)
        about_page = QWidget()
        layout = QVBoxLayout(about_page)
        layout.setContentsMargins(20, 20, 20, 20)
        about_label = QLabel("About")
        about_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        about_label.setStyleSheet("color: #BBBBBB; border: none;")
        layout.addWidget(about_label)
        self.stacked_widget.addWidget(about_page)

    def change_page(self, index):
        self.stacked_widget.setCurrentIndex(index)

    # --- Modified Download Methods for Pause/Resume ---
    def start_download0(self):
        """
        When the Start button is clicked:
         - If the download was paused and the current source/user are unchanged,
           resume from the saved progress.
         - Otherwise, start a fresh download.
        """
        current_source = self.source_dropdown.currentText().strip()
        current_user = self.user_input.text().strip()

        # If paused and the source and user haven't changed, resume.
        if self.paused and current_source == self.last_source and current_user == self.last_user:
            self.logs.append(f"🟢 Resuming download from {self.current_progress}%")
            self.thread = DownloadThread(start_value=self.current_progress)
            self.thread.log_signal.connect(self.logs.append)
            self.thread.progress_signal.connect(self.progress_bar.setValue)
            self.thread.finished_signal.connect(self.download_finished)
            self.thread.start()
            self.paused = False
        else:
            # If not paused or if options have changed, do a fresh download.
            if not current_user:
                self.logs.append("⚠️ Enter a username!")
                return
            self.logs.append(f"🟢 Starting download for {current_user} using option '{current_source}'")
            # Store the current selections for future resume comparisons
            self.last_source = current_source
            self.last_user = current_user

            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.progress_bar.setValue(0)
            self.current_progress = 1
            self.thread = DownloadThread(start_value=1)
            self.thread.log_signal.connect(self.logs.append)
            self.thread.progress_signal.connect(self.progress_bar.setValue)
            self.thread.finished_signal.connect(self.download_finished)
            self.thread.start()
            self.paused = False

        # Regardless, disable the Start button to prevent multiple clicks.
        self.start_btn.setEnabled(False)

    def start_download(self):
        selected_source = self.source_dropdown.currentText()
        user = self.user_input.text().strip()
        number = self.number_input.text().strip()

        if not user:
            self.logs.append("Please enter a user, ID, or URL.")
            return
        try:
            number = int(number)
            if number <= 0:
                raise ValueError
        except ValueError:
            self.logs.append("Please enter a valid positive integer for the number.")
            return

        download_func = self.downloader_map.get(selected_source)
        if download_func:
            self.thread = DownloadThread(download_func, user, number)
            self.thread.log_signal.connect(self.logs.append)
            self.thread.progress_signal.connect(self.progress_bar.setValue)
            self.thread.finished_signal.connect(self.download_finished)
            self.thread.start()
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
        else:
            self.logs.append("Invalid source selected.")
    def stop_download(self):
        """
        When the Stop button is clicked:
         - Request interruption of the running download thread.
         - Store the current progress.
         - Mark the download as paused.
         - Re-enable the Start button so that the user may click it to resume.
         - (The Stop button’s text remains unchanged.)
        """
        if self.thread and self.thread.isRunning():
            self.current_progress = self.progress_bar.value()
            self.thread.requestInterruption()
            self.paused = True

            self.logs.append(f"⛔ Download paused at {self.current_progress}%")
            # Enable the Start button so the user may resume.
            self.start_btn.setEnabled(True)

    def download_finished(self):
        """
        Reset UI elements once download is finished.
        """
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setValue(100)
        self.paused = False

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_path_input.setText(file_path)


    def setup_logging(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        handler = QTextEditLogger(self.logs)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info("Logger initialized.")


# =======================
# Application Entry Point
# =======================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("QToolTip { color: white; background-color: #333333; border: none; }")
    # load_stylesheet(app, "styles.qss")  # Use your stylesheet loader if needed
    window = DownloaderApp()
    window.show()
    sys.exit(app.exec())
