import streamlit as st
from datetime import datetime, timedelta, timezone
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
                # Convert to UTC datetime objects
                return [datetime.fromisoformat(ts).replace(tzinfo=timezone.utc) for ts in timestamps]
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

# Prune old clicks (older than 24 hours) and sort
cutoff = datetime.now(timezone.utc) - timedelta(hours=WINDOW_HOURS)
st.session_state.click_times = [t for t in st.session_state.click_times if t > cutoff]
st.session_state.click_times.sort()  # oldest → newest
save_data(st.session_state.click_times)

st.title("💬 Comment Button")

# Main comment button
if len(st.session_state.click_times) < MAX_CLICKS:
    if st.button(f"Comment ({len(st.session_state.click_times)})"):
        st.session_state.click_times.append(datetime.now(timezone.utc))
        save_data(st.session_state.click_times)
        st.rerun()
else:
    # Blocking click = oldest in current batch
    blocking_click = st.session_state.click_times[0]
    next_available = blocking_click + timedelta(hours=WINDOW_HOURS)
    
    # Convert UTC to Indian Standard Time (UTC+5:30)
    IST = timezone(timedelta(hours=5, minutes=30))
    next_ist = next_available.astimezone(IST)
    
    st.error(
        f"No more clicks! Next click available at "
        f"{next_ist.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )
