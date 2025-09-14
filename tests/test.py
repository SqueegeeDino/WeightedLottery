# Test file for WeightedLottery/src/main.py
import FreeSimpleGUI as sg
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sample data for the table
data = [
    ['Apple', 1.00, 100],
    ['Banana', 0.50, 200],
    ['Orange', 0.75, 150]
]

# Column headings
headings = ['Fruit', 'Price', 'Quantity']

# Define the window layout
layout = [
    [sg.Table(values=data, 
              headings=headings, 
              auto_size_columns=True, 
              display_row_numbers=False, 
              justification='left', 
              key='-TABLE-')]
]

# Create the window
window = sg.Window('Simple Table Example', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()