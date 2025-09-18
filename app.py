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

# Always prune old clicks and sort
cutoff = datetime.now() - timedelta(hours=WINDOW_HOURS)
st.session_state.click_times = [t for t in st.session_state.click_times if t > cutoff]
st.session_state.click_times.sort()  # keep oldest → newest
save_data(st.session_state.click_times)

st.title("💬 Comment Button")

# Show button if under the limit
if len(st.session_state.click_times) < MAX_CLICKS:
    if st.button(f"Comment ({len(st.session_state.click_times)})"):
        st.session_state.click_times.append(datetime.now())
        save_data(st.session_state.click_times)
        st.rerun()   # refresh the app after clicking
else:
    # Blocking click is the first (oldest) of the last 100
    blocking_click = st.session_state.click_times[0]
    next_available = blocking_click + timedelta(hours=WINDOW_HOURS)
    st.error(
        f"No more clicks! Next click available at "
        f"{next_available.strftime('%Y-%m-%d %H:%M:%S')}"
    )
