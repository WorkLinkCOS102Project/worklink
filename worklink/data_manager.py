"""All DB queries. No file I/O anywhere."""
from __future__ import annotations
import psycopg2
from psycopg2 import IntegrityError, OperationalError
from worklink.db import get_conn, release_conn

def _to_dict(cur, row):
    return dict(zip([d[0] for d in cur.description], row))

def save_user(name, email, password, role, skills):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("INSERT INTO users(name,email,password,role,skills) VALUES(%s,%s,%s,%s,%s)",
                      (name,email,password,role,skills))
        conn.commit(); return True
    except IntegrityError: conn.rollback(); return False
    except Exception: conn.rollback(); return "LOCKED"
    finally: release_conn(conn)

def validate_login(email, password):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("SELECT id,name,role,skills FROM users WHERE email=%s AND password=%s",(email,password))
            row = c.fetchone()
        return {"id":str(row[0]),"name":row[1],"role":row[2],"skills":row[3]} if row else None
    finally: release_conn(conn)

def save_job(employer_id, title, description, skills, experience):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("INSERT INTO jobs(employer_id,title,description,skills,experience) VALUES(%s,%s,%s,%s,%s)",
                      (int(employer_id),title,description,skills,experience))
        conn.commit(); return True
    except Exception: conn.rollback(); return "LOCKED"
    finally: release_conn(conn)

def get_employer_jobs(employer_id):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("SELECT id,employer_id,title,description,skills,experience FROM jobs WHERE employer_id=%s ORDER BY id DESC",(int(employer_id),))
            return [_to_dict(c,r) for r in c.fetchall()]
    finally: release_conn(conn)

def get_jobs():
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("SELECT id,employer_id,title,description,skills,experience FROM jobs ORDER BY id DESC")
            return [_to_dict(c,r) for r in c.fetchall()]
    finally: release_conn(conn)

def save_application(job_id, employee_id):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("INSERT INTO applications(job_id,employee_id) VALUES(%s,%s)",(int(job_id),int(employee_id)))
        conn.commit(); return True
    except IntegrityError: conn.rollback(); return False
    except Exception: conn.rollback(); return "LOCKED"
    finally: release_conn(conn)

def get_applications(employee_id):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("""SELECT a.id,a.job_id,a.employee_id,j.title,j.experience,j.skills
                         FROM applications a JOIN jobs j ON j.id=a.job_id
                         WHERE a.employee_id=%s ORDER BY a.id DESC""",(int(employee_id),))
            return [_to_dict(c,r) for r in c.fetchall()]
    finally: release_conn(conn)

def get_job_applicants(job_id):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("""SELECT u.id,u.name,u.email,u.role,u.skills
                         FROM applications a JOIN users u ON u.id=a.employee_id
                         WHERE a.job_id=%s ORDER BY u.name""",(int(job_id),))
            return [_to_dict(c,r) for r in c.fetchall()]
    finally: release_conn(conn)

def get_stats(user_id, role):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            if role == "Employer":
                c.execute("SELECT COUNT(*) FROM jobs WHERE employer_id=%s",(int(user_id),))
                jobs = c.fetchone()[0]
                c.execute("SELECT COUNT(*) FROM applications a JOIN jobs j ON j.id=a.job_id WHERE j.employer_id=%s",(int(user_id),))
                apps = c.fetchone()[0]
                return {"jobs": jobs, "applicants": apps}
            else:
                c.execute("SELECT COUNT(*) FROM applications WHERE employee_id=%s",(int(user_id),))
                apps = c.fetchone()[0]
                c.execute("SELECT COUNT(*) FROM jobs")
                total = c.fetchone()[0]
                return {"applied": apps, "available": total}
    finally: release_conn(conn)
