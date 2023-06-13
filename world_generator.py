import random

def draw_random_mass(radius_x, radius_y, randomness, center_x, center_y, size, island_map, symbol):
    for x in range(size):
        for y in range(size):
            dx = center_x - x + random.randint(-randomness, randomness)
            dy = center_y - y + random.randint(-randomness, randomness)
            if dx**2 / radius_x**2 + dy**2 / radius_y**2 <= 1:
                island_map[x][y] = symbol


def random_blobs(num, size, island_map, symbol):
    x = random.randint(0, size-1)
    y = random.randint(0, size-1)

    for _ in range(num):
        radius_x = random.randint(1, size//10)
        radius_y = random.randint(1, size//10)
        draw_random_mass(radius_x, radius_y, 0, x, y, size, island_map, symbol)
        x = random.randint(x-radius_x, x+radius_x) 
        if x < 0:
            x = 0
        if x >= size:
            x = size-1
        y = random.randint(y-radius_y, y+radius_y)
        if y < 0:
            y = 0
        if y >= size:
            y = size-1


def mountain_forest(radius, center_x, center_y, size, island_map):
    randomness = radius // 10  # degree of randomness

    ofset_x = random.randint(radius*-1, radius)
    ofset_y = random.randint(radius*-1, radius)

    # define a ring for the forest area
  
    forest_x = random.randint(center_x-radius, center_x+radius)
    forest_y = random.randint(center_y-radius, center_y+radius)

    draw_random_mass(forest_x, forest_y, randomness, center_x-ofset_x, center_y+ofset_y, size, island_map, 'T')

    # define a smaller ellipse for the mountain area
    mountain_radius_x = forest_x // 2 
    mountain_radius_y = forest_y // 2
    randomness = radius // 10  # degree of randomness

    
    draw_random_mass(mountain_radius_x, mountain_radius_y, randomness, center_x-ofset_x, center_y+ofset_y, size, island_map, '^')


def draw_map(size):
    island_map = [['~' for _ in range(size)] for _ in range(size)]
    center = size // 2
    radius = size // 3
    center_x, center_y = center, center
    # draw a circle for the island border
    draw_random_mass(radius, radius, 1, center_x, center_y, size, island_map, '.')
    
    mountain_forest(radius, center_x, center_y, size, island_map)
    
    return island_map

size = 50
island_map = draw_map(size)
for row in island_map:
    print(''.join(row))
