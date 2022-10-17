import dash
import dash_bootstrap_components as dbc
from dash import html,dcc,Output,Input,State,callback,ctx
from dash.exceptions import PreventUpdate
import pandas_datareader as web
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime,timedelta
import yfinance as yf
from dash_iconify import DashIconify

company_dict = {
    'AAPL':'https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg',
    'GOOGL':'https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg',
    'MSFT':'https://upload.wikimedia.org/wikipedia/commons/e/eb/Microsoft_Store_logo.svg',
    'AMZN':'https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg',
    'META':'https://upload.wikimedia.org/wikipedia/commons/7/7b/Meta_Platforms_Inc._logo.svg',
}
end_date = datetime.today()
start_date = datetime(2020,1,1)
stock_data = web.DataReader(['AMZN','GOOGL','META','MSFT','AAPL'],
                    'stooq', start=start_date, end=end_date)
stock_data2 = stock_data.stack().reset_index()
stock_data2['Date'] = pd.to_datetime(stock_data2['Date'])

month_data = yf.download(tickers=['AMZN','AAPL','MSFT','GOOGL','META'],period='1mo',interval='1d')
month_data2 = month_data.stack().reset_index()
month_data2.rename(columns={
        'level_0':'Date',
        'level_1':'Ticker'
    },inplace=True)

dash.register_page(__name__, name='STOCK',path='/')

layout = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H1('Stock Analysis Dashboard',className='text-center text-white'),
                                    dcc.Interval(
                                        id='inter2',
                                        n_intervals=1*3000
                                    )
                                ]
                            )
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [ 
                            dbc.Col(
                                [ 
                                    dbc.Card(
                                        dbc.CardBody(
                                            [ 
                                                html.Div(
                                                    [ 
                                                        html.H6('Open value for the past month',
                                                        style={'text-align':'center'})
                                                    ]
                                                )
                                            ]
                                        )
                                    ),
                                    dbc.Card(
                                        [ 
                                            dbc.CardHeader(
                                                [ 
                                                  dbc.Row(
                                                    [ 
                                                        dbc.Col(
                                                            [ 
                                                                html.Div(
                                                                    [ 
                                                                dcc.Dropdown(
                                                                    id='drop-1',
                                                                    options = [
                                                                        { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src='https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg',
                                                                                        style={
                                                                                            'width':'24px',
                                                                                            'height':'22px',
                                                                                            'margin-top':'3px'
                                                                                        }
                                                                                    ),
                                                                                    html.Span('Apple',
                                                                                    style={
                                                                                        'margin-left':'4px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'AAPL'
                                                                        },
                                                                        { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src='https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg'
                                                                                    ),
                                                                                    html.Span('Google',
                                                                                    style={
                                                                                        'margin-left':'4px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'GOOGL'
                                                                        },
                                                                        { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src = 'https://upload.wikimedia.org/wikipedia/commons/7/7b/Meta_Platforms_Inc._logo.svg',
                                                                                        style={
                                                                                            'width':'35px',
                                                                                            'height':'20px',
                                                                                            'margin-top':'5px'
                                                                                        }
                                                                                    ),
                                                                                    html.Span(' Meta',
                                                                                    style={
                                                                                        'margin-left':'6px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'META'
                                                                        }, 
                                                                         { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src = 'https://upload.wikimedia.org/wikipedia/commons/e/eb/Microsoft_Store_logo.svg',
                                                                                        style={
                                                                                            'width':'26px',
                                                                                            'height':'22px',
                                                                                            'margin-top':'5px'
                                                                                        }
                                                                                    ),
                                                                                    html.Span(' Microsoft',
                                                                                    style={
                                                                                        'margin-left':'6px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'MSFT'
                                                                        },
                                                                       { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src = 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg',
                                                                                        style={
                                                                                            'width':'39px',
                                                                                            'height':'22px',
                                                                                            'margin-top':'5px'
                                                                                        }
                                                                                    ),
                                                                                    html.Span(' Amazon',
                                                                                    style={
                                                                                        'margin-left':'6px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'AMZN'
                                                                        },
                                                                     ],
                                                                    style = {
                                                                         'width': '135px',
                                                                          'color': '#212121',
                                                                          'background-color': '#FFFFFF',
                                                                    },
                                                                    clearable=False,
                                                                    value = 'AAPL',
                                                                    persistence=True,
                                                                    persistence_type='session'
                                                                )
                                                            ]
                                                        )
                                                            ]
                                                        ),
                                                        dbc.Col([html.Div(
                                                            [ 
                                                                html.Div(id='text-1',
                                                                style={
                                                                    'display':'flex',
                                                                    'margin-left':'180px'
                                                                })
                                                            ]
                                                        )
                                                    ],align='end')
                                                    ]
                                                  )  
                                                ]
                                            ),
                                            dbc.CardBody(
                                                [ 
                                                    dcc.Graph(
                                                        id='graph_1',
                                                        figure={}
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ],sm=12,lg=6
                            ),
                            dbc.Col(
                                [ 
                                    dbc.Card(
                                        dbc.CardBody(
                                            [ 
                                                html.Div(
                                                    [ 
                                                        html.H6('Close Values for the past month',
                                                        style={
                                                            'text-align':'center'
                                                        })
                                                    ]
                                                )
                                            ]
                                        )
                                    ),
                                    dbc.Card(
                                        [ 
                                            dbc.CardHeader(
                                                [ 
                                                    html.Div(
                                                        [ 
                                                            html.Div(
                                                                [ 
                                                                    dcc.Dropdown(
                                                                        id='drop-2',
                                                                        options = [
                                                                        { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src='https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg',
                                                                                        style={
                                                                                            'width':'24px',
                                                                                            'height':'22px',
                                                                                            'margin-top':'3px'
                                                                                        }
                                                                                    ),
                                                                                    html.Span('Apple',
                                                                                    style={
                                                                                        'margin-left':'4px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'AAPL'
                                                                        },
                                                                        { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src='https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg'
                                                                                    ),
                                                                                    html.Span('Google',
                                                                                    style={
                                                                                        'margin-left':'4px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'GOOGL'
                                                                        },
                                                                        { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src = 'https://upload.wikimedia.org/wikipedia/commons/7/7b/Meta_Platforms_Inc._logo.svg',
                                                                                        style={
                                                                                            'width':'35px',
                                                                                            'height':'20px',
                                                                                            'margin-top':'5px'
                                                                                        }
                                                                                    ),
                                                                                    html.Span(' Meta',
                                                                                    style={
                                                                                        'margin-left':'6px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'META'
                                                                        }, 
                                                                         { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src = 'https://upload.wikimedia.org/wikipedia/commons/e/eb/Microsoft_Store_logo.svg',
                                                                                        style={
                                                                                            'width':'26px',
                                                                                            'height':'22px',
                                                                                            'margin-top':'5px'
                                                                                        }
                                                                                    ),
                                                                                    html.Span(' Microsoft',
                                                                                    style={
                                                                                        'margin-left':'6px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'MSFT'
                                                                        },
                                                                       { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src = 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg',
                                                                                        style={
                                                                                            'width':'39px',
                                                                                            'height':'22px',
                                                                                            'margin-top':'5px'
                                                                                        }
                                                                                    ),
                                                                                    html.Span(' Amazon',
                                                                                    style={
                                                                                        'margin-left':'6px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'AMZN'
                                                                        },
                                                                     ],
                                                                    style = {
                                                                         'width': '135px',
                                                                          'color': '#212121',
                                                                          'background-color': '#FFFFFF',
                                                                    },
                                                                    clearable=False,
                                                                    value = 'AAPL',
                                                                    persistence=True,
                                                                    persistence_type='session'
                                                                    )
                                                                ]
                                                            ),
                                                            html.Div(
                                                                [ 
                                                                    html.Div(id='text-2',
                                                                    style={'display':'flex'})
                                                                ]
                                                            )
                                                        ],
                                                        style={
                                                            'display':'flex',
                                                            'justify-content':'space-between'
                                                        }
                                                    )
                                                ]
                                            ),
                                            dbc.CardBody(
                                                [ 
                                                    dcc.Graph(
                                                        id='graph_2',
                                                        figure={}
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ],sm=12,lg=6
                            )
                        ],
                        align='center'
                    ),
                    html.Br(),
                    dbc.Row(
                        [ 
                            dbc.Col(
                                [ 
                                    dbc.Card(
                                        [ 
                                            dbc.CardBody(
                                                [ 
                                                    html.Div(
                                                        [ 
                                                            html.H6('Stock Rate Since 2020',
                                                            className='text-center')
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    dbc.Card(
                                        [ 
                                            dbc.CardHeader(
                                                [ 
                                                    html.Div(
                                                        dcc.Dropdown(
                                                            id='drop-3',
                                                            options = [
                                                                        { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src='https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg',
                                                                                        style={
                                                                                            'width':'24px',
                                                                                            'height':'22px',
                                                                                            'margin-top':'3px'
                                                                                        }
                                                                                    ),
                                                                                    html.Span('Apple',
                                                                                    style={
                                                                                        'margin-left':'4px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'AAPL'
                                                                        },
                                                                        { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src='https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg'
                                                                                    ),
                                                                                    html.Span('Google',
                                                                                    style={
                                                                                        'margin-left':'4px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'GOOGL'
                                                                        },
                                                                        { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src = 'https://upload.wikimedia.org/wikipedia/commons/7/7b/Meta_Platforms_Inc._logo.svg',
                                                                                        style={
                                                                                            'width':'35px',
                                                                                            'height':'20px',
                                                                                            'margin-top':'5px'
                                                                                        }
                                                                                    ),
                                                                                    html.Span(' Meta',
                                                                                    style={
                                                                                        'margin-left':'6px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'META'
                                                                        }, 
                                                                         { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src = 'https://upload.wikimedia.org/wikipedia/commons/e/eb/Microsoft_Store_logo.svg',
                                                                                        style={
                                                                                            'width':'26px',
                                                                                            'height':'22px',
                                                                                            'margin-top':'5px'
                                                                                        }
                                                                                    ),
                                                                                    html.Span(' Microsoft',
                                                                                    style={
                                                                                        'margin-left':'6px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'MSFT'
                                                                        },
                                                                       { 
                                                                            'label':
                                                                            html.Div(
                                                                                [ 
                                                                                    html.Img(
                                                                                        src = 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg',
                                                                                        style={
                                                                                            'width':'39px',
                                                                                            'height':'22px',
                                                                                            'margin-top':'5px'
                                                                                        }
                                                                                    ),
                                                                                    html.Span(' Amazon',
                                                                                    style={
                                                                                        'margin-left':'6px'
                                                                                    })
                                                                                ],
                                                                                style={'display':'flex'}
                                                                            ),
                                                                            'value':'AMZN'
                                                                        },
                                                                     ],
                                                                    style = {
                                                                         'width': '135px',
                                                                          'color': '#212121',
                                                                          'background-color': '#FFFFFF',
                                                                    },
                                                                    clearable=False,
                                                                    value = 'AAPL',
                                                                    persistence=True,
                                                                    persistence_type='session'
                                                        )
                                                    )
                                                ]
                                            ),
                                            dbc.CardBody(
                                                [ 
                                                    dcc.Graph(
                                                        id='all-graph',
                                                        figure = {}
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ],
                        align='center'
                    )
                ]
            ),
            color='dark'
        )
    ]
)
@callback(
    Output('stored-1','data'),
    Input('drop-1','value'),
    Input('drop-2','value'),
    Input('drop-3','value')
)
def send_company(value1,value2,value3):
    '''Store chosen Company Code'''
    triggred_id = ctx.triggered_id
    if triggred_id == 'drop-1':
        return value1
    elif triggred_id == 'drop-2':
        return value2
    elif triggred_id == 'drop-3':
        return value3
@callback(
    Output('text-1','children'),
    Output('text-2','children'),
    Input('drop-1','value'),
    Input('drop-2','value')
)
def send_texts(value1,value2):
    children1 = html.Div(
        [ 
            html.I(
                DashIconify(
                icon='cil:menu',
                height=20
            ),
            style={
                'margin-top':'6px'
            }
            ),
            html.Span(value1,
            style={'margin-top':'6px'})
        ],
        style={'display':'flex',
        'margin-bottom':'3px'}
    )
    children2 = html.Div(
        [ 
            html.I(
                DashIconify(
                icon='cil:menu',
                height=20
            ),
            style={
                'margin-top':'8px'
            }),
            html.Span(value2,
            style={'margin-top':'9px'})
        ],
        style={'display':'flex'}
    )
    return children1,children2

@callback(
    Output('graph_1','figure'),
    Input('drop-1','value')
)
def send_graph1(value):
    if value:
        df = month_data2[month_data2['Ticker']==value]
        trace1 = px.line(
            df,
            x='Date',
            y='Open',
            title=value
        )
        trace1.update_layout(
            title_x=0.5,
            titlefont=dict(
                color='white'
                ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                tickangle=45,
                showgrid=False,
                title='',
                tickfont=dict(
                    color='white'
                    )
                ),
            yaxis=dict(
                showgrid=False,
                tickangle=45,
                tickfont=dict(
                    color='white'
                    ),
                title=''
                )
            )
        trace1.update_traces(line_color='red')
        return trace1
    else:
        raise PreventUpdate
@callback(
    Output('graph_2','figure'),
    Input('drop-2','value')
)
def send_graph2(value):
    df = month_data2[month_data2['Ticker']==value]
    trace1 = px.line(
        df,
        x='Date',
        y='Close',
        title=value
    )
    trace1.update_layout(
        title_x=0.5,
        titlefont=dict(
            color='white'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            tickangle=45,
            showgrid=False,
            title='',
            tickfont=dict(
                color='white'
            )
        ),
        yaxis=dict(
            showgrid=False,
            tickangle=45,
            tickfont=dict(
                color='white'
            ),
            title=''
        )
    )
    trace1.update_traces(line_color='gold')
    return trace1
@callback(
    Output('all-graph','figure'),
    Input('drop-3','value')
)
def send_graph3(value):
    df = stock_data2[stock_data2['Symbols']==value]
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

