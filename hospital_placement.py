import tkinter as tk
from tkinter import ttk, messagebox
from hospital_logic import City

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
