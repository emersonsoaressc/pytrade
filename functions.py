#Funções utilizadas para o projeto

import pandas as pd 
import sgs
import plotly.graph_objects as go
import streamlit as st


### ==== FUNÇÃO PARA CRIAR DATAFRAMES A PARTIR DE BASE DE DADOS SGS BACEN ==== ###
def df_sgs(lista_sgs,ano_inicio, ano_fim, name):
    df = pd.DataFrame()
    for i in lista_sgs:
        data_inicio = ano_inicio
        data_fim = ano_fim
        split = i.split(sep='-')
        df1 = sgs.time_serie(split[0], data_inicio, data_fim,True)
        df1 = pd.DataFrame(df1)
        df1 = df1.rename(columns={f'{split[0]}':f'{split[1]}'})
        df = pd.concat([df,df1], axis=1)
    return df.to_csv(f'base_csv/base_{name}.csv')


### ==== FUNÇÃO PARA GERAR BASE DE DADOS ==== ###
def gera_base(ano_inicio, ano_fim):
    inicio = ano_inicio
    fim = ano_fim
    cod_list = pd.read_csv('base_csv/cod_ipca.csv', sep=';').set_index('codigo')
    df_sgs(cod_list['lista'], f'01/01/{inicio}', f'01/01/{fim}', 'ipca')
    df_base = pd.read_csv('base_csv/base_ipca.csv', encoding='UTF-8', sep=',', index_col=0)
    return df_base


### ==== FUNÇÃO PARA CRIAR GRÁFICOS DO PLOTLY A PARTIR DE BASE DE DADOS SGS BACEN ==== ###
def graf_plotly(data_frame, titulo):
    fig = go.Figure()
    fig.update_layout(
    title= f'{titulo}', 
    
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        #title= '%',
        showgrid=False,
        zeroline=True,
        showline=True,
        showticklabels=True,
    ),
    autosize=True,
    margin=dict(
        autoexpand=True,
        l=100,
        r=20,
        t=110,
    ),
    showlegend=True,
    plot_bgcolor='white',
    legend= dict(
        font=dict(
            family='Arial',
            size=9)
    )
    )
    count = 0
    for i in data_frame.columns:
        if count < 2:
            count += 1
            lines = fig.add_trace(go.Scatter(x=data_frame.index, y=data_frame[f'{i}'], name= f"{i}", mode="markers+lines", visible=True))
        elif count == 2:
            count += 1
            lines = fig.add_trace(go.Scatter(x=data_frame.index, y=data_frame[f'{i}'], name= f"{i}", mode="lines", visible=True))
        elif count >2:
            count += 1
            lines = fig.add_trace(go.Scatter(x=data_frame.index, y=data_frame[f'{i}'], name= f"{i}", mode="lines", visible='legendonly'))
    return lines
   

