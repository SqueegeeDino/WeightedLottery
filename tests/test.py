# hello_world.py
import FreeSimpleGUI as sg
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# === Global parameters ===
# Global parameter dictionary
params = {
    "m": 1,
    "n": 1.5,
    "x_offset": 0,
    "z": 5,
    "b": 0
}

params_default = params.copy()  # Store default parameters for reset

# Main dictionary to hold player names and their assigned numbers
my_dict = {}

# === Define functions ===
# Define the exponential function
def exponential_function(x):
    m = params['m']
    n = params['n']
    z = params['z']
    b = params['b']
    return m * n ** (x + z) + b

# Define the clamp function
def clamp(value, min_val, max_val):
        return max(min(value, max_val), min_val)

# Function to control slider logic in GUI
def controlSlider(param_name, slider, text, label):
    global params
    value = values[f'{slider}']  # Get value from GUI slider
    params[param_name] = value   # Dynamically assign value to param
    window[f'{text}'].update(f"{label} = {value}")
    window['-TERMINAL-'].update('')
    weights = [exponential_function(x) for x in participants]
    for p, w in zip(participants, weights):
        window['-TERMINAL-'].print(f"{my_dict[p]:<10}" + f"(#{p}): weight = {w:.2f}")
    return value

# === GUI Layout ===
# Header Image
image_file = r"C:\Users\CormacC\Documents\GitHub\WeightedLottery\src\logo.png"  # Replace with your image file path

# Column 1 layout
column1 = [
    [sg.Text("Column 1")],
    [sg.Button("Defaults", key='buttonDefaults', tooltip="Reset weighting equation to default values"), 
     sg.Checkbox(default=False, text="Clamp Weights", key='clampWeights', enable_events=True, tooltip="Enable weight clamping"),
     sg.Button("Run Lottery", key='buttonRun', tooltip="Run the lottery with current settings")],
    [sg.Input(key='clampHigh', size=(10,1), disabled=True), sg.Text("Clamp High"), sg.Input(key='clampLow', size=(10,1), disabled=True), sg.Text("Clamp Low")],
]

# Column 2 layout. Slider controls for m, n, x_offset, z, b
column2 = [
    [sg.Text("Column 2")],
    [sg.Text(f"M = {params['m']}", background_color='white', text_color='black', key="mText"), sg.Slider((0, 5), orientation='h', size=(20, 15), key='mSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
    [sg.Text(f"N = {params['n']}", background_color='white', text_color='black', key="nText"), sg.Slider((0, 5), orientation='h', size=(20, 15), key='nSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
    [sg.Text(f"X = {params['x_offset']}", background_color='white', text_color='black', key="xText"), sg.Slider((0, 5), orientation='h', size=(20, 15), key='xSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
    [sg.Text(f"Z = {params['z']}", background_color='white', text_color='black', key="zText"), sg.Slider((0, 5), orientation='h', size=(20, 15), key='zSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
    [sg.Text(f"B = {params['b']}", background_color='white', text_color='black', key="bText"), sg.Slider((0, 5), orientation='h', size=(20, 15), key='bSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
]

# Plot area
plotArea = [
    [sg.Text('My Plot')],
    [sg.Canvas(key='-CANVAS-', size=(400, 200))], # Adjust size as needed
]

# Terminal output area
terminal_output = [
    [sg.Multiline(
        size=(45, 8), 
        disabled=True, 
        autoscroll=True, 
        key='-TERMINAL-', 
        background_color='black', 
        text_color='white'
    )]
]

# Terminal output area 2
terminal_output_2 = [
    [sg.Multiline(
        size=(30, 8), 
        disabled=True, 
        autoscroll=True, 
        key='-TERMINAL2-', 
        background_color='black', 
        text_color='white'
    )]
]

# Player count pop up
player_count = sg.popup_get_text("Enter number of players:", title="Player Count")

# Player names loop
if player_count and player_count.isdigit():
    player_count = int(player_count)
    for i in range(player_count):
        name = sg.popup_get_text(f"Enter name for player {i + 1}:", title="Player Name")
        if name:
            my_dict[name] = i + 1

# Swap keys and values in dictionary, then set them back to my_dict
swapped_dict = {v: k for k, v in my_dict.items()}
my_dict = swapped_dict

# Full layout: Image and terminal at top, then two colums, then terminal at bottom
layout = [
    [
        sg.Image(filename=image_file),
        sg.VSeparator(),
        sg.Frame("Player List", terminal_output_2), sg.VSeparator(), sg.Frame("Terminal Output", terminal_output), sg.Button("Exit"),
    ],
    [
        [sg.Column(column1), sg.Column(column2),],
        sg.VSeparator(),
        #sg.Frame("Plot Area", plotArea)
    ]
]

# Create the window
window = sg.Window("Two Columns with Terminal", layout, finalize=True)

window['mSlider'].update(params['m'])
window['nSlider'].update(params['n'])
window['xSlider'].update(params['x_offset'])
window['zSlider'].update(params['z'])
window['bSlider'].update(params['b'])
window['mText'].update(f"M = {params['m']}")
window['nText'].update(f"N = {params['n']}")
window['xText'].update(f"X = {params['x_offset']}")
window['zText'].update(f"Z = {params['z']}")
window['bText'].update(f"B = {params['b']}")

# === Lottery Logic ===
# Initialize participants and compute initial weights
participants = list(range(1, int(player_count + 1)))  # Numbers 1 to 12
winners = []
weights = [exponential_function(x) for x in participants]

# Show weights before the draw
for p, w in zip(participants, weights):
    window['-TERMINAL-'].print(f"{my_dict[p]:<10}" + f"(#{p}): weight = {w:.2f}")

# Print player list to terminal
window['-TERMINAL2-'].print(f"Participants:{participants}")

# Print each player and their assigned number
for number, player in my_dict.items():
    window['-TERMINAL2-'].print(f"{number}: {player}")

# === GUI Event Loop ===
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    if event == 'mSlider':
        controlSlider('m', 'mSlider', 'mText', 'M')
    if event == 'nSlider':
        controlSlider('n', 'nSlider', 'nText', 'N')
    if event == 'xSlider':
        controlSlider('x_offset', 'xSlider', 'xText', 'X')
    if event == 'zSlider':
        controlSlider('z', 'zSlider', 'zText', 'Z')
    if event == 'bSlider':
        controlSlider('b', 'bSlider', 'bText', 'B')
    if event == 'clampWeights':
        if values['clampWeights']:
            window['clampHigh'].update(disabled=False)
            window['clampLow'].update(disabled=False)
        else:
            window['clampHigh'].update(disabled=True)
            window['clampLow'].update(disabled=True)
    if event == "buttonDefaults":
        params = params_default.copy()
        window['mSlider'].update(params['m'])
        window['nSlider'].update(params['n'])
        window['xSlider'].update(params['x_offset'])
        window['zSlider'].update(params['z'])
        window['bSlider'].update(params['b'])
        window['mText'].update(f"M = {params['m']}")
        window['nText'].update(f"N = {params['n']}")
        window['xText'].update(f"X = {params['x_offset']}")
        window['zText'].update(f"Z = {params['z']}")
        window['bText'].update(f"B = {params['b']}")
        weights = [exponential_function(x) for x in participants]
        window['-TERMINAL-'].update('')
        for p, w in zip(participants, weights):
            window['-TERMINAL-'].print(f"{my_dict[p]:<10}" + f"(#{p}): weight = {w:.2f}")

window.close()