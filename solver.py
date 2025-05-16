from collections import deque

def solve(initial_state):
    """
    Applique BFS pour résoudre le niveau à partir de l'état initial.
    Retourne une liste de mouvements (car_id, direction) ou None si pas de solution.
    """
    queue = deque([initial_state])
    visited = set()

    while queue:
        current_state = queue.popleft()

        if current_state.is_victory():
            return current_state.history

        state_id = get_state_id(current_state)
        if state_id in visited:
            continue

        visited.add(state_id)

        for next_state in current_state.get_next_states():
            queue.append(next_state)

    return None  # Pas de solution trouvée


def get_state_id(state):
    """
    Génère un identifiant unique pour un état,
    basé sur la position des voitures.
    """
    positions = sorted((car.id, car.x, car.y) for car in state.cars)
    return tuple(positions)
