from solver import solve
from game_state import GameState
from car import Car

cars = [
    Car("RED", 0, 2, 2, "H", "red"),
    Car("A", 0, 0, 3, "V", "blue"),
    Car("B", 3, 2, 2, "V", "green"),
]

state = GameState(cars, 6, 6)
solution = solve(state)

if solution:
    print("Solution trouvée :", solution)
else:
    print("Pas de solution.")
