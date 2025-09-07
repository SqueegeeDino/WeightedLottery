import random
import time
import matplotlib.pyplot as plt

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

# === Initialize participants and compute initial weights ===
participants = list(range(1, 13))  # Numbers 1 to 12
winners = []

# Show weights before the draw
weights = [exponential_function(x) for x in participants]
print("Remaining contestants and their weights:")
for p, w in zip(participants, weights):
    print(f"{name_map[p]:<10} (#{p}): weight = {w:.2f}")
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

time.sleep(1)  # Pause before starting the draw

# === Run 12 rounds ===
for round_number in range(1, 13):
    # Compute current weights for remaining participants
    weights = [exponential_function(x) for x in participants]

    # Pick the winner based on current weights
    winner = random.choices(participants, weights=weights, k=1)[0]
    winners.append(winner)

    # Announce winner
    print(f"\n🎉 Winner of Round {round_number}: {name_map[winner]} (#{winner})")

    # Remove winner from participant pool
    index = participants.index(winner)
    participants.pop(index)

    time.sleep(1)  # Pause for dramatic effect

# === Final summary ===
print("\n=== Final Winner Order ===")
for i, winner in enumerate(winners, start=1):
    print(f"{i}. {name_map[winner]} (#{winner})")