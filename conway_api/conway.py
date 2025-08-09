# conway_api/conway.py

from typing import List, Literal
import numpy as np
from scipy.signal import convolve2d


StateType = Literal["Static", "Oscillator", "MaxLimit", "Extinction"]

# Tested - working fine
def word_to_ascii_binary(word: str) -> List[List[int]]:
    """
    Convert a word into a list of binary bit lists representing each character's ASCII code.

    Args:
        word (str): The input word.

    Returns:
        List[List[int]]: Each inner list is an 8-bit binary representation of a character.
    """
    
    return [[int(bit) for bit in format(ord(c), '08b')] for c in word]


#should find a better placement
def seed_grid(word: str, grid_size=(60, 40)) -> np.ndarray:
    """
    Create a grid seeded with the ASCII binary representation of the input word,
    centered in the grid for Conway's Game of Life initialization.

    Args:
        word (str): The input word to convert into a seed pattern.
        grid_size (tuple): Size of the grid as (rows, columns).

    Returns:
        np.ndarray: 2D grid with the word’s binary pattern placed in the center.
    """
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

# for more optimized apprach using convolve2d
def next_generation(grid: np.ndarray) -> np.ndarray:
    """
    Calculate the next generation of the grid using Conway's Game of Life rules.

    Args:
        grid (np.ndarray): Current grid state (2D array of 0s and 1s).

    Returns:
        np.ndarray: Next generation grid state.
    """
    
    # Define the convolution kernel (3x3 with center 0)
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]], dtype=np.uint8)

    # Perform convolution to count neighbors
    neighbor_count = convolve2d(grid, kernel, mode='same', boundary='fill', fillvalue=0)

    # Apply rules
    birth = (neighbor_count == 3) & (grid == 0)
    survive = ((neighbor_count == 2) | (neighbor_count == 3)) & (grid == 1)

    return (birth | survive).astype(np.uint8)



# Util
def print_grid(grid: np.ndarray):
    for row in grid:
        print("".join('-' if cell else '@' for cell in row))
    print("\n" + "-" * grid.shape[1])


# Tested - working fine
def run_until_stable(seed_word: str, max_generations: int = 1000) -> dict:
    """
    Runs Conway's Game of Life simulation seeded by the ASCII binary of a word,
    iterating until a stable state or maximum generation count is reached.

    Args:
        seed_word (str): Word to seed the grid.
        max_generations (int): Maximum generations to simulate (default 1000).

    Returns:
        dict: Contains number of generations run, cumulative cell count score, and final state.
    """
    grid = seed_grid(seed_word)
    history = []
    generation_count = 0
    cumulative_score = int(np.sum(grid))
    

    while generation_count < max_generations:
        new_grid = next_generation(grid)
        generation_count += 1
        cumulative_score += int(np.sum(new_grid))


        if np.sum(new_grid) == 0:
            state: StateType = "Extinction"
            break

        if np.array_equal(new_grid, grid):
            generation_count-=1
            state: StateType = "Static"
            break


        if any(np.array_equal(new_grid, past) for past in history[-9:]):
            state: StateType = "Oscillator"
            break
        
        history.append(grid.copy())
        grid = new_grid

    else:
        state: StateType = "MaxLimit"

    for i in history[-7:]:
        print_grid(i)
    return {
        "generations": generation_count,
        "score": cumulative_score,
        "state": state
    }