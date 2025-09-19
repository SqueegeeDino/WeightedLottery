# Weighted Lottery System with Adjustable Exponential Weighting
import FreeSimpleGUI as sg
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# === Global parameters ===
# General variables
rowCount = 0
trueRowCount = 0

# Exponential function parameters
params = {
    "m": 1,
    "n": 1.5,
    "x_offset": 0,
    "z": 1,
    "b": 5
}

params_default = params.copy()  # Store default parameters for reset

# Clamping parameters
clamp_bool = False
clamp_high = 999999
clamp_low = 1
user_clampHigh = 0
user_clampLow = 0


myDict = {} # Main dictionary to hold player names and their assigned numbers
lottery_participants = []  # To hold participants for each lottery run  

# === Define functions === 
# Define the exponential function
def exponential_function(x):
    m = params['m']
    n = params['n']
    z = params['z']
    b = params['b']
    x = x + params['x_offset']
    return m * n ** (x + z) + b

# Define the odds function
def odds_function(x):
    m = params['m']
    n = params['n']
    z = params['z']
    b = params['b']
    x = x + params['x_offset']
    
    # Calculate raw weight
    weights = m * n ** (x + z) + b
    
    # Apply clamping
    weights = clamp(weights, clamp_low, clamp_high)
    
    # IMPORTANT: sum of weights also needs clamping applied
    all_weights = [m * n ** (xi + z + params['x_offset']) + b for xi in participants]
    all_weights = [clamp(w, clamp_low, clamp_high) for w in all_weights]
    
    odds = weights / sum(all_weights)

    return odds, weights

# Define the clamp function
def clamp(value, min_val, max_val):
        return max(min(value, max_val), min_val)

# New combined print weights and odds function
def print_odds():
    global participants, weights, myDict, clamp_bool, clamp_high, clamp_low
    
    # Get odds and weights
    odds = [odds_function(x)[0] for x in participants] # Calculate odds
    weights = [odds_function(x)[1] for x in participants] # Get weights from odds function

    # Clear terminal
    window['-TERMINAL-'].update('')
    
    # Fixed column widths
    name_width = 20
    id_width = 6
    weight_width = 10
    odds_width = 9
    
    # Print header
    window['-TERMINAL-'].print(
        f"{'Name':<{name_width}} {'ID':<{id_width}} {'Weight':>{weight_width}} {'Odds':>{odds_width}}"
    )
    window['-TERMINAL-'].print("-" * (name_width + id_width + weight_width + odds_width + 3))
    
    # Print rows
    for p, w, o in zip(participants, weights, odds):
        window['-TERMINAL-'].print(
            f"{myDict[p]:<{name_width}} (#{p:<3}) {w:{weight_width}.2f} {o*100:{odds_width}.2f}%"
        )

# Define table_populate function
def table_populate():
    global participants, weights, myDict, clamp_bool, clamp_high, clamp_low

    # Get odds and weights
    odds = [odds_function(x)[0] for x in participants] # Calculate odds
    weights = [odds_function(x)[1] for x in participants] # Get weights from odds function
    
    table_data = []
    for p, w, o in zip(participants, weights, odds):
        table_data.append([myDict[p], p, f"{w:.2f}", f"{o*100:.2f}%"])
    
    window['-TABLE-'].update(values=table_data)

# Function to control slider logic in GUI
def controlSlider(param_name, slider, text, label):
    global params, weights, participants
    value = values[f'{slider}']  # Get value from GUI slider
    params[param_name] = value   # Dynamically assign value to param
    window[f'{text}'].update(f"{label} = {value}") # Update text display
    table_populate() # Update table
    return value

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

# Define chosen dictionary by inputs
def instance_dict(dictionary):
    dict = dictionary
    dictionary = {} # Wipe the global dictonary value to replace rather than append
    for i in range(1, rowCount + 1):
        dict[i] = window[f'-DYNAMIC_INPUT_{i}-'].get()

def print_inputs():
    for i in range(1, rowCount + 1):
        print(window[f'-DYNAMIC_INPUT_{i}-'].get())

# === GUI Layout ===
# Header Image
image_file = os.path.abspath("./src/logo.png")  # Replace with your image file path

# Column 1 layout. Buttons and clamp inputs
column1 = [
    [sg.Text("Column 1")],
    [sg.Button("Defaults", key='buttonDefaults', tooltip="Reset weighting equation to default values"), 
     sg.Checkbox(default=False, text="Clamp Weights", key='clampWeights', enable_events=True, tooltip="Enable weight clamping"),
     sg.Button("Run Lottery", key='buttonRun', tooltip="Run the lottery with current settings")],
    [sg.Text("Clamp High"), sg.Input(key='clampHigh', size=(10,1), disabled=True, enable_events=True), sg.VSeparator(), sg.Text("Clamp Low"), sg.Input(key='clampLow', size=(10,1), disabled=True, enable_events=True),],
]

# Column 2 layout. Slider controls for m, n, x_offset, z, b
column2 = [
    [sg.Text("Column 2")],
    # Uncomment the following line to enable m slider. Currently disabled for simplicity. Has no effect on odds, only on weights.
    # [sg.Text(f"M = {params['m']}", background_color='white', text_color='black', key="mText"), sg.Slider((0.1, 5), orientation='h', size=(20, 15), key='mSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
    [sg.Text(f"N = {params['n']}", background_color='white', text_color='black', key="nText"), sg.Slider((1, 10), orientation='h', size=(20, 15), key='nSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
    # Uncomment the following line to enable x_offset slider. Currently disabled for simplicity. Has no effect on odds, only on weights.
    # [sg.Text(f"X = {params['x_offset']}", background_color='white', text_color='black', key="xText"), sg.Slider((0, 5), orientation='h', size=(20, 15), key='xSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
    # Uncomment the following line to enable z slider. Currently disabled for simplicity. Has no effect on odds, only on weights.
    # [sg.Text(f"Z = {params['z']}", background_color='white', text_color='black', key="zText"), sg.Slider((0.1, 5), orientation='h', size=(20, 15), key='zSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
    [sg.Text(f"B = {params['b']}", background_color='white', text_color='black', key="bText"), sg.Slider((-100, 100), orientation='h', size=(20, 15), key='bSlider', enable_events=True, disable_number_display=True, resolution=1)],
]

column3 = [
        [sg.Text("Column 0")],
        [sg.Button("Exit", key='Exit2'), sg.Button("Print")], 
        [sg.Button("Add Inputs"), sg.Input(key='input_add', size=(10,1), default_text="1")],
        [sg.Button("Remove Inputs"), sg.Input(key='input_remove', size=(10,1), default_text="1")],
        [sg.Button("Clear Inputs", tooltip="Reset input fields to default values"), sg.Button("Print Inputs")],
]

column4 = [
    [sg.Text("Dynamic Input Rows")],
    [sg.Column(
        [],              # start with empty row list
        key='-dCOL-',
        vertical_scroll_only=True,
        size=(200, 300),   # give it a fixed size if you want scroll
        expand_y=True,
        justification='right',   # align horizontally
        element_justification='left',  # align inside rows
        scrollable=True,
        vertical_alignment="t",
    )]
]

# Plot area
plotArea = [
    [sg.Text('My Plot')],
    [sg.Canvas(key='-CANVAS-', size=(400, 200))], # Adjust size as needed
]

# Terminal output area
terminal_output = [
    [sg.Multiline(
        size=(50, 8), 
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

# Table area
table_area = [
    [sg.Table(
        values=[],  # Will be populated later
        headings=['Player', 'ID', 'Weight', 'Odds'],
        auto_size_columns=True,
        display_row_numbers=False,
        justification='left',
        key='-TABLE-',
        num_rows=10,
        enable_events=True,
        tooltip='This is a table'
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
            myDict[name] = i + 1

# Swap keys and values in dictionary, then set them back to myDict
swapped_dict = {v: k for k, v in myDict.items()}
myDict = swapped_dict

# Tabs
tab_layout_1 = [
    [
        sg.Image(filename=image_file),
        sg.VSeparator(),
        sg.Frame("Player odds", table_area), sg.VSeparator(),
        sg.Frame("Player weights", terminal_output), 
        sg.Button("Exit"),
    ],
    [
        sg.Column(column1), sg.Column(column2),
        sg.VSeparator(),
        #sg.Frame("Plot Area", plotArea)
    ],
]

tab_layout_2 = [
    [sg.Text("Tab 2"), sg.Column(column3, key='-COL3-', vertical_alignment="t"), sg.VSeperator(), sg.Column(column4, key='-COL4-', vertical_alignment="t")],
]

# Full layout: Image and terminal at top, then two colums, then terminal at bottom
layout = [
    [sg.TabGroup([[sg.Tab('Main', tab_layout_1), sg.Tab('Tab 2', tab_layout_2)]], key='-TABGROUP-', expand_x=True, expand_y=True, enable_events=True)],
]

# Create the window
window = sg.Window("Two Columns with Terminal", layout, finalize=True)

#window['mSlider'].update(params['m'])
window['nSlider'].update(params['n'])
#window['xSlider'].update(params['x_offset'])
#window['zSlider'].update(params['z'])
window['bSlider'].update(params['b'])
#window['mText'].update(f"M = {params['m']}")
window['nText'].update(f"N = {params['n']}")
#window['xText'].update(f"X = {params['x_offset']}")
#window['zText'].update(f"Z = {params['z']}")
window['bText'].update(f"B = {params['b']}")

# === Lottery Logic ===
# Initialize participants and compute initial weights
participants = list(range(1, int(player_count + 1)))  # Numbers 1 to 12
winners = []
table_populate() # Initial population of table

# === GUI Event Loop ===
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit" or event == "Exit2":
        break
    if event == "-TABGROUP-":
        instance_dict(myDict)
        table_populate()
    # Sliders
    #if event == 'mSlider':
        #controlSlider('m', 'mSlider', 'mText', 'M')
    if event == 'nSlider':
        controlSlider('n', 'nSlider', 'nText', 'N')
    #if event == 'xSlider':
        #controlSlider('x_offset', 'xSlider', 'xText', 'X')
    #if event == 'zSlider':
        #controlSlider('z', 'zSlider', 'zText', 'Z')
    if event == 'bSlider':
        controlSlider('b', 'bSlider', 'bText', 'B')
    # Clamping
    if event == 'clampWeights':
        if values['clampWeights']: # Trigger when checking clamps to True
            clamp_bool = True
            window['clampHigh'].update(disabled=False)
            window['clampLow'].update(disabled=False)
            if values['clampHigh']:
                try:
                    clamp_high = int(values['clampHigh'])
                    if clamp_low >= clamp_high:
                        window['-TERMINAL-'].print("Low clamp value must be less than high clamp value. Please try again.")
                        continue
                except ValueError:
                    window['-TERMINAL-'].print("High clamp invalid input. Please enter integer values.")
                    continue
            if values['clampLow']:
                try:
                    clamp_low = int(values['clampLow'])
                    if clamp_low >= clamp_high:
                        window['-TERMINAL-'].print("Low clamp value must be less than high clamp value. Please try again.")
                        continue
                except ValueError:
                    window['-TERMINAL-'].print("Low clamp invalid input. Please enter integer values.")
        else: # Trigger when checking clamps to False
            clamp_bool = False
            clamp_high = 999999
            clamp_low = -999999
            window['clampHigh'].update(disabled=True)
            window['clampLow'].update(disabled=True)
        table_populate()
    if event == "clampHigh":
        try:
            clamp_high = int(values['clampHigh'])
            if clamp_low >= clamp_high:
                window['-TERMINAL-'].print("Low clamp value must be less than high clamp value. Please try again.")
                continue
            if clamp_high < 1:
                window['-TERMINAL-'].print("High clamp cannot be less than 1. Please try a higher value.")
                clamp_low = 1
                window['clampHigh'].update("")
                continue    
            user_clampHigh = clamp_high
            table_populate()
        except ValueError:
            window['-TERMINAL-'].print("Invalid input. Please enter integer values.")
            continue
    # Clamping checkbox
    if event == "clampLow":
        try:
            clamp_low = int(values['clampLow'])
            if clamp_low >= clamp_high:
                window['-TERMINAL-'].print("Low clamp value must be less than high clamp value. Please try again.")
                clamp_low = 1
                window['clampLow'].update("")
                continue
            if clamp_low < 1:
                window['-TERMINAL-'].print("Low clamp cannot be less than 1. Please try a higher value.")
                clamp_low = 1
                window['clampLow'].update("")
                continue
            user_clampLow = clamp_low
            table_populate()
        except ValueError:
            window['-TERMINAL-'].print("Invalid input. Please enter integer values.")
            continue
    # Defaults button
    if event == "buttonDefaults":
        params = params_default.copy()
        #window['mSlider'].update(params['m'])
        window['nSlider'].update(params['n'])
        #window['xSlider'].update(params['x_offset'])
        #window['zSlider'].update(params['z'])
        window['bSlider'].update(params['b'])
        #window['mText'].update(f"M = {params['m']}")
        window['nText'].update(f"N = {params['n']}")
        #window['xText'].update(f"X = {params['x_offset']}")
        #window['zText'].update(f"Z = {params['z']}")
        window['bText'].update(f"B = {params['b']}")
        window['clampWeights'].update(False)
        clamp_bool = False
        clamp_high = 999999
        clamp_low = 1
        # Get odds and weights
        odds = [odds_function(x)[0] for x in participants] # Calculate odds
        weights = [odds_function(x)[1] for x in participants] # Get weights from odds function
        window['-TERMINAL-'].update('')
        for p, w in zip(participants, weights):
            window['-TERMINAL-'].print(f"{myDict[p]:<10}" + f"(#{p}): weight = {w:.2f}")
    # Run Lottery button
    if event == "buttonRun":
        lottery_participants = participants.copy()  # Reset participants for new draw
        winners = [] # Reset winners list
        window['-TERMINAL-'].update("")
        window['-TERMINAL-'].print(f"Winners:\n")
        for round_number in range(1, int(player_count + 1)):
            # Compute current weights for remaining participants
            # Get odds and weights
            odds = [odds_function(x)[0] for x in lottery_participants] # Calculate odds
            weights = [odds_function(x)[1] for x in lottery_participants] # Get weights from odds function

            # Pick the winner based on current weights
            winner = random.choices(lottery_participants, weights=weights, k=1)[0]
            winners.append(winner)

            # Announce winner
            sg.popup(f"Winner of Round {round_number}:\n "f"{myDict[winner]} (#{winner})", title=f"Winner of Round {round_number}", no_titlebar=True, auto_close=True, auto_close_duration=2, button_justification="centered")
            window['-TERMINAL-'].print(f"{round_number}: {myDict[winner]}")

            # Remove winner from participant pool
            index = lottery_participants.index(winner)
            lottery_participants.pop(index)

    # Tab 2
    if event == "Print": # Print button
        print("Printing myDict:")
        print(myDict)
    if event == "Add Inputs": # Add inputs button
        add_inputs(int(values['input_add']))
        instance_dict(myDict)
    if event == "Remove Inputs": # Remove inputs button
        delete_inputs(int(values['input_remove']))
        instance_dict(myDict)
    if event == "Clear Inputs": # Clear inputs button
        clear_inputs()
        instance_dict(myDict)
    if event == "Print Inputs": # Print inputs button, mostly diagnostic
        print_inputs()
        instance_dict(myDict)
    if event == "Print": # Print button
        print("Printing myDict:")
        print(myDict)        

window.close()