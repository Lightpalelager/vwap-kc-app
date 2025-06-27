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

def get_distance_label(diff):
    # Set your custom thresholds here
    if diff >= 5:
        return "Large"
    elif diff >= 2:
        return "Moderate"
    elif diff > 0:
        return "Small"
    else:
        return "N/A"

st.title("VWAP & Keltner Channel Interpretation Tool")

# Initialize session state history
if "history" not in st.session_state:
    st.session_state.history = []

with st.form(key='input_form'):
    price_vwap = st.radio("Price vs VWAP", ["Above VWAP", "At VWAP", "Below VWAP"])
    vwap_slope = st.radio("VWAP Slope", ["Rising", "Falling"])
    kc_position = st.radio("KC Position", [
        "Above KC Upper",
        "Between KC Middle & Upper",
        "Near VWAP",
        "At or Near KC Middle",
        "Between KC Middle & Lower",
        "Below KC Lower"
    ])
    points_diff = st.number_input("Points Difference (Current Price - VWAP)", value=0.0, step=0.01)
    distance = get_distance_label(abs(points_diff))
    st.markdown(f"**Calculated Distance from VWAP:** `{distance}`")
    submit_button = st.form_submit_button(label='Interpret')

if submit_button:
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
            "points_diff": points_diff,
            "interpretation": interpretation,
            "action": action
        })
    else:
        st.warning("No interpretation found for this combination.")

# Display session history
if st.session_state.history:
    st.markdown("---")
    st.subheader("🕘 History")
    for entry in st.session_state.history[:10]:
        st.markdown(
            f"**{entry['timestamp']}** | *{entry['price_vwap']} / {entry['vwap_slope']} / {entry['kc_position']} / {entry['distance']}* (Δ={entry['points_diff']})\n\n"
            f"- 📊 {entry['interpretation']}\n"
            f"- ✅ {entry['action']}"
        )

# Clear history button
if st.button("Clear History"):
    st.session_state.history.clear()
    st.success("History cleared!")
