import pandas as pd
import plotly.express as px

import datetime as dt
from dash import Dash , html,  dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

#define nome do app usando o nome do arquivo
app = Dash(__name__)
server = app.server
#pandas lendo nosso CSV
df = pd.read_csv('dfEvasao.csv')
dfPura = pd.read_csv('dfFormaEvPura.csv')
dfCotasPie = pd.read_csv('dfCotasPie.csv')

fig = px.bar(df, x='ANO_EVASAO',y='ALUNOS',color='FORMA_EVASAO', barmode='group')
fig4 = px.pie(dfCotasPie, values=dfCotasPie['ALUNOS'],
                names= dfCotasPie['FORMA_INGRESSO'] ,
                title='Quantidade de aluno por forma de ingresso',
                color=dfCotasPie['FORMA_INGRESSO'],
                labels={
                    'FORMA_INGRESSO' : 'Modalidade',
                    'value' : 'Alunos'
                }
        )
fig4.update_traces(hoverinfo='label', textinfo='percent', textfont_size=20)
fig4.update_layout( 
        font=dict(
        family="Courier New, monospace",
        size=13,
        color="RebeccaPurple"
    ))  ,
                                            
fig3 = px.pie(  dfPura, values=dfPura['ALUNOS'], 
                names=dfPura['FORMA_EVASAO'], 
                title='Situacao dos Alunos de Sistema de Informacao',
                color=dfPura['TIPO_EVASAO'],
                labels={
                                                    'FORMA_EVASAO' : 'Situacao',
                                                    'value' : 'Alunos'
                                                }
        )
fig3.update_traces(hoverinfo='label', textinfo='percent', textfont_size=20)
fig3.update_layout( 
        font=dict(
        family="Courier New, monospace",
        size=23,
        color="RebeccaPurple"
    ))
#criando app
app.layout = html.Div(children=[
    html.H1(children="Aplicacao WEB com análises dos dados do curso de BSI", style={'text-align': 'center'}),
    html.Br(),

    html.H2(children="Dados disponibilizados pela EIA de acordo com as normas previstas na LGPD"),
  
    html.Div(id='output_container_div', children=[],
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
                figure=fig3,
                style={
                    "width": "100%",
                    "height": "100%"
                }
            ),
            style={
                "width": "100%",
                "height": "100%",
            },
        ),
        style={
                "width": "85%",
                "height": "800px",
                "display": "inline-block",
                "padding-top": "5px",
                "padding-left": "1px",
                "overflow": "hidden"
            }
    ),

    html.Br(),
    html.Div(
        html.Div(
            dcc.Graph(
                id='cotasPie',
                figure=fig4,
                style={
                    "width": "100%",
                    "height": "100%"
                }
            ),
            style={
                "width": "100%",
                "height": "100%",
            },
        ),
        style={
                "width": "85%",
                "height": "800px",
                "display": "inline-block",
                "padding-top": "5px",
                "padding-left": "1px",
                "overflow": "hidden"
            }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

