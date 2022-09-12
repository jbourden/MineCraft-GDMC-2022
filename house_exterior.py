#! /usr/bin/python3

__all__ = []

# __version__
import random
import interfaceUtils

'''
    @buildFlowerBed: build a flower bed for a park or in side the house plot.
    @param:
        x1,y1, z1, w, l, cy: the location of the o build 
    @return:
         none.

'''


def buildFlowerBed(x1, y1, z1, w, l, cy):
    fb_width = w
    fb_length = l

    flowers_arr = ["minecraft:blue_orchid", 'minecraft:azure_bluet', 'minecraft:red_tulip', 'minecraft:orange_tulip',
                   'minecraft:white_tulip',
                   'minecraft:pink_tulip', 'minecraft:oxeye_daisy', 'minecraft:cornflower',
                   'minecraft:lily_of_the_valley', 'minecraft:wither_rose', 'minecraft:sunflower', 'minecraft:lilac',
                   'minecraft:rose_bush', 'minecraft:peony']

    flower = flowers_arr[random.randint(0, len(flowers_arr) - 1)]

    # Our color options
    slab_colors = ["minecraft:granite_slab", "minecraft:jungle_slab", "minecraft:stone_slab", 'minecraft:andesite_slab']
    fb_colors = ["minecraft:granite", "minecraft:stripped_oak_wood", 'minecraft:stripped_acacia_wood',
                 "minecraft:dark_oak_wood'"]

    # Randomly selecting the colors
    slab_col = slab_colors[random.randint(0, len(slab_colors) - 1)]
    fb_col = fb_colors[random.randint(0, len(fb_colors) - 1)]

    # Building the dirt in the center
    for x in range(x1 + 1, x1 + fb_width):
        for z in range(z1 + 1, z1 + fb_length):
            interfaceUtils.placeBlockBatched(x, y1, z, "minecraft:dirt")

    # Planting the flowers
    for x in range(x1 + 1, x1 + fb_width):
        for z in range(z1 + 1, z1 + fb_length):
            interfaceUtils.placeBlockBatched(x, y1 + 1, z, flower)

    # Next four loops build the walls around the dirt

    for x in range(x1, x1 + fb_width + 1):
        if not cy:
            interfaceUtils.placeBlockBatched(x, y1, z1, fb_col)
        else:
            interfaceUtils.placeBlockBatched(x, y1, z1, "minecraft:dirt")
            interfaceUtils.placeBlockBatched(x, y1 + 1, z1, flower)

    for x in range(x1, x1 + fb_width + 1):
        interfaceUtils.placeBlockBatched(x, y1, z1 + fb_length, fb_col)

        if not cy:
            interfaceUtils.placeBlockBatched(x, y1, z1 + fb_length, fb_col)
        else:
            interfaceUtils.placeBlockBatched(x, y1, z1 + fb_length, "minecraft:dirt")
            interfaceUtils.placeBlockBatched(x, y1 + 1, z1 + fb_length, flower)

    for z in range(z1, z1 + fb_length + 1):

        if not cy:
            interfaceUtils.placeBlockBatched(x1, y1, z, fb_col)
        else:
            interfaceUtils.placeBlockBatched(x1, y1, z, "minecraft:dirt")
            interfaceUtils.placeBlockBatched(x1, y1 + 1, z, flower)

    for z in range(z1, z1 + fb_length + 1):
        if not cy:
            interfaceUtils.placeBlockBatched(x1 + fb_width, y1, z, fb_col)
        else:
            interfaceUtils.placeBlockBatched(x1 + fb_width, y1, z, "minecraft:dirt")
            interfaceUtils.placeBlockBatched(x1 + fb_width, y1 + 1, z, flower)

    # Next four loops build the slabs around the wall
    for x in range(x1 - 1, x1 + fb_width + 2):
        interfaceUtils.placeBlockBatched(x, y1, z1 - 1, slab_col)

    for x in range(x1 - 1, x1 + fb_width + 2):
        interfaceUtils.placeBlockBatched(x, y1, z1 + fb_length + 1, slab_col)

    for z in range(z1 - 1, z1 + fb_length + 2):
        interfaceUtils.placeBlockBatched(x1 - 1, y1, z, slab_col)

    for z in range(z1 - 1, z1 + fb_length + 2):
        interfaceUtils.placeBlockBatched(x1 + fb_width + 1, y1, z, slab_col)


# Build a swimming poll inside the house plot
def buildSwimmingPool(x1, y1, z1, pool_width, pool_length):
    # Our color options
    slab_colors = ["minecraft:granite_slab", "minecraft:jungle_slab", "minecraft:stone_slab", 'minecraft:andesite_slab']
    pool_colors = ["minecraft:granite", "minecraft:stripped_oak_wood", 'minecraft:stripped_acacia_wood',
                   "minecraft:dark_oak_wood'"]
    bottom_surface = ['minecraft:light_blue_terracotta','minecraft:light_blue_concrete','minecraft:blue_concrete',
                      'minecraft:blue_terracotta']
    bottom = bottom_surface[random.randrange(0,len(bottom_surface))]
    # Randomly selecting the colors
    slab_col = slab_colors[random.randint(0, len(slab_colors) - 1)]
    pool_col = pool_colors[random.randint(0, len(pool_colors) - 1)]

    # Building the dirt in the center
    for x in range(x1 + 1, x1 + pool_width):
        for z in range(z1 + 1, z1 + pool_length):
            for h in range(5):
                if h == 0:
                    if z%2 == 0 and x%2 ==0:
                        interfaceUtils.placeBlockBatched(x, y1 - 4 + h, z, 'minecraft:beacon')
                    else:
                        interfaceUtils.placeBlockBatched(x, y1 - 4 + h, z, bottom)
                else:
                    interfaceUtils.placeBlockBatched(x, y1 - 4 + h, z, "minecraft:water")

    # Next four loops build the walls around the dirt
    for x in range(x1, x1 + pool_width + 1):
        for h in range(6):
            interfaceUtils.placeBlockBatched(x, y1 - 5 + h, z1, pool_col)

    for x in range(x1, x1 + pool_width + 1):
        for h in range(6):
            interfaceUtils.placeBlockBatched(x, y1 - 5 + h, z1 + pool_length, pool_col)

    for z in range(z1, z1 + pool_length + 1):
        for h in range(6):
            interfaceUtils.placeBlockBatched(x1, y1 - 5 + h, z, pool_col)

    for z in range(z1, z1 + pool_length + 1):
        for h in range(6):
            interfaceUtils.placeBlockBatched(x1 + pool_width, y1 - 5 + h, z, pool_col)

    # Next four loops build the slabs around the wall
    for x in range(x1 - 1, x1 + pool_width + 2):
        interfaceUtils.placeBlockBatched(x, y1, z1 - 1, slab_col)

    for x in range(x1 - 1, x1 + pool_width + 2):
        interfaceUtils.placeBlockBatched(x, y1, z1 + pool_length + 1, slab_col)

    for z in range(z1 - 1, z1 + pool_length + 2):
        interfaceUtils.placeBlockBatched(x1 - 1, y1, z, slab_col)

    for z in range(z1 - 1, z1 + pool_length + 2):
        interfaceUtils.placeBlockBatched(x1 + pool_width + 1, y1, z, slab_col)
