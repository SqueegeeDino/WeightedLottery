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
inputList = []

myDict.items

layout = [
    [
        sg.Button("Exit"), sg.Button("Print"), sg.Button("Add Input")
    ],
    [
        [sg.Button("Add", bind_return_key='Add'), sg.Input(key='input1', size=(10,1))],
        [sg.Button("Remove"), sg.Input(key='input2', size=(10,1))],
        [sg.Button("Search"), sg.Input(key='input3', size=(10,1))],
    ],
    [
        sg.Column([], key='-COL1-'), # Container for dynamic content
    ],
]

window = sg.Window("MainWindow", layout, finalize=True)

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
    if event == "Add Input":
        rowCount += 1
        new_input_row = [sg.Text(f"{rowCount}", justification="left", p=(5,5)), sg.Input(key=f'-DYNAMIC_INPUT_{rowCount}-', default_text=f"Input {rowCount}")]
        window.extend_layout(window['-COL1-'], [new_input_row])