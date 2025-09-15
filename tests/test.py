import FreeSimpleGUI as sg
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

myList = []
myDict = {}

myDict.items

layout = [
    [
        sg.Button("Exit"), sg.Button("Print"),
    ],
    [
        [sg.Button("Add"), sg.Input(key='input1', size=(10,1))],
        [sg.Button("Remove"), sg.Input(key='input2', size=(10,1))]
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
                try:
                    myDict.pop(name)
                    window['input2'].update("")
                except ValueError: # Catch errors if trying to remove a name that doesn't exist
                    print(f"{name} not found in list.")
            else: # Prevent removing blanks
                print("No input value found")
        except ValueError: # Catch any other errors
            print("Error on removal")