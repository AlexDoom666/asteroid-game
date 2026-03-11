import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot

def main():
    pygame.init()
    pygame.font.init()  # Initialize the font module
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 74) # Default font, size 74

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            # Handle restart or quit after game over
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Restart by clearing groups and calling main again
                    for group in [updatable, drawable, asteroids, shots]:
                        group.empty()
                    main()
                    return
                if event.key == pygame.K_ESCAPE:
                    return

        dt = clock.tick(60) / 1000

        if not game_over:
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    game_over = True

                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        asteroid.split()

        log_state()

        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)

        if game_over:
            msg = font.render("GAME OVER", True, "red")
            sub_msg = font.render("SPACE to Restart - ESC to Quit", True, "white")
            # Draw messages centered
            screen.blit(msg, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 50))
            screen.blit(sub_msg, (SCREEN_WIDTH / 2 - 400, SCREEN_HEIGHT / 2 + 50))

        pygame.display.flip()

if __name__ == "__main__":
    main()
