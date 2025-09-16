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
        for i in range(rc - x + 1, rc -1, -1):
                window[f"-LABEL_{i}-"].update(visible=False)
                window[f'-DYNAMIC_INPUT_{i}-'].update(visible=False)
                rowCount -= 1
        window["-dCOL-"].contents_changed() # Update scroll region

def print_inputs():
    for i in range(1, rowCount + 1):
        print(window[f'-DYNAMIC_INPUT_{i}-'].get())

column0 = [
        [sg.Text("Column 0")],
        [sg.Button("Exit"), sg.Button("Print")], 
        [sg.Button("Add Inputs"), sg.Input(key='input_add', size=(10,1), default_text="1")],
        [sg.Button("Remove Inputs"), sg.Input(key='input_remove', size=(10,1), default_text="1")],
        [sg.Button("Add", bind_return_key=True), sg.Input(key='input1', size=(10,1))],
        [sg.Button("Remove"), sg.Input(key='input2', size=(10,1))],
        [sg.Button("Search"), sg.Input(key='input3', size=(10,1))],
]

column1 = [
    [sg.Text("Dynamic Input Rows")],
    [sg.Column(
        [],              # start with empty row list
        key='-dCOL-',
        vertical_scroll_only=True,
        size=(200, 200),   # give it a fixed size if you want scroll
        expand_y=True,
        justification='right',   # align horizontally
        element_justification='left',  # align inside rows
        scrollable=True,
        vertical_alignment="t",
    )]
]

layout = [
    [sg.Column(column0, key='-COL0-', vertical_alignment="t"), sg.VSeperator(), sg.Column(column1, key='-COL1-', vertical_alignment="t")],
]

window = sg.Window("MainWindow", layout, finalize=True, resizable=True)

# === GUI Event Loop
while True:
    event, values = window.read() # Necessary for reading window events
    if event == sg.WINDOW_CLOSED or event == "Exit": # Exit window event
        break
    if event == "Print": # Print button
        print("Printing myDict:")
        print(myDict)
    if event == "Add": # Add button
        try:
            if values['input1']:
                name = values['input1']
                if myDict.get(name):
                    print(f"Player {name} already exists")
                else: # Only append if no duplicates
                    myDict[name] = len(myDict) +1
                    window["input1"].update("")
            else: # Prevent adding blanks
                print("Cannot add blank player")
        except ValueError: # Catch any other errors
            print("Please enter valid values")
    if event == "Remove": # Remove button
        try:
            if values['input2']:   
                name = values['input2']   
                try: # Try to remove the name at 'input2'
                    myDict.pop(name)
                    cloneDict = {} # Wipe the clone dict
                    for p in myDict:
                        cloneDict[p] = len(cloneDict) + 1
                    window['input2'].update("")
                    myDict = cloneDict
                except ValueError: # Catch errors if trying to remove a name that doesn't exist
                    print(f"{name} not found in list.")
            else: # Prevent removing blanks
                print("No input value found")
        except ValueError: # Catch any other errors
            print("Error on removal")
    if event == "Search":
        if values['input3']:
            try:
                searchIndex = int(values['input3'])
                if searchIndex <= rowCount and searchIndex > 0:
                    print(values[f'-DYNAMIC_INPUT_{searchIndex}-'])
            except ValueError:
                print("Please input a valid integer")
    if event == "Add Inputs":
        print("Try adding inputs")
        print(f"Count to add: {int(values['input_add'])}")
        add_inputs(int(values['input_add']))
    if event == "Remove Inputs":
        print("Try removing inputs")
        print(f"Count to remove: {int(values['input_remove'])}")
        delete_inputs(int(values['input_remove']))