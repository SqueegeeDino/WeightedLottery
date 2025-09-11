# hello_world.py
import FreeSimpleGUI as sg

# Test values
test_value = "Hello, World!"

# Test list
my_list = [1, 2, 3, 4, 5]

# Test dictionary
my_dict = {}

# Flexible dictionary population
#num_keys = int(input("Enter number of key-value pairs to add to the dictionary: "))


# Header Image
image_file = r"C:\Users\CormacC\Documents\GitHub\WeightedLottery\src\logo.png"  # Replace with your image file path

# Column 1 layout
column1 = [
    [sg.Text(test_value)],
    [sg.Button("Button 1")],
    [sg.Input(key='Input 1')],
]

# Column 2 layout
column2 = [
    [sg.Text("Column 2")],
    [sg.Button("Button 2")],
    [sg.Input(key='Input 2')],
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
            #

# Full layout: Image and terminal at top, then two colums, then terminal at bottom
layout = [
    [
        sg.Image(filename=image_file),
        sg.VSeparator(),
        sg.Frame("Player List", terminal_output_2)
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

# Example event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Button 1":
        key = values['Input 1']
        my_list.append(name)
        window['-TERMINAL-'].print(f"{player_count}",)
        window['-TERMINAL2-'].print(f"{name}: #{key}")
    elif event == "Button 2":
        name = values['Input 1']
        window['-TERMINAL-'].print(f"{my_dict[name]}",)

window.close()