import copy
from car import Car


class GameState:
    def __init__(self, cars, width, height, history=None):
        self.cars = cars  # Liste d'objets Car (copiés) #
        self.width = width
        self.height = height
        self.history = history or []  # Liste de (car_id, move) #

    def is_victory(self):
        red_car = next(car for car in self.cars if car.id == "RED")
        return red_car.x + red_car.length == self.width

    def get_next_states(self):
        next_states = []

        for i, car in enumerate(self.cars):
            for direction in ["forward", "backward"]:
                # test le déplacement sans modifier l'original #
                future_car = Car(car.id, car.x, car.y, car.length, car.orientation, car.color)
                future_car.move(direction)

                future_positions = future_car.get_occupied_positions()
                if not self._is_valid_move(future_positions, car.id):
                    continue

                # Crée une nouvelle liste de voitures avec ce mouvement appliqué #
                new_cars = copy.deepcopy(self.cars)
                new_cars[i] = future_car
                next_states.append(GameState(new_cars, self.width, self.height, self.history + [(car.id, direction)]))

        return next_states

    def _is_valid_move(self, new_positions, moving_car_id):
        occupied = set()
        for car in self.cars:
            if car.id != moving_car_id:
                occupied.update(car.get_occupied_positions())
        for pos in new_positions:
            x, y = pos
            if not (0 <= x < self.width and 0 <= y < self.height):
                return False
            if pos in occupied:
                return False
        return True

    def __eq__(self, other):
        return all((c1.x, c1.y) == (c2.x, c2.y) for c1, c2 in zip(self.cars, other.cars))

    def __hash__(self):
        return hash(tuple((car.x, car.y) for car in self.cars))
