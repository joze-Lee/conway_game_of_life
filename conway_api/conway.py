# conway_api/conway.py

from typing import List, Tuple, Literal
import numpy as np

StateType = Literal["Static", "Oscillator", "MaxLimit", "Extinction"]

# Tested - working fine
def word_to_ascii_binary(word: str) -> List[List[int]]:
    """
    Converts an input word into a list of lists of bits.
    Each inner list represents the 8-bit ASCII binary for a single character.
    """
    return [[int(bit) for bit in format(ord(c), '08b')] for c in word]


#should find a better placement
def seed_grid(word: str, grid_size=(60, 40)) -> np.ndarray:
    grid = np.zeros(grid_size, dtype=int)
    binary_pattern = word_to_ascii_binary(word)  # This should return List[List[int]] of bits per char
    print(binary_pattern)
    num_chars = len(binary_pattern)            # Number of chars (rows needed)
    bits_per_char = len(binary_pattern[0]) if num_chars > 0 else 0  # Usually 8 bits
    
    center_row = grid_size[0] // 2
    center_col = grid_size[1] // 2
    
    # Calculate vertical start to center the block of characters
    start_row = center_row - num_chars // 2
    
    # Calculate horizontal start to center 8 bits
    start_col = center_col - bits_per_char // 2
    
    # Clamp boundaries to grid size
    if start_row < 0:
        start_row = 0
    if start_row + num_chars > grid_size[0]:
        start_row = grid_size[0] - num_chars
    
    if start_col < 0:
        start_col = 0
    if start_col + bits_per_char > grid_size[1]:
        start_col = grid_size[1] - bits_per_char
    
    # Place each character's bit pattern in its row
    for i, char_bits in enumerate(binary_pattern):
        row = start_row + i
        grid[row, start_col:start_col + bits_per_char] = char_bits
    
    return grid


#Tested - working fine
def next_generation(grid: np.ndarray) -> np.ndarray:
    """
    Computes the next generation of the grid using Conway's Game of Life rules.
    """
    # Pad and cast to uint8 for consistent type
    padded = np.pad(grid, pad_width=1, mode='constant').astype(np.uint8)
    new_grid = np.zeros_like(grid, dtype=np.uint8)

    # Calculate neighbor sums
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            new_grid += padded[1 + dx : 1 + dx + grid.shape[0],
                               1 + dy : 1 + dy + grid.shape[1]]

    # Apply rules
    birth = (new_grid == 3) & (grid == 0)
    survive = ((new_grid == 2) | (new_grid == 3)) & (grid == 1)

    return (birth | survive).astype(np.uint8)

# Util
def print_grid(grid: np.ndarray):
    for row in grid:
        print("".join('#' if cell else '.' for cell in row))
    print("\n" + "-" * grid.shape[1])


# Tested - working fine
def run_until_stable(seed_word: str, max_generations: int = 1000) -> dict:
    grid = seed_grid(seed_word)
    history = []
    generation_count = 0
    cumulative_score = int(np.sum(grid))

    print(f"Generation {generation_count}:")
    print_grid(grid)

    while generation_count < max_generations:
        new_grid = next_generation(grid)
        generation_count += 1
        cumulative_score += int(np.sum(new_grid))

        print(f"Generation {generation_count}:")
        print_grid(new_grid)

        if np.sum(new_grid) == 0:
            state: StateType = "Extinction"
            break

        if np.array_equal(new_grid, grid):
            state: StateType = "Static"
            break

        if any(np.array_equal(new_grid, past) for past in history[-9:]):
            state: StateType = "Oscillator"
            break

        history.append(grid.copy())
        grid = new_grid

    else:
        state: StateType = "MaxLimit"

    return {
        "generations": generation_count,
        "score": cumulative_score,
        "state": state
    }