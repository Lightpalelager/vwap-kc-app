import streamlit as st
from datetime import datetime

# Define the logic mapping based on input conditions
strategy_map = {
    ("Above VWAP", "Rising", "Above KC Upper", "Large"): (
        "Overbought, strong momentum but likely overextended",
        "Take profits, consider partial exit"
    ),
    ("Above VWAP", "Rising", "Between KC Middle & Upper", "Moderate"): (
        "Healthy uptrend, price supported by volume",
        "Buy on pullbacks toward VWAP"
    ),
    ("Above VWAP", "Rising", "Near VWAP", "Small"): (
        "Early stage of uptrend",
        "Consider entering longs"
    ),
    ("Above VWAP", "Falling", "Above KC Upper", "Large"): (
        "Weakening volume despite price strength",
        "Be cautious, reduce longs"
    ),
    ("Above VWAP", "Falling", "Between KC Middle & Upper", "Moderate"): (
        "Possible trend reversal",
        "Wait for confirmation, tighten stops"
    ),
    ("At VWAP", "Rising", "At or Near KC Middle", "N/A"): (
        "VWAP is support, volume confirming",
        "Buy with confirmation"
    ),
    ("At VWAP", "Falling", "At or Near KC Middle", "N/A"): (
        "VWAP support weakening",
        "Watch for breakdown, be cautious"
    ),
    ("Below VWAP", "Falling", "Below KC Lower", "Large"): (
        "Strong bearish trend, price oversold",
        "Consider shorts, wait for pullbacks"
    ),
    ("Below VWAP", "Falling", "Between KC Middle & Lower", "Moderate"): (
        "Bearish but not oversold",
        "Short or wait for confirmation"
    ),
    ("Below VWAP", "Rising", "Below KC Lower", "Large"): (
        "Possible early bounce attempt",
        "Watch closely for reversal"
    ),
    ("Below VWAP", "Rising", "Between KC Middle & Lower", "Moderate"): (
        "Potential pullback in bearish trend",
        "Wait for bounce or confirmation"
    ),
}

st.title("VWAP & Keltner Channel Interpretation Tool")

# Initialize session state history
if "history" not in st.session_state:
    st.session_state.history = []

price_vwap = st.selectbox("Price vs VWAP", ["Above VWAP", "At VWAP", "Below VWAP"])
vwap_slope = st.selectbox("VWAP Slope", ["Rising", "Falling"])
kc_position = st.selectbox("KC Position", [
    "Above KC Upper",
    "Between KC Middle & Upper",
    "Near VWAP",
    "At or Near KC Middle",
    "Between KC Middle & Lower",
    "Below KC Lower"
])
distance = st.selectbox("Distance from VWAP", ["Large", "Moderate", "Small", "N/A"])

key = (price_vwap, vwap_slope, kc_position, distance)

if key in strategy_map:
    interpretation, action = strategy_map[key]
    st.markdown(f"### 📊 Interpretation:\n{interpretation}")
    st.markdown(f"### ✅ Action:\n{action}")

    # Add to history
    st.session_state.history.insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price_vwap": price_vwap,
        "vwap_slope": vwap_slope,
        "kc_position": kc_position,
        "distance": distance,
        "interpretation": interpretation,
        "action": action
    })

# Display session history
if st.session_state.history:
    st.markdown("---")
    st.subheader("🕘 History")
    for entry in st.session_state.history[:10]:
        st.markdown(f"**{entry['timestamp']}** | *{entry['price_vwap']} / {entry['vwap_slope']} / {entry['kc_position']} / {entry['distance']}*\n\n- 📊 {entry['interpretation']}\n- ✅ {entry['action']}")

# Clear history button
if st.button("Clear History"):
    st.session_state.history.clear()
    st.success("History cleared!")
