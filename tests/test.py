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

layout = [
     [sg.Text("Main Window")],
     [sg.Button("Exit")]
]

window = sg.Window("Main Window", layout, finalize=True)

# === GUI Event Loop ===
while True:
     event, values = window.read()
     if event == sg.WINDOW_CLOSED or event == "Exit":
        break
