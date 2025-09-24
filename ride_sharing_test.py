from os import path
import streamlit as st
import pandas as pd
import math 

st.set_page_config(page_title ="Bike Sharing Price Comparator (SG)", page_icon = "🚲", layout = "wide")
st.title("Bike Sharing Price Comparator (Singapore)🚲")
st.write("Analysing your usage, this project will determine the most cost-effective bike sharing service out of the 2 main providers in Singapore: Anywheel and SG Bike.")

st.markdown("## Enter your ride details")
ride_duration = st.slider("Average ride duration (minutes):", 5,120,30, step =5)
rides_per_week = st.slider("Average rides per week:", 1, 50, 10, step = 1)

pricing_model = st.radio("Select your pricing model:", ["Pay-per-ride", "Pass Subscription"])

def anywheel_pricing(minutes:int):
    if minutes <= 30:
        return 1.0
    else:
        extra_minutes = (minutes - 1)//30
        return 1.0 + extra_minutes *1.0
    
def helloride_pricing(minutes:int):
    if minutes <=30:
        return 1.0
    else:
        extra_minutes = (minutes - 30)
        extra_charges = math.ceil(extra_minutes / 10) * 0.5
        return 1.0 + extra_charges
    
passes = {
    "Anywheel": {"7-day": 6.90, "30-day": 9.90, "90-day": 26.90},
    "HelloRide": {"7-day": 5.90, "30-day": 9.90, "90-day": 24.90}
}

pass_weeks = {"7-day": 1, "30-day": 4, "90-day": 13}

if pricing_model =="Pay-per-ride":
    anywheel_cost = anywheel_pricing(ride_duration) * rides_per_week
    helloride_cost = helloride_pricing(ride_duration) * rides_per_week

else:
    pass_choice = st.selectbox("Choose pass type:", ["7-day", "30-day", "90-day"])
    anywheel_weekly = passes["Anywheel"][pass_choice] / pass_weeks[pass_choice]    ##Calculating the weekly cost of the pass 
    helloride_weekly = passes["HelloRide"][pass_choice] / pass_weeks[pass_choice]

    if ride_duration >30 and ride_duration <=60:
        extra_anywheel = (ride_duration - 30) //30 * 0.5 * rides_per_week
        anywheel_cost = anywheel_weekly + extra_anywheel
        helloride_cost = helloride_weekly


    elif ride_duration >=60:
        extra_helloride = (ride_duration - 60) //10 * 0.5 * rides_per_week
        helloride_cost = helloride_weekly + extra_helloride
        extra_anywheel = (ride_duration - 30) //30 * 0.5 * rides_per_week
        anywheel_cost = anywheel_weekly + extra_anywheel

    else:
        anywheel_cost = anywheel_weekly
        helloride_cost = helloride_weekly


st.markdown("## Weekly Cost Comparison")
    
data = pd.DataFrame({
    "Service":["Anywheel", "HelloRide"],
    "Weekly Cost (SGD)":[anywheel_cost, helloride_cost]

})
    
st.bar_chart(data.set_index("Service"))
st.write(f"**Anywheel** ≈ S${anywheel_cost:.2f} per week")
st.write(f"**HelloRide** ≈ S${helloride_cost:.2f} per week")

if anywheel_cost < helloride_cost:
    st.success("Anywheel is more cost-effective for your usage!")
elif helloride_cost < anywheel_cost:
    st.success("HelloRide is more cost-effective for your usage!")
else:
    st.info("Both cost the same for your usage! Just use either whenever you see one!")

st.markdown("### Notes")
st.markdown("Prices are accurate as of ~September 2025 and are subject to changes by the providers")
st.markdown("This also only applies to regular bikes. Family bikes are excluded from this analysis")
st.markdown("Also, discounts/promotions are also excluded from this analysis")
st.markdown("As a general rule of thumb, Anywheel bikes are easier to find given their larger fleet size, but the quality of bikes may vary (with some being old and others being new)")
st.markdown("HelloRide bikes are generally newer and in better condition, but they tend to be harder to find in heartland areas due to their smaller fleet size")
st.markdown("[GitHub](https://github.com/talhamemon07)")