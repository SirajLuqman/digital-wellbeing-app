# main.py
# DigitalWellbeingApp - Modern, Attractive Dashboard UI with Keyboard Navigation for Inputs

import os
import re
import json
import requests
import threading
import random
import firebase_admin
from firebase_admin import credentials, firestore
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.checkbox import CheckBox
from kivy.properties import BooleanProperty, StringProperty
from kivy.clock import Clock
import time
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Rectangle, Mesh, Line, Ellipse
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.utils import platform
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp, sp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty
from kivy_garden.graph import Graph, MeshLinePlot
from dw_widgets import DWLabel, DWButton, DWCard, PRIMARY_BLUE, GRAY_TEXT, DARK_TEXT
from kivy.properties import ListProperty, StringProperty
from kivy.uix.scrollview import ScrollView
from dw_widgets import DWAppItem
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from plyer import notification
from plyer import filechooser
from kivy.uix.stencilview import StencilView
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.properties import BooleanProperty
from datetime import datetime, timedelta

try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False


Window.size = (420, 700)
Window.clearcolor = (1, 1, 1, 1)  # White background

APP_NAME = "Digital WellBeing"
APP_TAGLINE = "Live Beyond Screens"
PRIMARY_BLUE = [0.09, 0.47, 0.95, 1]
LIGHT_GRAY = [0.95, 0.95, 0.97, 1]
DARK_TEXT = [0.13, 0.14, 0.19, 1]
BORDER_COLOR = [0.81, 0.82, 0.83, 1]
INPUT_BG = [0.96, 0.97, 0.98, 1]
FONT_NAME = "Roboto"
GRAY_TEXT = [0.5, 0.5, 0.5, 1]  # RGBA for gray text
DARK_TEXT = [0.2, 0.2, 0.2, 1]  # RGBA for dark text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REMEMBER_ME_FILE = os.path.join(BASE_DIR, "remember_me.json")
GOOGLE_CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secret.json")
FIREBASE_API_KEY = "AIzaSyAer3MBV5qMSUInCCbPs0argbMvxlnxyrQ"
PROFILE_IMAGE_FILE = os.path.join(BASE_DIR, "profile_image.json")

WELLBEING_TIPS = [
    "Your eyes need a break! Stretch and look away for a few minutes.",
    "A quick walk can recharge your mind. Ready for a mini reset?",
    "Social media can wait. Your focus is more valuable right now.",
    "Time to unplug. Swap screens for restful sleep tonight.",
    "Weekend challenge: One hour offline. Can you do it?",
    "Friends are better than feeds. Call or meet someone you care about today.",
    "Limit reached! That’s progress—more time for you, less for apps.",
    "Doomscrolling won’t help. Read a book and upgrade your mind instead.",
    "Mute notifications and enjoy distraction-free focus time.",
    "Unused apps create digital clutter. Time for a clean-up.",
    "Hydrate your mind—drink a glass of water instead of scrolling.",
    "Deep breathing beats endless swiping. Take 5 calm breaths.",
    "Stand up, stretch, and reset your energy right now.",
    "Start your day screen-free. Plan before opening your phone.",
    "One mindful minute can refresh your whole hour.",
    "Nature time > screen time. Step outside for fresh air.",
    "Try journaling instead of checking your feed again.",
    "Silence your phone and enjoy the power of focus.",
    "Choose people over pixels. Talk face-to-face today.",
    "Clear your digital space—delete what you don’t need.",
    "Create before you consume. Write, draw, or build something.",
    "Protect your sleep—set a bedtime and stick to it.",
    "Move your body for 10 minutes instead of sitting online.",
    "Small breaks now prevent big burnout later.",
    "Today’s challenge: one meal with no screens at all.",
]

# ✅ Initialize Firebase app only once
if not firebase_admin._apps:
    cred = credentials.Certificate(os.path.join(BASE_DIR, "serviceAccountKey.json"))
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Define functions that use Firestore
def save_profile_to_firebase(user_email, name, mobile, age, hobby):
    doc_ref = db.collection("users").document(user_email)
    doc_ref.set({
        "name": name,
        "mobile": mobile,
        "age": age,
        "hobby": hobby,
    })
    print(f"✅ Profile saved for {user_email}")


def get_profile(user_email):
    doc_ref = db.collection("users").document(user_email)
    doc_ref = db.collection("users").document(user_email)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        print(f"❌ No profile found for {user_email}")
        return None

    profile = get_profile("user123")
    print(profile)

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def password_conditions(password):
    return {
        "At least 8 characters": len(password) >= 8,
        "At most 32 characters": len(password) <= 32,
        "A lowercase letter": bool(re.search(r"[a-z]", password)),
        "An uppercase letter": bool(re.search(r"[A-Z]", password)),
        "A number": bool(re.search(r"\d", password)),
        "A special character": bool(re.search(r"[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]", password)),
    }

class DWLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_size', 17)
        kwargs.setdefault('color', DARK_TEXT)
        kwargs.setdefault('font_name', FONT_NAME)
        kwargs.setdefault('halign', 'left')
        kwargs.setdefault('valign', 'middle')
        kwargs.setdefault('bold', False)
        kwargs.setdefault('italic', False)
        super().__init__(**kwargs)
        self.bind(size=self.setter('text_size'))

class DWButton(Button):
    def __init__(self, primary=True, **kwargs):
        kwargs.setdefault('font_size', 17)
        kwargs.setdefault('font_name', FONT_NAME)
        kwargs.setdefault('background_normal', '')
        kwargs.setdefault('background_down', '')
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', 44)
        if primary:
            kwargs.setdefault('background_color', PRIMARY_BLUE)
            kwargs.setdefault('color', [1, 1, 1, 1])
        else:
            kwargs.setdefault('background_color', [0.96, 0.97, 0.98, 1])
            kwargs.setdefault('color', PRIMARY_BLUE)
        super().__init__(**kwargs)

class TabNavigationTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_input = None

    def set_next_input(self, next_input):
        self.next_input = next_input

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] in ('tab', 'enter'):
            if self.next_input:
                target = self.next_input
                # if it's a BorderedInput, drill into its TextInput
                if hasattr(target, 'input'):
                    target = target.input
                # only focus if the widget supports it
                if hasattr(target, 'focus'):
                    target.focus = True
                    return True
        return super().keyboard_on_key_down(window, keycode, text, modifiers)


# A new widget for the collapsible section
class CollapsibleHeader(ButtonBehavior, BoxLayout):
    is_expanded = BooleanProperty(False)

    def __init__(self, title_text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(48)
        self.padding = [dp(16), 0]
        self.spacing = dp(10)

        self.title_label = DWLabel(text=title_text, font_size=sp(18), bold=True)
        self.icon_label = DWLabel(text="▼", size_hint_x=None, width=dp(20))
        self.add_widget(self.title_label)
        self.add_widget(self.icon_label)
        self.bind(is_expanded=self.on_expanded_change)

        with self.canvas.before:
            Color(*INPUT_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
            self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_release(self):
        self.is_expanded = not self.is_expanded

    def on_expanded_change(self, instance, value):
        self.icon_label.text = "▲" if value else "▼"


class BorderedInput(BoxLayout):
    def __init__(self, hint_text="", password=False, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, height=48, padding=[0, 0, 0, 0], **kwargs)
        with self.canvas.before:
            Color(*BORDER_COLOR)
            self.border = RoundedRectangle(pos=self.pos, size=self.size, radius=[8, ])
            Color(*INPUT_BG)
            self.bg = RoundedRectangle(pos=(self.x + 1, self.y + 1), size=(self.width - 2, self.height - 2),
                                       radius=[8, ])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.input = TabNavigationTextInput(
            hint_text=hint_text,
            background_normal='',
            background_active='',
            background_color=(0, 0, 0, 0),
            foreground_color=DARK_TEXT,
            cursor_color=PRIMARY_BLUE,
            font_size=17,
            font_name=FONT_NAME,
            password=password,
            padding=[12, 13, 12, 13],
            multiline=False,
            size_hint_y=None,
            height=48,
            write_tab=False
        )
        self.add_widget(self.input)

    def set_next_input(self, next_input):
        self.input.set_next_input(next_input.input if hasattr(next_input, 'input') else next_input)

    def update_rect(self, *args):
        self.border.pos = self.pos
        self.border.size = self.size
        self.bg.pos = (self.x + 1, self.y + 1)
        self.bg.size = (self.width - 2, self.height - 2)

class Card(BoxLayout):
    def __init__(self, title, value, color, **kwargs):
        super().__init__(orientation="vertical",
                         padding=16,
                         spacing=8,
                         size_hint_y=None,
                         height=150,
                         **kwargs)
        self.size_hint_x = 0.5
        self.canvas.before.clear()
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*color)
            self.bg = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)

        self.bind(pos=self._update_bg, size=self._update_bg)

        # Title
        self.add_widget(Label(text=title, font_size=18, bold=True,
                              color=[1, 1, 1, 1], halign="center", valign="middle"))

        # Value
        self.add_widget(Label(text=value, font_size=22,
                              color=[1, 1, 1, 1], halign="center", valign="middle"))

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class AppItem(ButtonBehavior, BoxLayout):
    def __init__(self, icon, name, time, progress, **kwargs):
        super().__init__(orientation="horizontal",
                         spacing=10,
                         size_hint_y=None,
                         height=60,
                         padding=[8, 8],
                         **kwargs)

        # Icon
        self.add_widget(Image(source=icon, size_hint=(None, None), size=(40, 40)))

        # App details (name + progress bar)
        details = BoxLayout(orientation="vertical", spacing=4)

        details.add_widget(Label(text=name, font_size=16, bold=True,
                                 halign="left", valign="middle",
                                 color=[0.2, 0.2, 0.2, 1],
                                 size_hint_y=None, height=20))

        pb = ProgressBar(max=100, value=progress, size_hint_y=None, height=10)
        details.add_widget(pb)

        self.add_widget(details)

        # Usage time (right aligned)
        self.add_widget(Label(text=time, font_size=14,
                              halign="right", valign="middle",
                              color=[0.3, 0.3, 0.3, 1],
                              size_hint=(None, 1), width=80))


class DrawerItem(ButtonBehavior, BoxLayout):
    """A single item in the sliding drawer."""
    text = StringProperty("")

    def __init__(self, text="", icon=None, **kwargs):
        super().__init__(orientation="horizontal", padding=12, spacing=10, size_hint_y=None, height=50, **kwargs)
        self.text = text
        if icon:
            self.add_widget(Image(source=icon, size_hint=(None, None), size=(30, 30)))
        self.add_widget(Label(text=self.text, font_size=16, color=DARK_TEXT, valign="middle"))

class ImageButton(ButtonBehavior, Image):
    """Clickable image button"""
    pass

# --- Define the new custom button class for the drawer ---
class DWDrawerButton(Button):
    """
    A custom button specifically for the drawer menu.
    It has a hover/press effect and a professional look.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = [0.95, 0.95, 0.97, 1]  # Normal state color
        self.color = [0.1, 0.1, 0.1, 1]  # Text color
        self.size_hint_y = None
        self.height = 50
        self.text_size = (None, None)
        self.halign = 'left'
        self.valign = 'middle'
        self.padding = [20, 0]
        self.font_size = 18
        self.bold = True
        self.opacity = 1
        self.on_press = self.animate_press
        self.on_release = self.animate_release

    def animate_press(self):
        """Animates the button's background color when pressed."""
        anim = Animation(background_color=[0.9, 0.9, 0.9, 1], duration=0.1)
        anim.start(self)

    def animate_release(self):
        """Animates the button's background color when released."""
        anim = Animation(background_color=[0.95, 0.95, 0.97, 1], duration=0.1)
        anim.start(self)

class CircularProfileButton(ButtonBehavior, StencilView):
    """
    Clickable circular profile image that intelligently handles double-triggers,
    and updates background color when the app theme changes.
    """

    source = StringProperty("icons/profile.png")

    def __init__(self, size=(80, 80), **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = size

        # A flag to prevent the file chooser from being opened multiple times.
        self._is_picking_file = False
        # Timestamp to prevent double-processing of a selection
        self._last_selection_time = 0

        # 🎨 Background ellipse (linked to theme)
        current_theme = App.get_running_app().get_current_theme()
        with self.canvas.before:   # always use canvas.before
            self.bg_color = Color(*current_theme["bg"])
            self.bg_circle = Ellipse(pos=self.pos, size=self.size)

        # 🖼️ Actual image inside stencil
        self.image = Image(
            source=self.source,
            size=self.size,
            pos=self.pos,
            allow_stretch=True,
            keep_ratio=False
        )
        self.add_widget(self.image)

        # Keep graphics in sync with widget position/size
        self.bind(pos=self.update_graphics, size=self.update_graphics)

        # 🔗 Hook into app theme so it updates automatically
        App.get_running_app().bind(is_dark_theme=self.update_theme)

    def update_graphics(self, *args):
        """Updates the position and size of the background and image."""
        self.bg_circle.pos = self.pos
        self.bg_circle.size = self.size
        self.image.pos = self.pos
        self.image.size = self.size

    def update_theme(self, instance, is_dark):
        """Schedule background color update when the theme switches."""
        Clock.schedule_once(self._perform_theme_update, 0)

    def _perform_theme_update(self, dt):
        """Internal method to safely update the theme."""
        current_theme = App.get_running_app().get_current_theme()
        self.bg_color.rgba = current_theme["bg"]

    def on_release(self):
        """Triggered by user click; prevents double-trigger of file chooser."""
        if not self._is_picking_file:
            self._is_picking_file = True
            self.open_file_chooser()

    def open_file_chooser(self):
        """A dedicated method to call the file chooser."""
        filechooser.open_file(
            on_selection=self.update_image,
            filters=["*.*"]
        )

    def update_image(self, selection):
        """Updates the image with the selected file and resets the flag."""
        current_time = time.time()
        if current_time - self._last_selection_time < 1.0:
            self.reset_file_picker_flag(0)
            return

        if selection:
            self.image.source = selection[0]
            self._last_selection_time = current_time

        Clock.schedule_once(self.reset_file_picker_flag, 0.5)

    def reset_file_picker_flag(self, dt):
        """Resets the file picker flag."""
        self._is_picking_file = False


class AIFeaturesScreen(Screen):
    """
    AI Features screen with professional text alignment and improved spacing.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_data = []
        self.analysis_results = {}
        self.root_layout = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(20))
        self.add_widget(self.root_layout)

    def on_pre_enter(self):
        """Refresh data every time the screen is shown"""
        self.user_data = self.get_user_data()
        self.analysis_results = self.analyze_productivity_patterns(self.user_data)
        self.root_layout.clear_widgets()

        # --- Improved Header with Better Spacing ---
        header_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(70),
            padding=[dp(0), dp(10), dp(0), dp(15)]
        )

        back_button = Button(
            text="< Back",
            size_hint_x=None,
            width=dp(100),
            background_color=(0, 0, 0, 0),
            background_normal='',
            color=(0, 0.7, 1, 1),
            bold=True,
            font_size=sp(16)
        )
        back_button.bind(on_release=lambda x: self.go_back_to_dashboard())

        # Add spacer to center the title properly
        spacer = Widget(size_hint_x=None, width=dp(100))


        title_label = Label(
            text="AI Productivity Insights",
            font_size=sp(22),
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_x=0.6,
            halign='center',
            valign='middle'
        )
        title_label.bind(texture_size=title_label.setter('size'))

        header_layout.add_widget(back_button)
        header_layout.add_widget(spacer)
        header_layout.add_widget(title_label)
        header_layout.add_widget(Widget(size_hint_x=1))
        self.root_layout.add_widget(header_layout)

        # --- Scrollable Content with Improved Spacing ---
        scroll_view = ScrollView(size_hint=(1, 1), bar_width=dp(8), bar_color=(0.5, 0.5, 0.5, 0.5))
        content = BoxLayout(orientation="vertical", spacing=dp(20), size_hint_y=None, padding=dp(10))
        content.bind(minimum_height=content.setter("height"))

        # Feature Cards with different colors
        content.add_widget(self.create_feature_card(
            "Productivity Score",
            "Get your daily productivity score based on focus patterns",
            self.generate_score,
            card_color=(0.25, 0.6, 0.95, 1),
        ))

        content.add_widget(self.create_feature_card(
            "AI Insights",
            "Understand your work patterns and peak performance hours",
            self.generate_insights,
            card_color=(0.35, 0.8, 0.6, 1)
        ))

        content.add_widget(self.create_feature_card(
            "Recommendations",
            "Get personalized improvement tips for better productivity",
            self.generate_recommendations,
            card_color=(0.95, 0.7, 0.3, 1)
        ))

        content.add_widget(self.create_feature_card(
            "Visualization",
            "See trends and patterns in your productivity over time",
            self.generate_visualization,
            card_color=(0.8, 0.5, 0.9, 1)
        ))

        scroll_view.add_widget(content)
        self.root_layout.add_widget(scroll_view)

    def create_feature_card(self, title, subtitle, callback, card_color):
        """Create a modern card with professional text alignment"""
        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(12)
        )

        # Modern gradient background
        with card.canvas.before:
            Color(*card_color)
            card.bg = RoundedRectangle(radius=[dp(15)], pos=card.pos, size=card.size)

            Color(0, 0, 0, 0.1)
            card.shadow = RoundedRectangle(
                radius=[dp(15)],
                pos=(card.pos[0] - 2, card.pos[1] - 2),
                size=(card.size[0] + 4, card.size[1] + 4)
            )

        card.bind(
            pos=lambda inst, val: (setattr(card.bg, "pos", val), setattr(card.shadow, "pos", (val[0] - 2, val[1] - 2))),
            size=lambda inst, val: (setattr(card.bg, "size", val),
                                    setattr(card.shadow, "size", (val[0] + 4, val[1] + 4)))
        )

        # Title label - LEFT ALIGNED for professional look
        title_label = Label(
            text=title,
            font_size=sp(20),
            bold=True,
            size_hint_y=None,
            halign='left',
            valign='top',
            color=(1, 1, 1, 1)
        )
        # 🔹 Fix: text_size matches card width dynamically, height matches text height
        title_label.bind(
            size=lambda inst, val: setattr(inst, "text_size", (val[0], None)),
            texture_size=lambda inst, val: setattr(inst, "height", val[1])
        )

        # Subtitle label - LEFT ALIGNED for readability
        subtitle_label = Label(
            text=subtitle,
            font_size=sp(16),
            color=(1, 1, 1, 0.9),
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        # 🔹 Same fix applied here
        subtitle_label.bind(
            size=lambda inst, val: setattr(inst, "text_size", (val[0], None)),
            texture_size=lambda inst, val: setattr(inst, "height", val[1])
        )

        # Result label - CENTERED for emphasis
        result_lbl = Label(
            text="Tap 'Generate Insight' for analysis",
            font_size=sp(16),
            color=(1, 1, 1, 0.8),
            size_hint_y=None,
            halign='center',
            valign='middle'
        )
        # 🔹 Keep fixed width wrapping for center alignment
        result_lbl.bind(
            size=lambda inst, val: setattr(inst, "text_size", (val[0], None)),
            texture_size=lambda inst, val: setattr(inst, "height", val[1] + dp(20))
        )

        # Modern button with better contrast and feedback
        btn = Button(
            text="Generate Insight",
            size_hint_y=None,
            height=dp(50),
            background_color=(0, 0, 0, 0.4),
            background_normal='',
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(16)
        )

        def on_btn_press(instance):
            btn.text = "Analyzing..."
            btn.background_color = (0, 0.5, 0.8, 1)
            Clock.schedule_once(lambda dt: callback(result_lbl, btn), 0.5)

        btn.bind(on_release=on_btn_press)

        # Calculate total card height dynamically
        total_height = (title_label.height + subtitle_label.height +
                        result_lbl.height + btn.height + dp(40))

        card.height = total_height

        card.add_widget(title_label)
        card.add_widget(subtitle_label)
        card.add_widget(result_lbl)
        card.add_widget(btn)

        return card

    # -------------------- Text Generators --------------------
    def generate_score(self, label, button):
        score = min(100, int(self.analysis_results.get("average_focus", 0) * 12 + 20))

        if score >= 85:
            feedback = "Excellent performance! Maintain your current habits."
        elif score >= 70:
            feedback = "Great job! Consistent focus patterns detected."
        elif score >= 60:
            feedback = "Good effort. Potential for improvement in time management."
        else:
            feedback = "Opportunity to develop better productivity habits."

        label.text = f"Score: {score}/100\n{feedback}"
        label.text_size = (dp(280), None)  # Added text_size update
        label.halign = 'center'
        label.valign = 'middle'
        button.text = "Generate Again"
        button.background_color = (0, 0, 0, 0.4)

    def generate_insights(self, label, button):
        peak = self.analysis_results.get("peak_hours", "10 AM - 1 PM")
        avg_focus = self.analysis_results.get("average_focus", 0)

        insights = f"Peak Performance: {peak}\nAverage Daily Focus: {avg_focus:.1f} hours\nConsistency: {'High' if avg_focus > 6 else 'Moderate' if avg_focus > 4 else 'Developing'}"

        label.text = insights
        label.text_size = (dp(280), None)  # Added text_size update
        label.halign = 'center'
        label.valign = 'middle'
        button.text = "Generate Again"
        button.background_color = (0, 0, 0, 0.4)

    def generate_recommendations(self, label, button):
        avg_focus = self.analysis_results.get("average_focus", 0)

        recommendations = {
            "high": "Maintain your current productivity system. Consider time-blocking for complex tasks.",
            "medium": "Try the Pomodoro technique with 25-minute focused sessions. Limit distractions during work blocks.",
            "low": "Start with shorter focused sessions. Identify and eliminate major distraction sources."
        }

        category = "high" if avg_focus > 7 else "medium" if avg_focus > 5 else "low"
        rec = recommendations[category]

        label.text = f"Recommendation:\n{rec}"
        label.text_size = (dp(280), None)  # Added text_size update
        label.halign = 'center'
        label.valign = 'middle'
        button.text = "Generate Again"
        button.background_color = (0, 0, 0, 0.4)

    def generate_visualization(self, label, button):
        avg_focus = self.analysis_results.get("average_focus", 0)

        if avg_focus > 6:
            trend = "Strong upward trend in productivity detected."
        elif avg_focus > 4:
            trend = "Steady productivity patterns maintained."
        else:
            trend = "Developing consistent work patterns."

        label.text = f"{trend}\n\nDetailed analytics visualization coming soon."
        label.text_size = (dp(280), None)  # Added text_size update
        label.halign = 'center'
        label.valign = 'middle'
        button.text = "Generate Again"
        button.background_color = (0, 0, 0, 0.4)

    # -------------------- Data Helpers --------------------
    def get_user_data(self):
        """Simulated daily focus hours with realistic patterns"""
        data = []
        today = datetime.today()
        for i in range(7):
            date = today - timedelta(days=i)
            is_weekend = date.weekday() >= 5
            base_focus = random.uniform(4, 7) if not is_weekend else random.uniform(2, 5)
            focus_hours = round(base_focus + random.uniform(-1, 1), 1)
            data.append({"date": date.strftime("%Y-%m-%d"), "focus_hours": focus_hours})
        return data

    def analyze_productivity_patterns(self, data):
        if not data:
            return {"average_focus": 0, "peak_hours": "N/A"}

        avg_focus = sum(d["focus_hours"] for d in data) / len(data)
        if avg_focus > 6:
            peak = "9 AM - 12 PM"
        elif avg_focus > 4:
            peak = "2 PM - 5 PM"
        else:
            peak = "10 AM - 3 PM"

        return {"average_focus": round(avg_focus, 1), "peak_hours": peak}

    def go_back_to_dashboard(self):
        """Navigate back to Dashboard screen"""
        self.manager.current = "dashboard"

# --- Updated DashboardScreen ---
class DashboardScreen(Screen):
    """
    Main screen for the dashboard, containing all widgets.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.drawer_width = 250
        self.drawer_open = False
        self.usage_data = self.get_usage_data()

        # --- Root layout ---
        self.root_layout = FloatLayout()
        self.add_widget(self.root_layout)

        # --- Main vertical layout for dashboard ---
        self.main_layout = BoxLayout(orientation='vertical', size_hint=(1, 1), spacing=20, padding=20)
        self.root_layout.add_widget(self.main_layout)

        # --- Non-scrolling content ---
        welcome = Label(
            text="[b]Welcome to your [color=4A90E2]Dashboard[/color]![/b]",
            markup=True,
            font_size=26,
            color=(0, 0.7, 1, 1),
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=50
        )
        self.main_layout.add_widget(welcome)

        # Metric cards
        cards_grid = GridLayout(cols=2, spacing=16, size_hint_y=None)
        cards_grid.bind(minimum_height=cards_grid.setter("height"))
        card_info = [
            {"title": "Screen Time", "value": self.usage_data["screen_time"], "color": [0.2, 0.6, 1, 1]},
            {"title": "Most Used App", "value": self.usage_data["most_used"], "color": [1, 0.4, 0.2, 1]},
            {"title": "Pickups", "value": str(self.usage_data["pickups"]), "color": [0.6, 0.3, 0.8, 1]},
            {"title": "Notifications", "value": str(self.usage_data["notifications"]), "color": [0.3, 0.8, 0.4, 1]},
        ]
        for info in card_info:
            cards_grid.add_widget(Card(info["title"], info["value"], info["color"]))
        self.main_layout.add_widget(cards_grid)

        # --- AI Productivity Card ---
        ai_card = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            padding=dp(15),
            spacing=dp(10)
        )

        # Add background to AI card
        with ai_card.canvas.before:
            Color(0.5, 0.0, 0.0, 1)
            ai_card.bg = RoundedRectangle(
                pos=ai_card.pos,
                size=ai_card.size,
                radius=[dp(10)]
            )

        ai_card.bind(
            pos=lambda inst, val: setattr(inst.bg, 'pos', val),
            size=lambda inst, val: setattr(inst.bg, 'size', val)
        )

        # AI icon
        ai_icon = Image(
            source="icons/ai.png",  # Use your AI icon file
            size_hint_x=None,
            width=dp(40),
            height=dp(40)
        )

        # AI text
        ai_text = Label(
            text="Get AI Productivity Insights",
            font_size=sp(18),
            color=(1, 1, 1, 1),
            halign='left',
            bold=True
        )

        # Right arrow
        arrow_icon = Label(
            text="> > >",
            font_size=sp(20),
            size_hint_x=None,
            width=dp(50),
            color=(1, 1, 1, 1),
        )

        ai_card.add_widget(ai_icon)
        ai_card.add_widget(ai_text)
        ai_card.add_widget(arrow_icon)

        # Make the whole card clickable
        ai_card.bind(on_touch_down=lambda instance, touch: self.goto_ai_features() if instance.collide_point(
            *touch.pos) else False)

        self.main_layout.add_widget(ai_card)

        # "Track Your App Usage" heading
        heading_container = BoxLayout(size_hint_y=None, height=50, padding=(12, 8))
        with heading_container.canvas.before:
            Color(0.93, 0.85, 0.77, 1)
            heading_container.bg = RoundedRectangle(radius=[12], pos=heading_container.pos, size=heading_container.size)
        heading_container.bind(
            pos=lambda *x: setattr(heading_container.bg, "pos", heading_container.pos),
            size=lambda *x: setattr(heading_container.bg, "size", heading_container.size)
        )
        heading_label = Label(
            text="Track Your App Usage",
            font_size=20,
            bold=True,
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle"
        )
        heading_container.add_widget(heading_label)
        self.main_layout.add_widget(heading_container)

        # --- Scrollable app list ---
        self.scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        app_list_container = BoxLayout(orientation="vertical", size_hint_y=None, spacing=12)
        app_list_container.bind(minimum_height=app_list_container.setter('height'))

        for app in self.usage_data["apps"]:
            app_list_container.add_widget(self.create_app_card(app["icon"], app["name"], app["time"], app["progress"]))

        self.scroll.add_widget(app_list_container)
        self.main_layout.add_widget(self.scroll)

        # --- Hamburger button (image-based) ---
        self.menu_button = Button(
            size_hint=(None, None),
            size=(80, 80),
            background_normal='icons/hamburger.png',
            background_down='icons/hamburger_pressed.png',
            background_color=[1, 1, 1, 1],
            pos_hint={"top": 1, "x": 0}
        )
        self.menu_button.bind(on_release=self.toggle_drawer)
        self.root_layout.add_widget(self.menu_button)

        # --- Notification button ---
        self.notification_button = Button(
            size_hint=(None, None),
            size=(60, 60),
            background_normal='icons/notification.png',  # You'll need an icon file for this
            background_down='icons/notification_pressed.png',
            background_color=[1, 1, 1, 1],
            pos_hint={"top": 1, "right": 1},
        )
        self.notification_button.bind(on_release=lambda x: App.get_running_app().go_to_notifications())
        self.root_layout.add_widget(self.notification_button)

        # --- Drawer ---
        self.drawer = BoxLayout(
            orientation="vertical",
            size_hint=(None, 1),
            width=self.drawer_width,
            pos=(-self.drawer_width, 0),
            padding=[10, 20, 10, 10],
            spacing=5
        )

        with self.drawer.canvas.before:
            Color(1, 1, 1, 1)
            self.drawer_bg = Rectangle(pos=self.drawer.pos, size=self.drawer.size)
        self.drawer.bind(
            pos=lambda *x: setattr(self.drawer_bg, "pos", self.drawer.pos),
            size=lambda *x: setattr(self.drawer_bg, "size", self.drawer.size)
        )

        # --- Drawer header with profile ---
        user_profile_header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=140,
            padding=10,
            spacing=5
        )

        # --- Profile Image ---
        self.profile_image_button = CircularProfileButton(
            source="icons/profile.png",
            size_hint=(None, None),
            size=(80, 80),
            pos_hint={'center_x': 0.5}
        )

        # --- User name label (keep reference so it can be updated) ---
        self.user_name_label = Label(
            text="[b]Hi, User![/b]",
            markup=True,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=30,
            color=[0.1, 0.1, 0.1, 1]
        )
        self.user_name_label.bind(
            size=lambda instance, value: setattr(instance, 'text_size', value)
        )

        # Add widgets into header
        user_profile_header.add_widget(Widget())  # Spacer
        user_profile_header.add_widget(self.profile_image_button)
        user_profile_header.add_widget(self.user_name_label)

        # Add header to drawer
        self.drawer.add_widget(user_profile_header)

        # --- Drawer buttons ---
        options = ["Profile", "Settings", "Logout"]
        for opt in options:
            btn = DWDrawerButton(text=opt)

            # Bind button to switch screen
            if opt == "Profile":
                btn.bind(on_release=lambda x: self.switch_to_screen("profile"))
            elif opt == "Settings":
                btn.bind(on_release=lambda x: self.switch_to_screen("settings"))
            elif opt == "Logout":
                btn.bind(on_release=self.logout)  # example logout method

            self.drawer.add_widget(btn)

        # Add spacer to push buttons to top under header
        self.drawer.add_widget(Widget())
        self.root_layout.add_widget(self.drawer)

        # --- Overlay (dynamic, added only when drawer opens) ---
        self.overlay = Widget(size_hint=(1, 1))
        with self.overlay.canvas:
            Color(0, 0, 0, 0.4)
            self.overlay_rect = Rectangle(pos=self.overlay.pos, size=self.overlay.size)
        self.overlay.bind(
            pos=lambda *x: setattr(self.overlay_rect, "pos", self.overlay.pos),
            size=lambda *x: setattr(self.overlay_rect, "size", self.overlay.size)
        )
        self.overlay.opacity = 0
        self.overlay.disabled = True
        self.overlay.bind(on_touch_down=self.on_overlay_touch)

        # --- Hamburger button (image-based) ---
        self.menu_button = Button(
            size_hint=(None, None),
            size=(80, 80),
            background_normal='icons/hamburger.png',
            background_down='icons/hamburger_pressed.png',
            background_color=[1, 1, 1, 1],
            pos_hint={"top": 1, "x": 0}
        )
        self.menu_button.bind(on_release=self.toggle_drawer)
        self.root_layout.add_widget(self.menu_button)

    def logout(self, instance):
        """Handles logout action."""
        from kivy.app import App
        app = App.get_running_app()
        # You can implement logout logic here
        # For now, just print and exit
        print("User logged out")
        self.manager.current = 'login'

    def switch_to_screen(self, screen_name):
        """Switches the main ScreenManager to the requested screen."""
        from kivy.app import App
        app = App.get_running_app()
        app.root.current = screen_name  # Switch to the target screen
        # Close the drawer
        if self.drawer_open:
            self.toggle_drawer()

    # --- New methods for profile picture ---
    def open_file_chooser(self, instance):
        """Opens the file chooser to select a new profile picture."""
        from plyer import filechooser
        filechooser.open_file(on_selection=self.update_profile_picture, filters=["*.*"])

    def update_profile_picture(self, selection):
        if selection:
            selected_file_path = selection[0]
            # This calls the reload() method on the nested Image widget
            self.profile_image_button.image.source = selected_file_path
            self.profile_image_button.image.reload()

    def create_app_card(self, icon, name, time, progress):
        container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=70,
            padding=8
        )
        with container.canvas.before:
            Color(0.92, 0.96, 1, 1)
            container.bg = RoundedRectangle(radius=[20], pos=container.pos, size=container.size)
        container.bind(
            pos=lambda *x: setattr(container.bg, "pos", container.pos),
            size=lambda *x: setattr(container.bg, "size", container.size)
        )
        container.add_widget(AppItem(icon, name, time, progress))
        return container

    def toggle_drawer(self, *args):
        if not self.drawer_open:
            self.root_layout.add_widget(self.overlay)
            self.root_layout.remove_widget(self.drawer)
            self.root_layout.add_widget(self.drawer)

            anim = Animation(x=0, duration=0.3, t='out_quad')
            anim.start(self.drawer)

            self.overlay.opacity = 1
            self.overlay.disabled = False
        else:
            anim = Animation(x=-self.drawer_width, duration=0.3, t='out_quad')
            anim.start(self.drawer)

            self.overlay.opacity = 0
            self.overlay.disabled = True
            self.root_layout.remove_widget(self.overlay)

        self.drawer_open = not self.drawer_open

    def on_overlay_touch(self, instance, touch):
        if not self.overlay.disabled:
            self.toggle_drawer()
            return True
        return False

    def get_usage_data(self):
        return {
            "screen_time": "3h 45m",
            "most_used": "YouTube - 2h 30m",
            "pickups": 47,
            "notifications": 120,
            "apps": [
                {"icon": "icons/youtube.png", "name": "YouTube", "time": "2h 30m", "progress": 80},
                {"icon": "icons/whatsapp.png", "name": "WhatsApp", "time": "1h 10m", "progress": 50},
                {"icon": "icons/instagram.png", "name": "Instagram", "time": "45m", "progress": 30},
                {"icon": "icons/chrome.png", "name": "Chrome", "time": "25m", "progress": 15},
                {"icon": "icons/facebook.png", "name": "Facebook", "time": "1h 45m", "progress": 60},
                {"icon": "icons/tiktok.png", "name": "TikTok", "time": "1h 20m", "progress": 55},
                {"icon": "icons/twitter.png", "name": "Twitter", "time": "35m", "progress": 20},
                {"icon": "icons/snapchat.png", "name": "Snapchat", "time": "50m", "progress": 25},
                {"icon": "icons/netflix.png", "name": "Netflix", "time": "2h 5m", "progress": 70}
            ]
        }
    # ➡️ Add the new on_pre_enter method here
    def on_pre_enter(self, *args):
        # Load profile image on startup
        if os.path.exists(PROFILE_IMAGE_FILE):
            try:
                with open(PROFILE_IMAGE_FILE, "r") as f:
                    data = json.load(f)
                    image_path = data.get("path")
                    if image_path and os.path.exists(image_path):
                        if hasattr(self, 'profile_image_button'):
                            self.profile_image_button.image.source = image_path
            except (IOError, json.JSONDecodeError):
                pass

        # Load user name on startup (existing logic)
        app = App.get_running_app()
        if hasattr(app, 'user_email') and app.user_email:
            # Use a thread to fetch Firebase data without freezing the UI
            threading.Thread(target=self.load_profile_name, args=(app.user_email,)).start()
        else:
            print("User email not found on startup.")

    # ➡️ Add the new load_profile_name method here
    def load_profile_name(self, email):
        try:
            profile = get_profile(email)
            if profile and "name" in profile:
                name = profile["name"]
                Clock.schedule_once(
                    lambda dt: setattr(self.user_name_label, 'text', f"[b]Hi, {name}![/b]"),
                    0
                )
        except Exception as e:
            print(f"Error loading profile name: {e}")

    def goto_ai_features(self, *args):
        """Navigate to AI features screen"""
        if hasattr(self, 'manager') and self.manager:
            # Add AI screen if it doesn't exist
            if 'ai_features' not in self.manager.screen_names:
                self.manager.add_widget(AIFeaturesScreen(name='ai_features'))

            # Navigate to the screen
            self.manager.current = 'ai_features'

# --- Profile Screen ---
class ProfileScreen(Screen):
    """Profile page where user can edit personal information and profile image."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # --- Scrollable root layout ---
        self.scroll = ScrollView()
        self.root_layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=20,
            padding=20
        )
        self.root_layout.bind(minimum_height=self.root_layout.setter('height'))
        self.scroll.add_widget(self.root_layout)
        self.add_widget(self.scroll)

        # --- Profile Image at top ---
        self.profile_image_button = CircularProfileButton(
            source="icons/profile.png",
            size=(80, 80),
            pos_hint={"center_x": 0.5}
        )
        self.root_layout.add_widget(self.profile_image_button)

        # --- User Information Fields ---
        self.inputs = {}

        # Get email from app/session (replace with your app’s actual attribute)
        app = App.get_running_app()
        user_email = getattr(app, "user_email", None)

        fields = [
            {"hint": "Name", "password": False, "input_filter": None, "default": "", "max_length": 30},
            {"hint": "Mobile Number", "password": False, "input_filter": "int", "default": "", "max_length": 15},
            {"hint": "Age", "password": False, "input_filter": "int", "default": "", "max_length": 3},
            {"hint": "Hobby", "password": False, "input_filter": None, "default": "", "max_length": 100},
        ]

        for field in fields:
            bi = BorderedInput(
                hint_text=field["hint"],
                password=field["password"]
            )
            if field.get("input_filter"):
                bi.input.input_filter = field["input_filter"]
            if field.get("default"):
                bi.input.text = field["default"]
            if field.get("readonly"):
                bi.input.readonly = True  # prevent editing email

            # Apply character limit
            max_len = field.get("max_length", 100)
            bi.input.bind(text=self.limit_text(max_len))

            self.inputs[field["hint"]] = bi
            self.root_layout.add_widget(bi)

        # --- Save Button ---
        self.save_btn = DWButton(text="Save", primary=True)
        self.save_btn.bind(on_release=self.save_profile)
        self.root_layout.add_widget(self.save_btn)

    def limit_text(self, max_len):
        """Returns a callback that enforces max length on TextInput."""
        def _limit(instance, value):
            if len(value) > max_len:
                instance.text = value[:max_len]
        return _limit

    # --- Load profile when entering screen ---
    def on_pre_enter(self, *args):
        app = App.get_running_app()
        user_email = getattr(app, "user_email", None)

        if user_email:
            profile = get_profile(user_email)
            if profile:
                self.inputs["Name"].input.text = profile.get("name", "")
                self.inputs["Mobile Number"].input.text = profile.get("mobile", "")
                self.inputs["Age"].input.text = profile.get("age", "")
                self.inputs["Hobby"].input.text = profile.get("hobby", "")

            # ➡️ Add this code block to load the profile image
        if os.path.exists(PROFILE_IMAGE_FILE):
            try:
                with open(PROFILE_IMAGE_FILE, "r") as f:
                    data = json.load(f)
                    image_path = data.get("path")
                    if image_path and os.path.exists(image_path):
                        # Correctly set the source on the nested Image widget
                        self.profile_image_button.image.source = image_path
            except (IOError, json.JSONDecodeError):
                pass

    # --- Save profile and return to dashboard ---
    def save_profile(self, instance):
        # Retrieve input values
        name = self.inputs["Name"].input.text
        mobile = self.inputs["Mobile Number"].input.text
        age = self.inputs["Age"].input.text
        hobby = self.inputs["Hobby"].input.text

        app = App.get_running_app()
        user_email = getattr(app, "user_email", None)
        print(f"Attempting to save profile for email: {user_email}")

        if user_email:
            # ✅ Call Firebase helper
            save_profile_to_firebase(user_email, name, mobile, age, hobby)
            print(f"✅ Profile saved for {user_email}: {name}, {mobile}, {age}, {hobby}")
            # ➡️ Add this code to save the image path
            profile_image_path = self.profile_image_button.image.source
            with open(PROFILE_IMAGE_FILE, "w") as f:
                json.dump({"path": profile_image_path}, f)
        else:
            print("❌ User email is not available. Cannot save profile.")

        # --- Update drawer label in Dashboard ---
        dashboard_screen = app.root.get_screen("dashboard")
        if hasattr(dashboard_screen, "user_name_label") and name:
            dashboard_screen.user_name_label.text = f"[b]Hi, {name}![/b]"

        # --- Update profile image in dashboard ---
        if hasattr(dashboard_screen, "profile_image_button"):
            dashboard_screen.profile_image_button.image.source = self.profile_image_button.image.source

        # Return to Dashboard
        app.root.current = "dashboard"


class LoginScreen(Screen):
    show_password = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[24, 32, 24, 16], spacing=8)
        layout.add_widget(Widget(size_hint_y=None, height=16))

        logo_box = BoxLayout(orientation='vertical', size_hint_y=None, height=350, spacing=0)
        logo_box.add_widget(Image(source="logo.png", size_hint_y=None, height=300))
        logo_box.add_widget(
            DWLabel(text=APP_NAME, font_size=36, color=PRIMARY_BLUE, halign='center', valign='middle', size_hint_y=None,
                    height=52, bold=True))
        layout.add_widget(logo_box)

        layout.add_widget(
            DWLabel(text=APP_TAGLINE, font_size=20, halign='center', valign='middle', color=App.get_running_app().get_current_theme()["text"], size_hint_y=None,
                    height=32, bold=True))

        self.email_input = BorderedInput(hint_text="Email")
        self.password_input = BorderedInput(hint_text="Password", password=True)
        pw_box = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=48)
        pw_box.add_widget(self.password_input)
        self.show_pw_btn = DWButton(text="Show", primary=False, width=68, size_hint_x=None,
                                    on_press=self.toggle_password)
        pw_box.add_widget(self.show_pw_btn)

        forgot_pw_btn = DWButton(text="Forgot Password?", primary=False, on_press=self.goto_forgot_password)
        forgot_pw_btn.size_hint_y = None
        forgot_pw_btn.height = 36
        forgot_pw_btn.font_size = 14

        self.remember_me_checkbox = CheckBox(active=False, size_hint=(None, None), size=(24, 24), color=PRIMARY_BLUE)
        remember_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=32)
        remember_layout.add_widget(self.remember_me_checkbox)
        remember_layout.add_widget(
            DWLabel(text="Remember Me", font_size=15, color=App.get_running_app().get_current_theme()["text"], size_hint_x=None, width=110,
                    halign="left"))

        self.message_label = DWLabel(text="", color=[1, 0, 0, 1], font_size=15, size_hint_y=None, height=24)

        login_button = DWButton(text="Log In", on_press=self.login_user)
        google_button = DWButton(text="Continue with Google", primary=False, on_press=self.start_google_sign_in)
        signup_button = DWButton(text="Don't have an account? Sign up", primary=False, on_press=self.goto_signup)

        layout.add_widget(self.email_input)
        layout.add_widget(pw_box)
        layout.add_widget(remember_layout)
        layout.add_widget(login_button)
        layout.add_widget(forgot_pw_btn)
        layout.add_widget(google_button)
        layout.add_widget(signup_button)
        layout.add_widget(self.message_label)
        layout.add_widget(Widget(size_hint_y=None, height=12))
        self.add_widget(layout)
        self.load_remembered_info()

        self.email_input.set_next_input(self.password_input)
        self.password_input.set_next_input(self.email_input.input)  # or to login_button if needed

    def start_google_sign_in(self, instance):
        self.message_label.text = "Opening browser for Google Sign-In..."
        self.message_label.color = PRIMARY_BLUE

        thread = threading.Thread(target=self.google_sign_in_thread)
        thread.daemon = True
        thread.start()

    def google_sign_in_thread(self):
        try:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_CLIENT_SECRETS_FILE,
                scopes=['openid', 'email', 'profile']
            )
            creds = flow.run_local_server(port=0)
            google_id_token = creds.id_token
            firebase_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={FIREBASE_API_KEY}"
            payload = {
                "postBody": f"id_token={google_id_token}&providerId=google.com",
                "requestUri": "http://localhost",
                "returnIdpCredential": True,
                "returnSecureToken": True
            }
            resp = requests.post(firebase_api_url, json=payload)
            data = resp.json()
            if "idToken" in data:
                Clock.schedule_once(lambda dt: self.update_ui_on_success(), 0)
            else:
                error_msg = data.get("error", {}).get("message", "Unknown error")
                Clock.schedule_once(lambda dt: self.update_ui_on_failure(error_msg), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_ui_on_failure(str(e)), 0)

    def update_ui_on_success(self, *args):
        self.message_label.text = "Google login successful!"
        self.message_label.color = [0, 0.7, 0, 1]
        Clock.schedule_once(lambda dt: self.goto_dashboard(), 0.5)

    def update_ui_on_failure(self, error_msg, *args):
        self.message_label.text = f"Google login failed: {error_msg}"
        self.message_label.color = [1, 0, 0, 1]

    def toggle_password(self, instance):
        self.show_password = not self.show_password
        self.password_input.input.password = not self.show_password
        self.show_pw_btn.text = "Hide" if self.show_password else "Show"
        self.show_pw_btn.focus = False

    def login_user(self, instance):
        email = self.email_input.input.text.strip()
        password = self.password_input.input.text.strip()
        self.message_label.text = ""

        if not is_valid_email(email):
            self.message_label.text = "Invalid email format"
            self.message_label.color = [1, 0, 0, 1]
            self.email_input.input.background_color = [1, 0.93, 0.93, 1]
            return
        else:
            self.email_input.input.background_color = [0, 0, 0, 0]

        if not password:
            self.message_label.text = "Please enter email and password"
            self.message_label.color = [1, 0, 0, 1]
            return

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        response = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
        data = response.json()
        if "idToken" in data:
            self.message_label.text = ""
            self.message_label.color = [0, 0.7, 0, 1]
            App.get_running_app().user_email = email

            if self.remember_me_checkbox.active:
                App.get_running_app().save_user_credentials(email, password)
            else:
                App.get_running_app().clear_remembered_info()

            Clock.schedule_once(lambda dt: self.goto_dashboard(), 0.5)
        else:
            error_msg = data.get("error", {}).get("message", "Unknown error")
            if "INVALID_PASSWORD" in error_msg:
                self.message_label.text = "Login Failed. Please check your password."
            elif "EMAIL_NOT_FOUND" in error_msg:
                self.message_label.text = "Account not found. Please check your email or create an account."
            elif "USER_DISABLED" in error_msg:
                self.message_label.text = "This account has been disabled. Please contact support."
            elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error_msg:
                self.message_label.text = "Too many failed attempts. Please try again later."
            elif "INVALID_EMAIL" in error_msg:
                self.message_label.text = "Invalid email format. Please check your email address."
            elif "INVALID_LOGIN_CREDENTIALS" in error_msg:
                self.message_label.text = "Login Failed. Please check your email and password."
            else:
                self.message_label.text = "Login failed. Please check your credentials and try again."
            self.message_label.color = [1, 0, 0, 1]

    def goto_signup(self, instance):
        App.get_running_app().root.current = "signup"
        self.message_label.text = ""
        self.email_input.input.background_color = [0, 0, 0, 0]

    def goto_forgot_password(self, instance):
        App.get_running_app().root.current = "forgot_password"
        self.message_label.text = ""

    def goto_dashboard(self, dt=None):
        App.get_running_app().root.current = "dashboard"

    def load_remembered_info(self):
        if os.path.exists(REMEMBER_ME_FILE):
            try:
                with open(REMEMBER_ME_FILE, "r") as f:
                    data = json.load(f)
                    email = data.get("email", "")
                    password = data.get("password", "")
                    if email:
                        self.email_input.input.text = email
                        self.remember_me_checkbox.active = True
                    if password:
                        self.password_input.input.text = password
            except (IOError, json.JSONDecodeError):
                pass

class ForgotPasswordScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[24, 32, 24, 16], spacing=8)
        layout.add_widget(Widget(size_hint_y=None, height=16))

        logo_box = BoxLayout(orientation='vertical', size_hint_y=None, height=350, spacing=0)
        logo_box.add_widget(Image(source="logo.png", size_hint_y=None, height=300))
        logo_box.add_widget(
            DWLabel(text="Forgot Password?", font_size=20, halign='center', valign='middle', color=DARK_TEXT,
                    size_hint_y=None, height=32, bold=True))
        layout.add_widget(logo_box)

        layout.add_widget(
            DWLabel(text="Enter your email to receive a password reset link.", font_size=15, halign='center',
                    valign='middle', color=DARK_TEXT, size_hint_y=None, height=32))

        self.email_input = BorderedInput(hint_text="Email")
        self.message_label = DWLabel(text="", color=[1, 0, 0, 1], font_size=15, size_hint_y=None, height=24)

        reset_button = DWButton(text="Send Reset Link", on_press=self.reset_password)
        back_to_login_button = DWButton(text="Back to Login", primary=False, on_press=self.goto_login)

        layout.add_widget(self.email_input)
        layout.add_widget(reset_button)
        layout.add_widget(back_to_login_button)
        layout.add_widget(self.message_label)
        layout.add_widget(Widget(size_hint_y=None, height=12))
        self.add_widget(layout)

        self.email_input.set_next_input(self.email_input)
        reset_button.focus = False  # Buttons aren't keyboard navigable by default

    def reset_password(self, instance):
        email = self.email_input.input.text.strip()
        self.message_label.text = ""

        if not is_valid_email(email):
            self.message_label.text = "Invalid email format"
            self.message_label.color = [1, 0, 0, 1]
            return

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_API_KEY}"
        payload = {
            "requestType": "PASSWORD_RESET",
            "email": email
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            data = response.json()

            if response.status_code == 200:
                self.message_label.text = "A password reset link has been sent to your email."
                self.message_label.color = [0, 0.7, 0, 1]
                self.email_input.input.text = ""
            else:
                error_msg = data.get("error", {}).get("message", "Unknown error")
                if "EMAIL_NOT_FOUND" in error_msg:
                    self.message_label.text = "Email not found. Please check the address."
                elif "INVALID_EMAIL" in error_msg:
                    self.message_label.text = "Invalid email address."
                else:
                    self.message_label.text = f"Failed to send reset link: {error_msg}"
                self.message_label.color = [1, 0, 0, 1]
        except requests.exceptions.RequestException as e:
            self.message_label.text = f"Connection error. Please try again later."
            self.message_label.color = [1, 0, 0, 1]
            print(f"Connection error: {e}")

    def goto_login(self, instance):
        self.manager.current = "login"
        self.message_label.text = ""
        self.email_input.input.text = ""

class SignupScreen(Screen):
    show_password = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[24, 32, 24, 16], spacing=8)
        layout.add_widget(Widget(size_hint_y=None, height=16))

        logo_box = BoxLayout(orientation='vertical', size_hint_y=None, height=350, spacing=0)
        logo_box.add_widget(Image(source="logo.png", size_hint_y=None, height=300))
        logo_box.add_widget(
            DWLabel(text=APP_NAME, font_size=36, color=PRIMARY_BLUE, halign='center', valign='middle', size_hint_y=None,
                    height=52, bold=True))
        layout.add_widget(logo_box)

        layout.add_widget(
            DWLabel(text="Create a new account", font_size=20, halign='center', valign='middle', color=DARK_TEXT,
                    size_hint_y=None, height=32, bold=True))

        self.email_input = BorderedInput(hint_text="Email")
        self.password_input = BorderedInput(hint_text="Password", password=True)
        pw_box = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=48)
        pw_box.add_widget(self.password_input)
        self.show_pw_btn = DWButton(text="Show", primary=False, width=68, size_hint_x=None,
                                    on_press=self.toggle_password)
        pw_box.add_widget(self.show_pw_btn)

        checklist_box = BoxLayout(orientation='vertical', padding=[10, 6, 10, 6], spacing=1, size_hint_y=None,
                                  height=140)
        self.pw_checklist_heading = DWLabel(
            text="[b]Password must contain:[/b]",
            markup=True,
            font_size=15, color=[0.45, 0.45, 0.45, 1], size_hint_y=None, height=26, halign="left"
        )
        self.pw_checklist_label = DWLabel(
            text="",
            markup=True,
            font_size=14,
            size_hint_y=None,
            height=110,
            halign="left",
            valign="top"
        )
        checklist_box.add_widget(self.pw_checklist_heading)
        checklist_box.add_widget(self.pw_checklist_label)

        self.password_input.input.bind(text=self.update_password_checklist)
        self.message_label = DWLabel(text="", color=[1, 0, 0, 1], font_size=15, size_hint_y=None, height=24)

        create_account_button = DWButton(text="Create Account", on_press=self.create_account)
        back_to_login_button = DWButton(text="Back to Login", primary=False, on_press=self.goto_login)

        layout.add_widget(self.email_input)
        layout.add_widget(pw_box)
        layout.add_widget(checklist_box)
        layout.add_widget(create_account_button)
        layout.add_widget(back_to_login_button)
        layout.add_widget(self.message_label)
        layout.add_widget(Widget(size_hint_y=None, height=12))
        self.add_widget(layout)
        self.update_password_checklist(self.password_input.input, "")

        self.email_input.set_next_input(self.password_input)
        self.password_input.set_next_input(self.email_input.input)  # or to create_account_button if needed

    def update_password_checklist(self, instance, value):
        pw = self.password_input.input.text
        reqs = password_conditions(pw)
        checklist_lines = []
        for label, met in reqs.items():
            mark = "[color=00c853]✓[/color]" if met else "[color=ea4335]×[/color]"
            color = "00c853" if met else "ea4335"
            checklist_lines.append(f"    {mark} [color={color}]{label}[/color]")
        self.pw_checklist_label.text = "\n".join(checklist_lines)
        self.password_input.input.background_color = [0, 0, 0, 0]

    def toggle_password(self, instance):
        self.show_password = not self.show_password
        self.password_input.input.password = not self.show_password
        self.show_pw_btn.text = "Hide" if self.show_password else "Show"
        self.show_pw_btn.focus = False

    def create_account(self, instance):
        email = self.email_input.input.text.strip()
        password = self.password_input.input.text.strip()
        self.message_label.text = ""

        if not is_valid_email(email):
            self.message_label.text = "Invalid email format"
            self.message_label.color = [1, 0, 0, 1]
            self.email_input.input.background_color = [1, 0.93, 0.93, 1]
            return
        else:
            self.email_input.input.background_color = [0, 0, 0, 0]

        reqs = password_conditions(password)
        if not all(reqs.values()):
            self.message_label.text = "Password does not meet requirements"
            self.message_label.color = [1, 0, 0, 1]
            self.password_input.input.background_color = [1, 0.93, 0.93, 1]
            return
        else:
            self.password_input.input.background_color = [0, 0, 0, 0]

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
        response = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
        data = response.json()
        if "idToken" in data:
            self.message_label.text = "Account created successfully! Redirecting to login..."
            self.message_label.color = [0, 0.7, 0, 1]
            Clock.schedule_once(lambda dt: self.goto_login(instance), 1.5)
        else:
            error_msg = data.get("error", {}).get("message", "Unknown error")

            if "EMAIL_EXISTS" in error_msg:
                self.message_label.text = "An account with this email already exists. Please login instead."
            elif "WEAK_PASSWORD" in error_msg:
                self.message_label.text = "Password is too weak. Please choose a stronger password."
            elif "INVALID_EMAIL" in error_msg:
                self.message_label.text = "Invalid email format. Please check your email address."
            else:
                self.message_label.text = "Account creation failed. Please try again."

            self.message_label.color = [1, 0, 0, 1]

    def goto_login(self, instance):
        self.manager.current = "login"
        self.message_label.text = ""
        self.email_input.input.background_color = [0, 0, 0, 0]
        self.password_input.input.background_color = [0, 0, 0, 0]
        self.update_password_checklist(self.password_input.input, "")


class SettingsScreen(Screen):
    """
    Settings page with improved theming support, robust touch handling,
    and reliable divider drawing.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # App reference and current theme
        self.app = App.get_running_app()
        self.current_theme = self.app.get_current_theme()
        self.theme_widgets = []  # Track widgets for theme updates

        # Main UI
        self.create_scroll_view()
        self.create_header()
        self.create_settings_list()
        self.load_settings()

    def create_scroll_view(self):
        """Main scrollable container"""
        self.scroll_view = ScrollView()
        self.root_layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=[dp(15), dp(10), dp(15), dp(10)],
            spacing=dp(5)
        )
        self.root_layout.bind(minimum_height=self.root_layout.setter('height'))
        self.scroll_view.add_widget(self.root_layout)
        self.add_widget(self.scroll_view)

    def create_header(self):
        """Header with back button and title"""
        header_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            padding=[dp(15), 0]
        )

        back_button = Button(
            text="< Back",
            size_hint_x=None,
            width=dp(80),
            background_color=(0, 0, 0, 0),
            color=(0, 0.7, 1, 1),
            bold=True
        )
        back_button.bind(on_release=lambda x: self.go_back_to_dashboard())
        header_layout.add_widget(back_button)
        header_layout.add_widget(Widget(size_hint_x=1))  # Spacer
        self.root_layout.add_widget(header_layout)

        title_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            padding=[dp(15), 0]
        )
        self.title_label = Label(
            text="Settings",
            font_size=sp(24),
            bold=True,
            halign="left",
            valign="middle",
            size_hint_x=None,
            width=Window.width - dp(30),  # Account for padding
            text_size=(Window.width - dp(30), None),  # Account for padding
            color=self.current_theme["text"]
        )
        self.theme_widgets.append(self.title_label)
        title_layout.add_widget(self.title_label)
        self.root_layout.add_widget(title_layout)

        self.add_divider()

    def create_settings_list(self):
        """Create list-style settings items"""
        self.create_setting_item("Dark Mode", "switch", self.app.is_dark_theme, self.on_theme_toggle)
        self.add_divider()

        self.create_setting_item("Enable Notifications", "switch", True, self.on_notifications_toggle)
        self.add_divider()

        self.create_setting_item("Tip Frequency", "value", "Every 4 hours", self.show_tip_frequency_options)
        self.add_divider()

        self.create_setting_item("About This App", "value", "»»»»", self.open_about_popup)
        self.add_divider()

        self.create_setting_item("Clear App Data", "button", None, self.confirm_clear_data)

    def create_setting_item(self, title, item_type, value=None, action=None):
        """Create a list-style setting item"""
        item_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            padding=[dp(15), 0]
        )

        title_label = Label(
            text=title,
            font_size=sp(18),
            size_hint_x=0.6,  # full width
            halign="left",
            valign="middle",
            text_size=(Window.width * 0.5, None),  # subtract scroll padding + control width
            color=self.current_theme["text"]
        )

        # Make text_size always match the label width
        title_label.bind(
            width=lambda instance, value: setattr(instance, 'text_size', (value, None))
        )

        self.theme_widgets.append(title_label)

        control_layout = BoxLayout(
            orientation="horizontal",
            size_hint_x=None,
            spacing=dp(5)
        )

        if item_type == "switch":
            control_layout.add_widget(Widget(size_hint_x=1))
            switch = Switch(active=value, size_hint_x=None, width=dp(60))
            switch.bind(active=action)
            if title == "Dark Mode":
                self.theme_switch = switch
            elif title == "Enable Notifications":
                self.notifications_switch = switch
            control_layout.add_widget(switch)

        elif item_type == "value":
            value_label = Label(
                text=str(value),
                font_size=sp(16),
                color=self.current_theme.get("accent", (0.2, 0.6, 1, 1)),
                halign="right",  # Change this from "left" to "right"
                valign="middle",
                size_hint_x=1
            )
            # Make sure text_size updates on width change
            value_label.bind(width=lambda instance, w: setattr(instance, 'text_size', (w, None)))
            self.theme_widgets.append(value_label)
            self.tip_value_label = value_label

            # Create a layout to hold the label and the transparent button
            control_container = RelativeLayout(size_hint=(1, 1))

            # Add the value label to the container
            control_container.add_widget(value_label)

            # Add a fully transparent button on top of the label to handle touch events
            btn = Button(
                size_hint=(1, 1),
                background_color=(0, 0, 0, 0),
                on_release=action
            )
            control_container.add_widget(btn)

            control_layout.add_widget(control_container)

            # Add a spacer to push the label to the right

        elif item_type == "button":
            # Add a spacer to push the button to the right (KEEP THIS)
            control_layout.add_widget(Widget(size_hint_x=1))
            button = Button(
                text="Clear",
                size_hint_x=None,  # Set size_hint_x to None
                width=dp(90),  # Set a fixed width similar to the switch
                size_hint_y=None,  # Set size_hint_y to None
                height=dp(35),  # Set a fixed height similar to the switch
                background_color=(1, 0.2, 0.2, 1),
                color=(1, 1, 1, 1),
                font_size=sp(14)
            )
            if action:
                button.bind(on_release=action)
            control_layout.add_widget(button)

        item_layout.add_widget(title_label)
        item_layout.add_widget(control_layout)
        self.root_layout.add_widget(item_layout)

    def show_tip_frequency_options(self, *args):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        title = Label(text='Tip Reminder Frequency', font_size=sp(20), bold=True,
                      size_hint_y=None, height=dp(40), halign='left', valign='middle')
        title.bind(width=lambda instance, w: setattr(instance, 'text_size', (w, None)))
        content.add_widget(title)

        # Safe current value
        current_text = getattr(self, 'tip_value_label', None)
        if current_text:
            current_text = self.tip_value_label.text
        else:
            current_text = "Every 4 hours"

        try:
            current_value = int(current_text.replace("Every", "").replace("hours", "").strip())
        except:
            current_value = 4

        value_display = Label(
            text=f"Every {current_value} hours",
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle',
            color=self.current_theme["text"]
        )
        value_display.bind(width=lambda instance, w: setattr(instance, 'text_size', (w, None)))
        content.add_widget(value_display)

        slider = Slider(min=1, max=12, value=current_value, step=1, size_hint_y=None, height=dp(40))
        slider.bind(value=lambda instance, val: setattr(value_display, 'text', f"Every {int(val)} hours"))
        content.add_widget(slider)

        # Buttons
        button_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        cancel_btn = Button(text="Cancel", background_color=(0.8, 0.8, 0.8, 1))
        save_btn = Button(text="Save", background_color=self.current_theme.get("accent", (0.2, 0.6, 1, 1)))
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(save_btn)
        content.add_widget(button_layout)

        popup = Popup(title='', content=content, size_hint=(0.8, 0.5), auto_dismiss=False)
        cancel_btn.bind(on_release=popup.dismiss)

        def save_value(instance):
            if hasattr(self, 'tip_value_label'):
                self.tip_value_label.text = value_display.text
            if hasattr(self.app, 'user_data'):
                try:
                    hours = int(value_display.text.replace("Every", "").replace("hours", "").strip())
                except:
                    hours = 4
                self.app.user_data['tip_frequency'] = hours
            popup.dismiss()

        save_btn.bind(on_release=save_value)
        popup.open()

    def add_divider(self):
        """Add a thin divider line"""
        divider = BoxLayout(size_hint_y=None, height=dp(1))
        with divider.canvas.before:
            Color(*self.current_theme.get("divider", (0.9, 0.9, 0.9, 1)))
            divider.line = Line(points=[divider.x, divider.y, divider.x + divider.width, divider.y], width=1)
        divider.bind(pos=self.update_divider, size=self.update_divider)
        self.root_layout.add_widget(divider)

    def update_divider(self, instance, value):
        """Update divider points reliably"""
        if hasattr(instance, 'line'):
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(*self.current_theme.get("divider", (0.9, 0.9, 0.9, 1)))
                instance.line = Line(points=[instance.x, instance.y, instance.x + instance.width, instance.y], width=1)

    def on_theme_toggle(self, instance, value):
        """Toggle dark mode and update theme"""
        self.app.is_dark_theme = value
        self.app.update_app_theme()
        self.update_theme()

    def on_notifications_toggle(self, instance, value):
        """Toggle notifications"""
        if hasattr(self.app, 'user_data'):
            self.app.user_data['notifications_enabled'] = value

    def open_about_popup(self, instance):
        """Creates and opens a neat 'About' popup."""

        # Layout container for popup content
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Title
        title = Label(
            text='About This App',
            font_size=sp(22),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            halign="center",
            valign="middle"
        )
        title.bind(width=lambda inst, w: setattr(inst, "text_size", (w, None)))
        content.add_widget(title)

        # Scrollable description
        scroll = ScrollView(size_hint=(1, 1))
        about_text = Label(
            text=("This application is designed to help users improve their digital wellbeing.\n\n"
                  "It provides features such as reminders, usage tracking, and helpful tips "
                  "to encourage healthier interaction with technology.\n\n"
                  "Version: 1.0\n"
                  "Developed with Python and Kivy."),
            font_size=sp(16),
            halign="left",
            valign="top",
            text_size=(Window.width * 0.7, None),
            size_hint_y=None
        )
        about_text.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1]))
        scroll.add_widget(about_text)
        content.add_widget(scroll)

        # Close button
        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        content.add_widget(close_btn)

        # Popup
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.85, 0.6),
            auto_dismiss=False
        )
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def load_settings(self):
        """Load saved settings"""
        if hasattr(self.app, 'user_data'):
            if 'notifications_enabled' in self.app.user_data and hasattr(self, 'notifications_switch'):
                self.notifications_switch.active = self.app.user_data['notifications_enabled']

            if 'tip_frequency' in self.app.user_data and hasattr(self, 'tip_value_label'):
                freq = self.app.user_data['tip_frequency']
                self.tip_value_label.text = f"Every {freq} hours"

    def go_back_to_dashboard(self):
        self.manager.current = "dashboard"

    def confirm_clear_data(self, instance):
        popup_layout = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(10))
        popup_layout.add_widget(Label(
            text="Are you sure you want to clear all data? This cannot be undone.",
            halign="center",
            color=(0, 0.7, 1, 1),
            text_size = (dp(280), None)
        ))

        button_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(48))
        cancel_btn = Button(text="Cancel", size_hint_x=0.5, background_color=(0.8, 0.8, 0.8, 1))
        confirm_btn = Button(text="Confirm", size_hint_x=0.5, background_color=(1, 0.2, 0.2, 1))

        popup = Popup(title="Clear Data", content=popup_layout, size_hint=(0.8, 0.4), auto_dismiss=False)
        cancel_btn.bind(on_release=popup.dismiss)
        confirm_btn.bind(on_release=lambda x: self.clear_data(popup))

        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(confirm_btn)
        popup_layout.add_widget(button_layout)
        popup.open()

    def clear_data(self, popup):
        if hasattr(self, 'notifications_switch'):
            self.notifications_switch.active = True
        if hasattr(self, 'theme_switch'):
            self.theme_switch.active = False
        if hasattr(self, 'tip_value_label'):
            self.tip_value_label.text = "Every 4 hours"

        if hasattr(self.app, 'user_data'):
            self.app.user_data.clear()

        popup.dismiss()

    def update_theme(self, *args):
        """Apply current theme to widgets"""
        self.current_theme = self.app.get_current_theme()
        for widget in self.theme_widgets:
            if widget:
                widget.color = self.current_theme["text"]

    def on_pre_enter(self, *args):
        if hasattr(self, 'theme_switch'):
            self.theme_switch.active = self.app.is_dark_theme
        self.load_settings()
        self.update_theme()


class NotificationScreen(Screen):
    def __init__(self, usage_data=None, **kwargs):
        super().__init__(**kwargs)
        self.usage_data = usage_data or {}
        self.build_ui()

    def build_ui(self):
        """Constructs the UI for the notification screen."""
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # --- Header with back button as text ---
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))

        # Back button using text, transparent background
        back_button = Button(
            text="< Back",
            size_hint_x=None,
            width=dp(80),
            background_color=(0, 0, 0, 0),  # transparent
            color=(0, 0.7, 1, 1),  # blue text
            bold=True
        )
        back_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'dashboard'))

        # Title label
        title_label = Label(
            text='Notifications',
            font_size=sp(24),
            bold=True,
            color=(0, 0.7, 1, 1),
            size_hint_x=1
        )

        # Add widgets with optional spacer for alignment
        header_layout.add_widget(back_button)
        header_layout.add_widget(title_label)
        header_layout.add_widget(Widget(size_hint_x=0.2))  # optional spacer to balance layout

        # Add header to main layout
        main_layout.add_widget(header_layout)

        # Horizontal line below header
        line = Widget(size_hint_y=None, height=dp(1))
        with line.canvas:
            Color(0.8, 0.8, 0.8, 1)
            RoundedRectangle(pos=line.pos, size=(Window.width, dp(1)))
        main_layout.add_widget(line)

        # --- Notification List ---
        scroll_view = ScrollView(size_hint=(1, 1))
        self.notification_list_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(10),
            padding=[dp(5), dp(10)]
        )
        self.notification_list_layout.bind(minimum_height=self.notification_list_layout.setter('height'))

        scroll_view.add_widget(self.notification_list_layout)
        main_layout.add_widget(scroll_view)
        self.add_widget(main_layout)

    def go_back(self, instance):
        """Navigate back to the dashboard screen."""
        if self.manager and 'dashboard' in self.manager.screen_names:
            self.manager.current = 'dashboard'

    def on_pre_enter(self):
        """Called each time the screen is about to be shown."""
        self.update_notification_list()

    def get_notifications(self):
        """Generates a list of notification dictionaries based on the current self.usage_data."""
        if platform in ("win", "linux", "macosx"):
            return self.get_dummy_notifications()
        else:
            return self.get_real_notifications()

    def get_dummy_notifications(self):
        """Creates realistic notifications based on the dashboard usage data."""
        notifs = []

        if not self.usage_data:
            return [{
                "title": "Welcome to Digital Wellness!",
                "message": "Start using your phone to see personalized insights here.",
                "unread": True
            }]

        # Screen time notification
        screen_time = self.usage_data.get("screen_time", "0h")
        notifs.append({
            "title": "Screen Time Summary",
            "message": f"You spent {screen_time} on your phone today.",
            "unread": True
        })

        # Pickups notification
        pickups = self.usage_data.get("pickups", 0)
        notifs.append({
            "title": "Phone Pickups",
            "message": f"You picked up your phone {pickups} times today.",
            "unread": True
        })

        # Notifications count
        notifications_count = self.usage_data.get("notifications", 0)
        notifs.append({
            "title": "Notifications Received",
            "message": f"You received {notifications_count} notifications today.",
            "unread": False
        })

        # Most used app notification
        most_used = self.usage_data.get("most_used", "No app")
        notifs.append({
            "title": "Most Used App",
            "message": f"Your most used app was {most_used}.",
            "unread": False
        })

        # App usage notifications (top 3 apps)
        if "apps" in self.usage_data:
            top_apps = sorted(
                self.usage_data["apps"],
                key=lambda x: self._time_to_minutes(x["time"]),
                reverse=True
            )[:3]

            for i, app in enumerate(top_apps):
                rank = ["1st", "2nd", "3rd"][i]
                notifs.append({
                    "title": f"{rank} Most Used App",
                    "message": f"You spent {app['time']} on {app['name']} today.",
                    "unread": i == 0  # Mark only the top app as unread
                })

        # Usage pattern notification
        total_minutes = self._get_total_screen_time_minutes()
        if total_minutes > 240:  # More than 4 hours
            notifs.append({
                "title": "High Usage Alert",
                "message": "You've spent more than 4 hours on your phone today.",
                "unread": True
            })
        elif total_minutes < 60:  # Less than 1 hour
            notifs.append({
                "title": "Low Usage",
                "message": "You've had minimal screen time today. Great job!",
                "unread": False
            })

        # Return notifications with the most recent first
        return notifs

    def _time_to_minutes(self, time_str):
        """Helper function to convert time string (e.g., '2h 30m') to minutes."""
        if 'h' in time_str and 'm' in time_str:
            hours, minutes = time_str.split('h ')
            hours = int(hours)
            minutes = int(minutes.replace('m', ''))
            return hours * 60 + minutes
        elif 'h' in time_str:
            return int(time_str.replace('h', '')) * 60
        elif 'm' in time_str:
            return int(time_str.replace('m', ''))
        return 0

    def _get_total_screen_time_minutes(self):
        """Calculate total screen time in minutes from screen_time string."""
        screen_time = self.usage_data.get("screen_time", "0h 0m")
        return self._time_to_minutes(screen_time)

    def get_real_notifications(self):
        """Placeholder for real notifications on mobile platforms."""
        return [{
            "title": "System",
            "message": "Real notifications will appear here on mobile.",
            "unread": True
        }]

    def update_notification_list(self):
        """Clears existing widgets and populates the list with new notifications."""
        self.notification_list_layout.clear_widgets()
        notifications_to_display = self.get_notifications()

        if not notifications_to_display:
            empty_label = Label(
                text='No new notifications',
                halign='center',
                valign='middle',
                color=(0.5, 0.5, 0.5, 1),
                font_size=sp(16),
                size_hint_y=None,
                height=dp(40)
            )
            self.notification_list_layout.add_widget(empty_label)
            return

        for notif in notifications_to_display:
            self.create_notification_item(notif)

    def create_notification_item(self, notif):
        """Creates a single visual notification item from a dictionary."""
        # Main container for each notification
        item_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(90),
            padding=dp(15)
        )

        with item_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            item_layout.bg = RoundedRectangle(
                pos=item_layout.pos,
                size=item_layout.size,
                radius=[dp(10)]
            )

        item_layout.bind(
            pos=lambda inst, val: setattr(inst.bg, 'pos', val),
            size=lambda inst, val: setattr(inst.bg, 'size', val)
        )

        # Text container (takes full width now)
        text_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(2)
        )

        title_label = Label(
            text=notif['title'],
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(26),
            text_size=(280, None),  # FIX: Let text size be calculated automatically
            bold=True,
            font_size=sp(16)
        )

        message_label = Label(
            text=notif['message'],
            halign='left',
            valign='top',
            color=(0.4, 0.4, 0.4, 1),
            font_size=sp(14),
            size_hint_y=None,
            height=dp(44),
            text_size=(280, None)  # FIX: Let text size be calculated automatically
        )

        text_layout.add_widget(title_label)
        text_layout.add_widget(message_label)
        item_layout.add_widget(text_layout)

        # Unread dot (positioned to the right)
        if notif.get('unread', False):
            unread_dot = Widget(
                size_hint=(None, None),
                size=(dp(12), dp(12)),
                pos_hint={'right': 0.95, 'center_y': 0.5}
            )
            with unread_dot.canvas:
                Color(0.2, 0.6, 1, 1)
                unread_dot.dot = Ellipse(pos=unread_dot.pos, size=unread_dot.size)

            unread_dot.bind(
                pos=lambda inst, val: setattr(inst.dot, 'pos', val),
                size=lambda inst, val: setattr(inst.dot, 'size', val)
            )
            item_layout.add_widget(unread_dot)

        # FIX: Bind to update text sizing after layout is complete
        def update_text_size(instance, value):
            available_width = instance.width - dp(30)  # Account for padding
            title_label.text_size = (available_width, None)
            message_label.text_size = (available_width, None)

        item_layout.bind(width=update_text_size)
        item_layout.bind(height=update_text_size)

        self.notification_list_layout.add_widget(item_layout)

class DigitalWellbeingApp(App):
    is_dark_theme = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_dark_theme = False
        self.user_email = None
        self.bg_color = None
        self.rect = None

    def get_current_theme(self):
        if self.is_dark_theme:
            return {
                "bg": (0.1, 0.1, 0.1, 1),
                "text": (1, 1, 1, 1),
                "button": (0.2, 0.2, 0.2, 1),
                "divider": (0.5, 0.5, 0.5, 1)
            }
        else:
            return {
                "bg": (1, 1, 1, 1),
                "text": (0, 0, 0, 1),
                "button": (0.9, 0.9, 0.9, 1),
                "divider": (0.8, 0.8, 0.8, 1)
            }

    def save_theme_preference(self, is_dark):
        try:
            with open("theme_preference.json", "w") as f:
                json.dump({"is_dark_theme": is_dark}, f)
        except Exception as e:
            print(f"Failed to save theme: {e}")

    def update_app_theme(self):
        current_theme = self.get_current_theme()
        if self.bg_color:
            self.bg_color.rgba = current_theme["bg"]
        for screen in self.root.screens:
            if hasattr(screen, 'update_theme'):
                screen.update_theme()

    def toggle_dark_theme(self, switch, value):
        self.is_dark_theme = value

    def on_is_dark_theme(self, instance, value):
        current_theme = self.get_current_theme()
        if self.bg_color:
            self.bg_color.rgba = current_theme["bg"]
        self.save_theme_preference(value)

    def build(self):
        # --- LOAD SAVED THEME PREFERENCE ---
        try:
            with open("theme_preference.json", "r") as f:
                data = json.load(f)
                self.is_dark_theme = data.get("is_dark_theme", False)
        except FileNotFoundError:
            self.is_dark_theme = False
        except Exception as e:
            print(f"Failed to load theme: {e}")
            self.is_dark_theme = False

        # Create the ScreenManager instance and apply the canvas
        sm = ScreenManager(transition=SlideTransition(direction='left', duration=0.2))
        current_theme = self.get_current_theme()
        with sm.canvas.before:
            self.bg_color = Color(*current_theme["bg"])
            self.rect = RoundedRectangle(size=sm.size, pos=sm.pos, radius=[0])
        sm.bind(size=self._update_rect, pos=self._update_rect)

        # ➕ Correctly create and add screen instances
        dashboard_screen = DashboardScreen(name="dashboard")
        notification_screen = NotificationScreen(name="notification")
        profile_screen = ProfileScreen(name="profile")
        settings_screen = SettingsScreen(name="settings")

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(ForgotPasswordScreen(name="forgot_password"))
        sm.add_widget(dashboard_screen)
        sm.add_widget(notification_screen)
        sm.add_widget(profile_screen)
        sm.add_widget(settings_screen)
        sm.add_widget(AIFeaturesScreen(name="ai_features"))

        # 🎨 Apply initial theme
        Clock.schedule_once(lambda dt: self.apply_theme(), 0)

        # App title
        self.title = APP_NAME

        # 📌 Load remembered login (if exists)
        if os.path.exists(REMEMBER_ME_FILE):
            try:
                with open(REMEMBER_ME_FILE, "r") as f:
                    data = json.load(f)
                    email = data.get("email")
                    if email:
                        self.user_email = email
                        # Pass the correctly defined dashboard_screen instance
                        threading.Thread(target=self.load_profile_name, args=(email, dashboard_screen)).start()
            except (IOError, json.JSONDecodeError):
                pass

        return sm

    def _update_rect(self, instance, value):
        if self.rect:
            self.rect.pos = instance.pos
            self.rect.size = instance.size

    def load_profile_name(self, email, dashboard_screen):
        try:
            profile = get_profile(email)
            if profile and "name" in profile:
                name = profile["name"]
                Clock.schedule_once(
                    lambda dt: setattr(dashboard_screen.user_name_label, 'text', f"[b]Hi, {name}![/b]"),
                    0
                )
        except Exception as e:
            print(f"Error loading profile name: {e}")

    def apply_theme(self):
        def _do_update(dt):
            current_theme = self.get_current_theme()
            if self.bg_color:
                self.bg_color.rgba = current_theme["bg"]
        Clock.schedule_once(_do_update, 0)

    def on_start(self):
        if self.root:
            self.root.current = "login"

    def save_user_credentials(self, email, password):
        with open(REMEMBER_ME_FILE, "w") as f:
            json.dump({"email": email, "password": password}, f)
        print("User credentials saved successfully.")

    def clear_remembered_info(self):
        if os.path.exists(REMEMBER_ME_FILE):
            os.remove(REMEMBER_ME_FILE)
            print("Remembered user info cleared.")

    def go_to_notifications(self):
        """
        Updates the NotificationScreen with the latest data and navigates to it.
        This method is called from the DashboardScreen's notification button.
        """
        dashboard_screen = self.root.get_screen("dashboard")
        notification_screen = self.root.get_screen("notification")

        # Update the notifications with the latest data
        notification_screen.usage_data = dashboard_screen.get_usage_data()
        notification_screen.update_notification_list()

        # Navigate to the screen
        self.root.current = "notification"

if __name__ == "__main__":
    DigitalWellbeingApp().run()
