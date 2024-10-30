def read_counter(filename):
    """
    Reads the counter value from the specified file.

    Args:
        filename (str): Path to the counter file.

    Returns:
        int: The counter value read from the file.
    """
    try:
        with open(filename, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        print(f"File '{filename}' not found. Initializing counter with value 0.")
        return 0

def update_counter(filename, counter):
    """
    Updates the counter value in the specified file.

    Args:
        filename (str): Path to the counter file.
        counter (int): The new counter value to write to the file.
    """
    try:
        with open(filename, "w") as file:
            file.write(str(counter))
        print(f"Counter updated in '{filename}'. New value: {counter}")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

# Example usage

