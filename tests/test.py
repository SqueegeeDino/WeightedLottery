# hello_world.py
import FreeSimpleGUI as sg

# Column 1 layout
column1 = [
    [sg.Text("Column 1")],
    [sg.Button("Button 1")],
    [sg.Input("Input 1")],
]

# Column 2 layout
column2 = [
    [sg.Text("Column 2")],
    [sg.Button("Button 2")],
    [sg.Input("Input 2")],
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
    [sg.Column(column1), sg.Column(column2)],
    [sg.Frame("Terminal Output", terminal_output)]
]

# Create the window
window = sg.Window("Two Columns with Terminal", layout, finalize=True)

# Example event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    # Print events and values to the terminal area
    window['-TERMINAL-'].print(f"Event: {event}, Values: {values}")

window.close()