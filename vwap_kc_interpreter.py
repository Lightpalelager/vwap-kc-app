import streamlit as st
import pandas as pd

st.set_page_config(page_title="VWAP & Keltner Scenario Analyzer", layout="centered")

st.title("VWAP & Keltner Channel Scenario Analyzer")

st.write(
    "Enter the current price, VWAP, and Keltner Channel levels. "
    "The system will automatically determine the scenario."
)

# User Inputs with help tooltips
price = st.number_input("Current Price", value=100.0, format="%.2f", help="The latest traded price.")
vwap = st.number_input("VWAP", value=100.0, format="%.2f", help="Volume Weighted Average Price.")
kc_upper = st.number_input("Keltner Channel Upper Band", value=102.0, format="%.2f", help="Upper band of the Keltner Channel.")
kc_middle = st.number_input("Keltner Channel Middle (EMA)", value=100.0, format="%.2f", help="Middle line (usually EMA) of the Keltner Channel.")
kc_lower = st.number_input("Keltner Channel Lower Band", value=98.0, format="%.2f", help="Lower band of the Keltner Channel.")

st.markdown("---")

# Input validation
if not (kc_lower < kc_middle < kc_upper):
    st.error("Invalid Keltner Channel: Ensure KC Lower < KC Middle < KC Upper!")
if vwap == 0:
    st.error("VWAP cannot be zero.")

# Calculate VWAP position
if price > vwap:
    vwap_position = "Above VWAP"
elif price < vwap:
    vwap_position = "Below VWAP"
else:
    vwap_position = "Same Level as VWAP"

# Calculate KC position (expanded for equality edge cases)
if price > kc_upper:
    kc_position = "Above Upper Band"
elif price == kc_upper:
    kc_position = "At Upper Band"
elif price > kc_middle:
    kc_position = "Between Upper and Middle Band"
elif price == kc_middle:
    kc_position = "At Middle Band"
elif price > kc_lower:
    kc_position = "Between Middle and Lower Band"
elif price == kc_lower:
    kc_position = "At Lower Band"
else:
    kc_position = "Below Lower Band"

# Calculate deviation from VWAP
deviation = abs((price - vwap) / vwap) * 100 if vwap else 0
if deviation < 0.3:
    deviation_label = "Neutral (<0.3%)"
elif deviation < 0.7:
    deviation_label = "Slight (0.3%-0.7%)"
elif deviation < 1.5:
    deviation_label = "Stretched (0.7%-1.5%)"
else:
    deviation_label = "Extreme (>1.5%)"

# Scenario logic (expanded)
def get_scenario(kc, vwap_pos, dev):
    if kc in ["Above Upper Band", "At Upper Band"]:
        if vwap_pos == "Above VWAP":
            if dev == "Extreme (>1.5%)":
                return "Very overextended breakout. High reversal risk."
            elif dev == "Stretched (0.7%-1.5%)":
                return "Overextended breakout. Watch for exhaustion."
            else:
                return "Bullish breakout. Trend-follow possible."
        elif vwap_pos == "Below VWAP":
            return "Suspect/fakeout breakout. Caution."
        elif vwap_pos == "Same Level as VWAP":
            return "Indecision at highs, possible top or consolidation."
    if kc in ["Below Lower Band", "At Lower Band"]:
        if vwap_pos == "Below VWAP":
            if dev == "Extreme (>1.5%)":
                return "Very overextended breakdown. High reversal risk."
            elif dev == "Stretched (0.7%-1.5%)":
                return "Overextended breakdown. Watch for exhaustion."
            else:
                return "Bearish breakdown. Trend-follow possible."
        elif vwap_pos == "Above VWAP":
            return "Bear trap/fake breakdown. Caution."
        elif vwap_pos == "Same Level as VWAP":
            return "Indecision at lows, possible bottom or consolidation."
    if kc == "At Middle Band":
        if vwap_pos == "Above VWAP":
            return "Testing support in uptrend. Watch for bounce or breakdown."
        elif vwap_pos == "Below VWAP":
            return "Testing resistance in downtrend. Watch for rejection or breakout."
        else:
            return "Price at balance point. Wait for direction."
    if kc == "Between Upper and Middle Band":
        if vwap_pos == "Above VWAP":
            return "Healthy uptrend, possible long setup."
        elif vwap_pos == "Below VWAP":
            return "Weak rally, likely mean reversion."
        elif vwap_pos == "Same Level as VWAP":
            return "Range or balance, wait for confirmation."
    if kc == "Between Middle and Lower Band":
        if vwap_pos == "Below VWAP":
            return "Healthy downtrend, possible short setup."
        elif vwap_pos == "Above VWAP":
            return "Weak dip, likely mean reversion."
        elif vwap_pos == "Same Level as VWAP":
            return "Range or balance, wait for confirmation."
    return "Balanced or range-bound market. Wait for clear direction."

scenario = get_scenario(kc_position, vwap_position, deviation_label)

# Visualization
chart_data = pd.DataFrame({
    "Price": [None, price, None],
    "VWAP": [vwap, vwap, vwap],
    "KC Upper": [kc_upper, kc_upper, kc_upper],
    "KC Middle": [kc_middle, kc_middle, kc_middle],
    "KC Lower": [kc_lower, kc_lower, kc_lower]
}, index=["Start", "Now", "End"])
st.subheader("Price & Indicators Visualization")
st.line_chart(chart_data)

# Display calculated scenario
st.header("Scenario Output")
st.markdown(
    f"""
    - **Price vs VWAP:** {vwap_position}  
    - **Price vs KC:** {kc_position}  
    - **VWAP Deviation:** {deviation_label} ({deviation:.2f}%)  
    - **Scenario:** :dart: **{scenario}**
    """
)
