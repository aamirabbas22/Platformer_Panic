from settings import * 
from sprites import AnimatedSprite
from random import randint
from timer import Timer

class UI:
    def __init__(self, font, frames):
        # Main display surface to draw UI elements on
        self.display_surface = pygame.display.get_surface()

        # Group to hold all UI sprites (e.g., hearts)
        self.sprites = pygame.sprite.Group()

        # Font for rendering text (e.g., coins)
        self.font = font

        # Heart (health) setup
        self.heart_frames = frames['heart']  # Animation frames for the hearts
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 6  # Space between hearts

        # Coin display setup
        self.coin_amount = 0  # Current amount to show
        self.coin_timer = Timer(1000)  # How long to display coin text
        self.coin_surf = frames['coin']  # Coin icon image

    def create_hearts(self, amount):
        # Create heart sprites to match the current health amount.
        # Clear any existing heart sprites
        for sprite in self.sprites:
            sprite.kill()

        # Create a new heart sprite for each health point
        for heart in range(amount):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x, y), self.heart_frames, self.sprites)

    def display_text(self):
        # Show coin text and icon on screen if timer is active.
        if self.coin_timer.active:
            # Render coin amount
            text_surf = self.font.render(str(self.coin_amount), False, YELLOW)
            text_rect = text_surf.get_frect(topleft=(16, 34))
            self.display_surface.blit(text_surf, text_rect)

            # Draw coin icon next to the text
            coin_rect = self.coin_surf.get_frect(center=text_rect.bottomleft).move(0, -6)
            self.display_surface.blit(self.coin_surf, coin_rect)

    def show_coins(self, amount):
        # Update coin amount and activate timer to display it.
        self.coin_amount = amount
        self.coin_timer.activate()

    def update(self, dt):
        # Update all UI elements and draw them.
        self.coin_timer.update()  # Update coin timer

        self.sprites.update(dt)   # Update animated hearts
        self.sprites.draw(self.display_surface)  # Draw hearts

        self.display_text()  # Draw coin info if needed

class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active = False  # Is this heart currently animating?

    def animate(self, dt):
        # Run the heart animation frames.
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active = False  # Stop animation
            self.frame_index = 0

    def update(self, dt):
        # Randomly trigger the heart animation sometimes.
        if self.active:
            self.animate(dt)
        else:
            # 1 in 2000 chance each frame to start the animation
            if randint(0, 2000) == 1:
                self.active = True
