import streamlit as st
import db
import pandas as pd

st.set_page_config(
    page_title="Study Hours Tracker",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1300px;
}

html, body, [class*="css"] {
    font-family: "Inter", "Segoe UI", sans-serif;
    background: #f1f5f9;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
}

div[data-testid="stSidebar"] * {
    color: white !important;
}

.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
    padding: 2rem;
    border-radius: 28px;
    color: white;
    margin-bottom: 1.2rem;
    box-shadow: 0 24px 50px rgba(15, 23, 42, 0.25);
}

.hero h1 {
    font-size: 2.8rem;
    margin: 0;
    color: white;
    font-weight: 800;
}

.hero p {
    margin-top: 0.7rem;
    color: #dbeafe;
    font-size: 1.02rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 1rem;
}

.stat-card {
    background: white;
    border-radius: 22px;
    padding: 1.2rem;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    border: 1px solid #e2e8f0;
}

.stat-title {
    color: #64748b;
    font-size: 0.9rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

.stat-value {
    color: #0f172a;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 0.4rem;
}

.panel {
    background: white;
    border-radius: 24px;
    padding: 1.3rem;
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.07);
    border: 1px solid #e2e8f0;
    margin-top: 1rem;
}

.panel h3 {
    color: #0f172a;
    margin-bottom: 1rem;
    font-size: 1.35rem;
    font-weight: 800;
}

.small-note {
    color: #64748b;
    font-size: 0.95rem;
    margin-bottom: 1rem;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    font-weight: 700;
}

.stButton > button:hover {
    color: white;
    background: linear-gradient(135deg, #115e59 0%, #134e4a 100%);
}

div[data-baseweb="input"], div[data-baseweb="select"] {
    border-radius: 12px !important;
}

[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}

.metric-box {
    background: linear-gradient(135deg, #ecfeff 0%, #f0fdfa 100%);
    border: 1px solid #99f6e4;
    padding: 1rem;
    border-radius: 18px;
    text-align: center;
}

.metric-box .label {
    color: #0f766e;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
}

.metric-box .value {
    color: #134e4a;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>📘 Study Hours Tracker</h1>
    <p>Track your daily study sessions, measure weekly progress, analyze focus levels, and stay consistent with a clean productivity dashboard.</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-title">Total Hours This Week</div>
        <div class="stat-value">{db.get_total_hours_this_week()}</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">Current Streak</div>
        <div class="stat-value">{db.get_current_streak()} days</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">Total Sessions</div>
        <div class="stat-value">{db.get_total_sessions()}</div>
    </div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", ["Log Session", "Weekly Summary", "Streak & Focus"])

if page == "Log Session":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("<h3>Log a New Study Session</h3>", unsafe_allow_html=True)
    st.markdown('<div class="small-note">Add a new session with subject, hours studied, topic, and focus level.</div>', unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        d = st.date_input("Date")
        subject = st.text_input("Subject")
        hours = st.number_input("Hours studied", min_value=0.0, step=0.5)
    with right:
        topic = st.text_input("Topic Covered")
        focus_level = st.slider("Focus level (1-5)", 1, 5, 3)

    if st.button("Save Session"):
        db.add_session(d, subject, hours, topic, focus_level)
        st.success("Session saved successfully!")
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Weekly Summary":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("<h3>Weekly Study Summary</h3>", unsafe_allow_html=True)
    st.markdown('<div class="small-note">View this week’s sessions and the total hours spent on each subject.</div>', unsafe_allow_html=True)

    sessions = db.get_sessions_this_week()
    if sessions:
        df_sessions = pd.DataFrame(sessions, columns=["Date", "Subject", "Hours", "Topic", "Focus Level"])
        st.dataframe(df_sessions, use_container_width=True)
    else:
        st.info("No sessions found for this week.")

    st.markdown("<br>", unsafe_allow_html=True)

    summary = db.get_weekly_hours_by_subject()
    if summary:
        df_summary = pd.DataFrame(summary, columns=["Subject", "Total Hours"])
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("<h3 style='font-size:1.1rem;'>Subject-wise Table</h3>", unsafe_allow_html=True)
            st.dataframe(df_summary, use_container_width=True)
        with c2:
            st.markdown("<h3 style='font-size:1.1rem;'>Subject-wise Chart</h3>", unsafe_allow_html=True)
            st.bar_chart(df_summary.set_index("Subject"))
    else:
        st.info("No summary data available for this week.")

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Streak & Focus":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("<h3>Consistency & Focus Analysis</h3>", unsafe_allow_html=True)
    st.markdown('<div class="small-note">Track your current streak and compare average focus across subjects.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="label">Current Streak</div>
            <div class="value">{db.get_current_streak()} days</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="label">Total Logged Sessions</div>
            <div class="value">{db.get_total_sessions()}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    focus_stats = db.get_avg_focus_by_subject()
    if focus_stats:
        df_focus = pd.DataFrame(focus_stats, columns=["Subject", "Average Focus"])
        left, right = st.columns([1, 1])
        with left:
            st.markdown("<h3 style='font-size:1.1rem;'>Focus Table</h3>", unsafe_allow_html=True)
            st.dataframe(df_focus, use_container_width=True)
        with right:
            st.markdown("<h3 style='font-size:1.1rem;'>Focus Chart</h3>", unsafe_allow_html=True)
            st.bar_chart(df_focus.set_index("Subject"))
    else:
        st.info("No focus data available yet.")

