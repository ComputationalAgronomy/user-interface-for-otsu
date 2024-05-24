from dash import Dash, dcc, html, Input, Output, State, callback
import argparse, cv2, datetime

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

head = html.H1(
            children='Otsu Image Segmentation',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }, 
        )

uploadImages = dcc.Upload(
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
                )

filterRadioButtons = html.Div(children = [
                        dcc.RadioItems(
                            id='filter-radio-buttons',
                            options={
                                'Red': 'Red',
                                'Green': 'Green',
                                'Blue': 'Blue',
                                'Hue': 'Hue',
                                'Saturation': 'Saturation',
                                'Value': 'Value',
                                'Lightness': 'Lightness',
                                'Red-greeness': 'Red-greeness',
                                'Blue-yellowness': 'Blue-yellowness'
                            },
                            value='Red'
                        )
                    ])

inputContainer = html.Div(children=[
                    html.H3(children="Upload images to be segmented"),
                    uploadImages,
                    html.Hr(),
                    html.H3(children="Color channel"),
                    filterRadioButtons
                ], 
                style={
                    'textAlign': 'center',
                    'float': 'left',
                    'width': '50%',
                    'height': '100vh',
                    'backgroundColor': colors['inpBackground'],
                }
                )

outputContainer = html.Div(
                    style={
                        'textAlign': 'center',
                        'float': 'left',
                        'width': '50%',
                        'height': '100vh',
                        'backgroundColor': colors['outBackground']
                    },
                    children=[
                        html.H3(children="Uploaded image"),
                        html.Div(
                            id='output-image-upload',
                            style={
                                'width': '80%',
                                'margin': 'auto', 
                                'backgroundColor': colors['inpBackground'],
                            } 
                        ),
                        html.Hr(),
                        html.H3(id='selected-filter'),
                        html.Hr(),
                        html.Div(
                            id='output-color-spaced-image',
                            style={
                                'width': '80%',
                                'margin': 'auto', 
                                'backgroundColor': colors['inpBackground'],
                            } 
                        )
                    ]
                )

mainContainer = html.Div(
                    children=[
                        head,
                        html.Div(
                            id='main-container',
                            children=[
                                inputContainer,
                                outputContainer
                            ],
                            style={
                                'width': '100%',
                                'height': '100vh',
                                'backgroundColor': colors['inpBackground']
                            }
                        )
                    ],
                    style={
                        'width': '100%',
                        'height': '100vh',
                        'backgroundColor': colors['inpBackground']
                    }
                )
