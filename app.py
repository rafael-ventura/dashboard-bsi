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
dfPrinc = pd.read_csv('dados/dfPrincipal.csv')
dfEvasoes = pd.read_csv('dados/evasoesDF.csv')
dfGenero = pd.read_csv('dados/generoDF.csv')
dfIdade = pd.read_csv('dados/idadeDF.csv')

# CRIACAO DOS GRAFICOS
evasaoFig = px.pie( dfEvasoes, values='ALUNOS', names='FORMA_EVASAO', 
                    title='Situacao de Conclusão de curso de todos os alunos',
                    color_discrete_sequence=px.colors.sequential.RdBu,
                    labels={
                    'FORMA_EVASAO' : 'Situacao',
                    'VALUE' : 'Alunos',
                    })

generoFig = px.pie( dfGenero, values='ALUNOS', names='SEXO', 
                    title='Análise da distribuicao de genero entre os alunos do curso',
                    labels={
                        'SEXO' : 'Genero',
                        'VALUE' : 'Alunos',
                    }
                    )
idadeFig = px.bar(dfIdade ,x='IDADE', y='ALUNOS', 
                    title='Perfil de Idade dos Alunos',
                     hover_data=['PERCENT'],
                    labels={
                        'PERCENT' : 'PERCENTUAL'
                    })


evasaoFig.update_traces(hoverinfo='label', textinfo='percent', textfont_size=20)
evasaoFig.update_layout( 
        font=dict(
        family="Courier New, monospace",
        size=16,
        color="RebeccaPurple"
    ))
generoFig.update_traces(hoverinfo='label', textinfo='percent', textfont_size=20)
generoFig.update_layout( 
        font=dict(
        family="Courier New, monospace",
        size=16,
        color="Black"
    ))


idadeFig.update_layout( 
        font=dict(
        family="Courier New, monospace",
        size=16,
        color="Black"
    ))

#criando APLICAO WEB
app.layout= html.Div(children=[
                html.H1(
                    children="Dashboard com análises dos dados do curso de BSI-UNIRIO", style={'textAlign': 'center'}
                ),
                html.Br(),
                html.H2(
                    children="Dados disponibilizados pela EIA de acordo com as normas previstas na LGPD"
                ),
                html.Br(),
                html.H2(
                    children="Os dados utilizados correspondem a todos os discentes matriculados de 2001 até 2021"
                ),
                html.Div(
                    html.Div(
                        dcc.Graph(
                            id='evasaoChart',
                            figure=evasaoFig,
                            style={"width": "50%", "height": "100%"}
                        ),
                        style={"width": "100%","height": "100%",},
                    ),
                    style={"width": "85%","height": "600px","display": "inline-block","paddingTop": "5px","paddingLeft": "1px","overflow": "hidden"}
                ),
                html.Div(
                    html.Div(
                        dcc.Graph(
                            id='generoChart',
                            figure=generoFig,
                            style={"width": "50%", "height": "100%"}
                        ),
                        style={"width": "100%","height": "100%",},
                    ),
                    style={"width": "85%","height": "600px","display": "inline-block","paddingTop": "5px","paddingLeft": "1px","overflow": "hidden"}
                ),
                html.Div(
                    html.Div(
                        dcc.Graph(
                            id='idadeChart',
                            figure=idadeFig,
                            style={"width": "50%", "height": "100%"}
                        ),
                        style={"width": "100%","height": "100%",},
                    ),
                    style={"width": "85%","height": "600px","display": "inline-block","paddingTop": "5px","paddingLeft": "1px","overflow": "hidden"}
                ),
            ])


if __name__ == '__main__':
    app.run_server(debug=True)