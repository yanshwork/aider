import random
import math
import tkinter as tk
from tkinter import ttk, messagebox

class City:
    def __init__(self, num_houses, num_hospitals):
        self.width = 500
        self.height = 500
        self.houses = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(num_houses)]
        self.hospitals = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(num_hospitals)]

    def total_distance(self):
        return sum(min(math.dist(house, hospital) for hospital in self.hospitals) for house in self.houses)

    def hill_climbing(self, max_iterations=1000):
        for _ in range(max_iterations):
            old_distance = self.total_distance()
            hospital_index = random.randint(0, len(self.hospitals) - 1)
            old_x, old_y = self.hospitals[hospital_index]
            new_x = max(0, min(self.width, old_x + random.randint(-5, 5)))
            new_y = max(0, min(self.height, old_y + random.randint(-5, 5)))
            self.hospitals[hospital_index] = (new_x, new_y)
            new_distance = self.total_distance()
            if new_distance >= old_distance:
                self.hospitals[hospital_index] = (old_x, old_y)

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
        self.houses_entry.insert(0, "50")

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

        ttk.Label(results_frame, text="Initial Total Distance:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(results_frame, textvariable=self.initial_distance_var).grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(results_frame, text="Final Total Distance:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(results_frame, textvariable=self.final_distance_var).grid(row=1, column=1, sticky=tk.W, pady=5)

    def optimize(self):
        try:
            num_houses = int(self.houses_entry.get())
            num_hospitals = int(self.hospitals_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for houses and hospitals.")
            return

        city = City(num_houses, num_hospitals)
        initial_distance = city.total_distance()
        self.initial_distance_var.set(f"{initial_distance:.2f}")

        city.hill_climbing()
        final_distance = city.total_distance()
        self.final_distance_var.set(f"{final_distance:.2f}")

        self.draw_city(city)

    def draw_city(self, city):
        self.canvas.delete("all")
        for x, y in city.houses:
            self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="blue")
        for x, y in city.hospitals:
            self.canvas.create_rectangle(x-5, y-5, x+5, y+5, fill="red")

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
