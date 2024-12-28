import pandas as pd
import os
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import base64
import io

# Initialize the Dash app
port = int(os.environ.get('PORT', 4000))
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Roles vs Event Awareness"), className="text-center")
    ]),
    dbc.Row([
        dbc.Col(dcc.Upload(
            id='upload-data',
            children=html.Button('Upload Excel File'),
            multiple=False
        ), width=13)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-plot'), width=13),
        dbc.Col(dcc.Graph(id='bar-plot-1'), width=12),
        dbc.Col(dcc.Graph(id='bar-plot-2'), width=12),  # fig3
        dbc.Col(dcc.Graph(id='bar-plot-3'), width=12),  # fig4
        dbc.Col(dcc.Graph(id='bar-plot-4'), width=12),  # fig6
        dbc.Col(dcc.Graph(id='bar-plot-5'), width=12),  # fig6
        dbc.Col(dcc.Graph(id='bar-plot-6'), width=12),  # fig7
        dbc.Col(dcc.Graph(id='bar-plot-7'), width=12),  # fig8
        dbc.Col(dcc.Graph(id='bar-plot-8'), width=12),  # fig9
        dbc.Col(dcc.Graph(id='bar-plot-9'), width=12), # fig10
        dbc.Col(dcc.Graph(id='pie-chart'), width=13),    # fig11 (pie chart)
        dbc.Col(dcc.Graph(id='bar-plot-11'), width=12), # fig10
    ])
])

def decode_file(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return pd.read_excel(io.BytesIO(decoded))

@app.callback(
    Output('bar-plot', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_graph(contents, filename):
    if contents is None:
        raise PreventUpdate

    df = decode_file(contents)
    conditions = [
        (df['Q4)  role_Owner'] + df['Q3)  role_Manager'] + df['Q3) role_Teacher']) > 1,
        (df['Q4)  role_Owner'] == 1),
        (df['Q4)  role_Manager'] == 1),
        df['Q4) role_Teacher'] == 1,
    ]

    values = ['More than One Role', 'Owner', 'Manager', 'Teacher']
    df['Roles'] = np.select(conditions, values, default='No Match')
    df = df[df['Roles'] != 'No Match']

    # Values for aggregation
    values = ['Q10_Other_words', 'Q9_Supervisor_Words', 'Q9_Friends_Family_Words',
              'Q10_Unknown_Words', 'Q9a) event_Notification_Cellphone_Alert_WORDS',
              'Q10_Parent_Guardian_Words', 'Q9_television_Radio_words']
    rows = ['Roles']

    # Pivot table
    pivot_table = pd.pivot_table(
        df,
        values=values,
        index=rows,
        columns=None,
        aggfunc='count'
    )

    pivot_table_percentage = round(pivot_table.div(pivot_table.sum(axis=2), axis=0) * 100, 2)
    pivot_table_percentage = pivot_table_percentage.reset_index()

    fig2 = px.bar(pivot_table_percentage, x='Roles', y=values,
                  title="Roles vs How they find out of an event could affect their facility",
                  labels={'Q10_Other_words': 'Label 1',
                          'Q10_Supervisor_Words': 'Label 2',
                          'Q10_Friends_Family_Words': 'Label 3',
                          'Q10_Unknown_Words': 'Label 55',
                          'Q10a) event_Notification_Cellphone_Alert_WORDS': 'Label 3',
                          'Q10_Parent_Guardian_Words': "Testing",
                          'Q10_television_Radio_words': "Hello World",
                          }
                  )

    fig2.update_layout(
        width=1001,
        height=601,
    )

    return fig2


@app.callback(
    Output('bar-plot-1', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_graph_3(contents, filename):
    if contents is None:
        raise PreventUpdate

    df = decode_file(contents)
    conditions = [
        (df['Q4)  role_Owner'] + df['Q3)  role_Manager'] + df['Q3) role_Teacher']) == 3,
        (df['Q4)  role_Owner'] == 1),
        (df['Q4)  role_Manager'] == 1),
        df['Q4) role_Teacher'] == 1,
    ]

    # Define corresponding values for the new column
    values = ['All', 'Owner', 'Manager', 'Teacher']

    # Apply the conditions
    df['Roles'] = np.select(conditions, values, default='No Match')
    df = df[df['Roles'] != 'No Match']

    # Values for aggregation
    values = ['Q11_Supervisor_words', 'Q10_Unknown_words', 'Q10_Computer_Alert_words',
              'Q11_Television_Radio_words', 'Q10_Parent_Guardian_words',
              'Q11b_fire_over_cell_Words\n\n', 'Q10_Family_Friend_words', 'Q10_Other_words']
    rows = ['Roles']  # Rows

    # Pivot table
    pivot_table = pd.pivot_table(
        df,
        values=values,
        index=rows,  # Rows
        columns=None,  # Columns
        aggfunc='count'  # Aggregation functions
    )

    pivot_table_percentage = round(pivot_table.div(pivot_table.sum(axis=2), axis=0) * 100, 2)
    pivot_table_percentage = pivot_table_percentage.reset_index()

    # Plotly bar plot
    fig3 = px.bar(pivot_table_percentage, x='Roles', y=values,
                  title="Section vs How they find out there's an event actively affecting their facility",
                  )

    # Figsize
    fig3.update_layout(
        width=1001,  # Set the width of the chart (adjust as needed)
        height=601,  # Set the height of the chart (adjust as needed)
    )

    return fig3

@app.callback(
    Output('bar-plot-2', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_graph_4(contents, filename):
    if contents is None:
        raise PreventUpdate

    df = decode_file(contents)

    # Your existing code for fig4 here
    df2 = df.groupby('Q1.1.family_center')['Q8) kids_affected_smoke_indoors_percentage \nUsing words'].value_counts().reset_index()
    df2 = df1.rename(columns={'Q8) kids_affected_smoke_indoors_percentage \nUsing words': 'Percentage'})
    df2 = df1[df1['Percentage'] != 0]
    category_totals = df2.groupby('Q1.1.family_center')['count'].sum()
    df2['proportion'] = df1.apply(lambda row: (row['count'] / category_totals[row['Q1.1.family_center']]) * 100, axis=1)

    fig4 = px.bar(df1, x="Q1.1.family_center", y="proportion", color="Percentage", title="Centre Type and Percentage of kids affected", barmode='stack')
    fig4.update_layout(width=1000, height=500)

    return fig4

@app.callback(
    Output('bar-plot-3', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_graph_5(contents, filename):
    if contents is None:
        raise PreventUpdate

    df = decode_file(contents)

    # Your existing code for fig5 here
    values = ['Q7)Not Affected', 'Q6)Affected but not a problem',
    'Q7)Affected']
    rows = ['Q2.1.family_center']

    pivot_table = pd.pivot_table(
        df,
        values=values,
        index=rows,
        columns=None,
        aggfunc='count'
    )

    pivot_table_percentage = round(pivot_table.div(pivot_table.sum(axis=2), axis=0) * 100, 2)
    pivot_table_percentage = pivot_table_percentage.reset_index()

    fig5 = px.bar(pivot_table_percentage, x='Q1.1.family_center', y=values, title="Type of Center vs level of effect observed (%)")
    fig5.update_layout(width=1000, height=500)

    return fig5

@app.callback(
    Output('bar-plot-4', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)

def update_graph_6(contents, filename):
		if contents is None:
			raise PreventUpdate

		df = decode_file(contents)
		values = ['Q13)Avoid_stove', 'Q12) central_AC', 'Q12) Other_AC', 'Q12) Close_W', 'Q12) clean_indoor', 'Q12)Cancel', 'Q12) Portable_air', 'Q12) Give_Masks', 'Q12) Seal_WD (WD=Windows/Doors)'] 	

		rows = ['Q2.1.family_center'] 

		pivot_table = pd.pivot_table(
			df,
			values= values,  
			index= rows,  # Rows
			columns=None,       # Columns
			aggfunc='count'  # Aggregation functions
		)

		pivot_table_percentage = round(pivot_table.div(pivot_table.sum(axis=2), axis=0) * 100,2)
		pivot_table_percentage=pivot_table_percentage.reset_index()
		pivot_table_percentage.columns

		fig6 = px.bar(pivot_table_percentage, x='Q1.1.family_center', y=values, title="Type of center vs How they react to wildfire smoke")

		fig6.update_layout(
			width=1001,  # Set the width of the chart (adjust as needed)
			height=601,  # Set the height of the chart (adjust as needed)
		)

		return fig6

@app.callback(
    Output('bar-plot-5', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)

def update_graph_7(contents, filename):
    if contents is None:
        raise PreventUpdate

    df = decode_file(contents)

    values = ['Q10_Other_words', 'Q9_Supervisor_Words', 'Q9_Friends_Family_Words', 
              'Q10_Unknown_Words', 'Q9a) event_Notification_Cellphone_Alert_WORDS', 
              'Q10_Parent_Guardian_Words', 'Q9_television_Radio_words']
    rows = ['Section']

    pivot_table = pd.pivot_table(
        df,
        values=values,
        index=rows,
        columns=None,
        aggfunc='count'
    )

    pivot_table_percentage = round(pivot_table.div(pivot_table.sum(axis=2), axis=0) * 100, 2)
    pivot_table_percentage = pivot_table_percentage.reset_index()

    fig7 = px.bar(pivot_table_percentage, x='Section', y=values, title="Section vs How they find out of an event could affect their facility")
    fig7.update_layout(width=1000, height=600)

    return fig7

@app.callback(
    Output('bar-plot-6', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_graph_8(contents, filename):
    if contents is None:
        raise PreventUpdate

    df = decode_file(contents)

    values = ['Q11_Supervisor_words', 'Q10_Unknown_words', 'Q10_Computer_Alert_words', 
              'Q11_Television_Radio_words', 'Q10_Parent_Guardian_words', 
              'Q11b_fire_over_cell_Words\n\n', 'Q10_Family_Friend_words', 'Q10_Other_words']
    rows = ['Section']

    pivot_table = pd.pivot_table(
        df,
        values=values,
        index=rows,
        columns=None,
        aggfunc='count'
    )

    pivot_table_percentage = round(pivot_table.div(pivot_table.sum(axis=2), axis=0) * 100, 2)
    pivot_table_percentage = pivot_table_percentage.reset_index()

    fig8 = px.bar(pivot_table_percentage, x='Section', y=values, title="Section vs How they find out of an event could affect their facility")
    fig8.update_layout(width=1000, height=600)

    return fig8

@app.callback(
    Output('bar-plot-7', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_graph_9(contents, filename):
    if contents is None:
        raise PreventUpdate

    df = decode_file(contents)

    # Group by to get the required percentage for fig9
    df2 = df.groupby('Section')['Q8) kids_affected_smoke_indoors_percentage \nUsing words'].value_counts().reset_index()
    df2 = df1.rename(columns={'Q8) kids_affected_smoke_indoors_percentage \nUsing words': 'Percentage Affected indoors'})
    df2 = df1[df1['Percentage Affected indoors'] != 0]

    # Calculate category-wise total count
    category_totals = df2.groupby('Section')['count'].sum()

    # Calculate proportion within category
    df2['proportion'] = df1.apply(lambda row: (row['count'] / category_totals[row['Section']]) * 100, axis=1)

    # Plotly bar plot

    fig9 = px.bar(df1, x="Section", y="proportion", color="Percentage Affected indoors", title="Section vs Percentage of Affected indoors", barmode='stack')
    fig9.update_layout(width=1000, height=500)

    return fig9

@app.callback(
    Output('bar-plot-8', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_graph_10(contents, filename):
    if contents is None:
        raise PreventUpdate

    df = decode_file(contents)

    # Group by to get the required percentage for fig10
    df2 = df.groupby('Section')['Q7 kids_affected_smoke_percentage_outdoors\nWORDS'].value_counts().reset_index()
    df2 = df1.rename(columns={'Q7 kids_affected_smoke_percentage_outdoors\nWORDS': 'Percentage Affected outdoors'})
    df2 = df1[df1['Percentage Affected outdoors'] != 0]

    # Calculate category-wise total count
    category_totals = df2.groupby('Section')['count'].sum()

    # Calculate proportion within category
    df2['proportion'] = df1.apply(lambda row: (row['count'] / category_totals[row['Section']]) * 100, axis=1)

    # Plotly bar plot
    fig10 = px.bar(df1, x="Section", y="proportion", color="Percentage Affected outdoors", title="Section vs Percentage of Affected outdoors", barmode='stack')
    fig10.update_layout(width=1000, height=500)

    return fig10

@app.callback(
    Output('bar-plot-9', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_graph_11(contents, filename):
    if contents is None:
        raise PreventUpdate

    df = decode_file(contents)

    # Values for aggregation for fig11
    values = ['Q7)Not Affected', 'Q6)Affected but not a problem', 'Q6)Affected']
    rows = ['Section']

    pivot_table = pd.pivot_table(
        df,
        values=values,
        index=rows,
        columns=None,
        aggfunc='count'
    )

    pivot_table_percentage = round(pivot_table.div(pivot_table.sum(axis=2), axis=0) * 100, 2)
    pivot_table_percentage = pivot_table_percentage.reset_index()

    fig11 = px.bar(pivot_table_percentage, x='Section', y=values, title="Section vs Level of effect on Children")
    fig11.update_layout(width=1000, height=600)

    return fig11

@app.callback(
    Output('pie-chart', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)

def update_pie_chart(contents, filename):
    if contents is None:
        raise PreventUpdate

    df = decode_file(contents)

    # Create pie chart for fig12
    df2 = (df['Section'].value_counts(normalize=True) * 100).reset_index()
    df2.columns = ['Section', 'Percentage']

    fig12 = px.pie(df1, values='Percentage', names='Section', title='Response from each section %')
    fig12.update_layout(width=1000, height=600)

    return fig12

@app.callback(
    Output('bar-plot-11', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)

def update_graph_13(contents, filename):
    if contents is None:
        raise PreventUpdate

    df = decode_file(contents)
    # Values for aggregation
    
    values = ['Q13)Avoid_stove', 'Q12) central_AC', 'Q12) Other_AC',
              'Q13) Close_W', 'Q12) clean_indoor', 'Q12)Cancel', 'Q12) Portable_air', 'Q12) Give_Masks',
              'Q13) Seal_WD (WD=Windows/Doors)'] 
    rows = ['Section'] #rows

    #Pivot table
    pivot_table = pd.pivot_table(
                df,
                values= values,  
                index= rows,  # Rows
                columns=None,       # Columns
                aggfunc='count'  # Aggregation functions
    )

    pivot_table_percentage = round(pivot_table.div(pivot_table.sum(axis=2), axis=0) * 100,2)
    pivot_table_percentage=pivot_table_percentage.reset_index()
    pivot_table_percentage.columns

    #Plotly bar plot
    fig13 = px.bar(pivot_table_percentage, x='Section', y=values, title="Section vs reaction to wildfire smoke")

    #Figsize
    fig13.update_layout(
                width=1001,  # Set the width of the chart (adjust as needed)
                height=601,  # Set the height of the chart (adjust as needed)
    )

    return fig13

 

if __name__ == '__main__':
    app.run_server(port=port)
