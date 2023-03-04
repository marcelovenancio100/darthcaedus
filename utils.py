from csv import reader
from os import walk
import pygame


def import_csv_layout(path):
    layouts = []

    with open(path) as file:
        layout = reader(file, delimiter=',')

        for l in layout:
            layouts.append(list(l))

        return layouts


def import_folder(path):
    surfs = []

    for _, __, img_files in walk(path):
        for img in img_files:
            full_path = f'{path}/{img}'
            img_surf = pygame.image.load(full_path).convert_alpha()
            surfs.append(img_surf)

    return surfs
