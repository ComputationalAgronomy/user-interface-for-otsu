from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px, pandas as pd, datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__, external_stylesheets=external_stylesheets, title='Otsu project', update_title='Loading...')

title = {
    'size': '40',
    'color': '#FFC300'
}

colors = {
    'inpBackground': '#AEB6BF',
    'outBackground': '#D6DBDF',
    'darkBlue': '#1B3B56',
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

    html.Div(children=[
        html.Div(children=[
            html.H3(
                children="Upload images to be segmented"
            ),
            dcc.Upload(
                id='upload-image',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '70%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': 'auto'
                },
                multiple=True
            ),
        ], 
        style={
            'textAlign': 'center',
            'float': 'left',
            'width': '50%',
            'height': '100vh',
            'backgroundColor': colors['inpBackground'],
        }),
        html.Div(
            style={
                'textAlign': 'center',
                'float': 'left',
                'width': '50%',
                'height': '100vh',
                'backgroundColor': colors['outBackground']
            },
            children=[
                html.H3(
                    children="Output"
                ),
                html.Div(
                    id='output-image-upload',
                    style={
                        'width': '80%',
                        'margin': 'auto', 
                        'backgroundColor': colors['inpBackground'],
                    } 
                )
            ]
        )
    ])
])

def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.Img(src=contents, style={'width':'70%'}),
        html.Hr()
    ])

@callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run(debug=True)
