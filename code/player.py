from settings import *  # Import shared game settings and constants
from timer import Timer  # Custom timer class to handle delays/cooldowns
from os.path import join
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, semi_collision_sprites, frames, data, attack_sound, jump_sound):
        # Base sprite setup
        super().__init__(groups)
        self.z = Z_LAYERS['main']  # Drawing layer order
        self.data = data

        # Load animations
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'idle', True  # Default state and direction
        self.image = self.frames[self.state][self.frame_index]

        # Set up rects
        self.rect = self.image.get_frect(topleft=pos)  # Visual rect for rendering
        self.hitbox_rect = self.rect.inflate(-65, -10) # Collision hitbox (smaller)
        self.old_rect = self.hitbox_rect.copy()        # Store previous frame for collision checks

        # Movement variables
        self.direction = vector()
        self.speed = 200
        self.gravity = 1300
        self.jump = False
        self.jump_height = 900
        self.deflecting = False  # Are we currently deflecting?

        # Collision
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites  # Platforms you can drop through
        self.on_surface = {'floor': False, 'left': False, 'right': False}  # Contact checks
        self.platform = None  # Moving platform we’re on

        # Timers for cooldowns and effects
        self.timers = {
            'wall jump': Timer(400),       # Prevents immediate re-wall jumping
            'wall slide block': Timer(250),# Blocks wall sliding right after jumping
            'platform skip': Timer(100),   # Allows dropping through platforms
            'attack block': Timer(500),    # Deflect cooldown
            'hit': Timer(400)              # Damage flicker duration
        }

        # audio 
        self.attack_sound = attack_sound
        self.jump_sound = jump_sound

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)

        # Ignore horizontal input during wall jump
        if not self.timers['wall jump'].active:
            if keys[pygame.K_RIGHT]:
                input_vector.x += 1
                self.facing_right = True

            if keys[pygame.K_LEFT]:
                input_vector.x -= 1
                self.facing_right = False

            if keys[pygame.K_DOWN]:
                self.timers['platform skip'].activate()  # Drop through platform

            if keys[pygame.K_x]:
                self.deflect()  # Try to deflect

            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_UP]:
            self.jump = True  # Flag jump

    def deflect(self):
        # Trigger deflect only if cooldown is ready
        if not self.timers['attack block'].active:
            self.deflecting = True  # Set deflect flag
            self.frame_index = 0    # Restart deflect animation
            self.timers['attack block'].activate()  # Start cooldown
            self.attack_sound.play()

    def move(self, dt):
        # Horizontal
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')  # Resolve horizontal collisions

        # Vertical
        if (not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right']))
            and not self.timers['wall slide block'].active):
            # Stick to wall: cancel gravity for wall slide
            self.direction.y = 0
            self.hitbox_rect.y += self.gravity / 10 * dt
        else:
            # Apply gravity
            self.direction.y += self.gravity / 2 * dt
            self.hitbox_rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt

        # Jump
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers['wall slide block'].activate()
                self.hitbox_rect.bottom -= 1  # Avoid sticking
                self.jump_sound.play()
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1  # Jump away from wall
                self.jump_sound.play()
            self.jump = False  # Reset jump

        self.collision('vertical')  # Resolve vertical collisions
        self.semi_collision()       # Resolve semi-solid platforms
        self.rect.center = self.hitbox_rect.center  # Update visual rect

    def platform_move(self, dt):
        # If standing on moving platform, move with it
        if self.platform:
            self.hitbox_rect.topleft += self.platform.direction * self.platform.speed * dt

    def check_contact(self):
        # Rects for surface detection
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft,(self.hitbox_rect.width,2))
        right_rect = pygame.Rect(self.hitbox_rect.topright + vector(0,self.hitbox_rect.height / 4),(2,self.hitbox_rect.height / 2))
        left_rect  = pygame.Rect(self.hitbox_rect.topleft + vector(-2,self.hitbox_rect.height / 4), (2,self.hitbox_rect.height / 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semi_collide_rect = [sprite.rect for sprite in self.semi_collision_sprites]

        # Floor detection (including semi-solids)
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 or floor_rect.collidelist(semi_collide_rect) >= 0 and self.direction.y >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left']  = True if left_rect.collidelist(collide_rects)  >= 0 else False

        # Detect moving platform underfoot
        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal':
                    # Collided from left
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right
                    # Collided from right
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left
                else:
                    # Collided from top
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom
                        if hasattr(sprite, 'moving'):
                            self.hitbox_rect.top += 6  # Offset for moving platforms
                    # Collided from bottom
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0  # Cancel vertical movement

    def semi_collision(self):
        # Allow passing through semi-solid platforms if 'platform skip' not active
        if not self.timers['platform skip'].active:
            for sprite in self.semi_collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = sprite.rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0

    def update_timers(self):
        # Tick all timers
        for timer in self.timers.values():
            timer.update()

    def animate(self, dt):
        # Update animation frame
        self.frame_index += ANIMATION_SPEED * dt

        # If deflect animation finishes, revert to idle
        if self.state == 'deflect' and self.frame_index >= len(self.frames[self.state]):
            self.state = 'idle'

        # Get current frame & flip if needed
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)

        # Automatically end deflect state when animation finishes
        if self.deflecting and self.frame_index > len(self.frames[self.state]):
            self.deflecting = False

    def get_state(self):
        # Decide current animation state
        if self.on_surface['floor']:
            if self.deflecting:
                self.state = 'deflect'
            else:
                self.state = 'idle' if self.direction.x == 0 else 'run'
        else:
            if self.deflecting:
                self.state = 'air_deflect'
            else:
                if any((self.on_surface['left'], self.on_surface['right'])):
                    self.state = 'wall'
                else:
                    self.state = 'jump' if self.direction.y < 0 else 'fall'

    def get_damage(self):
        # If not invincible, take damage and start flicker timer
        if not self.timers['hit'].active:
            self.data.health -= 1
            self.timers['hit'].activate()

    def flicker(self):
        # Make player flicker white when hit
        if self.timers['hit'].active and sin(pygame.time.get_ticks() * 100) >= 0:
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey('black')
            self.image = white_surf

    def update(self, dt):
        # Full player update each frame
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()

        self.input()
        self.move(dt)
        self.platform_move(dt)
        self.check_contact()

        self.get_state()
        self.animate(dt)
        self.flicker()
