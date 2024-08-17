import streamlit as st 
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
from gapminder import gapminder

st.set_page_config(layout="wide")

st.title("Data Visualization: การบ้านสัปดาห์ 2")
st.markdown("1. สร้าง barchart แสดงการเปรียบเทียบจำนวนประเทศในปี 2007 ที่ประชากรมีอายุขัยโดยเฉลี่ยสูงกว่า 65 ปี กับที่เหลือ")

col = st.columns(2)
with col[0] :
    code = '''
    data2007 = gapminder[gapminder['year']==2007]
    data_bar = data2007[['country','lifeExp']].groupby('country').mean().reset_index()
    data_bar['lifeExpMoreThan65'] = data_bar['lifeExp'].apply(lambda x : "TRUE" if x > 65 else "FALSE")
    data_bar['lifeExpMoreThan65'] = pd.Categorical(
        data_bar['lifeExpMoreThan65'],
        categories=('TRUE','FALSE'),
        ordered=True
    )
    data_bar = data_bar.groupby('lifeExpMoreThan65').size().reset_index().rename(columns={0 : 'Count'})
    fig = go.Figure(
        [
            go.Bar(
                x = data_bar['lifeExpMoreThan65'],
                y = data_bar['Count'],
                text=data_bar['Count'], 
                textposition='auto'
            )
        ]
    )

    fig.update_layout(
        title="Bar plot",
        xaxis_title="อายุไขโดยเฉลี่ยสูงกกว่า 65 ปี",
        yaxis_title="จำนวน",
        yaxis=dict(
            tickformat=',',
        ))'''
    st.code(code, language="python")

with col[1] :
    data2007 = gapminder[gapminder['year']==2007]
    data_bar = data2007[['country','lifeExp']].groupby('country').mean().reset_index()
    data_bar['lifeExpMoreThan65'] = data_bar['lifeExp'].apply(lambda x : "TRUE" if x > 65 else "FALSE")
    data_bar['lifeExpMoreThan65'] = pd.Categorical(
        data_bar['lifeExpMoreThan65'],
        categories=('TRUE','FALSE'),
        ordered=True
    )
    data_bar = data_bar.groupby('lifeExpMoreThan65').size().reset_index().rename(columns={0 : 'Count'})
    fig = go.Figure(
        [
            go.Bar(
                x = data_bar['lifeExpMoreThan65'],
                y = data_bar['Count'],
                text=data_bar['Count'], 
                textposition='auto'
            )
        ]
    )

    fig.update_layout(
        title="Bar plot",
        xaxis_title="อายุไขโดยเฉลี่ยสูงกกว่า 65 ปี",
        yaxis_title="จำนวน",
        yaxis=dict(
            tickformat=',',
        ))

    st.write(fig)

# -----------------------------------------------------------------
st.markdown("2. สร้าง barchart แสดงค่าเฉลี่ยของ gdpPercap จำแนกตามทวีป")
col = st.columns(2)

with col[0] :
    code = '''
    data2 = gapminder[['continent','gdpPercap']].groupby('continent').mean().reset_index()
    data2['gdpPercap'] = round(data2['gdpPercap'],2)
    fig = go.Figure(
        [
            go.Bar(
                x = data2['continent'],
                y = data2['gdpPercap'],
                text=data2['gdpPercap'], 
                textposition='auto',
                marker_color=px.colors.qualitative.Light24
            )
        ]
    )

    fig.update_layout(
        title="Bar plot",
        xaxis_title="ทวีป",
        yaxis_title="gdpPercap โดยเฉลี่ย",
        yaxis=dict(
            tickformat=',',
        ))'''
    st.code(code, language="python")

with col[1] :


    data2 = gapminder[['continent','gdpPercap']].groupby('continent').mean().reset_index()
    data2['gdpPercap'] = round(data2['gdpPercap'],2)
    fig = go.Figure(
        [
            go.Bar(
                x = data2['continent'],
                y = data2['gdpPercap'],
                text=data2['gdpPercap'], 
                textposition='auto',
                marker_color=px.colors.qualitative.Light24
            )
        ]
    )

    fig.update_layout(
        title="Bar plot",
        xaxis_title="ทวีป",
        yaxis_title="gdpPercap โดยเฉลี่ย",
        yaxis=dict(
            tickformat=',',
        ))

    st.write(fig)

# ----------------------------------------------------------
st.markdown("3. สร้าง barchart แสดงแนวโน้ม gdpPercap ของประเทศไทยในช่วงปีที่เก็บรวบรวมข้อมูล")
col = st.columns(2)
with col[0] :
    code = '''
    data3 = gapminder[gapminder['country'] == 'Thailand']
    fig = go.Figure(
        [
            go.Bar(
                x = data3['year'],
                y = data3['gdpPercap'],
                text=data3['gdpPercap'], 
                textposition='auto'
            )
        ]
    )


    fig.update_layout(
        title="Bar plot",
        xaxis_title="ปี",
        yaxis_title="gdpPercap โดยเฉลี่ย",
        yaxis=dict(
            tickformat=',',
        ))
    fig.update_xaxes(
        type='category'
        )'''
    st.code(code, language="python")

with col[1] :
    data3 = gapminder[gapminder['country'] == 'Thailand']
    data3['gdpPercap'] = round(data3['gdpPercap'],2)
    fig = go.Figure(
        [
            go.Bar(
                x = data3['year'],
                y = data3['gdpPercap'],
                text=data3['gdpPercap'], 
                textposition='auto'
            )
        ]
    )


    fig.update_layout(
        title="Bar plot",
        xaxis_title="ปี",
        yaxis_title="gdpPercap โดยเฉลี่ย",
        yaxis=dict(
            tickformat=',',
        ))
    fig.update_xaxes(
        type='category'
        )

    st.write(fig)

# ------------------------------------------------------------
st.markdown("4. สร้าง boxplot เปรียบเทียบการแจกแจงของ lifeExp ระหว่างประเทศที่มี gdpPercap สูงกว่าค่าเฉลี่ยของโลกในปี 2007 กับที่เหลือ")

col = st.columns(2)

with col[0] :
    code = '''
    mean2007 = gapminder[gapminder['year']==2007]['gdpPercap'].mean()
    data4 = data2007
    data4['gdpPercapMoreThanMean'] = data4['gdpPercap'].apply(lambda x : "TRUE" if x > mean2007 else "FALSE")
    myorder = ('TRUE','FALSE')
    data4['gdpPercapMoreThanMean'] = pd.Categorical(data4['gdpPercapMoreThanMean'],
                                                    categories = myorder,
                                                    ordered=True
                                                    )

    mycolor = ('#636EFA','#EF553B')
    fig = px.box(data4, 
                x="gdpPercapMoreThanMean", 
                y="lifeExp", 
                color='gdpPercapMoreThanMean',
                color_discrete_map = {e:mycolor[i] for i,e in enumerate(myorder)},
                category_orders={"gdpPercapMoreThanMean": myorder})
    fig.update_layout(
        title="Boxplot",
        xaxis_title = "gdpPercap สูงกว่า ค่าเฉลี่ยโลก (%.2f)"%mean2007,
        yaxis_title="lifeExp",
        yaxis=dict(
            tickformat=',',
        ))

    fig.update_xaxes(
        type='category'
        )'''
    st.code(code, language="python")

with col[1] :
    mean2007 = gapminder[gapminder['year']==2007]['gdpPercap'].mean()
    data4 = data2007
    data4['gdpPercapMoreThanMean'] = data4['gdpPercap'].apply(lambda x : "TRUE" if x > mean2007 else "FALSE")
    myorder = ('TRUE','FALSE')
    data4['gdpPercapMoreThanMean'] = pd.Categorical(data4['gdpPercapMoreThanMean'],
                                                    categories = myorder,
                                                    ordered=True
                                                    )

    mycolor = ('#636EFA','#EF553B')
    fig = px.box(data4, 
                x="gdpPercapMoreThanMean", 
                y="lifeExp", 
                color='gdpPercapMoreThanMean',
                color_discrete_map = {e:mycolor[i] for i,e in enumerate(myorder)},
                category_orders={"gdpPercapMoreThanMean": myorder})
    fig.update_layout(
        title="Boxplot",
        xaxis_title = "gdpPercap สูงกว่า ค่าเฉลี่ยโลก (%.2f)"%mean2007,
        yaxis_title="lifeExp",
        yaxis=dict(
            tickformat=',',
        ))

    fig.update_xaxes(
        type='category'
        )

    st.write(fig)


# --------------------------------------------------------------
