from turtle import width
import dash
from dash import html,dcc,Output,Input
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import pandas as pd
import yfinance as yf
from datetime import datetime
company_logos = {
    'AAPL':r'images\apple_logo.svg',
    'GOOGL':r'images\google_logo.svg',
    'MSFT':r'images\Microsoft_logo.svg',
    'AMZN':r'images\Amazon_logo.svg',
    'META':r'images\meta_logo.svg'
}
crypto_logos = {
    'BTC-USD':r'images\bitcoin.svg',
    'ETH-USD':r'images\eth.svg',
    'BNB-USD':r'images\bnb.svg',
    'DOGE-USD':r'images\doge.svg',
    'SOL-USD':r'images\solana.svg',
    'XRP-USD':r'images\xrp.svg',
    'MATIC-USD':r'images\matic.svg',
    'DOT-USD':r'images\dot.svg',
    'USDT-USD':r'images\usdt.svg',
    'USDC-USD':r'images\usdc.svg',
    'BUSD-USD':r'images\busd.svg',
    'ADA-USD':r'images\aoa.svg'
}
app = dash.Dash(__name__, use_pages=True,meta_tags=[ 
    {
        'name':'viewport',
        'content':'width=device-width,initial-scale=1.0'
    }
],title='Stock and Crypto')
server = app.server
dropdown = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem(page['name'], href=page['path'])
        for page in dash.page_registry.values()
    ],
    label='Explore',
    color='secondary'
)
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#333333",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.Div(
            [ 
                dbc.Row(
                    [ 
                        dbc.Col(
                            html.H6 ('Stock & Crypto', style={'margin-top':'7px'}),width=7
                        ),
                        dbc.Col(
                            dropdown,width=5
                        )
                    ]
                )
            ]
        ),
        html.Div(
            [ 
                '''This dash app contains dashboard for the analysis on crypto data from April of this year and stock data from 2020 till 17th of october
                from the yahoo finance api and also from stooq using the pandas datareader'''
            ]
        ),
        html.Div(
            [ 
            ],id='logo',
            style={'margin-top':'20px',
            'margin-left':'10px'}
        ),
        html.Div(
            [ 
                html.Div(
            [ 
                html.Span(id='val'),
                html.Span(id='time')
            ],
            style = {
                'display':'flex',
                'justify-content':'space-between'
            }
        ),
        html.Table(
            [ 
                html.Tr(
                    [ 
                        html.Td(id='table-1',style={
                            'border-width':'1px',
                            'border-color':'white',
                            'align':'center',
                            'text-align':'center'})
                    ]
                ),
                html.Tr(
                    [ 
                        html.Td(id='table-2', style={
                            'border-width':'1px',
                            'border-color':'white',
                            'align':'center',
                            'text-align':'center'})
                    ]
                ),
                html.Tr(
                    [ 
                        html.Td(id='table-3',style={
                            'border-width':'1px',
                            'border-color':'white',
                            'align':'center',
                            'text-align':'center'})
                    ]
                ),
                html.Tr(
                    [ 
                        html.Td(id='table-4',style={
                            'border-width':'1px',
                            'border-color':'white',
                            'align':'center',
                            'text-align':'center'})
                    ]
                ),
                html.Tr(
                    [ 
                        html.Td(id='table-5',style={
                            'border-width':'1px',
                            'border-color':'white',
                            'align':'center',
                            'text-align':'center'})
                    ]
                ),
                html.Tr(
                    [ 
                        html.Td(id='table-6',style={
                            'border-width':'1px',
                            'border-color':'white',
                            'align':'center',
                            'text-align':'center'})
                    ]
                ),
                html.Tr(
                    [ 
                        html.Td(id='table-7',style={
                            'border-width':'1px',
                            'border-color':'white',
                            'align':'center',
                            'text-align':'center'})
                    ]
                ),
                html.Tr(
                    [ 
                        html.Td(id='table-8',style={
                            'border-width':'1px',
                            'border-color':'white',
                            'align':'center',
                            'text-align':'center'})
                    ]
                )
            ],
            style = {
                'width':'100%'}
                )
            ],style={'margin-top':'50px'}
        )
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[dash.page_container], style=CONTENT_STYLE)

app.layout = dbc.Container([
    sidebar,
    dcc.Location(id='url'),
    dcc.Interval(id='inter-val', n_intervals=1*3000),
    dcc.Interval(id='interval2',n_intervals=1,max_intervals=1),
    content,
    dcc.Store(id='stored-1',data=None),
    dcc.Store(id='stored-2',data=None)
],fluid=True)

@app.callback(
    Output('logo','children'),
    Output('val','children'),
    Output('time','children'),
    Input('stored-1','data'),
    Input('stored-2','data'),
    Input('url','pathname'),
    Input('inter-val','n_intervals')
)
def send_logo(data1,data2,pathname,n_intervals):
    today = datetime.now()
    today = today.strftime('%H:%M:%S %d %m %Y')
    if pathname != '/crypto':
        image =  html.Img(src=app.get_asset_url(company_logos[data1]),
        style={
            'width':'170px',
            'height':'180px',
            'margin-left':'20px'
        })
        return image,data1,today

    elif pathname == '/crypto':
        image =  html.Img(src=app.get_asset_url(crypto_logos[data2]),
        style={
            'width':'170px',
            'height':'180px',
            'margin-left':'20px'
        })
        return image,data2,today
@app.callback(
    Output('table-1','children'),
    Output('table-2','children'),
    Output('table-3','children'),
    Output('table-4','children'),
    Output('table-5','children'),
    Output('table-6','children'),
    Output('table-7','children'),
    Output('table-8','children'),
    Input('interval2','n_intervals'),
    Input('url','pathname'),
    Input('stored-1','data'),
    Input('stored-2','data')
)
def send_rows(n_intervals,pathname,data1,data2):
    if pathname != '/crypto':
        current_rate = yf.download(tickers=data1,period='1m')
        current_rate2 = current_rate['Close'].values[0]
        this_week = yf.download(tickers=data1,period='1w',interval='1d')
        same = len(this_week.loc[round(this_week['Close'])==round(this_week['Open'])])
        diff = len(this_week.loc[round(this_week['Close'])!=round(this_week['Open'])])
        this_week['Date'] = pd.to_datetime(this_week.index)
        this_week['Date'] = this_week['Date'].dt.date
        maximum_date = this_week.loc[this_week['Close'].idxmax()]['Date']
        maximum_val = this_week['Close'].max()
        open_today = this_week.iloc[-1:,:]['Open'].values[0]
        minimum_val = this_week['Close'].min()
        current = f'Current rate is : {current_rate2:.2f}'
        same_rate = f'Has same rounded open and close rate for {same} days'
        diff_rate = f'Different close and open rate for {diff} days'
        max_date = f'Had its highest rate on {maximum_date}' 
        max_val = f'The hghest rate is {maximum_val:.2f}'
        min_val = f'The lowest rate is {minimum_val:.2f}'
        open_val = f'Today\' open rate is {open_today:.2f}'
        title_output = f'Weekly Report for {data1}'
        return title_output,current,same_rate,diff_rate,max_date,min_val,max_val,open_val
    elif pathname == '/crypto':
        current_rate = yf.download(tickers=[a for a in crypto_logos.keys()],period='1m')
        current_rate = current_rate.stack().reset_index()
        current_rate.rename(columns={
        'level_0':'Date',
        'level_1':'Ticker'
        },inplace=True)
        value_data = current_rate[current_rate['Ticker']==data2]
        current_rate2 = value_data['Close'].values[0]
        this_week_data = yf.download(tickers=[a for a in crypto_logos.keys()],period='1w',interval='1d')
        this_week_data = this_week_data.stack().reset_index()
        this_week_data.rename(columns={
        'level_0':'Date',
        'level_1':'Ticker'
        },inplace=True)
        this_week = this_week_data[this_week_data['Ticker']==data2]
        this_week.reset_index(inplace=True)
        same = len(this_week.loc[round(this_week['Close'])==round(this_week['Open'])])
        diff = len(this_week.loc[round(this_week['Close'])!=round(this_week['Open'])])
        this_week['Date'] = pd.to_datetime(this_week['Date'])
        this_week['Date'] = this_week['Date'].dt.date
        maximum_date = this_week.loc[this_week['Close'].idxmax()]['Date']
        maximum_val = this_week['Close'].max()
        open_today = this_week.iloc[-1:,:]['Open'].values[0]
        minimum_val = this_week['Close'].min()
        current = f'Current rate is : {current_rate2:.2f}'
        same_rate = f'Has same rounded open and close rate for {same} days'
        diff_rate = f'Different close and open rate for {diff} days'
        max_date = f'Had its highest rate on {maximum_date}' 
        max_val = f'The hghest rate is {maximum_val:.2f}'
        min_val = f'The lowest rate is {minimum_val:.2f}'
        open_val = f'Today\'s open rate is {open_today:.2f}'
        title_output = f'Weekly Report for {data2}'
        return title_output,current,same_rate,diff_rate,max_date,min_val,max_val,open_val
if __name__ == '__main__':
    app.run_server()