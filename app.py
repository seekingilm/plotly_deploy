import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import base64
import io

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Roles vs Event Awareness"), className="text-center")
    ]),
    dbc.Row([
        dbc.Col(dcc.Upload(
            id='upload-data',
            children=html.Button('Upload Excel File'),
            multiple=False
        ), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-plot'), width=12)
    ])
])

@app.callback(
    Output('bar-plot', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_graph(contents, filename):
    if contents is None:
        raise PreventUpdate

    # Decode the uploaded file
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded))

    # Making a new derived Roles column
    conditions = [
        (df['Q3)  role_Owner'] + df['Q3)  role_Manager'] + df['Q3) role_Teacher']) > 1,
        (df['Q3)  role_Owner'] == 1),
        (df['Q3)  role_Manager'] == 1),
        df['Q3) role_Teacher'] == 1,
    ]

    values = ['More than One Role', 'Owner', 'Manager', 'Teacher']
    df['Roles'] = np.select(conditions, values, default='No Match')
    df = df[df['Roles'] != 'No Match']

    # Values for aggregation
    values = ['Q9_Other_words', 'Q9_Supervisor_Words', 'Q9_Friends_Family_Words',
              'Q9_Unknown_Words', 'Q9a) event_Notification_Cellphone_Alert_WORDS',
              'Q9_Parent_Guardian_Words', 'Q9_television_Radio_words']
    rows = ['Roles']

    # Pivot table
    pivot_table = pd.pivot_table(
        df,
        values=values,
        index=rows,
        columns=None,
        aggfunc='count'
    )

    pivot_table_percentage = round(pivot_table.div(pivot_table.sum(axis=1), axis=0) * 100, 2)
    pivot_table_percentage = pivot_table_percentage.reset_index()

    # Plotly bar plot
    fig1 = px.bar(pivot_table_percentage, x='Roles', y=values,
                  title="Roles vs How they find out of an event could affect their facility",
                  labels={'Q9_Other_words': 'Label 1',
                          'Q9_Supervisor_Words': 'Label 2',
                          'Q9_Friends_Family_Words': 'Label 3',
                          'Q9_Unknown_Words': 'Label 55',
                          'Q9a) event_Notification_Cellphone_Alert_WORDS': 'Label 3',
                          'Q9_Parent_Guardian_Words': "Testing",
                          'Q9_television_Radio_words': "Hello World",
                          },
                  )

    # Figsize
    fig1.update_layout(
        width=1000,
        height=600,
    )

    return fig1

if __name__ == '__main__':
    app.run_server(debug=True)
