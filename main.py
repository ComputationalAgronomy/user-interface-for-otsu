from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__, title='Otsu project', update_title='Loading...')

title = {
    'size': '40',
    'color': '#FFC300'
}

colors = {
    'inp_background': '#AEB6BF',
    'out_background': '#D6DBDF',
    'text': '#111111'
}

container = {
    'float': 'left',
    'width': '50%',
}

app.layout = html.Div(children=[
    html.H1(
        children='Otsu Image Segmentation',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }, 
    ),

    html.Div(style={'display': 'flex'}, children=[
        html.Div(
        children=[
            html.H3(
                children="Input images to be segmented"
            )
        ], 
        style={
            'textAlign': 'center',
            'float': 'left',
            'width': '50%',
            'height': '100vh',
            'backgroundColor': colors['inp_background'],
        }),
        html.Div(children=[
                html.H3(
                    children="Output"
                )
            ], 
            style={
            'textAlign': 'center',
            'float': 'left',
            'width': '50%',
            'height': '100vh',
            'backgroundColor': colors['out_background'],
        })
    ])
    
])

if __name__ == '__main__':
    app.run(debug=True)
