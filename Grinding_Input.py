import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File to store data
CSV_FILE = "production_data.csv"

# Function to load data from CSV
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=[
        "Date", "Start", "Finish", "Style", "Size", "Qty", "Total output", 
        "TEMP (R)", "Temp (L)", "Defect", "Remark"
    ])

# Function to save data to CSV
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Initialize session state for the DataFrame
if 'df' not in st.session_state:
    st.session_state.df = load_data()

st.title("Production Data Entry")

# Placeholder for DataFrame (ensures it stays outside the input container)
table_placeholder = st.empty()

# Display the DataFrame at the top
if len(st.session_state.df) > 0:
    table_placeholder.dataframe(st.session_state.df)
else:
    table_placeholder.write("No data available.")

# Move input form to the sidebar
with st.sidebar:
    st.markdown("## Enter Production Data")

    date = st.date_input("📅 Date", datetime.today())
    today_date = date.strftime('%Y-%m-%d')

    col2, col3 = st.columns([1, 1])

  

    with col2:
        start_time = st.selectbox("Start", pd.date_range("07:00", "23:00", freq="1H").strftime("%H:%M"))
    with col3:
        finish_time = st.selectbox("Finish", pd.date_range("08:00", "23:00", freq="1H").strftime("%H:%M"))

    style = st.selectbox("👟Style", ["AA1", "BA1", "BB1"])

    st.markdown("### Size, Qty & Output")
    col4, col5, col6 = st.columns(3)
    with col4:
        size = st.selectbox(" 📏Size", list(range(5, 14)))
    with col5:
        qty = st.number_input("📦Qty", min_value=0)
    with col6:
        total_output = st.number_input("Total Output", min_value=0)

    st.markdown("### 🌡️Temperature (R & L)")
    col7, col8 = st.columns(2)
    with col7:
        temp_r = st.number_input("🌡️TEMP (R)")
    with col8:
        temp_l = st.number_input("🌡️TEMP (L)")

    defect = st.selectbox("⚠️Defect", ["Burn", "Black", "Excess"])
    remark = st.text_input("📝Remark")

    # Collect row data
    row_data = {
        "Date": today_date,
        "Start": start_time,
        "Finish": finish_time,
        "Style": style,
        "Size": size,
        "Qty": qty,
        "Total output": total_output,
        "TEMP (R)": temp_r,
        "Temp (L)": temp_l,
        "Defect": defect,
        "Remark": remark
    }

    # Button to submit data for one row
    if st.button("Submit Row Data"):
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([row_data])], ignore_index=True)
        save_data(st.session_state.df)  # Save to CSV
        st.success("Row added successfully!")
        st.rerun()  # Use st.rerun() instead of st.experimental_rerun()

    # Delete row functionality
    if len(st.session_state.df) > 0:
        st.markdown("### Delete a Row:")

        row_index = st.selectbox("Select a row to delete:",
                                    options=st.session_state.df.index,
                                    format_func=lambda x: f"Row {x+1}: {st.session_state.df.iloc[x]['Date']} | {st.session_state.df.iloc[x]['Start']} - {st.session_state.df.iloc[x]['Finish']}"
                                    )

        if st.button("Delete Selected Row", key="delete_button", help="Click to delete the selected row"):
            st.session_state.df = st.session_state.df.drop(index=row_index).reset_index(drop=True)
            save_data(st.session_state.df)  # Save after deletion
            st.warning(f"Deleted row {row_index + 1}")
            st.rerun()  # Use st.rerun() instead of st.experimental_rerun()