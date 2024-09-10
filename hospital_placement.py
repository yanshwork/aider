import random
import math
import tkinter as tk
from tkinter import ttk, messagebox

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

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Placement Optimizer")
        self.geometry("600x700")

        self.create_widgets()

    def create_widgets(self):
        # Input frame
        input_frame = ttk.Frame(self, padding="10")
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="Number of Houses:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.houses_entry = ttk.Entry(input_frame)
        self.houses_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.houses_entry.insert(0, "20")

        ttk.Label(input_frame, text="Number of Hospitals:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.hospitals_entry = ttk.Entry(input_frame)
        self.hospitals_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.hospitals_entry.insert(0, "5")

        ttk.Button(input_frame, text="Optimize", command=self.optimize).grid(row=2, column=0, columnspan=2, pady=10)

        # Canvas for city visualization
        self.canvas = tk.Canvas(self, width=500, height=500, bg="white")
        self.canvas.pack(pady=10)

        # Results frame
        results_frame = ttk.Frame(self, padding="10")
        results_frame.pack(fill=tk.X)

        self.initial_distance_var = tk.StringVar()
        self.final_distance_var = tk.StringVar()
        self.improvement_var = tk.StringVar()

        ttk.Label(results_frame, text="Initial Total Distance:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(results_frame, textvariable=self.initial_distance_var).grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(results_frame, text="Final Total Distance:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(results_frame, textvariable=self.final_distance_var).grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(results_frame, text="Improvement:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(results_frame, textvariable=self.improvement_var).grid(row=2, column=1, sticky=tk.W, pady=5)

    def optimize(self):
        try:
            num_houses = int(self.houses_entry.get())
            num_hospitals = int(self.hospitals_entry.get())
            if num_houses + num_hospitals > 100:
                raise ValueError("Total number of houses and hospitals cannot exceed 100")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        city = City(num_houses, num_hospitals)
        initial_distance = city.total_distance()
        self.initial_distance_var.set(f"{initial_distance:.2f}")

        city.hill_climbing()
        final_distance = city.total_distance()
        self.final_distance_var.set(f"{final_distance:.2f}")

        # Calculate and display improvement percentage
        improvement = (initial_distance - final_distance) / initial_distance * 100
        self.improvement_var.set(f"{improvement:.2f}%")

        self.draw_city(city)

    def draw_city(self, city):
        self.canvas.delete("all")
        
        # Draw grid lines
        for i in range(0, city.width + 1, city.cell_size):
            self.canvas.create_line(i, 0, i, city.height, fill="lightgray")
            self.canvas.create_line(0, i, city.width, i, fill="lightgray")
        
        # Draw houses
        for x, y in city.houses:
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue")
        
        # Draw hospitals
        for x, y in city.hospitals:
            self.canvas.create_rectangle(x-10, y-10, x+10, y+10, fill="red")

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
