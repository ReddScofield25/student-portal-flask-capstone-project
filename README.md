# Students' Portal Web Application

A Flask web application for registering and managing students, built as my capstone project for the **Startocode Backend Python Developer** course.

Users can register a student through a validated form with a photo upload, browse all students in a table, filter and search the list, view a full student record, and update admission status without a page reload.

## Features

- Student registration form with server-side validation (including email validation)
- Passport photo upload, saved to `static/uploads/` with the filename stored in the database
- Students list with search and filtering
- Student detail page showing the full record
- Dependent State → LGA dropdowns, populated asynchronously with `fetch()` from JSON endpoints
- Asynchronous admission status update (`admitted` / `undecided` / `rejected`), validated server-side
- MySQL database for persistent storage

## Tech Stack

- **Backend:** Python, Flask, Flask-MySQLdb
- **Database:** MySQL
- **Frontend:** Jinja2 templates, HTML, CSS, JavaScript (`fetch` API)
- **Libraries:** email-validator, Werkzeug, python-dotenv

## Project Structure

```
student-portal/
├── app.py                  # Flask application (routes, validation, DB logic)
├── requirements.txt
├── schema.sql              # Database and table definitions
├── .env.example            # Template for environment variables
├── templates/              # Jinja2 templates
├── static/
│   ├── css/
│   ├── js/                 # locations.js, status.js
│   ├── img/
│   ├── data/               # states-lgas.json
│   └── uploads/            # Uploaded student photos
└── docs/
    └── BACKEND_CONTRACT.md # Route specification this project implements
```

## Routes

| Endpoint | Method | Purpose |
|---|---|---|
| `/` (`home`) | GET | Landing page |
| `/portal` (`portal`) | GET | Registration form |
| `/save_student` (`save_student`) | POST | Validate and save a student, then redirect to the list |
| `/students` (`students`) | GET | List, search and filter students |
| `/student/<id>` (`student_detail`) | GET | Single student record |
| `/update_status` (`update_status`) | POST | Async status change, returns JSON |
| `/api/states` | GET | List of states (JSON) |
| `/api/lgas/<state>` | GET | LGAs for a state (JSON) |

See [`docs/BACKEND_CONTRACT.md`](docs/BACKEND_CONTRACT.md) for the full specification.

## Setup and Installation

### 1. Prerequisites

- Python 3.8+
- MySQL Server
- On Ubuntu, the system libraries required by `flask-mysqldb`:

```bash
sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config
```

### 2. Clone and create a virtual environment

```bash
git clone https://github.com/reddscofield25/[repo-name].git
cd [repo-name]
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up the database

```bash
mysql -u [your_mysql_user] -p < schema.sql
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your own MySQL credentials and a secret key:

```
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=student_portal
SECRET_KEY=change-me
```

### 5. Run the application

```bash
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## What I Built

The HTML, CSS and JavaScript scaffolding were provided by Startocode as a starter kit. My work covers:

- All Flask routes and the backend logic behind them
- MySQL database design and queries
- Form validation and image upload handling
- The search/filter query and persistent status updates
- The two asynchronous `fetch()` features (State → LGA dropdowns and status change)

## Acknowledgements

- Front-end templates, styling and project brief: **Startocode** starter kit
- Course pathway: Startocode Backend Python Developer, accessed through the One Million Coders programme

## Author

**Maxwell Asare Gyamfi** ([@reddscofield25](https://github.com/reddscofield25))
