# Project-PEAMS
# Professional Events Attendance Management System

A web-based attendance tracking system that allows organizers to manage events, register participants, and monitor attendance with QR code support.

---

## a. Introduction

### Background
Managing event attendance manually through paper-based sign-up sheets is inefficient, error-prone, and difficult to maintain over time. Organizations and academic institutions frequently struggle with tracking who attended which events, following up with absentees, and generating accurate attendance reports. This project addresses those challenges by providing a digital, database-driven solution.

### Problem Statement
The system aims to solve the following problems:
- Lack of a centralized platform for managing event information and attendance records
- Difficulty in tracking participant registration and check-in status across multiple events
- Absence of a reliable and searchable database for attendee information
- Inefficiency of manual attendance sheets that are prone to loss and human error

### Scope
The system covers the following:
- Creation, editing, and deletion of events by authorized users
- Registration and management of attendees
- Recording and updating of attendance status per event
- QR code generation for each registered attendee per event
- Basic reporting of attendance statistics

The system does **not** cover:
- Real-time QR code scanning via camera
- Email or SMS notifications to attendees
- Payment or ticketing functionality

### Target Users
- **Organizers/Admins** — Users who log in to the system to create and manage events and monitor attendance
- **Attendees** — Individuals who are registered into the system by organizers and whose attendance is tracked

---

## b. Project Objectives

### Primary Objective
To develop a functional web-based Events Attendance Management System using Python (Flask) and MySQL that enables organizers to efficiently manage events, register attendees, and track attendance.

### Secondary Objectives
- Implement full CRUD (Create, Read, Update, Delete) operations for all entities
- Establish a normalized relational database with at least 3 related tables
- Provide a user-friendly interface built with Bootstrap for ease of navigation
- Implement user authentication to restrict access to authorized organizers only
- Generate QR codes for attendee registrations to support faster check-in processes
- Enable search functionality for attendees and events

---

## c. Business Rules

### Detailed Business Logic
- Only registered users (organizers) can log into the system and manage data
- Passwords are stored securely using hashing
- An organizer can create, edit, and delete events they manage
- Each event must have a unique name, a valid date, and a location
- Attendees are registered globally and can be linked to multiple events via registrations
- Each attendee can only be registered once per event (no duplicate registrations)
- Attendance status can be set to `registered`, `present`, or `absent`
- A unique QR code is generated for each registration record
- Check-in time is recorded when an attendee's status is updated to `present`

### Constraints
- `email` in the `attendees` table must be unique
- `username` in the `users` table must be unique
- A registration entry must reference a valid `event_id` and `attendee_id`
- Deleting a user cascades to delete their associated events
- Deleting an event or attendee cascades to remove related registration records

### Conditions
- A user must be logged in to access any management feature
- Session expires upon logout or browser close
- Attendance status defaults to `registered` upon creation
- QR code field must be unique across all registrations

---

## d. Database Models

### Entity Relationship Diagram (ERD)
![ERD](docs/diagrams/erd.png)

The ERD illustrates the following entities and relationships:
- **users** — stores organizer accounts
- **events** — stores event details; linked to users (one user manages many events)
- **attendees** — stores participant information
- **registrations** — bridge table linking attendees to events; tracks attendance status and QR code

### Relational Model
![Relational Model](docs/diagrams/rm.png)

| Table         | Attributes                                                                 |
|---------------|----------------------------------------------------------------------------|
| users         | user_id (PK), username, password                                           |
| events        | event_id (PK), user_id (FK), event_name, event_date, location, description |
| attendees     | attendee_id (PK), fullname, email, contact_no, address                     |
| registrations | registration_id (PK), attendee_id (FK), event_id (FK), attendance_status, registration_date, qr_code |

---

## e. Project Overview

### Architecture
The application follows the **MVC (Model-View-Controller)** design pattern:
- **Model** — `database.py` handles all database connections and SQL queries
- **View** — HTML templates (Jinja2 + Bootstrap) handle the user interface
- **Controller** — `app.py` contains Flask routes that process requests and return responses

### Key Components
- `app.py` — Main Flask application; defines all routes and session handling
- `database.py` — Database helper functions for executing queries
- `templates/` — Jinja2 HTML templates organized by feature (events, attendees, registrations)
- `database/schema.sql` — SQL script to create all tables
- `database/initial_data.sql` — SQL script to populate tables with sample data
- `docs/diagrams/` — ERD and Relational Model diagrams

---

## f. Setup Instructions

### Prerequisites
- Python 3.x
- XAMPP (includes MySQL and phpMyAdmin)
- Git
- Web browser (Chrome or Firefox recommended)

### Step-by-Step Installation

**1. Clone the repository**
```bash
git clone https://github.com/kellysldo/Project-PEAM.git
cd Project-PEAM
```

**2. Set up a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Start XAMPP**
- Open XAMPP Control Panel
- Start **Apache** and **MySQL**

**5. Configure and import the database**
- Open your browser and go to `http://localhost/phpmyadmin`
- Create a new database named `CCCS105`
- Click **Import** → select `database/schema.sql` → click **Go**
- Click **Import** again → select `database/initial_data.sql` → click **Go**

**6. Set environment variables**

Create a `.env` file in the root directory:
```
SECRET_KEY=your_secret_key_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=CCCS105
```

**7. Run the application**
```bash
python app.py
```

**8. Access the application**

Open your browser and go to:
```
http://localhost:5000
```

---

## g. Team Members & Roles

| Name                    | Role                        | Responsibilities                                              |
|-------------------------|-----------------------------|---------------------------------------------------------------|
| Kelly Saldo             | Fullstack Developer         | Flask routes, database connection, CRUD logic, authentication, HTML templates,  Bootstrap layout |
| Micabelle Allison Nomo  | Frontend Developer          | HTML templates, CSS styling, Bootstrap layout, UI design, testing      |
| Rizelyn Joy Borbe       | Backend Developer, Database & Documentation    | ERD, relational model, SQL schema, initial data, README, testing, Flask routes, database connection |

---

## h. Dependencies

### Python Packages
| Package              | Version  | Purpose                          |
|----------------------|----------|----------------------------------|
| Flask                | 3.0.x    | Web framework                    |
| mysql-connector-python | 8.x.x  | MySQL database connectivity      |
| qrcode               | 7.x.x    | QR code generation               |
| Pillow               | 10.x.x   | Image processing for QR codes    |
| python-dotenv        | 1.x.x    | Environment variable management  |

### System Requirements
- OS: Windows 10/11, macOS 12+, or Ubuntu 20.04+
- Python: 3.8 or higher
- MySQL: 8.0 (via XAMPP)
- Browser: Chrome 110+, Firefox 110+, or Edge 110+

---

## i. Running Instructions

### Starting the Application
1. Open XAMPP → Start **Apache** and **MySQL**
2. Activate virtual environment:
```bash
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
```
3. Run the app:
```bash
python app.py
```
4. Open browser → go to `http://localhost:5000`

### Default Login Credentials
| Username | Password  |
|----------|-----------|
| admin    | admin123  |

### Stopping the Application
- Press `Ctrl + C` in the Terminal to stop the Flask server
- Stop Apache and MySQL in XAMPP Control Panel

### Navigating the Application
- **Dashboard** — Overview of events and recent registrations
- **Events** — View, add, edit, and delete events
- **Attendees** — View, add, edit, and delete attendees
- **Registrations** — Register attendees to events, update attendance status, view QR codes
- **Logout** — End the current session
