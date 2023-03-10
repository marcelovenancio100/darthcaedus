import pygame

from settings import *
from entity import Entity
from utils import *


class Enemy(Entity):
    def __init__(self, monster, position, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        self.animations = {'idle': [], 'move': [], 'attack': []}
        self.import_enemy_assets(monster)
        self.status = 'idle'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -10)

        self.stats = MONSTER_DATA[monster]
        self.health = self.stats['health']
        self.exp = self.stats['exp']
        self.speed = self.stats['speed']
        self.damage = self.stats['damage']
        self.attack_type = self.stats['attack_type']
        self.resistance = self.stats['resistance']
        self.attack_radius = self.stats['attack_radius']
        self.notice_radius = self.stats['notice_radius']

        self.can_attack = True
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

    def import_enemy_assets(self, monster):
        enemy_path = f'./graphics/monsters/{monster}/'

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(enemy_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0

            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False

            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def cooldown(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()

            if (current_time - self.attack_time) >= self.attack_cooldown:
                self.can_attack = True

    def update(self):
        self.move(self.speed)
        self.animate()
        self.cooldown()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
