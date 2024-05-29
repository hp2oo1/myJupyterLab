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
# create_table.ipynb

import excel_like_table as elt
from datetime import datetime

# Sample input
input_data = [
    {"name": "Alice", "age": 30, "birthday": datetime(1993, 5, 17, 14, 30), "salary": 60000.00, "city": ["New York", "Los Angeles"], "meetings": [datetime(2023, 5, 28, 10, 0), datetime(2023, 6, 15, 14, 0)]},
    {"name": "Bob", "age": 25, "birthday": datetime(1998, 8, 24, 9, 15), "salary": 50000.50, "city": ["San Francisco", "Seattle"], "meetings": [datetime(2023, 5, 30, 16, 0), datetime(2023, 6, 20, 11, 0)]}
]

# Create the table
elt.create_table(input_data)

# %%
# Load the saved table data
saved_data = elt.load_saved_table()
print(saved_data)
