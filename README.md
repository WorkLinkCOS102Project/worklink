# WorkLink

A desktop job board application built with Python and Tkinter, backed by a PostgreSQL database. Employers can post jobs and review applicants; job seekers can browse listings, apply, and discover learning resources for in-demand skills.

---

## Features

**Employers**
- Register and log in to a dedicated employer portal
- Post jobs with a title, description, required skills (multi-select), and experience level
- View all posted listings and drill into applicants for each role

**Job Seekers**
- Register with a multi-select skill profile
- Browse all available jobs with live search filtering
- Apply to roles in one click
- Track submitted applications
- Access a curated **Learn Skills** directory with free and paid resources for all 30 supported skills

**Shared**
- Purple-accented dark UI built entirely in Tkinter — no web browser required
- PostgreSQL connection pooling via `psycopg2`
- Schema auto-bootstrapped on first run (no manual SQL needed)

---

## Project Structure

```
worklink/
├── __init__.py        # Package marker
├── db.py              # Connection pool, DSN builder, schema bootstrap
├── data_manager.py    # All database queries (no file I/O)
├── styles.py          # Design tokens: colours, fonts, spacing, button styles, skill data
├── widgets.py         # Reusable Tkinter widgets (avatar, badge, card, stat_card, etc.)
├── job_browsing.py    # EmployeeDashboard tab widget (Browse Jobs + My Applications)
└── main.py            # App entry point, all screen functions, MultiSkillSelector widget
```

---

## Requirements

- Python 3.10 or higher
- PostgreSQL 13 or higher
- `psycopg2` Python package

Install the Python dependency:

```bash
pip install psycopg2-binary
```

---

## Database Setup

1. Make sure PostgreSQL is running on your machine.

2. Create the database:

```sql
CREATE DATABASE worklink;
```

3. That's it — WorkLink creates all three tables automatically on first launch using `CREATE TABLE IF NOT EXISTS`.

The three tables created are:
- `users` — stores both employers and employees
- `jobs` — job listings linked to an employer
- `applications` — many-to-many between jobs and employees (unique per pair)

---

## Configuration

By default the app connects with these values:

| Setting  | Default     |
|----------|-------------|
| Host     | `localhost` |
| Port     | `5432`      |
| Database | `worklink`  |
| User     | `postgres`  |
| Password | `COS101`    |

To override any of these without editing code, set environment variables before running:

```bash
# Linux / macOS
export WORKLINK_DB_HOST=localhost
export WORKLINK_DB_PORT=5432
export WORKLINK_DB_NAME=worklink
export WORKLINK_DB_USER=postgres
export WORKLINK_DB_PASSWORD=your_password

# Windows (Command Prompt)
set WORKLINK_DB_PASSWORD=your_password
```

Or edit the defaults directly in `db.py` inside `_build_dsn()`.

---

## Running the App

From the directory **containing** the `worklink/` folder:

```bash
python -m worklink.main
```

Or if `main.py` is your entry point at the top level:

```bash
python main.py
```

The window opens at 520 × 560 px on the landing screen and expands to 960 × 680 px after login.

---

## How to Use

### As an Employer
1. Click **Continue as Employer** on the landing screen
2. Go to **Create Account**, enter your company name, email, password, and select your industry fields
3. Once logged in, use **Post a Job** to create a listing — pick required skills from the checkbox selector
4. Visit **My Listings** to see your posted jobs and click **View Applicants** on any listing

### As a Job Seeker
1. Click **Continue as Job Seeker**
2. Register with your name, email, password, and tick all skills that apply to you
3. Use **Browse Jobs** to search and apply for roles
4. Check **My Applications** to see everything you've applied to
5. Visit **Learn Skills** to find free and paid courses for any of the 30 supported skills — click any link to open it in your browser

---

## Skill Categories Supported

Python, Java, C++, JavaScript, HTML/CSS, SQL, Data Analysis, Machine Learning, Project Management, UI/UX Design, Graphic Design, Technical Writing, Customer Service, Digital Marketing, SEO Optimization, Financial Accounting, Data Entry, Excel / Spreadsheets, Public Speaking, Sales & Negotiation, Cloud Computing (AWS/Azure), Cybersecurity, DevOps, Mobile App Development, Agile Methodologies, Content Strategy, Foreign Languages, Video Editing, Human Resources, Network Administration.

---

## Known Limitations

- Passwords are stored in plain text — suitable for coursework / local demos only. Hash with `bcrypt` or `argon2` before any real deployment.
- The `skills` column is `VARCHAR(100)` so very long multi-skill selections are truncated automatically.
- No password reset or email verification flow.

---
