import FreeSimpleGUI as sg
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

myList = []
myDict = {}
cloneDict = {}

rowCount = 0

trueRowCount = 0

inputList = []
testDict = {}

myDict.items

mojiUpArrow1 = "▲"
mojiDownArrow1 = "▼"
mojiNeutral = "\U00002796"

# === Functions for Dynamic Input Rows ===

# Define the clamp function
def clamp(value, min_val, max_val):
        return max(min(value, max_val), min_val)

# Clear all input fields
def clear_inputs():
    for i in range(1, trueRowCount + 1):
        window[f'-DYNAMIC_INPUT_{i}-'].update(f"Player {i}")

# Add x number of input fields
def add_inputs(x):
    global rowCount, trueRowCount
    rc = rowCount
    trc = trueRowCount
    for i in range(rc + 1, rc + x + 1):
        if i > trc:
            new_input_row = [
                sg.pin(sg.Text(f"{i}", key=f"-LABEL_{i}-", justification="left", p=(5,5))),
                sg.pin(sg.Input(key=f'-DYNAMIC_INPUT_{i}-', default_text=f"Player {i}"))]
            window.extend_layout(window['-dCOL-'], [new_input_row])
            rowCount += 1
            trueRowCount += 1
            window["-dCOL-"].contents_changed() # Update scroll region
        else:
            rowCount += 1
            window[f"-LABEL_{i}-"].update(visible=True)
            window[f'-DYNAMIC_INPUT_{i}-'].update(visible=True)
            window["-dCOL-"].contents_changed() # Update scroll region


# Delete x number of input fields
def delete_inputs(x):
    global rowCount, trueRowCount
    rc = rowCount
    if rc > 0:
        for i in range(rc, clamp(rc - x, 0, 100), -1):
                if window[f'-DYNAMIC_INPUT_{i}-']:
                    window[f"-LABEL_{i}-"].update(visible=False)
                    window[f'-DYNAMIC_INPUT_{i}-'].update(visible=False)
                    rowCount -= 1
        window["-dCOL-"].contents_changed() # Update scroll region

# Print input fields as a dictionary
def print_inputs():
    for i in range(1, rowCount + 1):
        print(window[f'-DYNAMIC_INPUT_{i}-'].get())

# Define chosen dictionary by inputs
def instance_dict(dictionary):
    dict = dictionary
    dictionary = {} # Wipe the global dictonary value to replace rather than append
    for i in range(1, rowCount + 1):
        dict[i] = window[f'-DYNAMIC_INPUT_{i}-'].get()

# === UI Elements ===

upArrow1 = sg.Text(f"{mojiUpArrow1}", k="upArrow1", font=(10), background_color="green2", text_color="grey4", enable_events=True)
downArrow1 = sg.Text(f"{mojiDownArrow1}", k="downArrow1", font=(10), background_color="firebrick2", text_color="grey4", enable_events=True)
neutral = sg.Text(f"{mojiNeutral}", k="neutral", font=(10), background_color="LightSteelBlue3", text_color="grey4", enable_events=True)

# Terminal output area
terminal_output = [
    [sg.Multiline(
        size=(50, 8), 
        disabled=True, 
        autoscroll=True, 
        key='-TERMINAL-', 
        background_color='black', 
    )]
]

# Column 0 layout. Dynamic name list
column0 = [
    [sg.Text("Column 0")],
    [sg.Column(
        [],
        key='-dCOL0-',
        vertical_scroll_only=True,
        size=(200,300),
        expand_y=True,
        justification='right',
        scrollable=True,
        vertical_alignment='t',
    )],
]

table_area = [
    [sg.Table(
        values=[
            ['Test 1', mojiDownArrow1],
            ['Test 2', upArrow1]
        ],
        headings=['Head 1', 'Emjoii'],
        auto_size_columns=True,
        justification='left',
        num_rows=10,
        expand_x=True,
        expand_y=True,
    )]
]

# Primary layout
layout = [
     [sg.Text("Main Window", relief="solid", font=(12))],
     [upArrow1, downArrow1, neutral],
     [sg.Frame("Frame 0", column0, relief="groove")],
     [table_area],
     [sg.Button("Print")],
     [sg.Button("Exit")]
]

window = sg.Window("Main Window", layout, finalize=True)

# === GUI Event Loop ===
while True:
     event, values = window.read()
     if event == sg.WINDOW_CLOSED or event == "Exit":
        break
     if event == "upArrow1":
        # Create a new row each time with text + the arrow
        new_row = [
            sg.Text("Name:", size=(10,1)), 
            sg.Text(mojiUpArrow1, font=(10), background_color="OliveDrab3"),
        ]
        separator_row = [sg.HSeparator()] # Horizontal separator

        window.extend_layout(window["-dCOL0-"], [new_row, separator_row]) # Extend the column with the text (new row), and the separator
        window["-dCOL0-"].contents_changed()  # update scroll region