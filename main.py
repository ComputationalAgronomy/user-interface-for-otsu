from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px, pandas as pd, datetime, numpy as np
import argparse, cv2
import components as comp

import base64
from PIL import Image
from io import BytesIO

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__, external_stylesheets=external_stylesheets, title='Otsu project', update_title='Loading...')

app.layout = html.Div(children=[
    #html.Div(html.Img(src=img, style={'width':'70%'})),
    #title
    comp.head,
    #body
    html.Div(children = [comp.inputContainer, comp.outputContainer]),
    html.Div(id='color-spaced')
])


def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.Img(src=contents, style={'width':'70%'}),
        html.Hr()
    ])

def color_space(contents):
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", type=str, default=contents,
        help="path to input image")
    args = vars(ap.parse_args())
    # load the original image and show it
    image = cv2.imread(args["image"])
    cv2.imshow("RGB", image)
    return html.Div(html.Img(src=image, style={'width':'70%'}))




#  ---------------------- callbacks ----------------------


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
    
@app.callback(
    Output('selected-filter', 'children'),
    [Input('filter-radio-buttons', 'value')])
def display_selected_filter(selected_filter):
    return f'Selected {selected_filter.upper()} channel'
    
if __name__ == '__main__':
    app.run(debug=True)
