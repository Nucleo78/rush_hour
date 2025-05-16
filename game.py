import pygame
from grid import Grid
from car import Car
from solver import solve
from game_state import GameState
import time

# Taille des cases (pixels)
CELL_SIZE = 80
MARGIN = 5


class Game:
    def __init__(self, level_data):
        pygame.init()
        self.grid = Grid(level_data["width"], level_data["height"])
        self.screen = pygame.display.set_mode(
            (self.grid.width * CELL_SIZE, self.grid.height * CELL_SIZE)
        )
        pygame.display.set_caption("Rush Hour")
        self.clock = pygame.time.Clock()
        self.selected_car_index = 0

        # Variable pour la résolution #
        self.solution = []
        self.solution_step_index = 0
        self.is_solving = False
        self.last_move_time = 0  # Pour contrôler le rythme d’animation

        self.init_level(level_data)

    def init_level(self, level_data):
        for car_data in level_data["cars"]:
            car = Car(
                car_data["id"],
                car_data["x"],
                car_data["y"],
                car_data["length"],
                car_data["orientation"],
                car_data["color"]
            )
            self.grid.add_car(car)

    def run(self):
        running = True

        while running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                    self.handle_input(event.key)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # bouton gauche
                        clicked_car = self.get_car_at_pixel(event.pos)
                        if clicked_car:
                            self.selected_car_index = self.grid.cars.index(clicked_car)

            self.screen.fill((30, 30, 30))
            self.draw_grid()
            self.draw_cars()
            pygame.display.flip()

            # Solving si possible #
            if self.is_solving and self.solution:
                now = time.time()
                if now - self.last_move_time >= 0.4:
                    if self.solution_step_index < len(self.solution):
                        car_id, direction = self.solution[self.solution_step_index]
                        car = next((c for c in self.grid.cars if c.id == car_id), None)
                        if car:
                            self.grid.move_car(car, direction)
                        self.solution_step_index += 1
                        self.last_move_time = now
                    else:
                        self.is_solving = False

            if self.grid.is_red_car_out("RED"):
                return self.show_victory_screen()

    def show_victory_screen(self):
        font = pygame.font.SysFont(None, 48)
        small_font = pygame.font.SysFont(None, 36)

        options = ["Rejouer", "Menu", "Quitter"]
        selected = 0

        while True:
            self.screen.fill((30, 30, 30))
            text = font.render("Victoire !", True, (255, 255, 0))
            self.screen.blit(text, (self.screen.get_width() // 2 - 80, 100))

            for i, option in enumerate(options):
                color = (0, 255, 0) if i == selected else (255, 255, 255)
                opt_text = small_font.render(option, True, color)
                self.screen.blit(opt_text, (self.screen.get_width() // 2 - 60, 180 + i * 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            return "replay"
                        elif selected == 1:
                            return "menu"
                        elif selected == 2:
                            return "quit"

    def handle_input(self, key):
        cars = self.grid.cars
        if not cars:
            return
        car = cars[self.selected_car_index]

        if key == pygame.K_TAB:
            self.selected_car_index = (self.selected_car_index + 1) % len(cars)

        # SOLVING #
        elif key == pygame.K_s and not self.is_solving:
            print("I'm solving.. Don't disturb me !")

            game_state = GameState([Car(c.id, c.x, c.y, c.length, c.orientation, c.color) for c in self.grid.cars],
                                   self.grid.width, self.grid.height)
            self.solution = solve(game_state)
            self.solution_step_index = 0
            self.is_solving = True
            self.last_move_time = time.time()

        elif key == pygame.K_LEFT and car.orientation == "H":
            self.grid.move_car(car, "backward")
        elif key == pygame.K_RIGHT and car.orientation == "H":
            self.grid.move_car(car, "forward")
        elif key == pygame.K_UP and car.orientation == "V":
            self.grid.move_car(car, "backward")
        elif key == pygame.K_DOWN and car.orientation == "V":
            self.grid.move_car(car, "forward")

    def draw_grid(self):
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                rect = pygame.Rect(
                    x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN
                )
                pygame.draw.rect(self.screen, (50, 50, 50), rect)

    def draw_cars(self):
        for index, car in enumerate(self.grid.cars):
            x_px = car.x * CELL_SIZE
            y_px = car.y * CELL_SIZE

            if car.orientation == "H":
                width = CELL_SIZE * car.length - MARGIN
                height = CELL_SIZE - MARGIN
            else:
                width = CELL_SIZE - MARGIN
                height = CELL_SIZE * car.length - MARGIN

            rect = pygame.Rect(x_px, y_px, width, height)
            color = car.color
            pygame.draw.rect(self.screen, color, rect)

            # Surligner la voiture sélectionnée #
            if index == self.selected_car_index:
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 3)

    def get_car_at_pixel(self, mouse_pos):
        x_pixel, y_pixel = mouse_pos
        grid_x = x_pixel // CELL_SIZE
        grid_y = y_pixel // CELL_SIZE
        return self.grid.get_car_at(grid_x, grid_y)
