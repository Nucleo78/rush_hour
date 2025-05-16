levels = {
    "niveau_1": {
        "width": 6,
        "height": 6,
        "cars": [
            {"id": "RED", "x": 0, "y": 2, "length": 2, "orientation": "H", "color": (255, 0, 0)},
            {"id": "E", "x": 2, "y": 0, "length": 3, "orientation": "V", "color": (0, 255, 255)},
            {"id": "F", "x": 5, "y": 1, "length": 2, "orientation": "V", "color": (200, 200, 0)},
            {"id": "G", "x": 1, "y": 3, "length": 2, "orientation": "H", "color": (100, 100, 255)},
        ]
    },
    "niveau_2": {
        "width": 6,
        "height": 6,
        "cars": [
            {"id": "RED", "x": 0, "y": 2, "length": 2, "orientation": "H", "color": (255, 0, 0)},
            {"id": "A", "x": 3, "y": 0, "length": 3, "orientation": "V", "color": (0, 255, 0)},
            {"id": "B", "x": 4, "y": 1, "length": 2, "orientation": "V", "color": (0, 0, 255)},
            {"id": "C", "x": 0, "y": 3, "length": 2, "orientation": "H", "color": (255, 255, 0)},
            {"id": "D", "x": 3, "y": 4, "length": 3, "orientation": "H", "color": (255, 0, 255)},
        ]
    },
    "niveau_3": {
        "width": 6,
        "height": 6,
        "cars": [
            {"id": "RED", "x": 0, "y": 2, "length": 2, "orientation": "H", "color": (255, 0, 0)},
            {"id": "A", "x": 2, "y": 0, "length": 3, "orientation": "V", "color": (0, 255, 0)},
            {"id": "B", "x": 4, "y": 0, "length": 2, "orientation": "H", "color": (0, 0, 255)},
            {"id": "C", "x": 5, "y": 1, "length": 2, "orientation": "V", "color": (255, 255, 0)},
            {"id": "D", "x": 0, "y": 3, "length": 2, "orientation": "V", "color": (255, 0, 255)},
            {"id": "E", "x": 1, "y": 3, "length": 2, "orientation": "H", "color": (0, 255, 255)},
            {"id": "F", "x": 3, "y": 3, "length": 3, "orientation": "H", "color": (255, 255, 255)},
        ]
    },
    "niveau_aléatoire": {
        "random": True,
    }
}

from car import Car
from random import choice, randint

def generate_random_level(width=6, height=6, num_cars=8):
    cars = []

    red_car = {
        "id": "RED",
        "x": 0,
        "y": height // 2,
        "length": 2,
        "orientation": "H",
        "color": (255, 0, 0)
    }
    cars.append(red_car)

    positions_taken = set(tuple(pos) for pos in Car(**red_car).get_occupied_positions())

    letters = [chr(i) for i in range(65, 91) if chr(i) != "R"]
    colors = [(0, 128, 255), (255, 255, 0), (0, 255, 0), (255, 0, 255)]

    while len(cars) < num_cars:
        car_id = letters[len(cars) - 1]
        orientation = choice(["H", "V"])
        length = choice([2, 3])
        color = choice(colors)

        if orientation == "H":
            x = randint(0, width - length)
            y = randint(0, height - 1)
        else:
            x = randint(0, width - 1)
            y = randint(0, height - length)

        new_car = Car(car_id, x, y, length, orientation, color)
        new_positions = set(new_car.get_occupied_positions())

        if new_positions.isdisjoint(positions_taken):
            cars.append({
                "id": car_id,
                "x": x,
                "y": y,
                "length": length,
                "orientation": orientation,
                "color": color
            })
            positions_taken.update(new_positions)

    return {
        "width": width,
        "height": height,
        "cars": cars
    }
