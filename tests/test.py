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
    "z": 1,
    "b": 5
}

weight = []  # To hold computed weights    

params_default = params.copy()  # Store default parameters for reset

# Clamping parameters
clamp_bool = False
clamp_high = 999999
clamp_low = 1


my_dict = {} # Main dictionary to hold player names and their assigned numbers
lottery_participants = []  # To hold participants for each lottery run 
participants = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # Example participant offsets 

# Define the odds function
def odds_function():
    m = params['m']
    n = params['n']
    z = params['z']
    b = params['b']
    x = params['x_offset']
    
    # Calculate raw weight
    weight = m * n ** (x + z) + b
    
    # Apply clamping if enabled
    weight = clamp(weight, clamp_low, clamp_high)
    
    # IMPORTANT: sum of weights also needs clamping applied
    all_weights = [m * n ** (xi + z + x) + b for xi in participants]
    all_weights = [clamp(w, clamp_low, clamp_high) for w in all_weights]
    
    return weight / sum(all_weights), weight

# Define the clamp function
def clamp(value, min_val, max_val):
        return max(min(value, max_val), min_val)

odds_function()
print(weight)