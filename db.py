import sqlite3
from datetime import date, timedelta

DB_NAME = "study.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def add_session(d, subject, hours, topic, focus_level):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO study_sessions (date, subject, hours, topic, focus_level)
        VALUES (?, ?, ?, ?, ?)
    """, (d.isoformat(), subject, hours, topic, focus_level))
    conn.commit()
    conn.close()

def get_sessions_this_week():
    conn = get_connection()
    cur = conn.cursor()
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    cur.execute("""
        SELECT date, subject, hours, topic, focus_level
        FROM study_sessions
        WHERE date >= ?
        ORDER BY date DESC
    """, (start_of_week.isoformat(),))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_weekly_hours_by_subject():
    conn = get_connection()
    cur = conn.cursor()
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    cur.execute("""
        SELECT subject, SUM(hours) as total_hours
        FROM study_sessions
        WHERE date >= ?
        GROUP BY subject
        ORDER BY total_hours DESC
    """, (start_of_week.isoformat(),))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_current_streak():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT date
        FROM study_sessions
        GROUP BY date
        HAVING SUM(hours) >= 1
        ORDER BY date DESC
    """)
    rows = cur.fetchall()
    conn.close()

    dates = [date.fromisoformat(r[0]) for r in rows]
    streak = 0
    current_day = date.today()
    while current_day in dates:
        streak += 1
        current_day = current_day - timedelta(days=1)
    return streak

def get_avg_focus_by_subject():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT subject, ROUND(AVG(focus_level), 2) as avg_focus
        FROM study_sessions
        GROUP BY subject
        ORDER BY avg_focus DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_total_sessions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM study_sessions")
    total = cur.fetchone()[0]
    conn.close()
    return total

def get_total_hours_this_week():
    conn = get_connection()
    cur = conn.cursor()
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    cur.execute("""
        SELECT COALESCE(SUM(hours), 0)
        FROM study_sessions
        WHERE date >= ?
    """, (start_of_week.isoformat(),))
    total = cur.fetchone()[0]
    conn.close()
    return round(total, 2)