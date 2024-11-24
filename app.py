import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import yfinance as yf

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.FLATLY])

server = app.server

Ticket = 'GOOG'
start_date = '2020-01-01'
end_date = '2023-12-31'


Base_Dados = yf.download( Ticket, start=start_date, end=end_date )


Base_Dados.head()

names = Base_Dados.columns
print(names)


Base_Dados.columns = [f"{price}_{ticker}" for price, ticker in Base_Dados]
df_new = Base_Dados.rename(columns = {"Adj Close_GOOG":'Adj_Close',"Close_GOOG":'Close', "High_GOOG":'High','Low_GOOG':'Low', 'Open_GOOG':'Open', 'Volume_GOOG':'Volume'})

df_new = df_new.reset_index()
#df_new.columns
#df_new.info()
df_new['Date'] = df_new['Date'].dt.strftime('%Y-%m-%d')
df_new.set_index('Date', inplace=True)

#df_new.info()

templattee = load_figure_template('flatly')


## Layout ##
app.layout = dbc.Container( children=[
    dbc.Row([
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Img(id="logo", src=app.get_asset_url("google-logo-1.png"), height=80, style={'margin-top':"20px"}),
                    html.H2(children="Calendário",style={'margin-top':"100px"} ),
                    html.H5(children="Escolha a data:", style={'margin-top':"20px"}),
                    dcc.DatePickerRange(
                id="date-picker-select",
                start_date=start_date,
                end_date=end_date,
                min_date_allowed=start_date,
                max_date_allowed=end_date,
                initial_visible_month=None,
                
            ),
                ])
            ], style = {'height': '97vh','margin-top':'10px'}),
        ],sm=12, md=3),
    
        dbc.Col([dbc.Row([
            dbc.Card([
                dbc.CardBody([
                    html.H1("Fechamento das ações do Google", style={'font-size':'40px', "textAlign": "center"})
                ])
            ],style={'margin-top':'10px', 'margin-bottom':'10px', 'margin-right':'15px', 'width':"100%"} ),
        ]),
        dbc.Row([
            dbc.Card([
                dbc.CardBody([
                     dcc.Graph(id='graph', config={
                "displayModeBar": False,})
                ])
        
            ], style={'height': '79vh', 'margin-right':'10px'}),
        ])
        ],sm=12, md=6),
        dbc.Col([
        dbc.Row([
            dbc.Card([
                dbc.CardBody([
                     dcc.Graph(id='ind1')
                ],style={
                "padding": "0",       
                "margin-top": "0",    
                "padding-top": "0px", 
            })
            ], style={ 'margin-top':'10px', 'margin-right':'10px', 'margin-bottom':'10px', 'height': '47vh', "padding-top": "35px"})
        ]),
        dbc.Row([
            dbc.Card([
                dbc.CardBody([
                     dcc.Graph(id='ind2')
                ])
            ], style={'margin-right':'10px', 'margin-bottom':'10px', 'height': '48vh', "padding-top": "20px"}),
        ]),
        ],sm=12, md=3)
    ])
], fluid=True, style={'height':'100%'})


###### Callback ######
@app.callback(
    Output('graph', 'figure'),
    Input('date-picker-select', 'start_date'),
    Input('date-picker-select', 'end_date')
)
def update_graph(start_date, end_date):
    filtered_df = df_new.loc[start_date:end_date]
    


    

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=filtered_df.index,
            y=filtered_df["Close"],
            mode="lines",
            line=dict(color="#007BFF"),
            name="Preço de Fechamento",
        )
    )
    
    fig.update_layout(height=450,margin=dict(l=10, r=10, t=20, b=40),
    yaxis=dict(showgrid=True, gridcolor="lightgray"))

    return fig

@app.callback(
    Output('ind1', 'figure'),
    Input('date-picker-select', 'start_date'),
    Input('date-picker-select', 'end_date')
)
def update_ind1(start_date, end_date):
    filtered_df = df_new.loc[start_date:end_date]
    first_value = filtered_df["Open"].iloc[0]
    latest_value = filtered_df["Open"].iloc[-1]
    delta = latest_value - first_value
    delta_percentage = (delta / first_value) * 100
    if not isinstance(filtered_df.index, pd.DatetimeIndex):
        filtered_df.index = pd.to_datetime(filtered_df.index)


    indicator_fig = go.Figure(
    go.Indicator(
        mode="number+delta",
        value=latest_value,
        title={
            "text": f"Abertura das Ações<br><span style='font-size:0.8em;color:gray'>Variação acumulada</span><br><span style='font-size:0.8em;color:gray'>Período:{filtered_df.index[0].strftime('%Y-%m-%d')} a {filtered_df.index[-1].strftime('%Y-%m-%d')}</span>"
        },
        number={
            "prefix": "US$ ",
        },
        delta={
            "reference": first_value,
            "relative": True,
            "valueformat": ".1%", 
        },
        domain={"x": [0, 1], "y": [0, 1]},
    )
)
    indicator_fig.update_layout(xaxis=dict(showgrid=False), height=250)
    return indicator_fig



@app.callback(
    Output('ind2', 'figure'),
    Input('date-picker-select', 'start_date'),
    Input('date-picker-select', 'end_date')
)
def update_ind1(start_date, end_date):
    filtered_df = df_new.loc[start_date:end_date]
    first_value = filtered_df["Close"].iloc[0]
    latest_value = filtered_df["Close"].iloc[-1]
    delta = latest_value - first_value
    delta_percentage = (delta / first_value) * 100
    if not isinstance(filtered_df.index, pd.DatetimeIndex):
        filtered_df.index = pd.to_datetime(filtered_df.index)


    indicator_fig = go.Figure(
    go.Indicator(
        mode="number+delta",
        value=latest_value,
        title={
            "text": f"Fechamento das Ações<br><span style='font-size:0.8em;color:gray'>Variação acumulada</span><br><span style='font-size:0.8em;color:gray'>Período:{filtered_df.index[0].strftime('%Y-%m-%d')} a {filtered_df.index[-1].strftime('%Y-%m-%d')}</span>"

        },
        number={
            "prefix": "US$ ",
        },
        delta={
            "reference": first_value,
            "relative": True,
            "valueformat": ".1%",
        },
        domain={"x": [0, 1], "y": [0, 1]},
    )
)
    indicator_fig.update_layout(xaxis=dict(showgrid=False), height=250)
    return indicator_fig




# Run server
if __name__ == '__main__':
    app.run_server(debug=True)