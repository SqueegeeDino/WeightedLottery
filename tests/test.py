import FreeSimpleGUI as sg
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

myList = []

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
        print("Printing myList:")
        print(myList)
    if event == "Add": # Add button
        try:
            if values['input1']:
                try:
                    myList.index(values['input1']) # Search the list for whatever is entered in 'input1'
                    print("Duplicate name found")
                except ValueError: # Only append if no duplicates
                    myList.append(values['input1'])
                    window["input1"].update("")
            else: # Prevent adding blanks
                print("Cannot add blank player")
        except ValueError: # Catch any other errors
            print("Please enter valid values")
    if event == "Remove": # Remove button
        try:
            if values['input2']:
                try:
                    myList.remove(values['input2'])
                    window['input2'].update("")
                except ValueError: # Catch errors if trying to remove a name that doesn't exist
                    print(f"{values['input2']} not found in list.")
            else: # Prevent removing blanks
                print("No input value found")
        except ValueError: # Catch any other errors
            print("Error on removal")