import streamlit as st
from datetime import datetime

# Session state for scenario history
if "scenario_history" not in st.session_state:
    st.session_state["scenario_history"] = []

st.title("Advanced Market Scenario Interpreter")

# Inputs
price = st.number_input("Current Price")
vwap = st.number_input("VWAP")
kc_upper = st.number_input("KC Upper Band")
kc_middle = st.number_input("KC Middle (EMA)")
kc_lower = st.number_input("KC Lower Band")
auto_deviation = st.checkbox("Auto-calculate Deviation from VWAP", value=True)

if auto_deviation and vwap != 0:
    deviation = abs((price - vwap) / vwap) * 100
    if deviation < 0.3:
        deviation_label = "Neutral (<0.3%)"
    elif deviation < 0.7:
        deviation_label = "Slight (0.3%-0.7%)"
    elif deviation < 1.5:
        deviation_label = "Stretched (0.7%-1.5%)"
    else:
        deviation_label = "Extreme (>1.5%)"
else:
    deviation_label = st.radio(
        "VWAP Deviation",
        ["Neutral (<0.3%)", "Slight (0.3%-0.7%)", "Stretched (0.7%-1.5%)", "Extreme (>1.5%)"]
    )

scenario_label = ""
risk_level = ""
trade_idea = ""
warning = ""

if st.button("Interpret"):
    # Detailed scenario mapping
    if price > kc_upper:
        if price > vwap:
            if "Extreme" in deviation_label:
                scenario_label = "Overextended Breakout"
                risk_level = "High Risk"
                trade_idea = "Consider taking profits or waiting for a pullback."
                warning = "Caution: Chasing highs here is risky; reversal possible."
            else:
                scenario_label = "Healthy Breakout"
                risk_level = "Low Risk"
                trade_idea = "Trend-following long entry possible."
                warning = "Monitor for signs of exhaustion if deviation increases."
        else:
            scenario_label = "Suspect Breakout / Fakeout Risk"
            risk_level = "High Risk"
            trade_idea = "Avoid new longs, possible reversal."
            warning = "Breakout not confirmed by VWAP."
    elif price < kc_lower:
        if price < vwap:
            if "Extreme" in deviation_label:
                scenario_label = "Overextended Breakdown"
                risk_level = "High Risk"
                trade_idea = "Consider covering shorts or watching for bounce."
                warning = "Caution: Chasing lows here is risky; snapback possible."
            else:
                scenario_label = "Healthy Breakdown"
                risk_level = "Low Risk"
                trade_idea = "Trend-following short entry possible."
                warning = "Monitor for signs of exhaustion if deviation increases."
        else:
            scenario_label = "Suspect Breakdown / Bear Trap Risk"
            risk_level = "High Risk"
            trade_idea = "Avoid new shorts, possible reversal."
            warning = "Breakdown not confirmed by VWAP."
    elif kc_middle < price < kc_upper:
        if price > vwap:
            scenario_label = "Trend-Follow Long Setup"
            risk_level = "Low Risk" if "Neutral" in deviation_label or "Slight" in deviation_label else "Medium Risk"
            trade_idea = "Long entries favored, watch for resistance at upper band."
            warning = "If deviation gets stretched, manage risk."
        else:
            scenario_label = "Weak Rally, Mean-Reversion Possible"
            risk_level = "Medium Risk"
            trade_idea = "Be cautious with longs; reversal possible."
            warning = "VWAP not confirming uptrend."
    elif kc_lower < price < kc_middle:
        if price < vwap:
            scenario_label = "Trend-Follow Short Setup"
            risk_level = "Low Risk" if "Neutral" in deviation_label or "Slight" in deviation_label else "Medium Risk"
            trade_idea = "Short entries favored, watch for support at lower band."
            warning = "If deviation gets stretched, manage risk."
        else:
            scenario_label = "Weak Dip, Mean-Reversion Possible"
            risk_level = "Medium Risk"
            trade_idea = "Be cautious with shorts; reversal possible."
            warning = "VWAP not confirming downtrend."
    else:
        scenario_label = "Balanced / Range-Bound Market"
        risk_level = "Low Risk"
        trade_idea = "Range or mean-reversion strategies favored."
        warning = "Wait for breakout or clear trend."

    st.subheader("Scenario Interpretation")
    st.write(f"**Scenario:** {scenario_label}")
    st.write(f"**Risk Level:** {risk_level}")
    st.write(f"**Trade Idea:** {trade_idea}")
    st.write(f"**Warning:** {warning}")

    # Save scenario to history
    scenario_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price": price,
        "vwap": vwap,
        "kc_upper": kc_upper,
        "kc_middle": kc_middle,
        "kc_lower": kc_lower,
        "deviation_label": deviation_label,
        "scenario_label": scenario_label,
        "risk_level": risk_level,
        "trade_idea": trade_idea,
        "warning": warning,
    }
    st.session_state["scenario_history"].insert(0, scenario_data)  # Insert at beginning

# Show scenario history
st.subheader("Scenario History (Last 10)")
for s in st.session_state["scenario_history"][:10]:
    st.write(f"{s['timestamp']} | Scenario: {s['scenario_label']} | Price: {s['price']} | VWAP: {s['vwap']} | Deviation: {s['deviation_label']} | Risk: {s['risk_level']}")

