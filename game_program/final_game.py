import pygame
import sys

# Constants for game configuration
GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT = 900, 473
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (255, 100, 50)
BUTTON_HOVER_COLOR = (255, 70, 30)
BUTTON_CLICK_COLOR = (200, 50, 20)
BUTTON_SHADOW_COLOR = (100, 50, 20)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))
        pygame.display.set_caption("UNO Cards By BOT_MATRIX")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.load_assets()
        self.main_menu()

    def load_assets(self):
        self.background_image = pygame.transform.scale(pygame.image.load("game_background.jpg"), 
                                                        (GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))
        pygame.mixer.music.load("game_background.mp3")
        pygame.mixer.music.set_volume(0.5)
        self.click_sound = pygame.mixer.Sound("button-click.mp3")
        self.transition_sound = pygame.mixer.Sound("transition.wav")
        pygame.mixer.music.play(-1)

    def draw_text(self, text, pos, color=FONT_COLOR, size=48):
        font = pygame.font.Font(None, size)
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, pos)

    def fade(self, direction, duration=1000):
        fade_surface = pygame.Surface((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 255) if direction == 'out' else range(255, -1, -1):
            fade_surface.set_alpha(alpha)
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(duration // 255)

    def main_menu(self):
        menu_running = True
        while menu_running:
            self.screen.blit(self.background_image, (0, 0))
            self.draw_text("v1.0.0", (10, 10), (180, 180, 180), 24)
            self.draw_text("Developed by BOT_MATRIX", (10, GAME_WINDOW_HEIGHT - 30), (180, 180, 180), 24)

            mouse_pos = pygame.mouse.get_pos()
            is_clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    is_clicked = True

            start_button = Button("Start Game", (GAME_WINDOW_WIDTH // 2, GAME_WINDOW_HEIGHT // 2 - 50))
            quit_button = Button("Quit", (GAME_WINDOW_WIDTH // 2, GAME_WINDOW_HEIGHT // 2 + 50))

            if start_button.draw(self.screen, mouse_pos, is_clicked):
                self.click_sound.play()
                self.fade('out', 700)
                self.transition_sound.play()
                self.fade('in', 700)
                self.game_screen()

            if quit_button.draw(self.screen, mouse_pos, is_clicked):
                self.click_sound.play()
                self.fade('out', 700)
                pygame.quit()
                sys.exit()

            pygame.display.flip()
            self.clock.tick(60)

    def game_screen(self):
        game_running = True
        while game_running:
            self.screen.blit(self.background_image, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            is_clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    is_clicked = True

            camera_button = Button("Camera", (GAME_WINDOW_WIDTH // 2, GAME_WINDOW_HEIGHT // 2 - 70))
            upload_button = Button("Image", (GAME_WINDOW_WIDTH // 2, GAME_WINDOW_HEIGHT // 2))
            back_button = Button("Back", (GAME_WINDOW_WIDTH // 2, GAME_WINDOW_HEIGHT // 2 + 70))

            if camera_button.draw(self.screen, mouse_pos, is_clicked):
                self.click_sound.play()
                print("Camera Capture selected")

            if upload_button.draw(self.screen, mouse_pos, is_clicked):
                self.click_sound.play()
                print("Image Upload selected")

            if back_button.draw(self.screen, mouse_pos, is_clicked):
                self.click_sound.play()
                self.fade('out', 700)
                self.transition_sound.play()
                self.fade('in', 700)
                self.main_menu()

            pygame.display.flip()
            self.clock.tick(60)


class Button:
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.width = 200
        self.height = 60
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.position

    def draw(self, surface, mouse_pos, is_clicked):
        color = BUTTON_HOVER_COLOR if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        if is_clicked and self.rect.collidepoint(mouse_pos):
            color = BUTTON_CLICK_COLOR

        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(5, 5)
        pygame.draw.rect(surface, BUTTON_SHADOW_COLOR, shadow_rect, border_radius=15)
        pygame.draw.rect(surface, color, self.rect, border_radius=15)

        text_surface = pygame.font.Font(None, 48).render(self.text, True, FONT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

        return is_clicked and self.rect.collidepoint(mouse_pos)


if __name__ == "__main__":
    Game()
    pygame.quit()
    sys.exit()
