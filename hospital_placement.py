import random
import math

class City:
    def __init__(self, num_houses, num_hospitals):
        self.width = 100
        self.height = 100
        self.houses = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(num_houses)]
        self.hospitals = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(num_hospitals)]

    def total_distance(self):
        return sum(min(math.dist(house, hospital) for hospital in self.hospitals) for house in self.houses)

    def hill_climbing(self, max_iterations=1000):
        for _ in range(max_iterations):
            old_distance = self.total_distance()
            hospital_index = random.randint(0, len(self.hospitals) - 1)
            old_x, old_y = self.hospitals[hospital_index]
            new_x = max(0, min(self.width, old_x + random.randint(-1, 1)))
            new_y = max(0, min(self.height, old_y + random.randint(-1, 1)))
            self.hospitals[hospital_index] = (new_x, new_y)
            new_distance = self.total_distance()
            if new_distance >= old_distance:
                self.hospitals[hospital_index] = (old_x, old_y)

def main():
    num_houses = int(input("Enter the number of houses: "))
    num_hospitals = int(input("Enter the number of hospitals: "))

    city = City(num_houses, num_hospitals)
    print(f"Initial total distance: {city.total_distance():.2f}")

    city.hill_climbing()
    print(f"Final total distance: {city.total_distance():.2f}")

    print("\nFinal hospital locations:")
    for i, (x, y) in enumerate(city.hospitals, 1):
        print(f"Hospital {i}: ({x}, {y})")

if __name__ == "__main__":
    main()
