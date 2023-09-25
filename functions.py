import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
import pywt
from scipy.interpolate import interp1d


def draw_five_pattern_chart_matplotlib(pumping_df,ms_seismic_df,date_col,time_col,pressure_col,\
                                       rate_col,ms_date_col,ms_time_col,ms_x,ms_y,ms_z
                                       
                                       ):
    fig, axes = plt.subplots(6, 1, figsize=(12, 12), sharex=True)

    #pumping data
    #combine data_col and time_col to one column named datetime and convert to datetime
    pumping_df[date_col] = pumping_df[date_col].astype(str)
    st.write(pumping_df)
    pumping_df[date_col] = pd.to_datetime(pumping_df[date_col].str.split("-", expand=True).agg("-".join, axis=1), format="%d-%m-%Y").astype(str)
    pumping_df[time_col] = pumping_df[time_col].astype(str)

    pumping_df[pressure_col] = pd.to_numeric(pumping_df[pressure_col])

    pumping_df['datetime'] = pd.to_datetime(pumping_df[date_col] + ' ' + pumping_df[time_col])
    #change the index of datetime column to be the first column
    pumping_df = pumping_df[['datetime'] + [col for col in pumping_df.columns if col != 'datetime']]

    #convert date_datetime to seconds cumulative from datetime
    pumping_df['time_data'] = (pumping_df['datetime'] - pumping_df['datetime'][0]).dt.total_seconds()

    

    #micro seismic data
    ms_seismic_df[ms_date_col] = ms_seismic_df[ms_date_col].astype(str)
    ms_seismic_df[ms_date_col] = pd.to_datetime(ms_seismic_df[ms_date_col].str.split("-", expand=True).agg("-".join, axis=1), format="%d-%m-%Y").astype(str)

    ms_seismic_df[ms_time_col] = ms_seismic_df[ms_time_col].astype(str)
    ms_seismic_df[ms_x] = pd.to_numeric(ms_seismic_df[ms_x])
    ms_seismic_df[ms_y] = pd.to_numeric(ms_seismic_df[ms_y])
    ms_seismic_df[ms_z] = pd.to_numeric(ms_seismic_df[ms_z])


    ms_seismic_df['datetime'] = pd.to_datetime(ms_seismic_df[ms_date_col] + ' ' + ms_seismic_df[ms_time_col])
    ms_seismic_df = ms_seismic_df[['datetime'] + [col for col in ms_seismic_df.columns if col != 'datetime']]


    # Adjust the spacing between subplots
    plt.subplots_adjust(hspace=0.5)



    new_ms_df = interpolate_pumping_pressure_with_micro_seismic(pumping_df,ms_seismic_df[['datetime',ms_x,ms_y,ms_z]])

    # Plot data on each subplot
    axes[0].plot(pumping_df['time_data'] , pumping_df[pressure_col] , label='Pumping pressure')
    axes[1].plot(pumping_df['time_data'] ,  pumping_df[rate_col], label='Pumping rate')
    # Now, add the continuous wavelet transform as the sixth subplot
    scales_a = np.linspace(1, 256, 256)
    coef_a, freqs_a = pywt.cwt(pumping_df[pressure_col], scales_a, "cmor1.5-1.0")

    energy = np.sqrt(coef_a.real**2 + coef_a.imag**2)
    coef2_a = np.log2(energy)
    period = 1.0 / freqs_a
    scaler=preprocessing.MinMaxScaler(feature_range=(0,1)).fit(coef2_a)
    norm_coef2_a=scaler.transform(coef2_a)
    axes[2].grid(False)
    p1 = axes[2].pcolor(pumping_df['time_data'],scales_a, norm_coef2_a,  cmap="nipy_spectral" ,vmin=0, vmax=1)
    fig.colorbar(p1,ax=axes[2], orientation="horizontal")
    #update axes[2] size
    st.dataframe(pumping_df, use_container_width=True)

    st.dataframe(new_ms_df)
    axes[3].plot(new_ms_df['time_data'], new_ms_df[ms_x], label='x')
    axes[4].plot(new_ms_df['time_data'], new_ms_df[ms_y], label='y')
    axes[5].plot(new_ms_df['time_data'], new_ms_df[ms_z], label='z')

    # Set labels and legends
    for i, ax in enumerate(axes):
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        #show ticks values
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.legend()
    return fig



def interpolate_pumping_pressure_with_micro_seismic(pp_df:pd.DataFrame,ms_df:pd.DataFrame):
        
        # Check if df2's range is smaller than df1's range
    if pp_df['datetime'].min() < ms_df['datetime'].min():
        #insert new row at the top of the dataframe
        new_row = pd.DataFrame({'datetime': [pp_df['datetime'].min()],
                        ms_df.columns[1]: [None], 
                        ms_df.columns[2]: [None],
                        ms_df.columns[3]: [None],
                        
                       })

        # Concatenate the new row with the original DataFrame at the 0 index
        ms_df = pd.concat([new_row, ms_df],axis=0).reset_index(drop=True)

    if ms_df['datetime'].max() < pp_df['datetime'].max():
        new_row_max = pd.DataFrame({'datetime': [pp_df['datetime'].max()],
                        ms_df.columns[1]: [None], 
                        ms_df.columns[2]: [None],
                        ms_df.columns[3]: [None],
                        
                       })
        ms_df = pd.concat([ms_df,new_row_max],axis=0).reset_index(drop=True)

        ms_df['time_data'] = (ms_df['datetime'] - ms_df['datetime'][0]).dt.total_seconds()

        return ms_df