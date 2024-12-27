import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_excel("Final Sheet.xlsx", sheet_name="Data (2)")

# Making a new derived Roles column
# Define conditions
conditions = [
    (df['Q3)  role_Owner']+df['Q3)  role_Manager']+df['Q3) role_Teacher'])>1,
    (df['Q3)  role_Owner']==1),
    (df['Q3)  role_Manager']==1),
    df['Q3) role_Teacher']==1,
]

# Define corresponding values for the new column
values = ['More than One Role', 'Owner', 'Manager','Teacher']

# Apply the conditions
df['Roles'] = np.select(conditions, values, default='No Match')
df=df[df['Roles']!='No Match']

# Values for aggregation
values = ['Q9_Other_words','Q9_Supervisor_Words','Q9_Friends_Family_Words','Q9_Unknown_Words','Q9a) event_Notification_Cellphone_Alert_WORDS',
'Q9_Parent_Guardian_Words','Q9_television_Radio_words'] 
rows = ['Roles'] #rows

#Pivot table
pivot_table = pd.pivot_table(
    df,
    values= values,  
    index= rows,  # Rows
    columns=None,       # Columns
    aggfunc='count'  # Aggregation functions
)

pivot_table_percentage = round(pivot_table.div(pivot_table.sum(axis=1), axis=0) * 100,2)
pivot_table_percentage=pivot_table_percentage.reset_index()
pivot_table_percentage.columns

#Plotly bar plot
fig1 = px.bar(pivot_table_percentage, x='Roles', y=values, 
              title="Roles vs How they find out of an event could affect their facility",
              labels={'Q9_Other_words': 'Label 1', 
                     'Q9_Supervisor_Words': 'Label 2', 
                     'Q9_Friends_Family_Words': 'Label 3',
					 'Q9_Unknown_Words' : 'label 55', 
					 'Q9a) event_Notification_Cellphone_Alert_WORDS': 'labl3lew',
					 'Q9_Parent_Guardian_Words': "testing",
					 'Q9_television_Radio_words': "hellowl",
					  },
				) 
#Figsize
fig1.update_layout(
    width=1000,  # Set the width of the chart (adjust as needed)
    height=600,  # Set the height of the chart (adjust as needed)
)

fig1.show()
