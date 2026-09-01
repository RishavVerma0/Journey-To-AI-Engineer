# 3568. Minimum Moves to Clean the Classroom
# Medium
# Topics
# premium lock icon
# Companies
# Hint
# You are given an m x n grid classroom where a student volunteer is tasked with cleaning up litter scattered around the room. Each cell in the grid is one of the following:

# 'S': Starting position of the student
# 'L': Litter that must be collected (once collected, the cell becomes empty)
# 'R': Reset area that restores the student's energy to full capacity, regardless of their current energy level (can be used multiple times)
# 'X': Obstacle the student cannot pass through
# '.': Empty space
# You are also given an integer energy, representing the student's maximum energy capacity. The student starts with this energy from the starting position 'S'.

# Each move to an adjacent cell (up, down, left, or right) costs 1 unit of energy. If the energy reaches 0, the student can only continue if they are on a reset area 'R', which resets the energy to its maximum capacity energy.

# Return the minimum number of moves required to collect all litter items, or -1 if it's impossible.

 

# Example 1:

# Input: classroom = ["S.", "XL"], energy = 2

# Output: 2

# Explanation:

# The student starts at cell (0, 0) with 2 units of energy.
# Since cell (1, 0) contains an obstacle 'X', the student cannot move directly downward.
# A valid sequence of moves to collect all litter is as follows:
# Move 1: From (0, 0) → (0, 1) with 1 unit of energy and 1 unit remaining.
# Move 2: From (0, 1) → (1, 1) to collect the litter 'L'.
# The student collects all the litter using 2 moves. Thus, the output is 2.
# Example 2:

# Input: classroom = ["LS", "RL"], energy = 4

# Output: 3

# Explanation:

# The student starts at cell (0, 1) with 4 units of energy.
# A valid sequence of moves to collect all litter is as follows:
# Move 1: From (0, 1) → (0, 0) to collect the first litter 'L' with 1 unit of energy used and 3 units remaining.
# Move 2: From (0, 0) → (1, 0) to 'R' to reset and restore energy back to 4.
# Move 3: From (1, 0) → (1, 1) to collect the second litter 'L'.
# The student collects all the litter using 3 moves. Thus, the output is 3.
# Example 3:

# Input: classroom = ["L.S", "RXL"], energy = 3

# Output: -1

# Explanation:

# No valid path collects all 'L'.

from typing import List
from collections import deque


class Solution:
    def minMoves(self, classroom: List[str], energy: int) -> int:
        m, n = len(classroom), len(classroom[0])

        litter_id = {}
        start_x = start_y = 0
        count = 0

        # Find start position and assign each litter a bit
        for i in range(m):
            for j in range(n):
                if classroom[i][j] == 'S':
                    start_x, start_y = i, j
                elif classroom[i][j] == 'L':
                    litter_id[(i, j)] = count
                    count += 1

        # No litter
        if count == 0:
            return 0

        full_mask = (1 << count) - 1

        # State: (x, y, remaining_energy, collected_mask)
        queue = deque([(start_x, start_y, energy, 0)])

        visited = {
            (start_x, start_y, energy, 0)
        }

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        moves = 0

        while queue:
            for _ in range(len(queue)):
                x, y, curr_energy, mask = queue.popleft()

                # All litter collected
                if mask == full_mask:
                    return moves

                # Cannot move anymore
                if curr_energy == 0:
                    continue

                for dx, dy in directions:
                    nx, ny = x + dx, y + dy

                    if not (0 <= nx < m and 0 <= ny < n):
                        continue

                    if classroom[nx][ny] == 'X':
                        continue

                    # Every movement costs 1 energy
                    next_energy = curr_energy - 1

                    # Reset energy if landing on R
                    if classroom[nx][ny] == 'R':
                        next_energy = energy

                    next_mask = mask

                    # Collect litter
                    if classroom[nx][ny] == 'L':
                        bit = litter_id[(nx, ny)]
                        next_mask |= (1 << bit)

                    state = (nx, ny, next_energy, next_mask)

                    if state not in visited:
                        visited.add(state)
                        queue.append(state)

            moves += 1

        return -1