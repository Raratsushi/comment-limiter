import streamlit as st
from datetime import datetime, timedelta
import json
import os

DATA_FILE = "click_data.json"
MAX_CLICKS = 100
WINDOW_HOURS = 24

# Load saved clicks
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                timestamps = json.load(f)
                return [datetime.fromisoformat(ts) for ts in timestamps]
            except:
                return []
    return []

# Save clicks
def save_data(click_times):
    with open(DATA_FILE, "w") as f:
        json.dump([t.isoformat() for t in click_times], f)

# Initialize session state
if "click_times" not in st.session_state:
    st.session_state.click_times = load_data()

# Clean old clicks
cutoff = datetime.now() - timedelta(hours=WINDOW_HOURS)
st.session_state.click_times = [t for t in st.session_state.click_times if t > cutoff]
save_data(st.session_state.click_times)

st.title("💬 Comment Button")

# Show button
if len(st.session_state.click_times) < MAX_CLICKS:
    if st.button(f"Comment ({len(st.session_state.click_times)})"):
        st.session_state.click_times.append(datetime.now())
        save_data(st.session_state.click_times)
        st.experimental_rerun()
else:
    next_available = min(st.session_state.click_times) + timedelta(hours=WINDOW_HOURS)
    st.error(f"No more clicks! Next click available at {next_available.strftime('%Y-%m-%d %H:%M:%S')}")
