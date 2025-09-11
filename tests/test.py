# hello_world.py
import FreeSimpleGUI as sg

# Test values
test_value = "Hello, World!"

# Test list
my_list = [1, 2, 3, 4, 5]


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
        size=(80, 10), 
        disabled=True, 
        autoscroll=True, 
        key='-TERMINAL-', 
        background_color='black', 
        text_color='white'
    )]
]

# Full layout: two columns on top, terminal output below
layout = [
    [sg.Image(filename=image_file)],
    [sg.Column(column1), sg.VSeparator(), sg.Column(column2)],
    [sg.Frame("Terminal Output", terminal_output)]
]

# Create the window
window = sg.Window("Two Columns with Terminal", layout, finalize=True)

# Example event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Button 1":
        name = values['Input 1']
        my_list.append(name)
        window['-TERMINAL-'].print(f"{name}",)
    elif event == "Button 2":
        window['-TERMINAL-'].print(f"{my_list}")

window.close()