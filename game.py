import pygame
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((320, 480))  # Set screen resolution to a multiple of 320x480
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.bullets = []
        self.score = 0
        self.asteroids = []
        self.end = False

        # load images
        self.player = pygame.image.load('images/blueship2.png').convert_alpha()  # Use convert_alpha() for transparent background
        self.background = pygame.image.load('images/background_space.png').convert()
        self.background = pygame.transform.scale(self.background, (320, 480))
        self.player = pygame.transform.scale(self.player, (40, 40))
        self.bullet = pygame.image.load('images/bullet.png').convert_alpha()
        self.bullet = pygame.transform.scale(self.bullet, (15, 15))
        self.bullet = pygame.transform.rotate(self.bullet, 270)
        self.asteroid = pygame.image.load('images/asteroid.png').convert_alpha()
        self.asteroid = pygame.transform.scale(self.asteroid, (50, 50))

        # initialize positions
        self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.background_pos = pygame.Vector2(0, 0)
        self.background2_pos = pygame.Vector2(0, -self.screen.get_height())  # Initialize the second background position above the screen

        # Menu variables
        self.start_menu = True
        self.selected_option = 0
        self.options = ["Start", "Quit"]
        self.options_pause = ["Resume", "Quit"]
        self.options_end = ["Restart", "Quit"]
        self.font = pygame.font.Font(None, 28)

        # Background speed variables
        self.background_speed = 20
        self.background2_speed = 20
        self.speed_increment = 0.5
        self.max_speed = 100

        self.paused = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.start_menu:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.selected_option == 0:
                            self.start_menu = False
                            self.paused = False
                        elif self.selected_option == 1:
                            self.running = False
                elif self.paused:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected_option = (self.selected_option - 1) % len(self.options_pause)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected_option = (self.selected_option + 1) % len(self.options_pause)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.selected_option == 0:
                            self.paused = False
                        elif self.selected_option == 1:
                            self.running = False
                else:
                    # Shoot bullets
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        bullet_pos = pygame.Vector2(self.player_pos.x + self.player.get_width() / 2, self.player_pos.y)
                        self.bullets.append(bullet_pos)
                    elif event.key == pygame.K_ESCAPE:
                        self.paused = True

    def draw_menu(self):
        menu_options = self.options if self.start_menu else self.options_pause
        self.screen.blit(self.background, (self.background_pos.x, self.background_pos.y))  # Draw the first background
        self.screen.blit(self.background, (self.background2_pos.x, self.background2_pos.y))  # Draw the second background

        # Draw options
        for i, option in enumerate(menu_options):
            if self.paused:
                self.screen.blit(self.player, self.player_pos)
                for bullet_pos in self.bullets:
                    self.screen.blit(self.bullet, bullet_pos)
                for asteroid_pos, asteroid_speed in self.asteroids:
                    self.screen.blit(self.asteroid, asteroid_pos)
            text = self.font.render(option, True, (255, 255, 0) if i == self.selected_option else (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + i * 40))
            self.screen.blit(text, text_rect)
            rounded_score = round(self.score)
            self.screen.blit(self.font.render(f'Score: {rounded_score}', True, (255, 255, 255)), (10, 10))

        # Reset the first background position when it reaches the bottom
        if self.background_pos.y >= self.screen.get_height():
            self.background_pos.y = -self.screen.get_height()

        # Reset the second background position when it reaches the bottom
        if self.background2_pos.y >= self.screen.get_height():
            self.background2_pos.y = -self.screen.get_height()

    def game_logic(self):
        self.screen.blit(self.background, (self.background_pos.x, self.background_pos.y))
        self.screen.blit(self.background, (self.background2_pos.x, self.background2_pos.y))
        self.screen.blit(self.player, self.player_pos)  # Draw the player ship on top of the background

        keys = pygame.key.get_pressed()
        # UP
        if keys[pygame.K_w]:
            if self.player_pos.y > 0:
                self.player_pos.y -= 400 * self.dt
        # DOWN
        if keys[pygame.K_s]:
            if self.player_pos.y < self.screen.get_height() - self.player.get_height():
                self.player_pos.y += 400 * self.dt
        # LEFT
        if keys[pygame.K_a]:
            if self.player_pos.x > 0:
                self.player_pos.x -= 400 * self.dt
        # RIGHT
        if keys[pygame.K_d]:
            if self.player_pos.x < self.screen.get_width() - self.player.get_width():
                self.player_pos.x += 400 * self.dt

        # Move and draw bullets``
        for bullet_pos in self.bullets:
            bullet_pos.y -= 600 * self.dt
            self.screen.blit(self.bullet, bullet_pos)
            if bullet_pos.y < -self.bullet.get_height():
                self.bullets.remove(bullet_pos)

        # Move the backgrounds down with increasing speed
        self.background_pos.y += self.background_speed * self.dt
        self.background2_pos.y += self.background2_speed * self.dt

        # Increase background speed over time
        if self.background_speed < self.max_speed and not self.start_menu:
            self.background_speed += self.speed_increment * self.dt
        if self.background2_speed < self.max_speed and not self.start_menu:
            self.background2_speed += self.speed_increment * self.dt

        # Reset the first background position when it reaches the bottom
        if self.background_pos.y >= self.screen.get_height():
            self.background_pos.y = -self.screen.get_height()

        # Reset the second background position when it reaches the bottom
        if self.background2_pos.y >= self.screen.get_height():
            self.background2_pos.y = -self.screen.get_height()

        if not self.paused:
            if random.random() < 0.007:  # Adjust the probability to control the frequency of asteroid spawns
                asteroid_pos = pygame.Vector2(random.randint(0, self.screen.get_width() - self.asteroid.get_width()), -self.asteroid.get_height())
                asteroid_speed = self.background_speed * self.dt * 5 # Spawn asteroids with a speed proportional to the background speed

                # Check if there is enough distance between the new asteroid and existing asteroids
                if all(abs(asteroid_pos.y - existing_pos.y) > self.asteroid.get_height() for existing_pos, _ in self.asteroids):
                    self.asteroids.append((asteroid_pos, asteroid_speed))

        # Move and draw asteroids
        for asteroid_pos, asteroid_speed in self.asteroids:
            asteroid_pos.y += asteroid_speed
            self.screen.blit(self.asteroid, asteroid_pos)
            if asteroid_pos.y > self.screen.get_height():
                self.asteroids.remove((asteroid_pos, asteroid_speed))

        # Update and draw the score
        self.score += self.dt * 10
        rounded_score = round(self.score)
        self.screen.blit(self.font.render(f'Score: {rounded_score}', True, (255, 255, 255)), (10, 10))

        # Check for collisions between the player and asteroids
        for asteroid_pos, _ in self.asteroids:
            if self.player_pos.distance_to(asteroid_pos) < 40:
                self.running = False

        # Check for collisions between bullets and asteroids
        for bullet in self.bullets:
            for asteroid_pos, _ in self.asteroids:
                if bullet.distance_to(asteroid_pos) < 40:
                    self.asteroids.remove((asteroid_pos, _))
                    self.bullets.remove(bullet)
                    self.score += 100
    def run(self):
        while self.running:
            self.handle_events()

            if self.start_menu or self.paused:
                self.draw_menu()
            else:
                self.game_logic()

            pygame.display.flip()

            self.dt = self.clock.tick(120) / 1000

        pygame.quit()

game = Game()
game.run()
