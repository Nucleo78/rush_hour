class Grid:
    def __init__(self, width, height):
        """
        Initialise une grille vide de dimensions width x height.

        :param width: largeur de la grille (colonnes)
        :param height: hauteur de la grille (lignes)
        """
        self.width = width
        self.height = height
        self.cars = []

    def add_car(self, car):
        """
        Ajoute une voiture à la grille si elle ne rentre pas en collision et est dans les limites.

        :param car: instance de Car
        :raises ValueError: si une voiture est en dehors de la grille ou en collision
        """
        for (x, y) in car.get_occupied_positions():
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise ValueError(f"La voiture {car.id} dépasse la grille.")
            if self.get_car_at(x, y):
                raise ValueError(f"Collision détectée à ({x}, {y}) en ajoutant {car.id}.")
        self.cars.append(car)

    def is_cell_empty(self, x, y, except_car=None):
        """
        Vérifie si une cellule est vide (hors d'une voiture).

        :param x: coordonnée x
        :param y: coordonnée y
        :param except_car: une voiture à ignorer (utile pendant un mouvement)
        :return: True si vide, False sinon
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        for car in self.cars:
            if car == except_car:
                continue
            if (x, y) in car.get_occupied_positions():
                return False
        return True

    def get_car_at(self, x, y):
        """
        Retourne la voiture présente aux coordonnées (x, y), ou None.
        """
        for car in self.cars:
            if (x, y) in car.get_occupied_positions():
                return car
        return None

    def move_car(self, car, direction):
        """
        Tente de déplacer une voiture. Retourne True si réussi, False sinon.

        :param car: voiture à déplacer
        :param direction: 'forward' ou 'backward'
        """
        future_positions = car.preview_move(direction)

        for (x, y) in future_positions:
            if not self.is_cell_empty(x, y, except_car=car):
                return False  # collision ou hors limite #

        car.move(direction)
        return True

    def is_red_car_out(self, red_car_id):
        red_car = next((c for c in self.cars if c.id == red_car_id), None)
        return red_car and (red_car.x + red_car.length >= self.width)
