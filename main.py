from dash import Dash, html, dcc, callback, Output, Input, State, no_update
import dash
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
    html.Div(comp.mainContainer)
])


def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.Img(src=contents, style={'width': '70%'}),
        html.Hr()
    ])

def filter_image(image, filter_type):
    if filter_type == 'Red':
        channel = 2
        filtered_image = image.copy()
        filtered_image[:, :, (channel + 1) % 3] = 0
        filtered_image[:, :, (channel + 2) % 3] = 0
    elif filter_type == 'Green':
        channel = 1
        filtered_image = image.copy()
        filtered_image[:, :, (channel + 1) % 3] = 0
        filtered_image[:, :, (channel + 2) % 3] = 0
    elif filter_type == 'Blue':
        channel = 0
        filtered_image = image.copy()
        filtered_image[:, :, (channel + 1) % 3] = 0
        filtered_image[:, :, (channel + 2) % 3] = 0
    elif filter_type == 'Hue':
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        filtered_image = hsv_image[:, :, 0]
    elif filter_type == 'Saturation':
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        filtered_image = hsv_image[:, :, 1]
    elif filter_type == 'Value':
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        filtered_image = hsv_image[:, :, 2]
    elif filter_type == 'Lightness':
        lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
        filtered_image = lab_image[:, :, 0]
    elif filter_type == 'Red-greeness':
        rg_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
        filtered_image = rg_image[:, :, 1]
    elif filter_type == 'Blue-yellowness':
        by_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
        filtered_image = by_image[:, :, 2]
    else:
        filtered_image = image  # No filtering for unrecognized types

    if filter_type in ['Hue', 'Saturation', 'Value', 'Lightness', 'Red-greeness', 'Blue-yellowness']:
        filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_GRAY2BGR)

    return filtered_image

def process_image(contents, filter_type):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    np_arr = np.frombuffer(decoded, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    filtered_image = image
    if filter_type in ['Red', 'Green', 'Blue', 'Hue', 'Saturation',
        'Value', 'Lightness', 'Red-greeness', 'Blue-yellowness']:
        filtered_image = filter_image(image, filter_type)

    gray_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
    _, otsu_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    _, filtered_buffer = cv2.imencode('.jpg', filtered_image)
    encoded_filtered_image = base64.b64encode(filtered_buffer).decode('utf-8')
    
    _, otsu_buffer = cv2.imencode('.jpg', otsu_image)
    encoded_otsu_image = base64.b64encode(otsu_buffer).decode('utf-8')

    return f'data:image/jpeg;base64,{encoded_filtered_image}', f'data:image/jpeg;base64,{encoded_otsu_image}'



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

@callback(
    Output('selected-filter', 'children', allow_duplicate=True),
    Output('output-color-spaced-image', 'children'),
    Output('otsu-image', 'children'),
    Input('filter-radio-buttons', 'value'),
    Input('upload-image', 'contents'),
    State('upload-image', 'filename'),
    prevent_initial_call=True
)
def update_output(selected_filter, uploaded_image_content, uploaded_image_filename):
    ctx = dash.callback_context

    if not ctx.triggered:
        return no_update, no_update, no_update

    trigger_id = ctx.triggered[0]['prop_id']

    if uploaded_image_content is not None:
        if trigger_id in ['filter-radio-buttons.value', 'upload-image.contents']:
            filtered_image, otsu_image = process_image(uploaded_image_content[0], selected_filter)
            return (
                f'Selected {selected_filter.upper()} channel',
                html.Img(src=filtered_image, style={'width': '70%'}),
                html.Img(src=otsu_image, style={'width': '70%'})
            )
        else:
            return f'Selected {selected_filter.upper()} channel', no_update, no_update
    else:
        return f'Selected {selected_filter.upper()} channel', no_update, no_update

if __name__ == '__main__':
    app.run_server(debug=True)
