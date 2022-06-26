import pandas as pd
import plotly.express as px

import datetime as dt
from dash import Dash , html,  dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

#define nome do app usando o nome do arquivo
app = Dash(__name__)
server = app.server

# LENDO OS DATAFRAMES IMPORTADOS DA ANALISE FEITA
df = pd.read_csv('dfEvasao.csv')
dfCotasPie = pd.read_csv('dfCotasPie.csv')
dfIngresso = pd.read_csv('dfIngresso.csv')

# CRIACAO DOS GRAFICOS
fig = px.bar(df, x='ANO_EVASAO',y='ALUNOS',color='FORMA_EVASAO', barmode='group')

fig2 = px.pie(  df, values=df['ALUNOS'], 
                names=df['FORMA_EVASAO'], 
                title=' Situacao de matricula dos Alunos de Sistema de Informacao da UNIRIO',
                color=df['FORMA_EVASAO'],
                labels={
                    'FORMA_EVASAO' : 'Situacao',
                    'value' : 'Alunos'
                })

fig3 =go.Figure(go.Sunburst(
    ids=[
        'Discentes',
        'Ampla Concorrencia',
        'Outras Formas de Ingresso',
        'Cotistas',

        'EN - ENEM',
        'SISU Ampla Concorrencia',
        'VE - Vestibular',

        'Outros', 

        'SISU Escola Publica - Indep. de Renda', 
        'SISU Escola Publica até 1,5 S.M.',
        'SISU Escola Publica até 1,5 S.M. Preto, Pardo, Indígena',
        'SISU Escola Publica, Indep de Renda: Preto, Pardo, Indígena',
        'SISU Escola Pública até 1,5 S.M Preto e Pardo', 
        'SISU Escola Pública até 1,5 S.M Índio',
        'SISU Escola Pública, Indep. de Renda : Preto e Pardo', 
        'SISU Escola Pública, Indep. de Renda : Índio'
        ],

    labels=[
        'Discentes',
        'Ampla<br>Concorrencia',
        'Outras<br>Formas<br>de<br>Ingresso',
        'Cotistas',

        'ENEM',
        'SISU<br>Ampla<br>Concorrencia',
        'Vestibular',

        'Outros', 

        'SISU<br>Escola<br>Publica<br>Indep. de Renda', 
        'SISU<br>Escola<br>Publica<br>até 1,5 S.M.',
        'SISU<br>Escola<br>Publica<br>até 1,5 S.M.<br>Preto,Pardo,<br>Indígena',
        'SISU<br>Escola<br>Publica<br>Indep de Renda:<br>Preto, Pardo,<br>Indígena',
        'SISU<br>Escola<br>Publica<br>até 1,5 S.M Preto e Pardo', 
        'SISU<br>Escola<br>Publica<br>até 1,5 S.M Índio',
        'SISU<br>Escola<br>Publica<br>Indep. de Renda<br>Preto e Pardo', 
        'SISU<br>Escola<br>Publica<br>Indep. de Renda<br>Índio'
        ],

    parents=[
        '',
        'Discentes',
        'Discentes',
        'Discentes',

        'Ampla Concorrencia',
        'Ampla Concorrencia',
        "Ampla Concorrencia",

        'Outras Formas de Ingresso', 

        "Cotistas", 
        "Cotistas", 
        "Cotistas", 
        "Cotistas",
        "Cotistas", 
        "Cotistas",
        "Cotistas", 
        "Cotistas"],

    values=[1260, 924, 40 , 296 , 248 , 323 , 353,  40 , 78, 63, 34, 35, 37, 5, 40, 4],

    domain=dict(column=1),
    maxdepth=3,
    hovertemplate='<b>%{label} </b> <br> Alunos: %{value}<br>',
    name='',
    branchvalues="total",
))
fig3.update_layout(margin = dict(t=0, l=0, r=0, b=0))

# fig4 = px.pie(dfCotasPie, values=dfCotasPie['ALUNOS'],
#                 names= dfCotasPie['FORMA_INGRESSO'] ,
#                 title='Quantidade de aluno por forma de ingresso',
#                 color=dfCotasPie['FORMA_INGRESSO'],
#                 labels={
#                     'FORMA_INGRESSO' : 'Modalidade',
#                     'value' : 'Alunos'
#                 })

fig3.update_traces(hoverinfo='label',  textfont_size=18)
# fig3.update_layout( 
#         font=dict(family="Courier New, monospace",size=23,color="RebeccaPurple"),
#         #grid= dict(columns=2, rows=1),
#         #margin = dict(t=0, l=0, r=0, b=0)
#     ) 


fig2.update_traces(hoverinfo='label', textinfo='percent', textfont_size=20)
fig2.update_layout( 
        font=dict(
        family="Courier New, monospace",
        size=23,
        color="RebeccaPurple"
    ))

#criando APLICAO WEB
app.layout= html.Div(children=[
                html.H1(
                    children="Aplicacao WEB com análises dos dados do curso de BSI", style={'textAlign': 'center'}
                ),
                html.Br(),
                html.H2(
                    children="Dados disponibilizados pela EIA de acordo com as normas previstas na LGPD"
                ),
                html.Div(
                    id='output_container_div', 
                    children=[], 
                    style=dict(display='flex', justifyContent='center')),
                html.Br(),
                dcc.Graph(
                    id='my_bsi_graph', 
                    figure=fig
                ),
                html.Br(),
                html.Div(
                    html.Div(
                        dcc.Graph(
                            id='my_bsi_pizza_graph',
                            figure=fig2,
                            style={"width": "100%", "height": "100%"}
                        ),
                        style={"width": "100%","height": "100%",},
                    ),
                    style={"width": "85%","height": "800px","display": "inline-block","paddingTop": "5px","paddingLeft": "1px","overflow": "hidden"}
                ),    
                html.Div(
                    html.Div(
                        dcc.Graph(
                            id='sunburst',
                            figure=fig3,
                            style={"width": "100%", "height": "100%"}
                        ),
                        style={"width": "100%","height": 
                        "100%",},
                    ),
                    style={"width": "95%","height": "1000px","display": "inline-block","padding-top": "5px","padding-left": "1px","overflow": "hidden"}
                )
            ])


if __name__ == '__main__':
    app.run_server(debug=True)