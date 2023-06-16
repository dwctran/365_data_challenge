import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(layout="wide")
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("365 Data Science Student Analysis")
tab1, tab2, tab3 = st.tabs(
    ["Engagement Dashboard", "Subscrition Prediction", "Repository Link"]
)
with tab1:
    components.iframe(
        "https://app.powerbi.com/view?r=eyJrIjoiNzcyODM2NDEtMDg2ZC00NTdjLWEyYzAtMmIzMzNmZmJmZjNjIiwidCI6IjA3ZDUyNWRmLWZhMGQtNGQwNS1iZjY5LTRkYmY0OTY0YzYyZCIsImMiOjEwfQ%3D%3D&pageName=ReportSection3ecabeb1724b04ee9691",
        width=1280,
        height=750,
    )
with tab2:
    data = pd.read_csv(
        "final_prediction_data.csv",
        encoding="latin-1",
    )
    country_codes = pd.read_csv("country_codes.csv")
    country_codes = country_codes[["name", "alpha-2"]]
    country_codes = country_codes.rename(columns={"name": "country_name"})
    data = data.merge(
        country_codes, how="inner", left_on="student_country", right_on="alpha-2"
    )

    data = data.drop(columns=data.columns[0], axis=1)
    data["date_registered"] = pd.to_datetime(
        data["date_registered"], infer_datetime_format=True
    )
    student_country = st.selectbox(
        "Select a country", options=data["country_name"].sort_values().unique()
    )
    student_id = st.selectbox(
        "Select a student",
        options=data[data.country_name == student_country].sort_values(
            by="convert_proba", ascending=False
        )["student_id"],
    )
    st.write(f"Student ID: {student_id}")
    date_registered = (
        data.loc[data["student_id"] == student_id, ["date_registered"]]
        .to_string()
        .split(" ")[-1]
    )
    date_registered = datetime.strptime(date_registered, "%Y-%m-%d")
    date_registered = date_registered.strftime("%B %d, %Y")
    days_engaged = (
        data.loc[data["student_id"] == student_id, ["days_engaged"]]
        .to_string()
        .split(" ")[-1]
    )

    conversion_probability = (
        round(data.loc[data["student_id"] == student_id, ["convert_proba"]] * 100, 2)
        .to_string()
        .split(" ")[-1]
        + "%"
    )
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Student Country", student_country)
    col2.metric("Registration Date", date_registered)
    col3.metric("Number of days engaged", days_engaged)
    col4.metric("Conversion Probability", conversion_probability)

    with st.expander("See full student information: "):
        data_to_display = data[data["student_id"] == student_id].reset_index(drop=True)
        student_info = data_to_display.drop(
            ["student_id", "student_country", "alpha-2"], axis=1
        )
        st.write(student_info.reindex(sorted(student_info.columns), axis=1))
    with st.expander("See full table"):
        data_full = data.sort_values(
            by="convert_proba", ascending=False, ignore_index=False
        ).reset_index(drop=True)
        data_full = data_full.rename(columns={"student_id": "a_student_id"})
        data_full = data_full.drop(["student_country", "alpha-2"], axis=1)
        st.write(data_full.reindex(sorted(data_full.columns), axis=1))

with tab3:
    st.write("https://github.com/dwctran/365_data_challenge")
