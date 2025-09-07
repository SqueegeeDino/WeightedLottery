def clamp(value, min_val, max_val):
        return max(min(value, max_val), min_val)

# Example usage
print(clamp(10, 0, 5))   # Output: 5
print(clamp(-2, 0, 5))  # Output: 0
print(clamp(3, 0, 5))   # Output: 3