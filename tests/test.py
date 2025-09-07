# Define the clamp function
def clamp(value, min_val, max_val):
        return max(min(value, max_val), min_val)

# Create high and low clamp values
cl_high = 10
cl_low = 1
''' === Uncomment to get user input for clamp values ===
# Get user input for high and low clamp values
while True:
    try:
        cl_high = int(input("Enter high clamp value: "))
        cl_low = int(input("Enter low clamp value: "))
        if cl_low >= cl_high:
            print("Low clamp value must be less than high clamp value. Please try again.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter integer values.")

# Test the clamp function
print(clamp(15, cl_low, cl_high))
'''

# Text colors
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m' # Resets all formatting

print(RED + "This text is red." + RESET)
print(GREEN + "This text is green." + RESET)
print(BLUE + "This text is blue." + RESET)

# Background colors
BG_YELLOW = '\033[43m'
print(BG_YELLOW + "This text has a yellow background." + RESET)

# Combined formatting
print(RED + BG_YELLOW + "Red text on a yellow background." + RESET)
print(GREEN + "Green text" + RESET + " with normal text in between." + RESET)