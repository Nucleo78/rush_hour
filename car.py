class Car:
    def __init__(self, id, x, y, length, orientation, color):
        """
        Initialise une voiture.

        :param id: Identifiant unique de la voiture
        :param x: Coordonnée x (colonne) de la voiture (extrémité gauche/haut)
        :param y: Coordonnée y (ligne) de la voiture (extrémité gauche/haut)
        :param length: Longueur de la voiture (2 ou 3)
        :param orientation: 'H' pour horizontale, 'V' pour verticale
        :param color: Couleur de la voiture (tuple RGB ou string)
        """
        self.id = id
        self.x = x
        self.y = y
        self.length = length
        self.orientation = orientation  # 'H' ou 'V'
        self.color = color

    def get_occupied_positions(self):
        """
        Retourne une liste des positions (x, y) occupées par la voiture.
        """
        positions = []
        for i in range(self.length):
            if self.orientation == 'H':
                positions.append((self.x + i, self.y))
            else:
                positions.append((self.x, self.y + i))
        return positions

    def move(self, direction):
        """
        Déplace la voiture d'une case dans la direction donnée (si valide).

        :param direction: 'forward' ou 'backward' dans le sens de l’orientation
        """
        if self.orientation == 'H':
            if direction == 'forward':
                self.x += 1
            elif direction == 'backward':
                self.x -= 1
        elif self.orientation == 'V':
            if direction == 'forward':
                self.y += 1
            elif direction == 'backward':
                self.y -= 1

    def preview_move(self, direction):
        """
        Retourne les positions que la voiture occuperait si elle se déplaçait.

        C'est pour tester les collisions sans bouger réellement.
        """
        future = Car(self.id, self.x, self.y, self.length, self.orientation, self.color)
        future.move(direction)
        return future.get_occupied_positions()
