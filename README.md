# Digital Wellbeing App: A Python-Based Screen Time Manager

## 🖥️ Project Overview

The **Digital Wellbeing App** is a cross-platform application built with Python and Kivy, designed to help users monitor and improve their relationship with technology. It provides insightful analytics on device usage, sends personalized notifications about digital habits, and offers productivity tips—all through an intuitive, themeable interface.

The application addresses modern concerns about screen time and productivity by turning raw usage data into actionable insights, promoting a more mindful and balanced digital lifestyle.

---

## ✨ Key Features

*   **🔐 Multi-User Authentication:** Secure login and registration system powered by **Firebase Authentication**, supporting email/password and "Remember Me" functionality.
*   **📊 Interactive Dashboard:** A central hub displaying key metrics: total screen time, most-used apps, phone pickups, and notification counts with visual progress indicators.
*   **🔔 Smart Notification System:** Generates context-aware alerts based on usage patterns (e.g., high usage warnings, top app summaries, and daily screen time recaps).
*   **🎨 Dynamic Theme Engine:** Seamless switching between Light and Dark modes. User preference is saved locally and applied across all app screens.
*   **👤 User Profile Management:** Users can update personal information, and upload a profile picture which is stored locally and synced with Firebase.
*   **🤖 Productivity Insights:** A dedicated module that generates random, helpful tips for digital wellbeing and simulated productivity analytics based on user patterns.
*   **⚙️ Customizable Settings:** Granular control over app behavior, including notification toggles, tip frequency, and an option to clear all local app data.
*   **🧠 Modular & Scalable Architecture:** Built using Kivy's `ScreenManager` for smooth navigation. The code is structured for easy maintenance and future feature addition.

---

## 🛠️ Tech Stack & Implementation

*   **Core Language:** Python
*   **GUI Framework:** Kivy (for cross-platform compatibility)
*   **Backend Services:** Firebase (Authentication, Realtime Database for user profiles)
*   **Local Storage:** JSON files (for user preferences, theme settings, and local profile data)
*   **Key Python Libraries:**
    *   `requests` for HTTP calls to Firebase REST API
    *   `plyer` for accessing system-level features (file chooser)
    *   `threading` for running background tasks without freezing the UI
    *   `json` and `os` for local data management
*   **Development Tools:** Git, GitHub
*   **Key Concepts Applied:** Computational Thinking (Decomposition, Abstraction, Algorithmic Thinking), Object-Oriented Programming (OOP), Event-Driven Programming.

---

## 🧩 Application Architecture

The app follows a modular, screen-based architecture:
```
Main App (DigitalWellbeingApp)
    |
    |--- ScreenManager
        |
        |--- LoginScreen
        |--- SignupScreen
        |--- ForgotPasswordScreen
        |--- DashboardScreen (Main Hub)
        |--- ProfileScreen
        |--- SettingsScreen
        |--- NotificationScreen
        |--- AIFeaturesScreen
```
*   **State Management:** Global states (like theme and user session) are managed at the app level.
*   **Data Flow:** User credentials and profile data are authenticated and fetched from Firebase. All other preferences (theme, notifications) are stored locally in JSON files for fast access and offline capability.
*   **UI Components:** Custom reusable widgets (buttons, input fields, cards) ensure a consistent and responsive user interface across different screen sizes.

---

## 🚀 Getting Started (For Developers)

### Prerequisites
*   Python 3.7 or higher
*   Pip (Python package manager)

### Installation & Setup
1.  **Clone the repository**
    ```bash
    git clone https://github.com/SirajLuqman/digital-wellbeing-app.git
    cd digital-wellbeing-app
    ```

2.  **Create and activate a virtual environment (Recommended)**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install required dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Typical requirements: `kivy`, `requests`, `plyer`)*

4.  **Configure Firebase**
    *   Create a project in the [Firebase Console](https://console.firebase.google.com/).
    *   Enable **Email/Password** authentication.
    *   Create a **Realtime Database**.
    *   Locate your project's Web API Key and Database URL.
    *   In the app's source code (e.g., a config file), replace the placeholder Firebase configuration variables with your actual keys:
        ```python
        FIREBASE_API_KEY = "YOUR_WEB_API_KEY"
        FIREBASE_DB_URL = "YOUR_DATABASE_URL"
        ```

5.  **Run the Application**
    ```bash
    python main.py
    ```

---

## 📁 Project Structure (Abridged)
```
Digital-Wellbeing-App/
├── main.py                    # Application entry point
├── requirements.txt           # Project dependencies
├── assets/                    # Images, icons, and fonts
├── data/                      # Local JSON storage files
│   ├── theme_preference.json
│   ├── user_preferences.json
│   └── profile_image.json
└── screens/                   # Kivy Screen classes for each module
    ├── login.py
    ├── dashboard.py
    ├── profile.py
    └── ...
```

---

## 📄 License & Acknowledgments

This project was developed as an academic assignment for the **Fundamental of Computational Thinking: Python** course. The design and concept are inspired by the growing need for digital wellness tools.

**References:**
*   Kivy Framework Documentation: [https://kivy.org/doc/stable/](https://kivy.org/doc/stable/)
*   Firebase Documentation: [https://firebase.google.com/docs](https://firebase.google.com/docs)
*   Twenge, J. M. (2019). *iGen: Why Today’s Super-Connected Kids Are Growing Up Less Rebellious, More Tolerant, Less Happy—and Completely Unprepared for Adulthood.* Atria Books.
