from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px, pandas as pd, datetime
import components as comp

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__, external_stylesheets=external_stylesheets, title='Otsu project', update_title='Loading...')

app.layout = html.Div(children=[
    #title
    comp.head,
    #body
    html.Div(children = [comp.inputContainer, comp.outputContainer])
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
