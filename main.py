import pygame
from os.path import join
from random import randint, uniform
import random
from sympy import symbols, Eq, solve


# import streamlit as st
Window_Height,Window_Width=720,1280
# Initialize the level variable
level = 0
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf, kind):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midtop=pos)
        self.speed = 200
        self.kind = kind

    def update(self, dt, *args, **kwargs):
        self.rect.centery += self.speed * dt
        if self.rect.top > Window_Height:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.original = pygame.image.load(join('image', 'plane1.png'))
        self.original_surf= pygame.transform.smoothscale(self.original, (100, 170))
        self.image =self.original_surf
        self.rect=self.image.get_rect(center=(Window_Width/2, Window_Height/2)) 
        self.player_direction = pygame.math.Vector2()
        self.speed=300
        self.power_ups = {}
        self.shield_active = False
        self.diagonal_arrows_active = False
        self.laser_damage = 20
        #cooldown
        self.can_shoot=True
        self.laser_shoot_time=0
        self.cooldown_duration=400
    
        #mask
        self.mask=pygame.mask.from_surface(self.image)
          
    def laser_timer(self):
        if not self.can_shoot:
            current_time=pygame.time.get_ticks()
            if current_time-self.laser_shoot_time>=self.cooldown_duration:
                self.can_shoot=True
    
    def apply_powerup(self, kind):
        if kind == 'speed':
            self.speed += 100
            self.power_ups['speed'] = pygame.time.get_ticks() + 60000  # Speed lasts 1 minute
        elif kind == 'shield':
            self.shield_active = True
            self.power_ups['shield'] = pygame.time.get_ticks() + 7000  # Shield lasts 1 minute
        elif kind == 'diagonal_arrows':
            self.diagonal_arrows_active = True
            self.power_ups['diagonal_arrows'] = pygame.time.get_ticks() + 60000  # Diagonal arrows last 1 minute
        elif kind == 'more_damage':
            self.laser_damage += 10
            self.power_ups['more_damage'] = pygame.time.get_ticks() + 60000  # More damage lasts 1 minute

        # Ensure the player's position remains unchanged
        self.rect.center = self.rect.center
        # Ensure the player's image remains consistent
        self.image = self.original_surf

    def update(self, dt, *args, **kwargs):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.shoot_lasers()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
        self.player_direction = pygame.math.Vector2()
        self.player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction
        self.rect.center += self.player_direction * self.speed * dt

        # Prevent the player from going out of the window
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Window_Width:
            self.rect.right = Window_Width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Window_Height:
            self.rect.bottom = Window_Height

        self.speed = 300
        self.laser_timer()
        expired = []
        for power, expiry in self.power_ups.items():
            if pygame.time.get_ticks() > expiry:
                expired.append(power)
        for power in expired:
            if power == 'speed':
                self.speed -= 100
            elif power == 'shield':
                self.shield_active = False
            elif power == 'diagonal_arrows':
                self.diagonal_arrows_active = False
            elif power == 'more_damage':
                self.laser_damage -= 10
            del self.power_ups[power]
      
    
    def shoot_lasers(self):
        Laser((all_sprites, laser_sprites), self.rect.midtop, laser_surf, damage=self.laser_damage)
        if self.diagonal_arrows_active:
            Laser((all_sprites, laser_sprites), self.rect.midtop, laser_surf, direction=(-0.5, -1), damage=self.laser_damage)
            Laser((all_sprites, laser_sprites), self.rect.midtop, laser_surf, direction=(0.5, -1), damage=self.laser_damage)

class Player2(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.original = pygame.image.load(join('image', 'player2.png'))
        self.original_surf= pygame.transform.smoothscale(self.original, (100, 170))
        self.image =self.original_surf
        self.rect=self.image.get_rect(center=(Window_Width/2, Window_Height/2)) 
        self.player_direction = pygame.math.Vector2()
        self.speed=300
        self.power_ups = {}
        self.shield_active = False
        self.diagonal_arrows_active = False
        self.laser_damage = 20
        #cooldown
        self.can_shoot=True
        self.laser_shoot_time=0
        self.cooldown_duration=400
    
        #mask
        self.mask=pygame.mask.from_surface(self.image)
        #wall collision
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Window_Width:
            self.rect.right = Window_Width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Window_Height:
            self.rect.bottom = Window_Height    
    def laser_timer(self):
        if not self.can_shoot:
            current_time=pygame.time.get_ticks()
            if current_time-self.laser_shoot_time>=self.cooldown_duration:
                self.can_shoot=True
    
    def apply_powerup(self, kind):
        if kind == 'speed':
            self.speed += 100
            self.power_ups['speed'] = pygame.time.get_ticks() + 60000  # Speed lasts 1 minute
        elif kind == 'shield':
            self.shield_active = True
            self.power_ups['shield'] = pygame.time.get_ticks() + 7000  # Shield lasts 1 minute
        elif kind == 'diagonal_arrows':
            self.diagonal_arrows_active = True
            self.power_ups['diagonal_arrows'] = pygame.time.get_ticks() + 60000  # Diagonal arrows last 1 minute
        elif kind == 'more_damage':
            self.laser_damage += 10
            self.power_ups['more_damage'] = pygame.time.get_ticks() + 60000  # More damage lasts 1 minute

        # Ensure the player's position remains unchanged
        self.rect.center = self.rect.center
        # Ensure the player's image remains consistent
        self.image = self.original_surf

    def update(self,dt, *args, **kwargs):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_1 ] and self.can_shoot:
            self.shoot_lasers()
            self.can_shoot=False
            self.laser_shoot_time=pygame.time.get_ticks()
            laser_sound.play()
        self.player_direction = pygame.math.Vector2()
        self.player_direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.player_direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.player_direction=self.player_direction.normalize() if self.player_direction else self.player_direction
        self.rect.center += self.player_direction * self.speed *dt
        self.speed=300
        self.laser_timer()
        expired = []
        for power, expiry in self.power_ups.items():
            if pygame.time.get_ticks() > expiry:
                expired.append(power)
        for power in expired:
            if power == 'speed':
                self.speed -= 100
            elif power == 'shield':
                self.shield_active = False
            elif power == 'diagonal_arrows':
                self.diagonal_arrows_active = False
            elif power == 'more_damage':
                self.laser_damage -= 10
            del self.power_ups[power]

    def shoot_lasers(self):
        Laser((all_sprites, laser_sprites), self.rect.midtop, laser_surf, damage=self.laser_damage)
        if self.diagonal_arrows_active:
            Laser((all_sprites, laser_sprites), self.rect.midtop, laser_surf, direction=(-0.5, -1), damage=self.laser_damage)
            Laser((all_sprites, laser_sprites), self.rect.midtop, laser_surf, direction=(0.5, -1), damage=self.laser_damage)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, kind, dx=0, dy=-1, owner=None):
        super().__init__()
        self.image = pygame.Surface((10, 20), pygame.SRCALPHA)
        if kind == 1:
            self.image.fill((255, 0, 0, 255))  # Red bullet
        elif kind == 2:
            self.image.fill((0, 255, 0, 255))  # Green bullet
        else:
            self.image.fill((255, 255, 0, 255))  # Yellow bullet
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5 + kind

        # Use provided dx and dy for direction
        self.dx = dx
        self.dy = dy

        self.owner = owner

    def update(self, *args, **kwargs):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if self.rect.top > Window_Height or self.rect.bottom < 0 or self.rect.left > Window_Width or self.rect.right < 0:
            self.kill()
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx=0, dy=1, speed=1):
        super().__init__()
        self.image = pygame.Surface((10, 20), pygame.SRCALPHA)
        self.image.fill((0, 0, 255, 255))  # Blue bullet for enemies
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx
        self.dy = dy
        self.speed = speed

    def update(self, *args, **kwargs):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if self.rect.top > Window_Height or self.rect.bottom < 0 or self.rect.left > Window_Width or self.rect.right < 0:
            self.kill()
# Alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self, image_path, health=100, speed=3, bullet_group=None):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(self.image, (180, 160))
        self.rect = self.image.get_rect(topleft=(0, 50))
        self.direction = 1
        self.speed = speed
        self.health = health
        self.max_health = health
        self.last_attack = pygame.time.get_ticks()
        self.cooldown = 999
        self.bullet_group = bullet_group

    def update(self, *args, **kwargs):
        # Move left and right
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >=  Window_Width:
            self.direction *= -1

    def attack(self, bullet_group):
        now = pygame.time.get_ticks()
        if self.health > 0:
            if now - self.last_attack > self.cooldown:
                kind = random.randint(1, 3)
                print(f"Alien shooting bullet of kind {kind} at position ({self.rect.centerx}, {self.rect.bottom})")
                if kind == 2:
                    # Green bullet: 2 bullets with slight horizontal offset
                    for dx in [-1, 1]:
                        bullet = Bullet(self.rect.centerx + dx * 10, self.rect.bottom, kind, dx * 0.2, dy=1)
                        bullet_group.add(bullet)
                elif kind == 3:
                    # Yellow bullet: 5 bullets spread like a shotgun
                    for dx in [-2, -1, 0, 1, 2]:
                        bullet = Bullet(self.rect.centerx + dx * 20, self.rect.bottom, kind, dx * 0.2, dy=1)
                        bullet_group.add(bullet)
                self.last_attack = now

    def draw_health_bar(self, surface):
        ratio = self.health / self.max_health
        pygame.draw.rect(surface, RED, (Window_Width // 2 - 100, 20, 200, 20))
        pygame.draw.rect(surface, GREEN, (Window_Width // 2 - 100, 20, 200 * ratio, 20))
class Alien2(Alien):
    def __init__(self, image_path, health, speed, bullet_group):
        super().__init__(image_path, health, speed, bullet_group)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(self.image, (180, 160))
        self.rect = self.image.get_rect(topleft=(0, 50))
        self.direction = 1
        self.speed = speed
        self.health = health
        self.max_health = health
        self.last_attack = pygame.time.get_ticks()
        self.bullet_group = bullet_group

    def update(self, *args, **kwargs):
        self.cooldown = 1000
        now = pygame.time.get_ticks()
        if self.health > 0:
            if now - self.last_attack > self.cooldown:
                self.attack(self.bullet_group)
        # Move in a zigzag pattern
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >=  Window_Width:
            self.direction *= -1

       
        
    def attack(self, bullet_group):
        now = pygame.time.get_ticks()
        if self.health > 0:
            if now - self.last_attack > self.cooldown:
                # Alien2 shoots a spread of bullets
                print("Alien2 is attempting to fire bullets.")  # Debugging statement
                for angle in [-2, -1, 0, 1, 2]:
                    bullet = Bullet(self.rect.centerx, self.rect.bottom, 3, dx=angle * 0.1, dy=0.5)  # Slower bullets
                    bullet_group.add(bullet)
                    print(f"Bullet created at ({self.rect.centerx}, {self.rect.bottom}) with angle {angle}.")  # Debugging statement
                self.last_attack = now
                print("Alien2 fired a spread of bullets!")  # Debugging statement
# Add a new Enemy class for additional enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, health, speed, bullet_group):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(randint(100, Window_Width - 100), randint(50, 200)))
        self.health = health
        self.max_health = health
        self.speed = speed
        self.direction = 1
        self.bullet_group = bullet_group
        self.last_attack = pygame.time.get_ticks()
        self.cooldown = 3000

    def update(self, *args, **kwargs):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= Window_Width:
            self.direction *= -1

        # Ensure enemies shoot consistently
        self.attack()

    def attack(self):
        self.cooldown = 3000
        now = pygame.time.get_ticks()
        if now - self.last_attack > self.cooldown:
            # Enemies shoot unique blue bullets
            bullet = Bullet(self.rect.centerx, self.rect.bottom, 2, dx=0, dy=1)  # Slower bullets
            self.bullet_group.add(bullet)
            self.last_attack = now  
    def draw_health_bar(self, surface):
        ratio = self.health / self.max_health
        pygame.draw.rect(surface, RED, (self.rect.left, self.rect.top - 10, 100, 5))
        pygame.draw.rect(surface, GREEN, (self.rect.left, self.rect.top - 10, 100 * ratio, 5))
class Enemy2(Enemy):
    def __init__(self, image_path, health, speed, bullet_group):
        super().__init__(image_path, health, speed, bullet_group)
        self.original = pygame.image.load(join('image', 'enemy2.png'))
        self.original_surf= pygame.transform.smoothscale(self.original, (100, 170))
        self.image =self.original_surf
        self.rect = self.image.get_rect(center=(randint(100, Window_Width - 300), randint(50, 200)))
        self.health = health
        self.max_health = health
        self.speed = speed
        self.direction = 1
        self.bullet_group = bullet_group
        self.last_attack = pygame.time.get_ticks()
        self.cooldown = 1000
    def update(self, *args, **kwargs):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= Window_Width:
            self.direction *= -1
        if random.random() < 0.01:
            self.attack()
    def attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack > self.cooldown:
            # Create slower bullets for Enemy2 with a specific kind
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, dx=0, dy=1, speed=9 )
            self.bullet_group.add(bullet)
            self.last_attack = now
class Enemy3(Enemy):
    def __init__(self, image_path, health, speed, bullet_group):
        super().__init__(image_path, health, speed, bullet_group)
        self.original = pygame.image.load(join('image', 'enemy3.png'))
        self.original_surf= pygame.transform.smoothscale(self.original, (100, 170))
        self.image =self.original_surf
        self.rect = self.image.get_rect(center=(randint(100, Window_Width - 300), randint(50, 200)))
        self.health = health
        self.max_health = health
        self.speed = speed
        self.direction = 1
        self.bullet_group = bullet_group
        self.last_attack = pygame.time.get_ticks()
        self.cooldown = 100
    def update(self, *args, **kwargs):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= Window_Width:
            self.direction *= -1
        if random.random() < 0.01:
            self.attack()
    def attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack > self.cooldown:
            # Correct the argument order and include the 'kind' argument for EnemyBullet
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, dx=0, dy=1, speed=3)
            self.bullet_group.add(bullet)
            self.last_attack = now
class Star(pygame.sprite.Sprite):
    def __init__(self,groups,):  
        super().__init__(groups,)
        self.image = pygame.image.load('/Users/barbaratao/Documents/Hao/video games easy/spaceship game/image/star_small.png')
        self.rect= self.image.get_rect(center=(random.randint(0, Window_Width), random.randint(0, Window_Height)))   

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf, direction=(0, -1), speed=400, damage=20):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midbottom=pos)
        self.direction = pygame.Vector2(direction).normalize()
        self.speed = speed
        self.damage = damage

    def update(self, dt, *args, **kwargs):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.bottom < 0 or self.rect.top > Window_Height or self.rect.left > Window_Width or self.rect.right < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self,surf, pos, groups):
        super().__init__(groups)
        self.image = surf  # Use preloaded image
        self.original_surf = surf
        self.rect = self.image.get_rect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.rotation = 0
        self.rotation_speed = random.randint(-100, 100)
        
    def update(self,dt, *args, **kwargs):
        self.rect.center+=self.direction*self.speed*dt
        
        if pygame.time.get_ticks()-self.start_time>=self.lifetime:
            self.kill()    
        self.rotation+=self.rotation_speed*dt
        self.image=pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self,frames,pos, groups):
        super().__init__(groups)
        self.frames=frames
        self.frame_index=0
        
        
        self.image=self.frames[self.frame_index]
        self.rect=self.image.get_rect(center=pos)

    def update(self,dt, *args, **kwargs):
        self.frame_index+=20*dt
        if self.frame_index<len(self.frames):
            self.image=self.frames[int(self.frame_index)]
        else:
            self.kill()

# Define a new IceMonster class
class IceMonster(pygame.sprite.Sprite):
    def __init__(self, image_path, health, speed, bullet_group):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(randint(100, Window_Width - 100), randint(50, 200)))
        self.health = health
        self.max_health = health
        self.speed = speed
        self.direction = 1
        self.bullet_group = bullet_group
        self.last_attack = pygame.time.get_ticks()
        self.cooldown = 2000

    def update(self, *args, **kwargs):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= Window_Width:
            self.direction *= -1
        if random.random() < 0.01:
            self.attack()

    def attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack > self.cooldown:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, dx=0, dy=1, speed=2)
            self.bullet_group.add(bullet)
            self.last_attack = now

    def draw_health_bar(self, surface):
        ratio = self.health / self.max_health
        pygame.draw.rect(surface, RED, (self.rect.left, self.rect.top - 10, 100, 5))
        pygame.draw.rect(surface, GREEN, (self.rect.left, self.rect.top - 10, 100 * ratio, 5))

# Update the collisions function to allow the shield to block bullets
def collisions():
    global running, alien_alive
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        if player.shield_active:
            # Shield blocks the meteor
            pass
        else:
            running = False
    # collision2_sprites = pygame.sprite.spritecollide(player2, meteor_sprites, True, pygame.sprite.collide_mask)
    # if collision2_sprites:
    #     if player2.shield_active:
    #         # Shield blocks the meteor
    #         pass
    #     else:
    #         running = False
    
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()

        if alien_alive and pygame.Rect.colliderect(laser.rect, alien.rect):
            alien.health -= laser.damage
            laser.kill()
            if alien.health <= 0:
                alien.kill()
                AnimatedExplosion(explosion_frames, alien.rect.midtop, all_sprites)
                explosion_sound.play()
                alien_alive = False

        enemy_collisions = pygame.sprite.spritecollide(laser, enemies, False)
        for enemy in enemy_collisions:
            enemy.health -= laser.damage
            laser.kill()
            if enemy.health <= 0:
                enemy.kill()
                AnimatedExplosion(explosion_frames, enemy.rect.midtop, all_sprites)
                explosion_sound.play()

    collision_bullets = pygame.sprite.spritecollide(player, bullet_group, True, pygame.sprite.collide_mask)
    if collision_bullets:
        if player.shield_active:
            # Shield blocks the bullet
            pass
        else:
            running = False
    # player2_collided = pygame.sprite.spritecollide(player2, bullet_group, True, pygame.sprite.collide_mask)
    # if player2_collided:
    #     if player2.shield_active:
    #         # Shield blocks the bullet
    #         pass
    #     else:
    #         running = False
    collided = pygame.sprite.spritecollide(player, powerup_group, True)
    for power in collided:
        if ask_math_question():
            print(f"Collided with power-up: {power.kind}")  # Debugging statement
            player.apply_powerup(power.kind)
        else:
            print("Incorrect answer. Power-up not granted.")

    player2_collided = pygame.sprite.spritecollide(player2, powerup_group, True)
    for power in player2_collided:
        if ask_math_question():
            player2.apply_powerup(power.kind)
        else:
            print("Incorrect answer. Power-up not granted.")
    # Add logic to slow down the player if hit by an ice monster bullet
        collision_bullets = pygame.sprite.spritecollide(player, bullet_group, True, pygame.sprite.collide_mask)
        for bullet in collision_bullets:
            if isinstance(bullet, EnemyBullet):
                player.speed = max(100, player.speed - 50)  # Reduce player speed temporarily 
def display_score():
    curent_time=pygame.time.get_ticks()//1000
    text_surf=font.render(str(curent_time), True, (240, 240, 240))
    text_rect=text_surf.get_rect(midbottom=(Window_Width/2, Window_Height-50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(20,10).move(0,-8),5,10)


def generate_math_question():
    # Define the variable
    x = symbols('x')

    # Generate random constants
    a, b, c, d, e = [random.randint(1, 10) for _ in range(5)]

    # Create a random equation
    equation = Eq(a + (b - c), d + e * x)

    # Solve for x
    solution = solve(equation, x)

    # Ensure the solution is valid and simple
    if solution and solution[0].is_rational:
        return equation, solution[0]
    else:
        return generate_math_question()  # Retry if no valid solution

def ask_math_question():
    equation, solution = generate_math_question()
    user_answer = ""
    solution = float(solution)  # Convert the solution to a float
    print(f"Math question: {equation}, Solution: {solution}")  # Debugging statement

    while True:
        display_surface.fill((0, 0, 0))
        q_surf = font.render(f"Solve: {equation}", True, WHITE)
        input_surf = font.render(user_answer, True, WHITE)
        display_surface.blit(q_surf, q_surf.get_rect(center=(Window_Width/2, Window_Height/2 - 50)))
        display_surface.blit(input_surf, input_surf.get_rect(center=(Window_Width/2, Window_Height/2 + 50)))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        # Allow a small tolerance for floating-point comparison
                        is_correct = abs(float(user_answer) - solution) < 0.01
                        print(f"User answered: {user_answer}, Correct: {is_correct}")  # Debugging statement
                        return is_correct
                    except ValueError:
                        print("Invalid input. Please enter a number.")  # Debugging statement
                        user_answer = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                else:
                    user_answer += event.unicode

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Add a global variable to track if ice monsters have been spawned
ice_monsters_spawned = False

# Initialize Alien
alien = Alien(join('image', 'alien.png'))
alien_group = pygame.sprite.GroupSingle(alien)
bullet_group = pygame.sprite.Group()

# Preload meteor image once at the start of the game
meteor_surf = pygame.image.load(join('image', 'meteor_smaller_nobg.png'))

# general setup 
pygame.init()
Window_Width, Window_Height=1280,720
display_surface = pygame.display.set_mode (( Window_Width, Window_Height))

pygame.display.set_caption('Space shooter')
running=True
alien_alive = True
clock=pygame.time.Clock()
all_sprites=pygame.sprite.Group()
meteor_sprites=pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
alien_sprites=pygame.sprite.Group()
powerup_group = pygame.sprite.Group()
enemies = pygame.sprite.Group()

screen = pygame.display.set_mode((Window_Width, Window_Height))

# Create a separate group for background stars
background_sprites = pygame.sprite.Group()

# Add stars to the background_sprites group
for i in range(20):
    Star(background_sprites)
    
player = Player(all_sprites)
player2=Player2(all_sprites)
player2.rect.center = (Window_Width / 2, Window_Height - 100)
POWERUP_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(POWERUP_EVENT, 2000)   
#imports
original_laser = pygame.image.load(join('image', 'laser2_cropped (1).png'))
rotated_laser = pygame.transform.rotate(original_laser, 90)  # Rotate the laser 90 degrees
laser_surf = pygame.transform.smoothscale(rotated_laser, (100, 100))
laser_rect=laser_surf.get_rect(bottomleft =(20,Window_Height-20))
font=pygame.font.Font(None, 50)
explosion_frames=[pygame.image.load(join( 'explosions',f'{i}.png')).convert_alpha() for i  in range(14)]
explosion_sound=pygame.mixer.Sound(join('audio', 'explosion_x.wav'))
explosion_sound.set_volume(0.1)
laser_sound=pygame.mixer.Sound(join('audio', 'laser.mp3'))
laser_sound.set_volume(0.1)
game_sound=pygame.mixer.Sound(join('audio', 'game_music.mp3'))
game_sound.set_volume(0.1)
game_sound.play()

#custom events
meteor_event=pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 1000)

# Initialize the game_over variable
game_over = False

# Power-up setup
powerup_surf = pygame.image.load(join('image', 'powerup.png'))
powerup_surf = pygame.transform.smoothscale(powerup_surf, (50, 50))
powerup_sprites = pygame.sprite.Group()

powerup_event = pygame.event.custom_type()
pygame.time.set_timer(powerup_event, 2000)  # Spawn a power-up every 5 seconds

# Update the game loop to use the game_over variable
while running:
    if game_over:
        game_over_surf = font.render("Game Over! Press R to Restart", True, WHITE)
        game_over_rect = game_over_surf.get_rect(center=(Window_Width / 2, Window_Height / 2))
        display_surface.blit(game_over_surf, game_over_rect)
      
        pygame.display.update()
        continue

    dt = clock.tick(30) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = random.randint(0, Window_Width), random.randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))
        elif event.type == POWERUP_EVENT:
            kind = random.choice(['speed', 'shield', 'diagonal_arrows', 'more_damage'])
            image_path = 'image/star_small.png'  # Replace with actual icons
            PowerUp(image_path, kind, (all_sprites, powerup_group))
        if event.type == powerup_event:
            x = random.randint(0, Window_Width - 50)
            kind = random.choice(['speed', 'shield', 'diagonal_arrows', 'more_damage'])  # Randomly choose between abilities
            PowerUp(powerup_sprites, (x, -50), powerup_surf, kind=kind)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r and game_over:
                # Reset the game state
                player.alive = True
                player2.alive = True
                player.rect.center = (Window_Width / 2, Window_Height - 100)
                player2.rect.center = (Window_Width / 2, Window_Height - 100)
               
                # Restart the game
                alien.health = alien.max_health
                alien_alive = True
                player.__init__(all_sprites)
                player2.__init__(all_sprites)
                enemies.empty()
                game_over = False

    # Update
    all_sprites.update(dt)
    powerup_sprites.update(dt)
    collisions()
    alien_group.update()
    bullet_group.update()
    print(f"Alien alive: {alien_alive}, Level: {level}, Cooldown: {alien.cooldown}, Last attack: {alien.last_attack}")
    if alien_alive:
        alien.attack(bullet_group)
    else:
        if not alien_alive and len(enemies) == 0:
            level += 1

        if level == 1 and len(enemies) == 0:  # Spawn new enemies for level 1
            for _ in range(3):
                health = randint(50, max(50, alien.max_health - 10))
                speed = randint(2, 5)
                enemy = Enemy(join('image', 'enemy.png'), health, speed, bullet_group)
                enemies.add(enemy)
                all_sprites.add(enemy)
                enemy2 = Enemy2(join('image', 'enemy2.png'), health, speed, bullet_group)
                enemies.add(enemy2)

        if level == 2 and len(enemies) == 0:  # Spawn new enemies for level 2
            for _ in range(4):
                health = randint(50, max(100, alien.max_health - 10))
                speed = randint(2, 5)
                enemy = Enemy(join('image', 'enemy.png'), health, speed, bullet_group)
                enemies.add(enemy)
                all_sprites.add(enemy)
                enemy2 = Enemy2(join('image', 'enemy2.png'), health, speed, bullet_group)
                enemies.add(enemy2)

        if level == 3 and len(enemies) == 0:
            for _ in range(5):
                health = randint(50, max(150, alien.max_health - 10))  # Ensure valid range for health
                speed = randint(2, 5)
                enemy = Enemy(join('image', 'enemy.png'), health, speed, bullet_group)
                enemies.add(enemy)
                all_sprites.add(enemy)
                enemy2 = Enemy2(join('image', 'enemy2.png'), health, speed, bullet_group)
                enemies.add(enemy2)
            for _ in range(1):   
                health = randint(50, max(150, alien.max_health - 10))  # Ensure valid range for health
                speed = randint(2, 5)
                enemy3 = Enemy3(join('image', 'enemy3.png'), health, speed, bullet_group)
                enemies.add(enemy3)
                # all_sprites.add(enemy3)
        if level == 4 and len(enemies) == 0:
            alien_alive = True
            for _ in range(1):
                alien.attack (bullet_group)
                health = 500
                speed = randint(2, 5)
                alien = Alien(join('image', 'alien.png'), health, speed, bullet_group)
                enemies.add(alien)
            for _ in range(3):
                health = randint(50, max(200, alien.max_health - 10))  # Ensure valid range for health
                speed = randint(2, 5)
                enemy = Enemy(join('image', 'enemy.png'), health, speed, bullet_group)
                enemies.add(enemy)
        if level == 5 and len(enemies) == 0:
            for _ in range(6):
                health = randint(50, max(200, alien.max_health - 10))
                speed = randint(2, 5)
                enemy = Enemy(join('image', 'enemy.png'), health, speed, bullet_group)
                enemies.add(enemy)
                enemy2 = Enemy2(join('image', 'enemy2.png'), health, speed, bullet_group)
                enemies.add(enemy2)
                enemy3 = Enemy3(join('image', 'enemy3.png'), health, speed, bullet_group)
                enemies.add(enemy3)
        if level == 6 and len(enemies) == 0:
            for _ in range(1):
                health = 700
                speed = randint(2, 5)
                alien2 = Alien2(join('image', 'alien2.png'), health, speed, bullet_group)
                enemies.add(alien2)
    
    # Check for power-up collisions
    powerup_collision = pygame.sprite.spritecollide(player, powerup_sprites, True, pygame.sprite.collide_mask)
    if powerup_collision:
        powerup = powerup_collision[0]
        # if ask_single_math_question():
        if ask_math_question():  
            print(f"Correct answer! Granting power-up: {powerup.kind}") 
            player.apply_powerup(powerup.kind)
            # Display the ability granted
            ability_surf = font.render(f"You got: {powerup.kind.capitalize()}!", True, WHITE)
            ability_rect = ability_surf.get_rect(center=(Window_Width / 2, Window_Height / 2))
            display_surface.blit(ability_surf, ability_rect)
            pygame.display.update()
            pygame.time.delay(1000)  # Show the message for 2 seconds
        else:
            # Do not grant the power-up
            pass

    # Check for power-up collisions for player2
    powerup_collision_player2 = pygame.sprite.spritecollide(player2, powerup_sprites, True, pygame.sprite.collide_mask)
    if powerup_collision_player2:
        powerup = powerup_collision_player2[0]
        if ask_math_question():
            player2.apply_powerup(powerup.kind)
            # Display the ability granted for player2
            ability_surf = font.render(f"Player 2 got: {powerup.kind.capitalize()}!", True, WHITE)
            ability_rect = ability_surf.get_rect(center=(Window_Width / 2, Window_Height / 2 + 50))
            display_surface.blit(ability_surf, ability_rect)
            pygame.display.update()
            pygame.time.delay(1000)  # Show the message for 1 second

    # Reset player speed after power-up effect ends
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT + 1:
            player.speed = 300

    # Draw  
    display_surface.fill('#3a2e3f')
    # Ensure the background is drawn first before other elements
    if level == 7 or level == 8 or level == 9 or level == 10:
        ice_background = pygame.image.load(join('image', 'ice_background.png'))
        ice_background = pygame.transform.smoothscale(ice_background, (Window_Width, Window_Height))
        display_surface.blit(ice_background, (0, 0))

    background_sprites.draw(display_surface)
    alien_group.draw(screen)
    bullet_group.draw(screen)
    powerup_sprites.draw(display_surface)
    if alien_alive:
        alien.draw_health_bar(screen)
    enemies.update()
    enemies.draw(screen)
    for enemy in enemies:
        enemy.draw_health_bar(screen)
    for ice_monster in enemies:
        ice_monster.draw_health_bar(screen)
        ice_monsters = pygame.sprite.Group()
        ice_monsters.draw(screen)
    all_sprites.draw(display_surface)
    display_score()
    
    # Add logic to draw a blue bubble around the player if the shield is active
    if player.shield_active:
        pygame.draw.circle(display_surface, (0, 0, 255), player.rect.center, player.rect.width, 5)  # Blue bubble

    # Check if the player is dead
    if not player.alive():
        if ask_math_question():
           if answer == True:
               player.alive = True 
        else:
            # Reset the player state
            player.alive = True
            player.rect.center = (Window_Width / 2, Window_Height - 100)
            alien.health = alien.max_health
            alien_alive = True
        ice_monsters_spawned = False


        # Spawn ice monsters only once
        if not ice_monsters_spawned:
            for _ in range(3):
                health = randint(50, 100)
                speed = randint(1, 3)
                ice_enemy = IceMonster(join('image', 'ice_enemy.png'), health, speed, bullet_group)
                enemies.add(ice_enemy)
                all_sprites.add(ice_enemy)
            ice_monsters_spawned = True
    if level == 8 and len(enemies) == 0:
        if not ice_monsters_spawned:
            for _ in range(4):
                health = randint(100, 150)
                speed = randint(1, 3)
                ice_enemy = IceMonster(join('image', 'ice_enemy.png'), health, speed, bullet_group)
                enemies.add(ice_enemy)
                all_sprites.add(ice_enemy)
            for _ in range(2):
                health = randint(100, 150)
                speed = randint(1, 3)
                enemy = Enemy(join('image', 'enemy.png'), health, speed, bullet_group)
                enemies.add(enemy)
                all_sprites.add(enemy)
            ice_monsters_spawned = True
    if level == 9 and len(enemies) == 0:
        if not ice_monsters_spawned:
            for _ in range(5):
                health = randint(150, 200)
                speed = randint(1, 3)
                ice_enemy = IceMonster(join('image', 'ice_enemy.png'), health, speed, bullet_group)
                enemies.add(ice_enemy)
                all_sprites.add(ice_enemy)
            for _ in range(3):
                health = randint(150, 200)
                speed = randint(1, 3)
                enemy = Enemy(join('image', 'enemy.png'), health, speed, bullet_group)
                enemies.add(enemy)
                all_sprites.add(enemy)
            ice_monsters_spawned = True
    if level == 10 and len(enemies) == 0:
        for _ in range(6):
            health = randint(200, 250)
            speed = randint(1, 3)
            ice_enemy = IceMonster(join('image', 'ice_enemy.png'), health, speed, bullet_group)
            enemies.add(ice_enemy)
            all_sprites.add(ice_enemy)
        for _ in range(1):
            health = 850
            speed = randint(1, 3)
            alien = Alien(join('image', 'enemy.png'), health, speed, bullet_group)
            enemies.add(enemy)
            all_sprites.add(enemy)
    if level==11:
        # Load and display the volcano backgroun             
        volcano_background = pygame.image.load(join('image', 'volcano.png'))  # Replace with the actual image path
        volcano_background = pygame.transform.smoothscale(volcano_background, (Window_Width, Window_Height))
        display_surface.blit(volcano_background)
    pygame.display.update()

pygame.quit()

# End of the game loop


