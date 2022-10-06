import pandas as pd
import numpy as np
import os
import plotly.express as px
import streamlit as st
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go

def plot_map(df_filtered, scope='europe'):
    hover_data = ["happiness_rank","happiness_score", 'country']

    fig = px.choropleth(df_filtered,
                        locations=df_filtered["country"],
                        locationmode="country names",
                        projection="natural earth",
                        custom_data=hover_data,
                        hover_name=df_filtered["country"],
                        color="happiness_rank",
                        color_continuous_scale=px.colors.sequential.RdBu[::-1],
                        scope=scope,
                        #title='AZERTYUI',
                       animation_frame='year'
                       )
    fig.update_layout(title_text='Happiness Rank for countries in the world',
                      coloraxis_colorbar=dict(title="Rank"),
                      height=700)

    fig.update_traces(
        hovertemplate="<br>".join([
            "Country : %{customdata[2]}",
            "Rank : %{customdata[0]}",
            "Score : %{customdata[1]:.2f}",
        ])
    )
    st.plotly_chart(fig, use_container_width=True)
    
    
def plot_score(df_interest):

    fig = px.box(df_interest,
                 x="happiness_score",
                 y="country",
                 color="country",
                 color_discrete_sequence=px.colors.qualitative.G10,
                 points='all')
    fig.update_traces(boxmean=True,
                      whiskerwidth=0.7,
                      marker_size=7,
                line_width=3
                      )
    fig.update_layout(height=700,
                      showlegend=False,
                      xaxis=dict(showticklabels = True,
                                 showgrid=True,
                                 zeroline=False,
                                gridwidth=2),
                      yaxis=dict(showticklabels = False,
                                 showgrid=False,
                                 zeroline=False,
                                visible=False),
                      title="Distribution of happiness score by region")
    
    fig.add_annotation(x=7.578, y=5.35,
            text="Denmark",
            showarrow=False,
            arrowhead=1)
    fig.add_annotation(x=7.493, y=4.35,
            text="Norway",
            showarrow=False,
            arrowhead=1)
    fig.add_annotation(x=7.645, y=3.35,
            text="Finland",
            showarrow=False,
            arrowhead=1)
    fig.add_annotation(x=7.348, y=2.35,
            text="Sweden",
            showarrow=False,
            arrowhead=1)
    fig.add_annotation(x=6.583, y=1.35,
            text="France",
            showarrow=False,
            arrowhead=1)
    fig.add_annotation(x=5.394, y=0.35,
            text="World",
            showarrow=False,
            arrowhead=1)
    fig.update_annotations(font_size=20)
    fig.update_layout(
    margin=dict(l=0, r=0, t=60, b=75))
    st.plotly_chart(fig, use_container_width=True)
    
    
def evol(df_plot): 
    fig = px.line(df_plot, x="year", y="happiness_score", facet_row="country",height=700, width=300)
    fig.update_xaxes(visible=False, fixedrange=False)
    fig.update_yaxes(visible=False, fixedrange=False)
    fig.update_layout(annotations=[], overwrite=True)
    fig.update_layout(
    margin=dict(l=0, r=0, t=60, b=75),
    title="Score evolution per year")
    fig.update_yaxes(matches=None)
    st.plotly_chart(fig, use_container_width=True)
    
def plot_heat_corr(happiness_df, region=[]):
    import numpy as np
    if len(region)==0:
        df = happiness_df
    else:
        df = happiness_df[happiness_df['country'].isin(region)]
    if 'France' in (region):
        temp = df[['happiness_score','economy', 'health', 'social_support', 'freedom', 'trust', 'generosity', 'Population (2020)']]
    else:
        temp = df[['happiness_score','economy', 'health', 'social_support', 'freedom', 'trust', 'generosity']]
    corr=temp.corr()
    corr=corr.drop('happiness_score')
    cols=corr.columns[1:]
    corr=(corr[['happiness_score']])
    fig = go.Figure(data=go.Heatmap(
        x=['Happiness Score'],
        y=cols,
        z=corr,
        colorscale=px.colors.diverging.Spectral,
        zmin=-1,
        zmax=1
    ))
    #corr = corr.drop('happiness_score')
    corr = corr.round(2)
    fig.update_traces(text=corr.values, texttemplate="%{text}",textfont_size=25)
    fig.update_layout(
    autosize=False,
    width=300,
    height=600)
    fig.update_traces(showscale=False)
    fig.update_layout(
    margin=dict(l=150, r=0, t=40, b=0),
    title="Correlation with happiness")
    st.plotly_chart(fig, use_container_width=False)

    
def bubble(happiness_df, region, xaxis='economy', yaxis='health'):
    if len(region)==0:
        df = happiness_df
    else:
        df = happiness_df[happiness_df['country'].isin(region)]
        
    if xaxis == 'economy' or yaxis=='economy':    
        fig = px.scatter(df, x=xaxis, y=yaxis, color="happiness_score", animation_frame='year',
                     hover_name="country", size_max=30, height=600,
                    range_x=[-0.1,2],
                    range_y =[-0.1,1.1],
                        color_continuous_scale=px.colors.sequential.RdBu)
    else:
        fig = px.scatter(df, x=xaxis, y=yaxis, color="happiness_score", animation_frame='year',
                     hover_name="country", size_max=30, height=600,
                    range_x=[-0.1,0.8],
                    range_y =[-0.1,0.8],
                        color_continuous_scale=px.colors.sequential.RdBu)
    fig.update_traces(marker=dict(size=15, line=dict(width=1), opacity=0.8))
    fig.update_layout(xaxis=dict(gridwidth=2),
                      yaxis=dict(gridwidth=2),
                      title=f"{xaxis} VS {yaxis} colored by happiness score")
    if 'France' in region or len(region)==0:
        x = float(df[df['country']=='France'][xaxis])
        y = float(df[df['country']=='France'][yaxis])
        fig.add_annotation(x=x, y=y,
            text="France",
            showarrow=True,
            arrowhead=1,
            arrowsize=3,
            arrowwidth=2,

                           
                          )
    fig.update_annotations(font_size=20)
    fig.update_layout(
    margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
def bubble2(happiness_df, region):
    if len(region)==0:
        df = happiness_df
    else:
        df = happiness_df[happiness_df['country'].isin(region)]
    fig = px.scatter(df, x="freedom", y="trust", color="happiness_score", animation_frame='year',
                 hover_name="country", size_max=30, height=600)
                #range_x=[min(df.economy)-0.1,max(df.economy)+0.1],
                #range_y =[min(df.health)-0.05, max(df.health)+0.05])
    fig.update_traces(marker=dict(size=15, line=dict(width=1), opacity=0.8))
    fig.update_layout(xaxis=dict(gridwidth=2),
                      yaxis=dict(gridwidth=2),
                      title="Freedom VS Trust colored by happiness score")
    fig.update_layout(
    margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
    
def filter_row(df, column_name, condition):
    return df[df[column_name] == condition]

import plotly.graph_objects as go

def plot_bar_criteria(df_interest, countries_of_interest, criteria_list, title):
    df_interest = df_interest.rename(columns={'trust':'corruption'})
    fig = go.Figure()
    
    for country in countries_of_interest:
        stats = filter_row(df_interest, 'country', country).describe()
        mean = stats.loc['mean']
        std = stats.loc['std']

        fig.add_trace(go.Bar(
            name=f'{country}',
            x=criteria_list, y=mean[criteria_list],
            error_y=dict(type='data', array=std[criteria_list])
        ))

    fig.update_layout(barmode='group',
                      title=title)
    fig.update_layout(
    margin=dict(l=0, r=0, t=60, b=0), height=350)
    st.plotly_chart(fig, use_container_width=True)


def sunshine(sunshine_df):
    
    countries_sun = ['Finland', 'Denmark', 'Sweden', 'France']

    months = ['Jan', 'Feb','Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    L = []
    for c in countries_sun:
        df = sunshine_df[sunshine_df['country']==c]
        l = []
        for m in months : 
            l.append(int(df[m]))
        L.append(l)
    
    fig = go.Figure()
    for i, n in enumerate(countries_sun):
        fig.add_trace(go.Scatter(x=months, y=L[i],
                            mode='lines',
                            name=n))
    fig.update_layout(
                      title='Sunshine hours per month')
    fig.update_layout(
    margin=dict(l=0, r=0, t=50, b=0), height=350)
    st.plotly_chart(fig, use_container_width=True)
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    