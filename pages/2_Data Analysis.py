import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from modules import helper_functions as hlp
from streamlit_extras.metric_cards import style_metric_cards


st.set_page_config(
    page_title="Apartments-Malmö",
    layout="wide",
    initial_sidebar_state="expanded"
)



df = pd.read_csv('housing_data.csv', delimiter=";")

calc = hlp.Calculations(df)
visualize = hlp.Visualize(df, hlp.COLOR_PALETTE)

district_dict = {
    'Centrum':'C',
    'Fosie-Oxie':'FO',
    'Hyllie':'HY',
    'Kirseberg':'KB',
    'Limhamn-Bunkeflo':'LB',
    'Rosengård-Husie':'RGH',
    'Södra Innerstaden':'SI',
    'Västra Innerstaden':'VI'
}

option = ["Centrum", "Fosie-Oxie", "Hyllie", "Kirseberg", "Limhamn-Bunkeflo", "Rosengård-Husie", "Södra Innerstaden", "Västra Innerstaden"]
load_dataset = st.sidebar.selectbox("Select City District", option)
district_key = district_dict.get(load_dataset)


def generate_sidebar():
    st.sidebar.header("Helping Tools")
    table = pd.DataFrame.from_dict(hlp.abbrev_dict, orient='index', columns=['Description'])
    show_table = st.sidebar.checkbox("Show Abbreviation Table")
    
    coords = pd.DataFrame(np.random.randn(1, 2) / [100, 100] + [hlp.MALMÖ_COORDINATES[0], hlp.MALMÖ_COORDINATES[1]],columns=['lat', 'lon'])
    map_checkbox = st.sidebar.checkbox("Show Map")
    if map_checkbox:
        st.sidebar.map(coords,10,use_container_width=True)
    if show_table:
      st.sidebar.table(table)

COL_0, COL_01 = st.columns(2)
COL_1, COL_2, COL_3, COL_4 = st.columns([3,1,1,1])
COL_5, COL_6 = st.columns(2)
COL_9, COL_10, COL_11, COL_12 = st.columns(4)
COL_13, COL_14 = st.columns(2)


if load_dataset in district_dict:
    generate_sidebar()
    COL_0.markdown(f'# {load_dataset}')
    fig_graphs= visualize.draw_scatter_plots(calc.calculate_sma(f"{district_key}_PPSM", [3,6,12]),'lines')
    fig_graphs.update_layout(title='Average Price per Square Meter with Simple Moving Average (SMA)')
    COL_1.plotly_chart(fig_graphs, use_container_width=True)


    sum_info = calc.summary(f'{district_key}', [3,6,12])
    visualize.draw_metrics(sum_info, [COL_2, COL_3, COL_4])
    
    fig_lines = visualize.draw_scatter_plots([f'{district_key}_PPSM1R',f'{district_key}_PPSM2R',f'{district_key}_PPSM3R',f'{district_key}_PPSM4PR'], 'lines')
    fig_lines.update_layout(title='Average Price per Square Meter by Number of Room(s)')
    fig_lines.add_hline(y=df[f"{district_key}_PPSM"].mean(), line_dash="dot",
              annotation_text=f"{district_key}_PPSM mean value",
              annotation_position="bottom right")
    COL_5.plotly_chart(fig_lines, use_container_width=True)    

    fig_scatter = visualize.draw_scatter_plots([f'{district_key}_PPSM1R',f'{district_key}_PPSM2R',f'{district_key}_PPSM3R',f'{district_key}_PPSM4PR'], 'markers')
    fig_scatter.update_layout(title='Cluster Points grouped by Number of Room(s)')
    COL_6.plotly_chart(fig_scatter, use_container_width=True)
    
    fig_1 = px.box(df, y=f"{district_key}_PPSM1R", points='all')
    fig_1.data[0].update(marker=dict(color=hlp.COLOR_PALETTE[0]))
    fig_1.add_hline(y=df[f'{district_key}_PPSM'].mean(), line_dash="dot",
              annotation_text=f"{district_key}_PPSM mean value",
              annotation_position="bottom right")
    fig_2 = px.box(df, y=f"{district_key}_PPSM2R", points='all')
    fig_2.data[0].update(marker=dict(color=hlp.COLOR_PALETTE[1]))

    fig_2.add_hline(y=df[f'{district_key}_PPSM'].mean(), line_dash="dot",
              annotation_text=f"{district_key}_PPSM mean value",
              annotation_position="bottom right")
    fig_3 = px.box(df, y=f"{district_key}_PPSM3R", points='all')
    fig_3.data[0].update(marker=dict(color=hlp.COLOR_PALETTE[2]))
    
    fig_3.add_hline(y=df[f'{district_key}_PPSM'].mean(), line_dash="dot",
              annotation_text=f"{district_key}_PPSM mean value",
              annotation_position="bottom right")
    
    fig_4 = px.box(df, y=f"{district_key}_PPSM4PR", points='all')
    fig_4.data[0].update(marker=dict(color=hlp.COLOR_PALETTE[3]))

    fig_4.add_hline(y=df[f'{district_key}_PPSM'].mean(), line_dash="dot",
              annotation_text=f"{district_key}_PPSM mean value",
              annotation_position="bottom right")



    COL_9.plotly_chart(fig_1, use_container_width=True)
    COL_10.plotly_chart(fig_2, use_container_width=True)
    COL_11.plotly_chart(fig_3, use_container_width=True)
    COL_12.plotly_chart(fig_4, use_container_width=True)

    #TOTAL NUMBER OF APARTMENT SALES BY MONTH FROM DECEMBER 2018-
    fig = visualize.draw_horizontal_bar(district_key, hlp.COLOR_PALETTE[5])
    fig.update_layout(title='Number of Apartment Sales by Month from December 2018-')
    COL_13.plotly_chart(fig, use_container_width=True)
  

    fig = calc.calculate_monthly_distribution(f'{district_key}_NOS')
    fig[0].update_layout(title=f'Monthly Sales of Apartments as a Percentage of Total Sales in {load_dataset}')
    COL_14.plotly_chart(fig[0], use_container_width=True)
elif load_dataset is 'Malmö':
    st.markdown('IT WORKS')
st.write('---')
st.write("**All data has been updated on December 21, 2021.**", markdown=True)

style_metric_cards()
