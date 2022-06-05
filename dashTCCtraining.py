import pandas as pd
import plotly.express as px

import datetime as dt
from dash import Dash , html,  dcc
from dash.dependencies import Input, Output

app = Dash(__name__)


df = pd.read_csv('dfEvasao.csv')
df2 = pd.read_csv('dfFormaEv.csv')
app.layout = html.Div([

    html.H1("Aplicacao WEB com análises dos dados do curso de BSI", style={'text-align': 'center'}),

    html.Br(),

    html.H2("Dados disponibilizados pela EIA de acordo com as normas previstas na LGPD"),

    dcc.Dropdown(id='slct_year',
                options=[
                    {"label": "2003", "value": 2003},
                    {"label": "2004", "value": 2004},
                    {"label": "2005", "value": 2005},
                    {"label": "2006", "value": 2006},
                    {"label": "2007", "value": 2007},
                    {"label": "2008", "value": 2008},
                    {"label": "2009", "value": 2009},
                    {"label": "2010", "value": 2010},
                    {"label": "2011", "value": 2011},
                    {"label": "2012", "value": 2012},
                    {"label": "2013", "value": 2013},
                    {"label": "2014", "value": 2014},
                    {"label": "2015", "value": 2015},
                    {"label": "2016", "value": 2016},
                    {"label": "2017", "value": 2017},
                    {"label": "2018", "value": 2018},
                    {"label": "2019", "value": 2019},
                    {"label": "2020", "value": 2020},
                    {"label": "2021", "value": 2021},
                    ],
                    multi= False,
                    value = 2021,
                    style={'width':"40%"}
                ),

    html.Div(id='output_container_div', children=[],
     style=dict(display='flex', justifyContent='center', width='200px',)),

    html.Br(),

    dcc.Graph(id='my_bsi_graph', figure={})
    #,style={'width': '80vh', 'height': '50vh'}
    

])

@app.callback(
    [Output(component_id='output_container_div', component_property='children'),
     Output(component_id='my_bsi_graph', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd): #option selected is the value up here
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["ANO_EVASAO"] == option_slctd]


    # fig = px.histogram(dff2, x='date', range_x=[inicio,fim])
    # fig = fig.update_layout(bargap=0.2)

    fig = px.bar(dff, x='ANO_EVASAO',y='ALUNOS',color='FORMA_EVASAO')

    #fig = px.timeline(dff, x_start="INICIO", x_end="FIM", y="ALUNOS", size='M12', autobinx=False)
    # # Plotly Express
    # fig = px.choropleth(
    #     data_frame=dff,
    #     locationmode='USA-states',
    #     locations='state_code',
    #     scope="usa",
    #     color='Pct of Colonies Impacted',
    #     hover_data=['State', 'Pct of Colonies Impacted'],
    #     color_continuous_scale=px.colors.sequential.YlOrRd,
    #     labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
    #     template='plotly_dark'
    # )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)

