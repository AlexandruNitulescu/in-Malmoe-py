import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import plotly.subplots as subplots
from streamlit_extras.metric_cards import style_metric_cards

class ImportData:
    def __init__(self) -> None:
        pass

class Calculations:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def calculate_mean(self, column: str):
        return self.df[column].mean()

    def calculate_sma(self, column: str, n: list[int]) -> list[str]:
        sma_columns = [f'{column}']
        for i in n:
            sma_column = f'SMA_{column}_{i}'
            self.df[sma_column] = self.df[column].rolling(window=i).mean()
            sma_columns.append(sma_column)
        return sma_columns

    def calculate_monthly_distribution(self, column:str):
        month_dict = {
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'
            }
        
        self.df['DATE'] = pd.to_datetime(self.df['DATE'])
        self.df['MONTH'] = self.df['DATE'].dt.month
        self.df['YEAR'] = self.df['DATE'].dt.month
        columns = ['YEAR', 'MONTH', f'{column}']
        df_new = self.df[columns]
        monthly_sums = df_new.groupby(columns[:2])[f'{column}'].sum()
        monthly_sums = monthly_sums.reset_index()
        monthly_sums['MONTH'] = monthly_sums['MONTH'].map(month_dict)
        monthly_sums = monthly_sums.drop(columns='YEAR')
        monthly_sums = monthly_sums.reset_index(drop=True)
        fig = px.pie(monthly_sums, values=f'{column}', names='MONTH',color_discrete_sequence=px.colors.sequential.RdBu)
        return fig, monthly_sums

    def calculate_difference(self, andel: str, column_1: str):
        self.df['DIFF'] = round(self.df[andel]/self.df[column_1] * 100,1)
        dataframe = self.df[['DATE', 'DIFF']]
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(dataframe.columns),
                        #fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[dataframe['DATE'], dataframe['DIFF']],
                       fill_color='lavender',
                       align='left'))
        ])
        return dataframe, fig

    def summary(self, district_key: str, months: list[int]):
        values = []
        for i in months:
            mean_sqm = self.df[f'{district_key}_PPSM'].tail(i).mean()
            sum_value = self.df[f'{district_key}_NOS'].tail(i).sum()
            last_element = self.df[f'{district_key}_PPSM'].iloc[-1]
            nth_element = self.df[f'{district_key}_PPSM'].iloc[-i-1]
            pct_difference = ((last_element-nth_element)/last_element)*100
            pct_difference = round(pct_difference, 1)
            values.append([f'{i} months', mean_sqm, sum_value, pct_difference])
        return values    

def draw_multiple_graphs(df: pd.DataFrame, columns: list[str]) -> go.Figure:
        """
        Plots the specified columns of a Pandas dataframe using Plotly.

        Parameters:
        - df: Pandas dataframe containing the data to plot.
        - columns: List of column labels to plot.

        Returns:
        - Plotly Figure object containing the plotted data.

        Example:
        draw_multiple_graphs(df, ['PPSM', 'SMA'])
        """
        fig = go.Figure()
        for column in columns:
            fig.add_trace(go.Scatter(x=df['DATE'], y=df[column], name=column))
        return fig

def update_colors_multiple_graphs(colors: list[str], fig: go.Figure):
    try:
        for i, trace in enumerate(fig.data):
            trace.update(marker=dict(color=colors[i]))
    except IndexError:
        print("Warning: The number of traces doesn't match the number of colors.")

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

def draw_histogram(df: pd.DataFrame, title: str, x_data: str, y_data: str, mean_value_trace=None):
    fig = go.Figure(
        data=[go.Bar(x=df[x_data], y=df[y_data])], 
        layout_title_text=title)
    if mean_value_trace == True:
        fig.add_trace(go.Scatter(
            x=[x_data], y=(df[y_data].mean(), df[y_data].mean()), mode='lines'))

    return fig


def draw_distribution_bar(df: pd.DataFrame, x_axis: str, y_axis: str, y1_axis: str, title:str):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df[x_axis],
                    y=df[y_axis],
                    name=f'{y_axis}',
                    #orientation='h',
                    marker_color='rgb(55, 83, 109)'
                    ))
    fig.add_trace(go.Bar(x=df[x_axis],
                    y=df[y1_axis],
                    name=f'{y1_axis}',
                    #orientation='h',
                    marker_color='rgb(26, 118, 255)'
                    ))

    fig.update_layout(
        title=f'{title}',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Number of Apartments',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1
    )
    return fig

def draw_horizontal_bar(df: pd.DataFrame, x_axis: str, date_column: str, y1_axis:str, title:str):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df[x_axis],
                    y=df[date_column],
                    name=f'{x_axis}',
                    marker_color='rgb(55, 83, 109)'
                    ))
    fig.add_trace(go.Bar(x=df[x_axis],
                    y=df[y1_axis],
                    name=f'{y1_axis}',
                    marker_color='rgb(26, 118, 255)'
                    ))
     
    fig.update_layout(
        title=f'{title}',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Number of Apartments',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1
    )
    return fig
               
def create_scatter_1(df: pd.DataFrame, date_column:str, columns: list[str]) -> go.Figure:
    data = []
    colors = ['red', 'blue', 'green', 'orange']
    for i, col in enumerate(columns):
        trace = go.Scatter(x=df[col], y=df[date_column], mode='markers', name=col, marker={'color': colors[i]})
        data.append(trace)
    fig = go.Figure(data=data)
    return fig

def draw_chart_bar(df: pd.DataFrame, x_data: str, y_data, title: str):
    fig = px.bar(df, x=x_data, y=y_data, title=title)
    avg_line = px.line(df, x=x_data, y=df[y_data].mean())
    fig.add_traces(avg_line.data)
    return fig

def transform_dtype(df: pd.DataFrame, column_to_change: str):
    df[column_to_change] = df[column_to_change].str.replace(',', '.')
    df[column_to_change] = pd.to_numeric(df[column_to_change])

def transform_date(df: pd.DataFrame, column_to_transform: str):
    df[column_to_transform] = pd.to_datetime(df[column_to_transform])

def draw_piechart(df: pd.DataFrame, color_palette):
    nos_columns = ['CE_NOS', 'C_NOS', 'FO_NOS', 'HY_NOS', 'KB_NOS', 'LB_NOS', 'RGH_NOS', 'SI_NOS', 'VI_NOS', 'MMA_NOS']
    nos_values = df[nos_columns].sum().tolist()
    fig = go.Figure(data=[go.Pie(labels=nos_columns, values=nos_values, marker=color_palette)])
    return fig

def draw_pie(df: pd.DataFrame, columns: list, info_dict: dict, colors):
    labels = list(info_dict.keys())
    values = df[columns].sum().tolist()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker={'colors':colors})])
    return fig


class Visualize:
    def __init__(self, df: pd.DataFrame, color_theme: list[str]):
        self.df = df
        self.color_theme = color_theme

    def draw_scatter_plots(self, columns: list[str], type: str) -> go.Figure:
        data = []
        if type == 'markers':
            for i, col in enumerate(columns):
                trace = go.Scatter(
                    x=self.df[col], y=self.df['DATE'],
                    mode=f'{type}', 
                    name=col, 
                    marker={'color': self.color_theme[i]})
                data.append(trace)
            fig = go.Figure(data=data)
        else:
            for i, col in enumerate(columns):
                trace = go.Scatter(
                    x=self.df['DATE'], y=self.df[col],
                    mode=f'{type}', 
                    name=col, 
                    marker={'color': self.color_theme[i]})
                data.append(trace)
            fig = go.Figure(data=data)     
        fig.update_layout(hovermode='x unified')     
        return fig

    def draw_box_1plots(self, district_key: str):
        fig = subplots.make_subplots(1, 4)
        fig.add_trace(px.box(self.df, y=f"{district_key}_PPSM1R"), row=1, col=1)
        fig.add_trace(px.box(self.df, y=f"{district_key}_PPSM2R"), row=1, col=2)
        fig.add_trace(px.box(self.df, y=f"{district_key}_PPSM1R"), row=1, col=3)
        fig.add_trace(px.box(self.df, y=f"{district_key}_PPSM2R"), row=1, col=4)

        return fig
    def draw_box_plots(self, district_key: str):
        columns = [f"{district_key}_PPSM1R", f"{district_key}_PPSM2R", f"{district_key}_PPSM3R", f"{district_key}_PPSM4PR"]
        data = [go.Box(y=self.df[column], name=column) for column in columns]
        fig = go.Figure(data=data)
        return fig
    
    def draw_metrics(self, sum_info, columns):
        j = 0
        for i in range(len(sum_info)):
          for column in columns:
            if j == 0:
              column.metric(label = f'{sum_info[i][0]}', value = f'{int(sum_info[i][1])}', delta= 'kr/sqm', delta_color='off')
            elif j == 1:
              column.metric(label = '', value = sum_info[i][2], delta='units', label_visibility="hidden", delta_color='off')
            elif j == 2:
              column.metric(label = '', value = str(sum_info[i][3])+ '%', delta='price development', label_visibility="hidden", delta_color='off')
            j += 1
            if j == 3:
              j = 0
        style_metric_cards()

    def set_color(self, district_key, y):
        reference = self.df[f'{district_key}_NOS'].mean()
        if(y >= 2*reference):
            return "#00BFA0"
        elif(y >= reference):
            return "#FFA300"
        elif(y >= 0):
            return "#E60049"

    def draw_horizontal_bar(self, district_key: str, color):
        fig = go.Figure(
            data=[go.Bar(
                x=self.df[f'{district_key}_NOS'],
                y=self.df['DATE'],
                orientation='h',
                name=f'{district_key}_NOS',
                marker=dict(color=f'{color}'
               #marker=dict(color = list(map(self.set_color, district_key, self.df[f'{district_key}_NOS']))
                ))]
        )
        return fig
    
    def draw_bar(self, district_key: str):
        month_dict = {
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'
            }

        self.df['DATE'] = pd.to_datetime(self.df['DATE'])
        self.df['MONTH'] = self.df['DATE'].dt.month
        self.df['YEAR'] = self.df['DATE'].dt.month
        columns = ['YEAR', 'MONTH', f'{district_key}']
        df_new = self.df[columns]
        monthly_sums = df_new.groupby(columns[:2])[f'{district_key}'].sum()
        monthly_sums = monthly_sums.reset_index()
        monthly_sums['MONTH'] = monthly_sums['MONTH'].map(month_dict)
        fig = px.bar(monthly_sums,x='MONTH',y=f'{district_key}_NOS',title='Total Sales of Apartment by month' ,color_discrete_sequence=px.colors.sequential.Plasma)
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

        return fig, monthly_sums

#LAT - LONG
MALMÖ_COORDINATES = [55.604981, 13.003822]
APP_DESCRIPTION = "Are you looking to make informed decisions about the Malmö housing market? Our app is here to help! With real-time data and advanced machine learning algorithms, you'll have access to the most accurate and up-to-date information on prices, trends, and more. Don't make a move without it – this is the ultimate tool for anyone looking to buy, sell, or simply stay informed about the Malmö real estate market. This text highlights the app's value as a source of reliable and current information, and emphasizes its usefulness for a range of purposes related to the housing market in Malmö. It also suggests that using the app is a smart way to avoid making unwise decisions."
APP_SUMMARY = ' *in-Malmö* Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam lobortis pellentesque lobortis. Aliquam aliquam, tortor id volutpat elementum, quam erat rhoncus felis, sed convallis nisl ligula nec dolor. Sed pretium ante ipsum, vel congue justo dignissim nec. Aenean hendrerit laoreet metus, id tempus est luctus vitae. Duis ullamcorper sapien eu leo consectetur elementum. Praesent dictum nibh sit amet ipsum lobortis porttitor. Duis luctus convallis dui, in tincidunt libero aliquam ac. Praesent id auctor enim, et porttitor risus. Phasellus semper lobortis vestibulum. Suspendisse varius semper enim, ut hendrerit dolor. Duis elit nulla, interdum quis erat eu, gravida pellentesque turpis. Nam faucibus fringilla pulvinar. Nulla porttitor pretium urna in ornare. Nulla dictum elit nulla, at pretium dolor gravida eu. Curabitur elit ex, volutpat ac justo nec, lacinia maximus enim. Nullam tristique fringilla pulvinar. Nulla at ligula ac urna interdum facilisis nec sed justo. Pellentesque elit tellus, consectetur non est eget, congue ullamcorper felis. Aenean mattis felis id mollis pellentesque. In hac habitasse platea dictumst. Curabitur condimentum enim eget vehicula maximus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce quis tortor tincidunt, viverra justo et, consectetur eros. Vestibulum ac lobortis nisi, in ullamcorper neque. Sed scelerisque imperdiet.'
MALMOE_DESCRIPTION = 'Malmö is the third-largest city in Sweden, located in the southern part of the country in the county of Skåne. While the city is known for its vibrant culture and diverse population, it has recently gained attention for its high housing prices. Housing prices in Malmö have been on the rise for the past few years, with the average price of a single-family home reaching almost 7 million SEK (approximately $830,000) in 2021. This increase has been fueled by a number of factors, including a strong economy, a high demand for housing, and limited supply. The high housing prices in Malmö have had a number of consequences for the city and its residents. For one, it has made it more difficult for young people and families to afford to buy a home, leading many to rent or to move to other cities. The high prices have also made it more difficult for businesses to attract and retain employees, as the cost of living in the city can be quite high. Despite the challenges posed by high housing prices, Malmö remains a popular place to live, with a strong economy and a high quality of life. The city has made efforts to address the housing crisis, including the construction of new homes and the implementation of policies to increase the supply of affordable housing. Overall, the high housing prices in Malmö are a significant issue for the city and its residents. While efforts are being made to address the crisis, it is likely to continue to be a challenge in the coming years.'
INFLATION_DESCRIPTION = 'Inflation is a measure of the overall increase in the level of prices of goods and services in an economy over a period of time. It is typically expressed as a percentage change from a base period, such as the previous year or month. The inflation rate in Sweden has fluctuated over time, with periods of both high and low inflation. In recent years, the inflation rate in Sweden has been relatively low and stable, with an average rate of around 2% per year. There are a number of factors that can affect the inflation rate in Sweden, including economic growth, employment, and the exchange rate. For example, if the economy is growing quickly and there is high demand for goods and services, this can put upward pressure on prices and lead to higher inflation. On the other hand, if the economy is slowing down or there is excess capacity in the market, this can lead to lower inflation. To measure the inflation rate in Sweden, the Swedish central bank, the Riksbank, uses a measure called the Harmonized Index of Consumer Prices (HICP), which is based on the prices of a basket of goods and services consumed by households in the country. The HICP is used as a benchmark for monetary policy and to compare the inflation rate in Sweden with other countries. Overall, the inflation rate in Sweden has been relatively low and stable in recent years, but it is important to monitor changes in the rate over time to understand the impact of inflation on the economy and on household budgets.'
HYLLIE_DESCRIPTION = 'Hyllie is a district located in the southern part of Malmö, Sweden that has become a popular place to live in recent years. It is known for its modern and vibrant atmosphere, and is home to a variety of amenities including shopping centers, restaurants, and entertainment venues.The housing market in Hyllie is quite competitive, with demand for apartments and houses outpacing supply in many cases. As a result, prices for both rental and purchased properties are generally higher in Hyllie than in other parts of the city. The average salary in Hyllie is also relatively high, which can make it easier for residents to afford housing in the area. Despite the high cost of housing, many people are attracted to Hyllie because of its proximity to the city center and the many job opportunities in the area. There are a variety of apartment buildings and houses available, ranging from modern high-rise buildings to more traditional Swedish homes. Overall, Hyllie is a desirable place to live, but it can be challenging to find affordable housing due to the high demand and relatively high prices.'
KIRSEBERG_DESCRIPTION = 'Kirseberg is a district located in the eastern part of Malmö, Sweden. It is a diverse and vibrant area that is popular with both young professionals and families. The housing market in Kirseberg is diverse, with a mix of rental apartments, condominiums, and detached houses available. Prices for both rental and purchased properties tend to be lower in Kirseberg than in other parts of the city, making it a more affordable option for many people. The average salary in Kirseberg is also relatively low, which can make it more challenging for some residents to afford housing in the area. Despite the lower prices, Kirseberg is a desirable place to live because of its proximity to the city center and the many job opportunities in the area. There are a variety of apartment buildings and houses available, ranging from modern high-rise buildings to more traditional Swedish homes. Kirseberg is also home to several educational institutions, including the Malmö University and several primary and secondary schools. This makes it a great place for families with children, as well as for students who are studying in the city. Overall, Kirseberg is a diverse and affordable district that is popular with people of all ages and backgrounds. It is a great place to live, work, and receive an education.'
CENTRUM_DESCRIPTION = 'Centrum is a district located in the heart of Malmö, Sweden. It is a vibrant and lively area that is known for its diverse population and rich cultural offerings. One of the main attractions of Centrum is its central location and easy access to the rest of the city. It is home to a number of shopping centers, restaurants, and entertainment venues, making it a popular destination for both tourists and locals.The housing market in Centrum is quite competitive, with demand for apartments and houses outpacing supply in many cases. As a result, prices for both rental and purchased properties are generally higher in Centrum than in other parts of the city. The average salary in Centrum is also relatively high, which can make it easier for residents to afford housing in the area.Despite the high cost of housing, many people are attracted to Centrum because of its central location and the many job opportunities in the area. There are a variety of apartment buildings and houses available, ranging from modern high-rise buildings to more traditional Swedish homes. Overall, Centrum is a desirable place to live, but it can be challenging to find affordable housing due to the high demand and relatively high prices. However, for those who are able to afford it, the central location and many amenities make it a great place to call home.'
INTRODUCTION_DESCRIPTION = 'The Swedish real estate market has been performing well in recent years, with strong demand for both rental and purchased properties. According to statistics from the Swedish Real Estate Agency, the number of home sales in Sweden has been steadily increasing since 2018, with a slight dip in 2020 due to the COVID-19 pandemic.One of the main drivers of the strong performance of the Swedish real estate market has been the countrys strong economy and low unemployment rate. This has made it easier for people to afford housing and invest in real estate. In addition, Sweden has a high standard of living and a high quality of life, which has made it a desirable place to live for many people. Another factor contributing to the strong performance of the Swedish real estate market is the limited supply of housing. The demand for housing in Sweden has been consistently outpacing the supply, which has led to rising prices in many parts of the country. Overall, the Swedish real estate market has been performing well in recent years, with strong demand and limited supply driving prices higher. However, it is worth noting that the market can be volatile and is subject to change based on economic and other factors.'
INFLATION_DESCRIBTION = 'Inflation is a measure of the overall increase in prices of goods and services in an economy over a period of time, and can affect the cost of housing among other things. However, it is important to note that the impact of inflation on the housing market can vary depending on a number of factors.In the case of Sweden, the inflation rate has generally been low in recent years, averaging around 2% per year. This means that the overall increase in prices in the Swedish economy has been relatively moderate. As a result, it is likely that the impact of inflation on the housing market in Sweden has also been moderate.However, it is important to note that the impact of inflation on the housing market is likely to be just one of many contributing factors. Other important factors include the state of the economy, changes in housing demand and supply, and government policies.In general, when the overall price level in the economy is increasing, it is natural for the cost of housing to follow suit to some extent. However, the impact of inflation on the housing market is likely to be more nuanced and complex, and it is important to consider the overall economic and market context when analyzing the impact of inflation on the housing market.'
RECESSION_DESCRIPTION = 'It is difficult to predict with certainty whether or not the economy is heading towards a recession. Recessions are generally characterized by a significant decline in economic activity, such as a decrease in gross domestic product (GDP) and an increase in unemployment. There are a number of indicators that economists and analysts use to track the health of the economy and identify potential signs of a recession. These include measures of economic activity such as GDP and employment, as well as financial indicators such as stock market performance and interest rates. If the economy does enter a recession, it could have an impact on the housing market in Malmö, Sweden. During a recession, people may be more hesitant to invest in real estate due to economic uncertainty and a decrease in disposable income. This could lead to a decrease in demand for housing and potentially a drop in housing prices. On the other hand, a recession could also lead to a decrease in the supply of housing, as builders and developers may be less likely to start new projects during economic downturns. This could help to support housing prices to some extent. Overall, it is difficult to predict the exact impact of a recession on the housing market in Malmö. The market is subject to a number of complex and interconnected factors, and the impact of a recession on the housing market is likely to depend on a variety of economic and market conditions.'
REAL_ESTATE_INDEX_DESCRIPTION = 'A real estate index is a statistical measure that tracks the changes in the value of a particular group of real estate assets over time. These assets can include residential properties, commercial properties, or a mix of both. Real estate indexes can be used to measure the overall health of the real estate market, as well as to gauge the performance of specific sectors within the market.There are several different types of real estate indexes, including national indexes, regional indexes, and local indexes. National indexes track the overall value of real estate assets across the country, while regional and local indexes track the value of real estate assets in specific areas.To interpret a real estate index, it is important to consider the type of index being used and the time frame being measured. For example, a local index that tracks the value of residential properties in a specific city over the past year may show a different trend than a national index that tracks the value of commercial properties across the country over the past decade. It is also important to consider other factors that may affect the value of real estate assets, such as economic conditions, population trends, and changes in local laws and regulations. By taking these factors into account, you can get a more accurate picture of the real estate market and how it is likely to perform in the future.'
KPI_DESCRIPTION = 'The consumer price index (KPI) is a measure of the average change over time in the prices paid by consumers for a basket of goods and services. It is calculated by taking the cost of a fixed basket of goods and services at a given time and comparing it to the cost of the same basket in a base year. The KPI is commonly used to measure inflation, as it shows the overall change in prices that consumers are paying for goods and services. The consumer price index at fixed rate (KPIF) is a variant of the KPI that is used to measure inflation in the eurozone (the 19 European Union countries that have adopted the euro as their currency). Like the KPI, the KPIF measures the change in the prices paid by consumers for a basket of goods and services over time. However, the basket of goods and services used to calculate the KPIF is fixed in terms of the amount of each item consumed, rather than the amount of money spent on each item. This means that the KPIF takes into account changes in the prices of goods and services as well as changes in the quantities consumed. To interpret the KPI or the KPIF, it is important to consider the specific basket of goods and services being measured and the time frame being considered. For example, a KPI that measures the prices of goods and services consumed by urban households may show a different trend than a KPI that measures the prices of goods and services consumed by rural households.There are some differences between the KPI and the KPIF. The most significant difference is that the KPIF takes into account changes in the quantities of goods and services consumed, while the KPI does not. In addition, the KPIF is specific to the eurozone, while the KPI can be used to measure inflation in any country.'
HOW_TO_USE_DESCRIPTION = "On the home page, you'll find some general information about Malmö's housing market and Swedish inflation. This page is a good starting point for getting an overview of the current market conditions. To dive deeper into the data, head over to the Data Analyser page. Here, you can browse through a variety of graphs and charts that visualize the housing market data in different ways. Use the navigation buttons to switch between different views and customize the data being displayed. As you explore the data, try to draw your own conclusions about the trends and patterns you see. The data visualizations are a powerful tool for understanding the housing market and making informed decisions. I hope you enjoy using our web app and find it helpful in your analysis of the housing market! If you have any questions or feedback, don't hesitate to contact us."

##COLORS
palette = ['rgb(255, 173, 173)','rgb(255, 214, 165)','rgb(253, 255, 182)','rgb(202, 255, 191)','rgb(155, 246, 255)','rgb(160, 196, 255)','rgb(189, 178, 255)','rgb(255, 198, 255)']
GRAPH_COLORS_4 = ['#000000', '#2a9d8f', '#eb5e28', '#c1121f']
GRAPH_COLORS_10 = ["006466","065a60","0b525b","144552","1b3a4b","212f45","272640","312244","3e1f47","4d194d","4d194d","4d194d"]
#COLOR_PALETTE = ["#e60049", "#0bb4ff", "#50e991", "#e6d800", "#9b19f5", "#ffa300", "#dc0ab4", "#b3d4ff", "#00bfa0"]
COLOR_PALETTE = ["#001219","#005f73","#0a9396","#94d2bd","#e9d8a6","#ee9b00","#ca6702","#bb3e03","#ae2012","#9b2226"]

# Number of sales dictionary
NOS_dict = {
    'Centrum':'C_NOS',
    'Fosie-Oxie':'FO_NOS',
    'Hyllie':'HY_NOS',
    'Kirseberg':'KB_NOS',
    'Limhamnd-Bunkeflo':'LB_NOS',
    'Rosengård-Husie':'RGH_NOS',
    'Södra Innerstaden':'RGH_NOS',
    'Västra Innerstaden':'RGH_NOS'
}

abbrev_dict = {
    "C": 'Centrum',
    "FO": 'Fosie-Oxie',
    "HY": 'Hyllie',
    "KB": 'Kirseberg',
    "LB": 'Limhamn-Bunkeflo',
    "RGH": 'Rosengård-Husie',
    "SI":'Södra Innerstaden',
    'VI':'Västra Innerstaden',
    'PPSM':'Average price per SqM in SEK',
    'PPSMxR':'Average price per SqM in SEK for x Room(s)',
    'NOS': 'Number of Sales'
}