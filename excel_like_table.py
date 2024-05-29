# excel_like_table.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_ag_grid as dag
import json
import os
from datetime import datetime

# Function to determine the type of column
def get_column_type(values):
    for value in values:
        if isinstance(value, list):
            if all(isinstance(item, str) for item in value):
                return "list_string"
            elif all(isinstance(item, datetime) for item in value):
                return "list_date"
            elif all(isinstance(item, (int, float)) for item in value):
                return "list_number"
    if all(isinstance(value, datetime) for value in values):
        return "date"
    if all(isinstance(value, int) for value in values):
        return "integer"
    if all(isinstance(value, float) for value in values):
        return "double"
    return "string"

# Function to convert lists and dates to comma-separated strings using column metadata
def preprocess_input_data(input_data, columns):
    processed_data = []
    for row in input_data:
        processed_row = {}
        for col in columns:
            key = col['field']
            col_type = col['type']
            if col_type in {"list_string", "list_number"}:
                processed_row[key] = ",".join(map(str, row[key]))
            elif col_type == "list_date":
                processed_row[key] = ",".join(item.isoformat() for item in row[key])
            elif col_type == "date":
                processed_row[key] = row[key].isoformat()
            else:
                processed_row[key] = row[key]
        processed_data.append(processed_row)
    return processed_data

# Function to convert comma-separated strings back to lists and dates using column metadata
def postprocess_row_data(row_data, columns):
    processed_data = []
    for row in row_data:
        processed_row = {}
        for col in columns:
            key = col['field']
            col_type = col['type']
            if col_type == "list_string":
                processed_row[key] = row[key].split(",")
            elif col_type == "list_date":
                processed_row[key] = [datetime.fromisoformat(date) for date in row[key].split(",")]
            elif col_type == "list_number":
                processed_row[key] = list(map(float, row[key].split(",")))
            elif col_type == "date":
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
        if col_type == "date":
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
        dcc.Store(id='store', data=processed_data)
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
            return rowData, rowData, "Save Table", ""
        
        elif 'remove-row-button' in changed_id and len(rowData) > 1:
            rowData.pop()
            return rowData, rowData, "Save Table", ""
        
        elif 'save-table-button' in changed_id:
            # Postprocess row data before saving
            processed_row_data = postprocess_row_data(rowData, columnDefs)
            # Convert datetime objects to strings for JSON serialization
            json_compatible_data = preprocess_input_data(processed_row_data, columnDefs)
            # Save the JSON data to the specified file
            with open(saved_table_path, 'w') as f:
                json.dump(json_compatible_data, f, indent=4)
            
            return rowData, rowData, "Table Saved", f"Data saved to: {saved_table_path}"
        
        elif 'table' in changed_id and cell_value_changed:
            return rowData, rowData, "Save Table", ""
        
        return rowData, rowData, "Save Table", ""

    app.run_server(mode='inline', port=8050, debug=True)

def load_saved_table(saved_table_path="saved_table_data.json"):
    with open(saved_table_path, 'r') as f:
        data = json.load(f)
    return data
