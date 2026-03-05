import streamlit as st
import json, numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --- PAGE SETUP ---
st.set_page_config(page_title="Warehouse Vision Assistant", layout="wide")

# --- HEADER ---
st.title("📦 Warehouse Vision Intelligence")
st.caption("Visualize throughput from your warehouse video and interact with the analytics (offline mode).")

# --- LOAD DATA ---
summary_path = Path("throughput_summary.json")
video_path = Path("warehouse_full.mp4")

if not summary_path.exists():
    st.error("❌ throughput_summary.json not found in app directory.")
    st.stop()

with open(summary_path) as f:
    summary = json.load(f)

# --- LAYOUT ---
left, right = st.columns([1.3, 1])  # 60% left (video) / 40% right (chat)

# ======================
# 🎥 LEFT PANEL — VIDEO
# ======================
with left:
    if video_path.exists():
        st.subheader("🎥 Warehouse Footage")
        st.video(str(video_path))
    else:
        st.warning("⚠️ warehouse_full.mp4 not found. Upload or place it in root directory to view.")

# ============================
# 📊 RIGHT PANEL — INTERACTIVITY
# ============================
with right:
    st.subheader("📈 Throughput Analytics")

    # --- Chart ---
    tpm = summary["throughput_by_minute"]
    fig, ax = plt.subplots()
    ax.plot(list(tpm.keys()), list(tpm.values()), marker="o")
    ax.set_xlabel("Minute")
    ax.set_ylabel("Objects per Minute")
    ax.set_title("Throughput Trend")
    st.pyplot(fig)

    # --- Metrics summary ---
    total_frames = summary["total_frames"]
    total_objects = summary["total_objects"]
    avg_throughput = sum(tpm.values()) / len(tpm)
    peak_minute = max(tpm, key=tpm.get)

    st.markdown(f"""
    **Summary Stats**
    - Total Frames: `{total_frames}`
    - Total Objects Tracked: `{total_objects}`
    - Average Throughput: `{avg_throughput:.1f} objects/min`
    - Peak Throughput: `{tpm[peak_minute]} objects in minute {peak_minute}`
    """)

    # --- Chat-like interaction ---
    st.markdown("---")
    query = st.chat_input("Ask a question about throughput or performance...")
    if query:
        st.chat_message("user").write(query)
        lower_q = query.lower()

        if "max" in lower_q or "highest" in lower_q:
            answer = f"The highest throughput was {tpm[peak_minute]} objects during minute {peak_minute}."
        elif "min" in lower_q or "lowest" in lower_q:
            min_minute = min(tpm, key=tpm.get)
            answer = f"The lowest throughput was {tpm[min_minute]} objects during minute {min_minute}."
        elif "average" in lower_q:
            answer = f"The average throughput per minute was {avg_throughput:.1f} objects."
        elif "total" in lower_q:
            answer = f"A total of {total_objects} objects were tracked across {len(tpm)} minutes."
        else:
            answer = (
                "Offline mode — try asking:\n"
                "- Which minute had the highest throughput?\n"
                "- What’s the average throughput?\n"
                "- What’s the total throughput?"
            )
        st.chat_message("assistant").write(answer)
