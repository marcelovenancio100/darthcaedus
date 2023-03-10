from random import choice

from settings import *
from tile import Tile
from player import Player
from debug import debug
from utils import *
from weapon import Weapon
from ui import UI


class Level:
    def __init__(self):
        self.player = None

        self.display_surf = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

        self.current_attack = None

        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('./map/map_Grass.csv'),
            'objects': import_csv_layout('./map/map_Objects.csv')
        }

        graphics = {
            'grass': import_folder('./graphics/grass'),
            'objects': import_folder('./graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'boundary':
                            Tile((x, y), (self.obstacle_sprites,), 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'grass', random_grass_image)
                        if style == 'objects':
                            object_image = graphics['objects'][int(col)]
                            Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'objects', object_image)

        self.player = Player(
            (2000, 1415),
            (self.visible_sprites,),
            self.obstacle_sprites,
            self.create_attack,
            self.destroy_attack,
            self.create_magic
        )

    def create_attack(self):
        self.current_attack = Weapon(self.player, (self.visible_sprites,))

    def create_magic(self, style, strength, cost):
        pass

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()

        self.current_attack = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)
        # debug(self.player.direction)
        # debug(self.player.status)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.half_width = self.display_surf.get_size()[0] // 2
        self.half_height = self.display_surf.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load('./graphics/tilemap/ground.png')
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surf.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda spr: spr.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surf.blit(sprite.image, offset_pos)
