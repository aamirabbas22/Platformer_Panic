from settings import * 
from random import choice
from timer import Timer

class Spider(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites, player):
        super().__init__(groups)

        # Animation frames
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]

        # Position and layer
        self.rect = self.image.get_frect(topleft=pos)
        self.z = Z_LAYERS['main']

        # Direction: randomly choose left or right
        self.direction = choice((-1, 1))

        # Collision detection
        self.collision_rects = [sprite.rect for sprite in collision_sprites]

        # Movement
        self.speed = 200

        # Timer to prevent instant reversal spam
        self.hit_timer = Timer(250)

        # Reference to player for stomp detection
        self.player = player

    def reverse(self):
        # Reverse direction and activate cooldown to avoid immediate re-reversal.
        if not self.hit_timer.active:
            self.direction *= -1
            self.hit_timer.activate()

    def check_player_collision(self):
        # Check if the player stomps the spider from above and destroy spider if so.
        player_velocity_y = getattr(self.player, 'velocity', vector(0, 0)).y
        if self.player.hitbox_rect.colliderect(self.rect) and player_velocity_y > 0:
            if self.player.hitbox_rect.bottom <= self.rect.top + 10:  # Allow slight overlap
                self.kill()
                self.player.velocity.y = -300  # Bounce player upward

    def update(self, dt):
        # Update timers
        self.hit_timer.update()

        # Check for stomp
        self.check_player_collision()

        # Animate spider walking
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        if self.direction < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        # Move horizontally
        self.rect.x += self.direction * self.speed * dt

        # Check for edge or wall to reverse direction
        floor_rect_right = pygame.FRect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1, 1))
        wall_rect = pygame.FRect(self.rect.topleft + vector(-1, 0), (self.rect.width + 2, 1))

        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0 or \
           floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0 or \
           wall_rect.collidelist(self.collision_rects) != -1:
            self.reverse()


class Clown(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, reverse, player, create_pearl):
        super().__init__(groups)

        # Setup animations (flip if needed)
        self.frames = {
            key: [pygame.transform.flip(surf, True, False) for surf in surfs] if reverse else surfs
            for key, surfs in frames.items()
        }
        self.bullet_direction = -1 if reverse else 1

        self.frame_index = 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]

        # Position and state
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']

        # References
        self.player = player
        self.create_pearl = create_pearl

        # Shooting cooldown
        self.shoot_timer = Timer(3000)
        self.has_fired = False

    def check_player_collision(self):
        # Check if player stomps the clown from above and destroy clown if so.
        player_velocity_y = getattr(self.player, 'velocity', vector(0, 0)).y
        if self.player.hitbox_rect.colliderect(self.rect) and player_velocity_y > 0:
            if self.player.hitbox_rect.bottom <= self.rect.top + 10:
                self.kill()
                self.player.velocity.y = -300

    def state_management(self):
        # Check if player is in line of sight and within range to fire a pearl.
        player_pos = vector(self.player.hitbox_rect.center)
        clown_pos = vector(self.rect.center)

        player_near = clown_pos.distance_to(player_pos) < 500
        player_front = clown_pos.x < player_pos.x if self.bullet_direction > 0 else clown_pos.x > player_pos.x
        player_level = clown_pos.y - player_pos.y < 30

        if player_near and player_front and player_level and not self.shoot_timer.active:
            self.state = 'fire'
            self.frame_index = 0
            self.shoot_timer.activate()

    def update(self, dt):
        # Update timers and check for stomp
        self.shoot_timer.update()
        self.check_player_collision()
        self.state_management()

        # Animate based on state
        self.frame_index += ANIMATION_SPEED * dt

        if self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frame_index)]

            # Fire pearl at correct frame
            if self.state == 'fire' and int(self.frame_index) == 3 and not self.has_fired:
                self.create_pearl(self.rect.center, self.bullet_direction)
                self.has_fired = True
        else:
            self.frame_index = 0
            if self.state == 'fire':
                self.state = 'idle'
                self.has_fired = False


class Pearl(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf, direction, speed):
        super().__init__(groups)

        # Identify as pearl bullet
        self.pearl = True

        # Visual and position
        self.image = surf
        self.rect = self.image.get_frect(center=pos + vector(70 * direction, 0))

        # Direction and speed
        self.direction = direction
        self.speed = speed
        self.z = Z_LAYERS['main']

        # Timers: lifetime & reversal cooldown
        self.timers = {
            'lifetime': Timer(5000),  # 5 seconds max lifetime
            'reverse': Timer(250)     # Delay before it can reverse again
        }
        self.timers['lifetime'].activate()

    def reverse(self):
        # Reverse pearl direction if not in cooldown.
        if not self.timers['reverse'].active:
            self.direction *= -1
            self.timers['reverse'].activate()

    def update(self, dt):
        # Update timers
        for timer in self.timers.values():
            timer.update()

        # Move horizontally
        self.rect.x += self.direction * self.speed * dt

        # Destroy if expired
        if not self.timers['lifetime'].active:
            self.kill()
