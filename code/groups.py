from settings import *  # Import global settings/constants (e.g., TILE_SIZE, WINDOW_WIDTH, etc.)
from sprites import Sprite, Cloud
from random import choice, randint
from timer import Timer

class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height, clouds, horizon_line, bg_tile=None, top_limit=0):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()  # Camera offset vector

        # Full level/world dimensions in pixels
        self.width, self.height = width * TILE_SIZE, height * TILE_SIZE

        # Define camera borders/constraints
        self.borders = {
            'left': 0,  # Left limit
            'right': -self.width + WINDOW_WIDTH,  # Right limit (negative because offset works in reverse)
            'bottom': -self.height + WINDOW_HEIGHT,  # Bottom limit (negative)
            'top': top_limit  # Top limit (can be positive or negative)
        }

        # If no bg_tile is provided, it's a sky background
        self.sky = not bg_tile
        self.horizon_line = horizon_line  # Y-coordinate for horizon line

        if bg_tile:
            # If using ground tiles, create a Sprite for each tile in the level
            for col in range(width):
                for row in range(-int(top_limit / TILE_SIZE) - 1, height):
                    x, y = col * TILE_SIZE, row * TILE_SIZE
                    Sprite((x, y), bg_tile, self, -1)  # Z-index -1: drawn first
        else:
            # Setup for sky + clouds instead of ground tiles
            self.large_cloud = clouds['large']
            self.small_clouds = clouds['small']
            self.cloud_direction = -1  # Clouds move to the left

            # Large repeating cloud setup
            self.large_cloud_speed = 50  # Pixels per second
            self.large_cloud_x = 0  # Scrolling X position
            self.large_cloud_tiles = int(self.width / self.large_cloud.get_width()) + 2
            self.large_cloud_width, self.large_cloud_height = self.large_cloud.get_size()

            # Small random clouds setup with timer
            self.cloud_timer = Timer(2500, self.create_cloud, True)
            self.cloud_timer.activate()

            # Generate some starting small clouds
            for cloud in range(20):
                pos = (randint(0, self.width), randint(self.borders['top'], self.horizon_line))
                surf = choice(self.small_clouds)
                Cloud(pos, surf, self)

    def camera_constraint(self):
       # Make sure the camera offset stays within the defined borders.
       # This prevents the camera from scrolling beyond the level edges.
    
        # Clamp horizontal offset
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else self.borders['left']
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']

        # Clamp vertical offset
        self.offset.y = self.offset.y if self.offset.y > self.borders['bottom'] else self.borders['bottom']
        self.offset.y = self.offset.y if self.offset.y < self.borders['top'] else self.borders['top']

    def draw_sky(self):
        # Draw the static sky background, horizon line, and sea.
        self.display_surface.fill('#ddc6a1')  # Sky color

        # Calculate horizon line position with offset
        horizon_pos = self.horizon_line + self.offset.y

        # Draw sea below the horizon
        sea_rect = pygame.FRect(0, horizon_pos, WINDOW_WIDTH, WINDOW_HEIGHT - horizon_pos)
        pygame.draw.rect(self.display_surface, '#92a9ce', sea_rect)

        # Draw horizon line
        pygame.draw.line(self.display_surface, '#f5f1de', (0, horizon_pos), (WINDOW_WIDTH, horizon_pos), 4)

    def draw_large_cloud(self, dt):
        # Scroll and draw large repeating clouds near the horizon.
        # Update cloud position based on direction and speed
        self.large_cloud_x += self.cloud_direction * self.large_cloud_speed * dt

        # Wrap clouds when they scroll out of view
        if self.large_cloud_x <= -self.large_cloud_width:
            self.large_cloud_x = 0

        # Draw the tiled clouds along the horizon
        for cloud in range(self.large_cloud_tiles):
            left = self.large_cloud_x + self.large_cloud_width * cloud + self.offset.x
            top = self.horizon_line - self.large_cloud_height + self.offset.y
            self.display_surface.blit(self.large_cloud, (left, top))

    def create_cloud(self):
        # Create a new small cloud and place it off-screen to the right.
        pos = (
            randint(self.width + 500, self.width + 600),  # Off-screen X
            randint(self.borders['top'], self.horizon_line)  # Random Y above horizon
        )
        surf = choice(self.small_clouds)
        Cloud(pos, surf, self)

    def draw(self, target_pos, dt):
        """
        Main draw method:
        1) Calculate camera offset based on target_pos (e.g., player)
        2) Apply camera constraints
        3) Draw sky & clouds if needed
        4) Draw all sprites, sorted by z for layering
        """
        # Calculate offset: camera centers on target
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        # Keep the camera within world limits
        self.camera_constraint()

        # Draw sky & clouds if there's no bg tile map
        if self.sky:
            self.cloud_timer.update()
            self.draw_sky()
            self.draw_large_cloud(dt)

        # Draw all sprites, sorted by z-index
        for sprite in sorted(self, key=lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)
