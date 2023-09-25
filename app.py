import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from functions import *

# functions


def get_df_from_uploaded_file(file):
    file_name = file.name
    file_extension = file_name.split(".")[-1]

    # Read and display the data from each uploaded file
    if file_extension.lower() == "xlsx" or file_extension.lower() == "xls":
        file_df = pd.read_excel(file)
    elif file_extension.lower() == "csv":
        file_df = pd.read_csv(file)
    elif file_extension.lower() == "txt":
        file_df = pd.read_csv(file, delimiter="\t")

    return file_df


if 'data' not in st.session_state:
    st.session_state['data'] = {}

# set the wide layout
st.set_page_config(layout="wide")

st.sidebar.title("Load data")
st.sidebar.markdown("Upload your pumping data in CSV format")


pumping_data_file = st.sidebar.file_uploader("Upload your files", type=[
                                             "xlsx", "xls", "csv", "txt"], accept_multiple_files=False, key="11")

# Check if files were uploaded
if pumping_data_file:
    st.write("Pumping date file Uploaded:")
    pumping_data_file_df = get_df_from_uploaded_file(pumping_data_file)
    # add pumping data to session state data dic
    st.session_state['data']['pumping_data_file_df'] = pumping_data_file_df

    st.sidebar.markdown("Upload your micro seismic data in CSV format")
    micro_seismic_file = st.sidebar.file_uploader("Upload your files", type=[
                                                  "xlsx", "xls", "csv", "txt"], accept_multiple_files=False, key="22")
    # Check if files were uploaded
    if micro_seismic_file:
        st.write("Micro seismic file Uploaded:")
        micro_seismic_file_df = get_df_from_uploaded_file(micro_seismic_file)
        # add micro seismic data to session state data dic
        st.session_state['data']['micro_seismic_file_df'] = micro_seismic_file_df

        # selector for x column
        mc_date_column = st.sidebar.selectbox(
            "Select the date column", micro_seismic_file_df.columns, key="5")
        # add micro seismic date column to session state data dic
        st.session_state['data']['ms_date_column'] = mc_date_column

        # selector for y column
        mc_time_column = st.sidebar.selectbox(
            "Select the time column", micro_seismic_file_df.columns, key="6")
        # add micro seismic time column to session state data dic
        st.session_state['data']['ms_time_column'] = mc_time_column
        # selector for x column
        x_column = st.sidebar.selectbox(
            "Select the X column", micro_seismic_file_df.columns, key="7")
        # add micro seismic x column to session state data dic
        st.session_state['data']['x_column'] = x_column
        # selector for y column
        y_column = st.sidebar.selectbox(
            "Select the Y column", micro_seismic_file_df.columns, key="8")
        # add micro seismic y column to session state data dic
        st.session_state['data']['y_column'] = y_column
        # selector for z column
        z_column = st.sidebar.selectbox(
            "Select the Z column", micro_seismic_file_df.columns, key="9")
        # add micro seismic z column to session state data dic
        st.session_state['data']['z_column'] = z_column

    # Display the data
    st.subheader(pumping_data_file.name)

    # selector for date column
    p_date_column = st.sidebar.selectbox(
        "Select the date column", pumping_data_file_df.columns, key="1")
    # add pumping date column to session state data dic
    st.session_state['data']['p_date_column'] = p_date_column

    # selector for time column
    p_time_column = st.sidebar.selectbox(
        "Select the time column", pumping_data_file_df.columns, key="2")
    # add pumping time column to session state data dic
    st.session_state['data']['p_time_column'] = p_time_column

    # selector for pressure column
    pressure_column = st.sidebar.selectbox(
        "Select the pressure column", pumping_data_file_df.columns, key="3")
    # add pumping pressure column to session state data dic
    st.session_state['data']['pressure_column'] = pressure_column

    # selector for rate column
    rate_column = st.sidebar.selectbox(
        "Select the rate column", pumping_data_file_df.columns, key="4")
    # add pumping rate column to session state data dic
    st.session_state['data']['rate_column'] = rate_column

    # btn with nice css to execute
    pumping_btn = st.sidebar.button("Plot pumping data")

    if pumping_btn:
        if 'data' in st.session_state:
            fig = draw_five_pattern_chart_matplotlib(pumping_df=st.session_state.data['pumping_data_file_df'],
                                                     ms_seismic_df=st.session_state.data['micro_seismic_file_df'],
                                                     date_col=st.session_state.data['p_date_column'],
                                                     time_col=st.session_state.data['p_time_column'],
                                                     pressure_col=st.session_state.data['pressure_column'],
                                                     rate_col=st.session_state.data['rate_column'],
                                                     ms_date_col=st.session_state.data['ms_date_column'],
                                                     ms_time_col=st.session_state.data['ms_time_column'],
                                                     ms_x=st.session_state.data['x_column'],
                                                     ms_y=st.session_state.data['y_column'],
                                                     ms_z=st.session_state.data['z_column']




                                                     )

            # show matplotlib chart
            st.pyplot(fig)
