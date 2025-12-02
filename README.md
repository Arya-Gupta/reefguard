# ReefGuard - Coral Reef Monitoring & Restoration Platform
<img width="1000" height="400" alt="Gemini_Generated_Image_sxw3vesxw3vesxw3" src="https://github.com/user-attachments/assets/8451b044-6c2f-4d0d-8e97-9cf330e2270c" />


ReefGuard is a Django-based web application for monitoring and protecting coral reefs worldwide. The platform enables researchers, students, and conservationists to track reef health, report pollution incidents, share coral sightings, and contribute to global reef conservation efforts.
## 📖 About The Project

**ReefGuard** is a Django-based web application designed to monitor and protect coral reefs worldwide. The platform enables researchers, students, and conservationists to track reef health, report pollution incidents, share coral sightings, and contribute to global reef conservation efforts.

[cite_start]Our goal is to raise awareness and highlight coral restoration efforts through an interactive and community-driven platform[cite: 16].

## 🌏 Problem & Motivation

Coral reefs are vital to our planet's health, yet they are under severe threat.
**Biodiversity:** While covering less than 1% of the ocean floor, reefs support approximately 25% of all marine life.
**Climate Balance:** They help balance Earth’s climate by producing oxygen and absorbing CO₂.
**Economic & Coastal Value:** Reefs generate billions in fisheries and tourism and protect coastlines from storms.
**The Crisis:** Over 50% of shallow corals have been lost in the past 30 years due to warming seas, pollution, overfishing, and cyclones.

## 🚀 Key Features

* **Reef Health Tracking:** Monitor vital statistics of reef ecosystems.
* **Pollution Reporting:** A system for users to report and geolocate pollution incidents.
* **Community Sightings:** Share and view coral sightings from divers and researchers.
* **User Accounts:** Secure authentication for researchers and general users.
* **Interactive Dashboard:** Data visualization for reef metrics.

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite (Development) / PostgreSQL (Production)

## 👥 Meet the Team (Group 17)

[cite_start]This project was developed by **Group 17**[cite: 2]:

* **Aleena Ali Azeem**
* **Arya Gupta**
* **Gurleen Kaur**
* **Mehakpreet Kaur**
* **Simranpreet Kaur**
  
## Features

### Core Functionality
- **Reef Database**: Comprehensive information on coral reefs worldwide with health status tracking
- **Event Monitoring**: Track pollution reports, coral sightings, bleaching events, and restoration activities
- **Article System**: Educational content about reef conservation and research
- **Media Gallery**: Upload and browse photos and videos of coral reefs
- **User Roles**: Admin, Researcher, and Student roles with appropriate permissions

### Key Features
- **Search & Filter**: Filter reefs by region, health status, and search events by type, severity, and year
- **Forms**: Report pollution, submit coral sightings, and contact the team
- **Authentication**: Complete user management with registration, login, and password recovery
- **Session Tracking**: Tracks viewed reefs and user filter preferences
- **Responsive Design**: Bootstrap-based responsive interface
- **File Uploads**: Support for photos and videos

## Technology Stack

- **Backend**: Python 3.x, Django 4.2+
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Database**: SQLite (easily switchable to PostgreSQL/MySQL)
- **IDE**: PyCharm (recommended)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- PyCharm IDE (recommended)

## Installation & Setup

### 1. Clone or Extract the Project

```bash
cd /path/to/ReefGuard
```

### 2. Create a Virtual Environment

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Load Initial Data (Fixtures)

```bash
python manage.py loaddata core/fixtures/initial_data.json
```

This loads sample data including:
- 6 coral reefs (Great Barrier Reef, Belize Barrier Reef, etc.)
- 5 educational articles about coral conservation

### 6. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

### 8. Access the Admin Panel

Navigate to `http://127.0.0.1:8000/admin/` and login with your superuser credentials.

## Project Structure

<img width="400" height="400" alt="ChatGPT Image Dec 1, 2025, 12_50_50 AM" src="https://github.com/user-attachments/assets/24eba22e-8bf6-4eb5-9204-8bfd4e4f8244" />

## Usage Guide

### User Registration
1. Click **Register** in the navigation bar
2. Fill in your details and select your role (Student, Researcher, or Admin)
3. Submit the form and login with your credentials

### Exploring Reefs
1. Navigate to **Reefs** from the main menu
2. Use filters to search by region or health status
3. Click on any reef to view detailed information

### Reporting Events
1. Login to your account
2. Select **Report > Pollution** or **Report > Coral Sighting** from the menu
3. Fill in the form with event details
4. Submit to add your report to the system

### Uploading Media
1. Login to your account
2. Go to **Report > Upload Media**
3. Select the media type (photo/video), add details, and upload your file
4. Optionally link the media to a specific reef or event

### Viewing Articles
1. Click **Articles** in the navigation
2. Filter by category (Education, Research, News, Conservation, Restoration)
3. Click any article to read the full content

## Admin Functions

Access the admin panel at `/admin/` to:
- Manage users and assign roles
- Add, edit, or delete reefs
- Moderate event reports
- Publish and feature articles
- Manage gallery items
- View system statistics

## Database Models

### CustomUser
- Extended Django user with role field (Admin, Researcher, Student)
- Additional fields: bio, organization

### Reef
- Name, region, country, coordinates
- Area, depth, health status
- Timestamps and creator tracking

### Event
- Types: Pollution, Sighting, Bleaching, Restoration, Monitoring, Damage
- Severity levels, dates, status
- Links to reefs and reporters

### Article
- Categories: Education, Research, News, Conservation, Restoration
- Publishing and featuring options
- Author attribution

### ImageGallery
- Photo and video uploads
- Links to reefs and events
- User attribution

## Session & Cookie Features

The application tracks:
- Last 10 viewed reefs (stored in session)
- User filter preferences (region, health status, etc.)
- User authentication state
- Session expiry: 2 weeks

## Security Notes

**For Production Deployment:**
1. Change `SECRET_KEY` in settings.py
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Use a production database (PostgreSQL recommended)
5. Set up proper media file serving (e.g., S3, CDN)
6. Configure email backend for password recovery
7. Enable HTTPS
8. Review and update security settings

---

**ReefGuard** - Protecting Our Oceans, One Reef at a Time 🌊


