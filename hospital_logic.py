import random
import math

class City:
    def __init__(self, num_houses, num_hospitals):
        self.grid_size = 10
        self.cell_size = 50
        self.width = self.grid_size * self.cell_size
        self.height = self.grid_size * self.cell_size
        self.houses = self.generate_random_positions(num_houses)
        self.hospitals = self.generate_random_positions(num_hospitals)

    def generate_random_positions(self, count):
        positions = set()
        while len(positions) < count:
            x = random.randint(0, self.grid_size - 1) * self.cell_size + self.cell_size // 2
            y = random.randint(0, self.grid_size - 1) * self.cell_size + self.cell_size // 2
            positions.add((x, y))
        return list(positions)

    def total_distance(self):
        return sum(min(math.dist(house, hospital) for hospital in self.hospitals) for house in self.houses)

    def hill_climbing(self, max_iterations=1000):
        for _ in range(max_iterations):
            old_distance = self.total_distance()
            hospital_index = random.randint(0, len(self.hospitals) - 1)
            old_pos = self.hospitals[hospital_index]
            new_pos = self.get_new_position(old_pos)
            if new_pos not in self.hospitals and new_pos not in self.houses:
                self.hospitals[hospital_index] = new_pos
                new_distance = self.total_distance()
                if new_distance >= old_distance:
                    self.hospitals[hospital_index] = old_pos

    def get_new_position(self, old_pos):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        dx, dy = random.choice(directions)
        new_x = (old_pos[0] // self.cell_size + dx) % self.grid_size
        new_y = (old_pos[1] // self.cell_size + dy) % self.grid_size
        return (new_x * self.cell_size + self.cell_size // 2, 
                new_y * self.cell_size + self.cell_size // 2)
