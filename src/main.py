import random
import time
import matplotlib.pyplot as plt

# Text colors
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m' # Resets all formatting

# Background colors
BG_YELLOW = '\033[43m'

# === Global parameters for the exponential function (adjust as needed) ===
m = 1
n = 1.5
x_offset = 0
z = 5
b = 0

# === Map participant numbers to names ===
name_map = {
    1: "Cormac",
    2: "Nick",
    3: "Lindsay",
    4: "Ryan",
    5: "Jo",
    6: "Rourke",
    7: "Sean",
    8: "Austin",
    9: "Laura",
    10: "Matt",
    11: "Charlie",
    12: "Tara"
}

# === Define the exponential function ===
def exponential_function(x):
    return m * n ** (x + z) + b

# === Define the clamp function ===
def clamp(value, min_val, max_val):
        return max(min(value, max_val), min_val)

# === Initialize participants and compute initial weights ===
participants = list(range(1, 13))  # Numbers 1 to 12
winners = []
weights = [exponential_function(x) for x in participants]

# Show weights before the draw
print(BLUE + "Remaining contestants and their weights:" + RESET)
for p, w in zip(participants, weights):
    print(BLUE + f"{name_map[p]:<10}" + RESET + f"(#{p}): weight = {w:.2f}")
''' === Uncomment to visualize initial weights ===
# === Plot the weights at the start ===
names = [name_map[p] for p in participants]

plt.figure(figsize=(10, 6))
plt.bar(names, weights, color='skyblue')
plt.xlabel("Participants")
plt.ylabel("Exponential Weight")
plt.title("Initial Weights of Participants Based on Exponential Function")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
'''

choice = input(BG_YELLOW + "\nWould you like to clamp the weights? (Y/N): ").strip().lower()
if choice == 'y':
    while True:
        try:
            cl_high = int(input("Enter high clamp value: "))
            cl_low = int(input("Enter low clamp value: " ))
            if cl_low >= cl_high:
                print(RED + "Low clamp value must be less than high clamp value. Please try again." + RESET)
                continue
            break
        except ValueError:
            print(RED + "Invalid input. Please enter integer values." + RESET)
    
    # Apply clamping to weights
    weights = [clamp(w, cl_low, cl_high) for w in weights]
    
    # Show clamped weights
    print(RESET + GREEN + "\nClamped weights:" + RESET)
    for p, w in zip(participants, weights):
        print(BLUE + f"{name_map[p]:<10}" + RESET + f"(#{p}): weight = {w:.2f}")
elif choice != 'n':
    print(RED + "Invalid input. Proceeding without clamping." + RESET)


time.sleep(1)  # Pause before starting the draw

# === Run 12 rounds ===
for round_number in range(1, 13):
    # Compute current weights for remaining participants
    weights = [exponential_function(x) for x in participants]

    # Pick the winner based on current weights
    winner = random.choices(participants, weights=weights, k=1)[0]
    winners.append(winner)

    # Announce winner
    print(RESET + f"\n🎉 Winner of Round {round_number}: " + BLUE + f"{name_map[winner]} (#{winner})" + RESET)

    # Remove winner from participant pool
    index = participants.index(winner)
    participants.pop(index)

    time.sleep(1)  # Pause for dramatic effect

# === Final summary ===
print(GREEN + "\n=== Final Winner Order ===" + RESET)
for i, winner in enumerate(winners, start=1):
    print(RESET + f"{i}. " + BLUE + f"{name_map[winner]} + BLUE + (#{winner})" + RESET)