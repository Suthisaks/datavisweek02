import streamlit as st 
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from plotnine import ggplot, aes ,geom_density, theme_light, ggtitle, theme, element_text
from plotly.subplots import make_subplots
import numpy as np
import io
import statsmodels.api as sm
from gapminder import gapminder

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=K2D:wght@300;400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'K2D', sans-serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("Data Visualization: สัปดาห์ที่ 2")


st.table(gapminder.head())

col = st.columns(2) 
with col[0] :
    code = '''
    fig = px.scatter(
        x = gapminder['gdpPercap'],
        y = gapminder['lifeExp']
    )

    fig.update_layout(
        title="Scatter plot",
        xaxis_title="gdpPercap",
        yaxis_title="lifeExp",
        yaxis=dict(
            tickformat=',',
        ))'''
    st.code(code, language="python")
    fig = px.scatter(
        x = gapminder['gdpPercap'],
        y = gapminder['lifeExp']
    )

    fig.update_layout(
        title="Scatter plot",
        xaxis_title="gdpPercap",
        yaxis_title="lifeExp",
        yaxis=dict(
            tickformat=',',
        ))
    st.write(fig)

with col[1] :
    code = '''
    fig = px.scatter(
        x = data2007['gdpPercap'],
        y = data2007['lifeExp']
    )

    fig.update_layout(
        title="Scatter plot (กิจกรรมที่ 2)",
        xaxis_title="gdpPercap",
        yaxis_title="lifeExp",
        yaxis=dict(
            tickformat=',',
        ))'''
    st.code(code, language="python")
    data2007 = gapminder[gapminder['year']==2007]
    fig = px.scatter(
        x = data2007['gdpPercap'],
        y = data2007['lifeExp']
    )

    fig.update_layout(
        title="Scatter plot (กิจกรรมที่ 2)",
        xaxis_title="gdpPercap",
        yaxis_title="lifeExp",
        yaxis=dict(
            tickformat=',',
        ))
    st.write(fig)

col = st.columns(2)

with col[0] :
    data_bar = gapminder.groupby('continent').size().reset_index().rename(columns={0 : 'count'})
    code = '''
    fig = go.Figure(
        go.Bar(
            x = data_bar['continent'],
            y = data_bar['count']
        )
    )

    fig.update_layout(
        title="Bar plot",
        xaxis_title="continent",
        yaxis_title="count",
        yaxis=dict(
            tickformat=',',
        ))'''
    st.code(code, language="python")
    fig = go.Figure(
        go.Bar(
            x = data_bar['continent'],
            y = data_bar['count']
        )
    )

    fig.update_layout(
        title="Bar plot",
        xaxis_title="continent",
        yaxis_title="count",
        yaxis=dict(
            tickformat=',',
        ))

    st.write(fig)
# -----------------------------------------------------
col = st.columns(2)

with col[0] :
    fig = px.scatter(
        data2007,
        x = 'gdpPercap',
        y = 'lifeExp',
        symbol='continent'
        )

    fig.update_layout(
        title="Scatter plot (กิจกรรมที่ 3)",
        xaxis_title="gdpPercap",
        yaxis_title="lifeExp",
        yaxis=dict(
            tickformat=',',
        ))
    st.write(fig)

with col[1] :
    continent2size = {}
    i = 10
    for conti in data2007['continent'].unique() :
        continent2size.update({conti : i})
        i += 10

    data2007['size'] = data2007['continent'].apply(lambda x : continent2size.get(x))
    fig = px.scatter(
        data2007,
        x = 'gdpPercap',
        y = 'lifeExp',
        size='size'
        )

    fig.update_layout(
        title="Scatter plot (กิจกรรมที่ 3)",
        xaxis_title="gdpPercap",
        yaxis_title="lifeExp",
        yaxis=dict(
            tickformat=',',
        ))
    st.write(fig)

# -----------------------------------------------------


import numpy as np

lowess = sm.nonparametric.lowess
trendline = lowess(data2007['lifeExp'], data2007['gdpPercap'], frac=0.3)

x_trend = trendline[:, 0]
y_trend = trendline[:, 1]

n = len(x_trend)
se = np.std(y_trend) / np.sqrt(n)
ci = 1.96 * se  # 95% confidence interval

# Create scatter plot
fig = px.scatter(
    data2007,
    x='gdpPercap',
    y='lifeExp'
)

# Add trendline with confidence interval
fig.add_trace(go.Scatter(
    x=x_trend,
    y=y_trend,
    mode='lines',
    line=dict(color='red'),
    name='Lowess Trendline'
))

# Add confidence interval band
fig.add_trace(go.Scatter(
    x=np.concatenate([x_trend, x_trend[::-1]]),
    y=np.concatenate([y_trend + ci, (y_trend - ci)[::-1]]),
    fill='toself',
    fillcolor='rgba(255, 0, 0, 0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip",
    showlegend=False,
    name='95% CI'
))

st.write(fig)
