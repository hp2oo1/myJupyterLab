# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_ag_grid as dag
import json
from datetime import datetime

# Function to determine the type of column
def get_column_type(values):
    for value in values:
        if isinstance(value, list):
            if all(isinstance(item, str) for item in value):
                return "list_string"
            elif all(isinstance(item, datetime) for item in value):
                if all(item.time() == datetime.min.time() for item in value):
                    return "list_date"
                return "list_datetime"
            elif all(isinstance(item, (int, float)) for item in value):
                return "list_number"
    if all(isinstance(value, datetime) for value in values):
        if all(value.time() == datetime.min.time() for value in values):
            return "dateString"
        return "datetime"
    if all(isinstance(value, int) for value in values):
        return "integer"
    if all(isinstance(value, float) for value in values):
        return "double"
    return "string"

# Function to preprocess input data for display
def preprocess_input_data(input_data, columns):
    processed_data = []
    for row in input_data:
        processed_row = {}
        for col in columns:
            key = col['field']
            col_type = col['type']
            if col_type == "list_string" and isinstance(row[key], list):
                processed_row[key] = ",".join(row[key])
            elif col_type == "list_date" and isinstance(row[key], list):
                processed_row[key] = ",".join(item.strftime('%Y-%m-%d') for item in row[key])
            elif col_type == "list_datetime" and isinstance(row[key], list):
                processed_row[key] = ",".join(item.isoformat() for item in row[key])
            elif col_type == "list_number" and isinstance(row[key], list):
                processed_row[key] = ",".join(map(str, row[key]))
            elif col_type == "dateString" and isinstance(row[key], datetime):
                processed_row[key] = row[key].strftime('%Y-%m-%d')
            elif col_type == "datetime" and isinstance(row[key], datetime):
                processed_row[key] = row[key].isoformat()
            else:
                processed_row[key] = row[key]
        processed_data.append(processed_row)
    return processed_data

# Function to convert datetime objects to strings for JSON serialization
def convert_datetimes_for_json(data, columns):
    json_data = []
    for row in data:
        json_row = {}
        for col in columns:
            key = col['field']
            col_type = col['type']
            if col_type == "dateString" and isinstance(row[key], datetime):
                json_row[key] = row[key].strftime('%Y-%m-%d')
            elif col_type == "datetime" and isinstance(row[key], datetime):
                json_row[key] = row[key].isoformat()
            elif col_type == "list_date" and isinstance(row[key], list):
                json_row[key] = [item.strftime('%Y-%m-%d') for item in row[key]]
            elif col_type == "list_datetime" and isinstance(row[key], list):
                json_row[key] = [item.isoformat() for item in row[key]]
            else:
                json_row[key] = row[key]
        json_data.append(json_row)
    return json_data

# Function to convert datetime strings back to datetime objects
def convert_strings_to_datetimes(data, columns):
    for row in data:
        for col in columns:
            key = col['field']
            col_type = col['type']
            if col_type == "dateString" and isinstance(row[key], str):
                row[key] = datetime.strptime(row[key], '%Y-%m-%d')
            elif col_type == "datetime" and isinstance(row[key], str):
                row[key] = datetime.fromisoformat(row[key])
            elif col_type == "list_date" and isinstance(row[key], list):
                row[key] = [datetime.strptime(item, '%Y-%m-%d') for item in row[key]]
            elif col_type == "list_datetime" and isinstance(row[key], list):
                row[key] = [datetime.fromisoformat(item) for item in row[key]]
    return data

# Function to postprocess row data for saving
def postprocess_row_data(row_data, columns):
    processed_data = []
    for row in row_data:
        processed_row = {}
        for col in columns:
            key = col['field']
            col_type = col['type']
            if col_type == "list_string" and isinstance(row[key], str):
                processed_row[key] = row[key].split(",")
            elif col_type == "list_date" and isinstance(row[key], str):
                processed_row[key] = [datetime.strptime(date, '%Y-%m-%d') for date in row[key].split(",")]
            elif col_type == "list_datetime" and isinstance(row[key], str):
                processed_row[key] = [datetime.fromisoformat(date) for date in row[key].split(",")]
            elif col_type == "list_number" and isinstance(row[key], str):
                processed_row[key] = list(map(float, row[key].split(",")))
            elif col_type == "dateString" and isinstance(row[key], str):
                processed_row[key] = datetime.strptime(row[key], '%Y-%m-%d')
            elif col_type == "datetime" and isinstance(row[key], str):
                processed_row[key] = datetime.fromisoformat(row[key])
            elif col_type == "integer":
                processed_row[key] = int(row[key])
            elif col_type == "double":
                processed_row[key] = float(row[key])
            else:
                processed_row[key] = row[key]
        processed_data.append(processed_row)
    return processed_data

# Function to determine which columns originally contained lists and their types
def get_columns(input_data):
    columns = []
    for col in input_data[0].keys():
        values = [row[col] for row in input_data]
        col_type = get_column_type(values)
        column_def = {
            "headerName": col,
            "field": col,
            "editable": True,
            "type": col_type
        }
        if col_type in ["datetime", "list_date", "list_datetime"]:
            column_def["cellEditor"] = "agTextCellEditor"
        columns.append(column_def)
    return columns

# Initialize the Dash app
app = dash.Dash(__name__)

def create_table(input_data, saved_table_path="saved_table_data.json"):
    # Determine columns and preprocess input data
    columns = get_columns(input_data)
    processed_data = preprocess_input_data(input_data, columns)

    app.layout = html.Div([
        dag.AgGrid(
            id='table',
            columnDefs=columns,
            rowData=processed_data,
            columnSize='autoSize',
            defaultColDef={'sortable': True, 'filter': True, 'resizable': True, 'editable': True},
        ),
        html.Button('+ row', id='add-row-button', n_clicks=0),
        html.Button('- row', id='remove-row-button', n_clicks=0),
        html.Button('Save Table', id='save-table-button', n_clicks=0),
        html.Div(id='file-path', style={'marginTop': '20px', 'whiteSpace': 'pre-wrap'}),
        dcc.Store(id='store', data={'data': processed_data, 'columns': columns})
    ])

    @app.callback(
        Output('table', 'rowData'),
        Output('store', 'data'),
        Output('save-table-button', 'children'),
        Output('file-path', 'children'),
        Input('add-row-button', 'n_clicks'),
        Input('remove-row-button', 'n_clicks'),
        Input('save-table-button', 'n_clicks'),
        Input('table', 'cellValueChanged'),
        State('table', 'rowData'),
        State('store', 'data'),
        State('table', 'columnDefs'),
        prevent_initial_call=True
    )
    def handle_callbacks(n_clicks_add_row, n_clicks_remove_row, n_clicks_save, cell_value_changed, rowData, stored_data, columnDefs):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        
        if 'add-row-button' in changed_id:
            rowData.append(rowData[-1].copy())  # Duplicate last row
            return rowData, {'data': rowData, 'columns': columnDefs}, "Save Table", ""
        
        elif 'remove-row-button' in changed_id and len(rowData) > 1:
            rowData.pop()
            return rowData, {'data': rowData, 'columns': columnDefs}, "Save Table", ""
        
        elif 'save-table-button' in changed_id:
            # Postprocess row data before saving
            processed_row_data = postprocess_row_data(rowData.copy(), columnDefs)
            # Convert datetime objects to strings for JSON serialization
            json_compatible_data = convert_datetimes_for_json(processed_row_data, columnDefs)
            # Save the JSON data to the specified file, including columns
            with open(saved_table_path, 'w') as f:
                json.dump({'data': json_compatible_data, 'columns': columnDefs}, f, indent=4)
            
            return rowData, {'data': rowData, 'columns': columnDefs}, "Table Saved", f"Data saved to: {saved_table_path}"
        
        elif 'table' in changed_id and cell_value_changed:
            # Update the stored data to reflect the cell value change
            for row in rowData:
                for col in columnDefs:
                    key = col['field']
                    col_type = col['type']
                    if col_type == "dateString" and isinstance(row[key], datetime):
                        row[key] = row[key].strftime('%Y-%m-%d')
            return rowData, {'data': rowData, 'columns': columnDefs}, "Save Table", ""
        
        return rowData, {'data': rowData, 'columns': columnDefs}, "Save Table", ""

    app.run_server(mode='inline', port=8050, debug=True)

def load_saved_table(saved_table_path="saved_table_data.json"):
    with open(saved_table_path, 'r') as f:
        saved_data = json.load(f)
    data = saved_data['data']
    columns = saved_data['columns']
    processed_data = convert_strings_to_datetimes(data, columns)
    return processed_data

# %%
# Sample input
input_data = [
    {"name": "Alice", "age": 30, "birthday": datetime(1993, 5, 17), "salary": 60000.00, "city": ["New York", "Los Angeles"], "meetings": [datetime(2023, 5, 28, 10, 0), datetime(2023, 6, 15, 14, 0)]},
    {"name": "Bob", "age": 25, "birthday": datetime(1998, 8, 24), "salary": 50000.50, "city": ["San Francisco", "Seattle"], "meetings": [datetime(2023, 5, 30, 16, 0), datetime(2023, 6, 20, 11, 0)]}
]

# Create the table
create_table(input_data)

# %%
# Load the saved table data
saved_data = load_saved_table()
print(saved_data)

# %%
