# hello_world.py
import FreeSimpleGUI as sg
import random
import time
import matplotlib.pyplot as plt

# === Global parameters for the exponential function (adjust as needed) ===
m = 1.0
n = 1.5
x_offset = 0
z = 5.0
b = 0

# Test dictionary
my_dict = {}

# Flexible dictionary population
#num_keys = int(input("Enter number of key-value pairs to add to the dictionary: "))


# Header Image
image_file = r"C:\Users\CormacC\Documents\GitHub\WeightedLottery\src\logo.png"  # Replace with your image file path

# Column 1 layout
column1 = [
    [sg.Text("Column 1")],
    [sg.Button("Button 1")],
    [sg.Input(key='Input 1')],
]

# Column 2 layout
column2 = [
    [sg.Text("Column 2")],
    [sg.Text(f"M = {m}", background_color='white', text_color='black', key="mText"), sg.Slider((0, 5), orientation='h', size=(20, 15), key='mSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
    [sg.Text(f"N = {n}", background_color='white', text_color='black', key="nText"), sg.Slider((0, 5), orientation='h', size=(20, 15), key='nSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
    [sg.Text(f"X = {x_offset}", background_color='white', text_color='black', key="xText"), sg.Slider((0, 5), orientation='h', size=(20, 15), key='xSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
    [sg.Text(f"Z = {z}", background_color='white', text_color='black', key="zText"), sg.Slider((0, 5), orientation='h', size=(20, 15), key='zSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
    [sg.Text(f"B = {b}", background_color='white', text_color='black', key="bText"), sg.Slider((0, 5), orientation='h', size=(20, 15), key='bSlider', enable_events=True, disable_number_display=True, resolution=0.1)],
]

# Terminal output area
terminal_output = [
    [sg.Multiline(
        size=(100, 10), 
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
        size=(45, 15), 
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
        sg.Frame("Player List", terminal_output_2), sg.Button("Exit"),
    ],
    [
        sg.Column(column1),
        sg.VSeparator(),
        sg.Column(column2)
    ],
    [
        sg.Frame("Terminal Output", terminal_output)
    ]
]

# Create the window
window = sg.Window("Two Columns with Terminal", layout, finalize=True)

# Print player list to terminal
window['-TERMINAL2-'].print(f"{my_dict}")

# Print each player and their assigned number
for number, player in my_dict.items():
    window['-TERMINAL2-'].print(f"{number}: {player}")

# Example event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    if event == 'mSlider':
        m = (values['mSlider'])
        window['mText'].update(f"M = {m}")
    if event == 'nSlider':
        n = (values['nSlider'])
        window['nText'].update(f"N = {n}")
    if event == 'xSlider':
        x_offset = (values['xSlider'])
        window['xText'].update(f"X = {x_offset}")
    if event == 'zSlider':
        z = (values['zSlider'])
        window['zText'].update(f"Z = {z}")
    if event == 'bSlider':
        b = (values['bSlider'])
        window['bText'].update(f"B = {b}")
    elif event == "Button 1":
        try:
            keySearch = (values['Input 1'])
        except ValueError:
            window['-TERMINAL2-'].print("Please enter a valid integer key.")
            continue
        window['-TERMINAL2-'].print(f"{my_dict[keySearch] if keySearch in my_dict else 'Key not found'}")

window.close()