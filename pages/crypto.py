import dash
from dash import html,dcc,Input,Output,callback,dash_table
import dash_bootstrap_components as dbc
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import warnings
from dash.exceptions import PreventUpdate
from datetime import datetime
warnings.filterwarnings('ignore')


crypto_dict = {
    'Bitcoin':'BTC-USD',
    'Ethereum':'ETH-USD',
    'BNB':'BNB-USD',
    'XRP':'XRP-USD',
    'Solana':'SOL-USD',
    'Dogecoin':'DOGE-USD',
    'Polygon':'MATIC-USD',
    'Polkadot':'DOT-USD',
    'Tether':'USDT-USD',
    'USD Coin':'USDC-USD',
    'Binance USD':'BUSD-USD',
    'Cardano':'ADA-USD'
}
start_date = datetime(2022,4,1)
end_date = datetime.today()
crypto_data = yf.download(tickers=[a for a in crypto_dict.values()],start=start_date,end=end_date)
crypto_data = crypto_data.stack().reset_index()
crypto_data.rename(columns={
        'level_0':'Date',
        'level_1':'Ticker'
    },inplace=True)
dash.register_page(__name__ , name='CRYPTO')
layout = html.Div(
    [ 
        dbc.Row(
            [ 
                dbc.Col(
                    [ 
                        html.H3('Cryptocurrency Analysis Dashboard', className='text-center'),
                        dcc.Interval(id='inter',
                        n_intervals=1,
                        max_intervals=1)
                    ]
                )
            ]
        ),
        dbc.Row(
            dbc.Col(
                [ 
                    dbc.Card(
                        dbc.CardBody(
                            [ 
                                html.Div(
                                    html.H4('Crypto Rate from April',
                                    className='text-center')
                                )
                            ]
                        )
                    ),
                    dbc.Card(
                        [ 
                            dbc.CardHeader(
                                [ 
                                    html.Div(
                                        dcc.RadioItems(
                                            id='checklist',
                                            options= [ 
                                                {'label':key,'value':crypto_dict[key]}
                                                for key in crypto_dict.keys()
                                            ],
                                            style={'display':'flex'},
                                            inputStyle={'cursor':'pointer'},
                                            labelStyle={'background':'#333333',
                                            'padding':'0.4rem',
                                            'border-radius':'10%'},
                                            value='BTC-USD',
                                            persistence=True,
                                            persistence_type='session'
                                        ),
                                        style={'margin':'auto'},
                                    )
                                ]
                            ),
                            dbc.CardBody(
                                [ 
                                    dcc.Graph(
                                        id='all_g',
                                        figure = {}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ),
        dbc.Row(
            [ 
                dbc.Col(
                    [ 
                        html.H5(id='table-title',className='text-center'),
                        html.Div(id='table')
                    ]
                )
            ]
        )
    ]
)
@callback(
    Output('stored-2','data'),
    Input('checklist','value')
)
def store_data(value):
    '''Store the chosen value'''
    to_return = value
    return to_return
@callback(
    Output('all_g','figure'),
    Input('checklist','value')
)
def send_figure(value):
    df = crypto_data[crypto_data['Ticker']==value]
    trace1 = go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )
    layout11 = go.Layout(
        title=value,
        title_x=0.5,
        titlefont=dict(
            color='white',
            size=20
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            tickfont=dict(
                color='white'
            )
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(
                color='white'
            )
        )
    )
    fig = go.Figure(data=[trace1],layout=layout11)
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig
@callback(
    Output('table','children'),
    Output('table-title','children'),
    Input('checklist','value'),
    Input('inter','n_intervals')
)
def send_table(value,n_intervals):
    if value:
        table_data = yf.download(tickers=[a for a in crypto_dict.values()],period='15h',interval='1h')
        table_data = table_data.stack().reset_index()
        table_data.rename(columns={
        'level_0':'Date',
        'level_1':'Ticker'
        },inplace=True)
        table_data['time'] = table_data['Date'].dt.strftime('%H:%M')
        table_data.drop('Date',axis=1,inplace=True)
        value_data = table_data[table_data['Ticker']==value]
        value_data.drop('Ticker',axis=1,inplace=True)
        dash_t = dash_table.DataTable(
            value_data.to_dict('records'),
            [ 
                {'name':i,'id':i}
                for i in value_data.columns
            ],
            style_header={
                'backgroundColor':'rgba(0,0,0,0)'
            },
            style_data={
                'backgroundColor':'rgba(0,0,0,0)'
            },
            editable=False
        )
        table_title = f'{value} Rate in the last 12 hours'
        return dash_t,table_title
    else:
        raise PreventUpdate
    
