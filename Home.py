import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from modules import helper_functions as hlp

def draw_line(df: pd.DataFrame, x_data: str, y_data: str, graph_title:str, x_axis_title: str, y_axis_title: str):
    fig = px.line(df, x=x_data, y=y_data, markers=True)
    fig.update_traces(hovertemplate=None)
    fig.update_layout(
        title=f'{graph_title}',
        xaxis_title = x_axis_title,
        yaxis_title = y_axis_title,
        font=dict(
            family = "Courier New, monospace",
            size=18
        ),
        hovermode='x unified')
    return fig


df = pd.read_csv('../in-Malmoe-py/resources/real_estate_index.csv', delimiter=";")
df_inflation = pd.read_csv('../in-Malmoe-py/resources/inflation_rate.csv', delimiter=";")

hlp.transform_dtype(df_inflation, 'KPI')
hlp.transform_dtype(df_inflation, 'KPIF')


st.set_page_config(
    page_title="in-Malmö - the guru in housing market.",
    layout="wide",
    initial_sidebar_state="expanded"
)



def sidebar():
    st.sidebar.header('Documentation')
    st.sidebar.info("For more information, please see the documentation at the following link: [Documentation](https://example.com/documentation)")

    st.sidebar.markdown('## Future releases')
    st.sidebar.info("The plan in the future is to implement a variety of machine learning models to further enhance the capabilities of in-Malmö. These models will be carefully selected and tested to ensure that they provide the best possible results for the users. I'm excited to see the potential improvements that these models will bring.")
    st.sidebar.header('Source(s)')
    st.sidebar.info(
        "The data used in this analysis was sourced from Statistikmyndigheten (https://www.scb.se/en/)."
    )




def first_section():
    col1, col2 = st.columns(2)
    coords = pd.DataFrame(np.random.randn(1, 2) / [100, 100] + [hlp.MALMÖ_COORDINATES[0], hlp.MALMÖ_COORDINATES[1]],columns=['lat', 'lon'])
    col1.map(coords,10, use_container_width=True)
    col2.markdown("# :city_sunset: in-Malmö")
    col2.write(f"{hlp.APP_DESCRIPTION}")
    #col2.markdown(f"""{hlp.APP_DESCRIPTION}""")
    col2.markdown('')

    col2.markdown(
        """**Created by Alexandru Nitulescu** |
        [![Star](https://img.shields.io/github/stars/anitulescu_/train.svg?logo=github&style=social)](https://github.com/AlexandruNitulescu/in-Malmoe-py)
        [![Follow](https://img.shields.io/twitter/follow/anitulescu_?style=social)](https://www.twitter.com/anitulescu_)
        """)
#        [![Buy me a coffe](https://img.shields.io/badge/Buy%20me%20a%20coffee--yellow.svg?logo=buy-me-a-coffee&logoColor=orange&style=social)](https://www.buymeacoffee.com/anitulescu_)
    st.markdown("---")

def second_section():
    col3, col4 = st.columns(2)
    col3.markdown(
        f"""
        ### :arrow_lower_right: A sharp price correction is coming
       {hlp.INTRODUCTION_DESCRIPTION}""")
    fig = hlp.draw_multiple_graphs(df, df.columns[1:])
    fig.update_layout(
        title='Real Estate Index (REI) in Sweden from 1970-',
        xaxis_title = 'DATE',
        yaxis_title = 'REI',
        font_family="Courier New",
        title_font_family="Times New Roman",
        hovermode='x unified')

    col4.plotly_chart(fig)
    st.subheader('Real Estate Index: A Key Indicator of the Health of the Market')
    st.markdown(f"{hlp.REAL_ESTATE_INDEX_DESCRIPTION}")
    st.markdown("---")
    
def third_section():
    col5, col6 = st.columns(2)    
    #fig = hlp.draw_line(df_inflation, df_inflation['DATE'], ['KPI', 'KPIF'], 'KPI - Consumer Price Index','Date', 'KPI in %')
    fig = hlp.draw_multiple_graphs(df_inflation,['KPIF',"KPI"])
    fig.update_layout(
        title='Consumer Price Index w/o fixed rate, KPIF & KPI',
        xaxis_title = 'DATE',
        yaxis_title = 'in %',
        font_family="Courier New",
        title_font_family="Times New Roman",
        hovermode='x unified')
    fig.data[0].update(marker={
    'color': '#463f3a'
    })
    fig.data[1].update(marker={
        'color':'#2a9d8f'
    })
    col5.plotly_chart(fig, use_container_width=True)
    col6.markdown(
        f"""
        ### :scales: Global recession may not bring down the demand?
       {hlp.RECESSION_DESCRIPTION}""")
    st.markdown('#### The Role of the Consumer Price Index (KPI) and the Consumer Price Index at Fixed Rate (KPIF) in Economic Analysis')
    st.markdown(f"{hlp.KPI_DESCRIPTION}")
    st.markdown("---")

def fourth_section():
    st.subheader('"Statistics Sweden provides society with useful and trusted statistics"')
    st.markdown('''
    "The data for this project is sourced from SCB.se, the official website of Statistics Sweden (Statistikmyndigheten, SCB). SCB is the government agency responsible for producing official statistics on Sweden's society, economy, and environment. The data on SCB.se is a rich and reliable resource that covers a wide range of topics, including population, labor market, income, education, and much more. In this project, we have used SCB data to [insert specific purpose or analysis]. We believe that the data provided by SCB is an invaluable source for understanding and improving various aspects of Swedish society.
    In a future version of this project, we plan to include an API and an API scraper to allow users to more easily access and retrieve data from SCB.se. The API and API scraper will provide a convenient and efficient way to retrieve data for various purposes, such as data analysis, visualization, and more. Stay tuned for updates on this feature!"
    ''')
    st.write("**All data has been updated on December 21, 2021.**", markdown=True)

sidebar()
first_section()
second_section()
third_section()
fourth_section()