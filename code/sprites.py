from settings import * 
from math import sin, cos, radians
from random import randint

# Base sprite class for any static object
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf=pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = None, z = Z_LAYERS['main']):
        super().__init__(groups)
        self.image = surf  # Sprite image
        self.rect = self.image.get_frect(topleft=pos)  # Position on screen
        self.old_rect = self.rect.copy()  # Store previous position (for collisions)
        self.z = z  # Layer for rendering order

# Base class for any animated sprite (like coins, hearts, effects)
class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z=Z_LAYERS['main'], animation_speed = ANIMATION_SPEED):
        self.frames = frames  # List of animation frames
        self.frame_index = 0  # Current frame index
        super().__init__(pos, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed  # Speed at which frames change

    def animate(self, dt):
        # Advance animation frames based on delta time
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        # Update animation each frame
        self.animate(dt)

# Pickup items that increase coins or health when activated
class Item(AnimatedSprite):
    def __init__(self, item_type, pos, frames, groups, data):
        super().__init__(pos, frames, groups)
        self.rect.center = pos
        self.item_type = item_type  # e.g., 'gold', 'silver', 'diamond', 'potion'
        self.data = data  # Reference to Data class to modify coins/health

    def activate(self):
        # Add coins or health depending on item type
        if self.item_type == 'gold':
            self.data.coins += 5
        if self.item_type == 'silver':
            self.data.coins += 1
        if self.item_type == 'diamond':
            self.data.coins += 20
        if self.item_type == 'skull':
            self.data.coins += 50
        if self.item_type == 'potion':
            self.data.health += 1

# Temporary sprite for effects like explosions or sparkles
class ParticleEffectSprite(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.rect.center = pos
        self.z = Z_LAYERS['fg']  # Render in foreground

    def animate(self, dt):
        # Play effect and self-destruct when done
        self.frame_index += self.animation_speed * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()  # Remove sprite when animation finishes

# Moving platforms or enemies that move back and forth
class MovingSprite(AnimatedSprite):
    def __init__(self, frames, groups, start_pos, end_pos, move_dir, speed, flip = False):
        super().__init__(start_pos, frames, groups)

        # Position setup based on direction
        if move_dir == 'x':
            self.rect.midleft = start_pos
        else:
            self.rect.midtop = start_pos

        self.start_pos = start_pos
        self.end_pos = end_pos

        # Movement settings
        self.moving = True
        self.speed = speed
        self.direction = vector(1, 0) if move_dir == 'x' else vector(0, 1)
        self.move_dir = move_dir

        self.flip = flip  # Whether to flip sprite when changing direction
        self.reverse = {'x': False, 'y': False}  # Used for flipping

    def check_border(self):
        # Change direction when reaching start/end positions
        if self.move_dir == 'x':
            if self.rect.right >= self.end_pos[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.end_pos[0]
            if self.rect.left <= self.start_pos[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.start_pos[0]
            self.reverse['x'] = True if self.direction.x < 0 else False
        else:
            if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.end_pos[1]
            if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.start_pos[1]
            self.reverse['y'] = True if self.direction.y > 0 else False

    def update(self, dt):
        # Update position and flip image if needed
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * dt
        self.check_border()

        self.animate(dt)
        if self.flip:
            self.image = pygame.transform.flip(self.image, self.reverse['x'], self.reverse['y'])

# Circular moving hazard like rotating spikes
class Spike(Sprite):
    def __init__(self, pos, surf, groups, radius, speed, start_angle, end_angle, z=Z_LAYERS['main']):
        self.center = pos  # Center of rotation
        self.radius = radius  # Distance from center
        self.speed = speed  # Rotation speed
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.angle = self.start_angle
        self.direction = 1  # Direction of rotation
        self.full_circle = True if self.end_angle == -1 else False  # Whether to rotate fully

        # Calculate initial position using trigonometry
        y = self.center[1] + sin(radians(self.angle)) * self.radius
        x = self.center[0] + cos(radians(self.angle)) * self.radius

        super().__init__((x, y), surf, groups, z)

    def update(self, dt):
        # Update angle and position around the center
        self.angle += self.direction * self.speed * dt

        if not self.full_circle:
            if self.angle >= self.end_angle:
                self.direction = -1
            if self.angle < self.start_angle:
                self.direction = 1

        y = self.center[1] + sin(radians(self.angle)) * self.radius
        x = self.center[0] + cos(radians(self.angle)) * self.radius
        self.rect.center = (x, y)

# Cloud that drifts left and despawns when off-screen
class Cloud(Sprite):
    def __init__(self, pos, surf, groups, z = Z_LAYERS['clouds']):
        super().__init__(pos, surf, groups, z)
        self.speed = randint(50, 120)  # Random speed
        self.direction = -1  # Move left
        self.rect.midbottom = pos

    def update(self, dt):
        # Move cloud and remove when off-screen
        self.rect.x += self.direction * self.speed * dt

        if self.rect.right <= 0:
            self.kill()