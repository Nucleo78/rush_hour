from car import Car
from game_state import GameState

# Création d'un niveau simple
cars = [
    Car("RED", 0, 2, 2, "H", "red"),   # La voiture rouge à la ligne 2
    Car("A", 0, 0, 3, "V", "blue"),
    Car("B", 3, 2, 2, "V", "green"),
]

width, height = 6, 6

state = GameState(cars, width, height)

print("Victoire ?", state.is_victory())
next_states = state.get_next_states()
print(f"{len(next_states)} états générés.")

# Affiche les mouvements possibles
for ns in next_states:
    print(ns.history[-1])  # (id, direction)
