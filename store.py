import random
import interfaceUtils
from userUtils import UserUtilities


class Store:
    def __init__(self, area):
        self.utils = UserUtilities(area)

    '''
        @buildStore: create given size store. 
        @param:
            x1, y1, z1, x2, y2, z2 : the location and the height of the store in the build area
            plot, roof: plot map for store 
            size: size of the store
            heightmapGround: height map for ground blocks
            heightmapTree: height map for trees or any kind of obstacle above the build location
        @return:
            none
    '''

    def build(self, x1, y1, z1, x2, z2, plot, size, heightmapGround, heightmapTree):
        ground_block = interfaceUtils.getBlock(x1, y1 - 1, z1)
        self.utils.fill_plot(x1, x2, y1, z1, z2, heightmapGround, 'minecraft:stripped_jungle_wood')
        self.utils.clean_plot((x1, z1, x2, z2,), y1, heightmapTree)
        stones = ['minecraft:glowstone', 'minecraft:redstone_block', 'minecraft:infested_stone',
                  'minecraft:infested_cobblestone']
        stones2 = ['minecraft:blackstone', 'minecraft:sandstone', 'minecraft:stone']
        woods = ['minecraft:birch_wood', 'minecraft:jungle_wood', 'minecraft:stripped_oak_wood',
                 'minecraft:acacia_wood',
                 'minecraft:dark_oak_wood', 'minecraft:stripped_dark_oak_wood']
        terracottas = ['minecraft:white_wool', 'minecraft:orange_wool', 'minecraft:yellow_terracotta',
                       'minecraft:gray_terracotta', 'minecraft:red_terracotta']
        wools = ['minecraft:orange_wool', 'minecraft:white_wool', 'minecraft:orange_wool', 'minecraft:magenta_wool',
                 'minecraft:light_blue_wool']
        fences = ['minecraft:dark_oak_fence', 'minecraft:spruce_fence', 'minecraft:crimson_fence',
                  'minecraft:warped_fence']
        logs = ['minecraft:stripped_spruce_log', 'minecraft:stripped_birch_log', 'minecraft:jungle_log',
                'minecraft:acacia_log', 'minecraft:oak_log', 'minecraft:dark_oak_log']
        concretes = ['minecraft:blue_concrete','minecraft:brown_concrete','minecraft:green_concrete',
                     'minecraft:yellow_concrete','minecraft:cyan_concrete','minecraft:red_concrete']
        carpets = ['minecraft:white_carpet', 'minecraft:black_carpet']
        stairs = ['minecraft:birch_stairs','minecraft:quartz_stairs','minecraft:acacia_stairs']
        terracotta = terracottas[random.randrange(0, len(terracottas))]
        wool = wools[random.randrange(0, len(wools))]
        stone = stones[random.randrange(0, len(stones))]
        stone2 = stones2[random.randrange(0, len(stones2))]
        wood = woods[random.randrange(0, len(woods))]
        fence = fences[random.randrange(0, len(fences))]
        log = logs[random.randrange(0, len(logs))]
        concrete = concretes[random.randrange(0, len(concretes))]
        stair = stairs[random.randrange(0,len(stairs))]
        # small structure, which we will use for park or something else;
        if size == "small":
            blocks = [terracottas[random.randrange(0, len(terracottas))],
                      wools[random.randrange(0, len(wools))]]  # roof blocks
            for x in range(plot.shape[0]):
                for z in range(plot.shape[1]):
                    x_pos, z_pos = x1 + x, z1 + z
                    if plot[x, z] == 0:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, stone)
                    if plot[x, z] == 6:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, stone)
                        block = self.utils.blockColor(x, z, blocks)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 4, z_pos, block)
                    if plot[x, z] == 1:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, stone)
                        interfaceUtils.placeBlockBatched(x_pos, y1, z_pos, wood)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 1, z_pos, stone2)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 2, z_pos, fence)
                        block = self.utils.blockColor(x, z, blocks)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 3, z_pos, block)
                    if plot[x, z] == 2:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, stone)
                        interfaceUtils.placeBlockBatched(x_pos, y1, z_pos, wood)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 1, z_pos, fence)
                        block = self.utils.blockColor(x, z, blocks)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 3, z_pos, block)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 4, z_pos, block)
                    if plot[x, z] == 3:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, stone)
                        interfaceUtils.placeBlockBatched(x_pos, y1, z_pos, wood)
                        block = self.utils.blockColor(x, z, blocks)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 3, z_pos, block)
                    if plot[x, z] == 4:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, stone)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 1, z_pos, "oak_trapdoor")
                        block = self.utils.blockColor(x, z, blocks)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 3, z_pos, block)
                    if plot[x, z] == 7:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, stone)
                        chests = ["ender_chest", "chest", 'trapped_chest']
                        interfaceUtils.placeBlockBatched(x_pos, y1, z_pos, chests[random.randrange(0, 3)])
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 1, z_pos, 'minecraft:lantern')
                        block = self.utils.blockColor(x, z, blocks)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 4, z_pos, block)

        # medium struture, which we will use for park or something else;
        if size == "medium":
            for x in range(plot.shape[0]):
                for z in range(plot.shape[1]):
                    x_pos, z_pos = x1 + x, z1 + z
                    if plot[x, z] == 0:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, log)
                    if plot[x, z] == 1:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, log)
                        interfaceUtils.placeBlockBatched(x_pos, y1, z_pos, stone)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 1, z_pos, stone)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 2, z_pos, terracotta)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 3, z_pos, fence)
                    if plot[x, z] == 2:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, log)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 3, z_pos, wool)
                    if plot[x, z] == 3:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, log)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 3, z_pos, terracotta)
                    if plot[x, z] == 4 or plot[x, z] == 6 or plot[x,z] == 9 or plot[x,z] == 10 or plot[x,z] == 11 or plot[x,z] == 12:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, log)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 4, z_pos, wool)
                        if plot[x,z] == 6:
                            interfaceUtils.placeBlockBatched(x_pos, y1 + 3, z_pos, 'minecraft:soul_lantern')
                            interfaceUtils.placeBlockBatched(x_pos, y1, z_pos, 'minecraft:soul_campfire')
                        if plot[x,z] == 12:
                            interfaceUtils.placeBlockBatched(x_pos, y1, z_pos,
                                                             f'{stair}[facing=east,half= bottom, shape=straight]')
                        if plot[x,z] == 9:
                            interfaceUtils.placeBlockBatched(x_pos, y1, z_pos,
                                                             f'{stair}[facing=west,half= bottom, shape=straight]')
                        if plot[x,z] == 10:
                            interfaceUtils.placeBlockBatched(x_pos, y1, z_pos,
                                                             f'{stair}[facing=north,half= bottom, shape=straight]')
                        if plot[x,z] == 11:
                            interfaceUtils.placeBlockBatched(x_pos, y1, z_pos,
                                                             f'{stair}[facing=south,half= bottom, shape=straight]')

                    if plot[x, z] == 8:
                        carpet = self.utils.blockColor(x, z, carpets)
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, log)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 4, z_pos, concrete)
                        interfaceUtils.placeBlockBatched(x_pos, y1 , z_pos, fence)
                        interfaceUtils.placeBlockBatched(x_pos, y1+1, z_pos, carpet)
                    if plot[x, z] == 7:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, log)
                        if x !=6:
                            interfaceUtils.placeBlockBatched(x_pos, y1, z_pos, "iron_bars")


        # large store with glass walls. i will do some more modification after.
        if size == "large":
            height = random.randrange(4, 7)
            carpets = ['minecraft:white_carpet', 'minecraft:black_carpet']
            roofs = ['minecraft:brown_glazed_terracotta', 'minecraft:light_blue_glazed_terracotta',
                     'minecraft:white_glazed_terracotta']
            corners = ['minecraft:infested_stone', 'minecraft:birch_log', 'minecraft:quartz_block']
            glasses = ['minecraft:orange_stained_glass_pane', 'minecraft:light_blue_stained_glass_pane',
                       'minecraft:gray_stained_glass_pane']
            walls = ['minecraft:white_terracotta', 'minecraft:gray_terracotta', 'minecraft:red_terracotta', ]
            glass = glasses[random.randrange(0, len(glasses))]
            corner = corners[random.randrange(0, len(corners))]
            roof = roofs[random.randrange(0, len(roofs))]
            wall = walls[random.randrange(0, len(walls))]

            flowers = ['oak_sapling', 'spruce_sapling', 'birch_sapling',
                       'jungle_sapling',
                       'acacia_sapling', 'dark_oak_sapling',
                       'dandelion', 'poppy', 'blue_orchid', 'allium',
                       'azure_bluet', 'red_tulip', 'orange_tulip',
                       'white_tulip',
                       'pink_tulip', 'oxeye_daisy', 'cornflower',
                       'lily_of_the_valley', 'wither_rose', 'sunflower']
            ground_blocks = ['minecraft:stripped_birch_wood', 'minecraft:birch_wood', 'minecraft:jungle_wood',
                             'minecraft:stripped_jungle_wood']
            ground_block = ground_blocks[random.randrange(0, len(ground_blocks))]
            for x in range(plot.shape[0]):
                for z in range(plot.shape[1]):
                    x_pos, z_pos = x1 + x, z1 + z
                    flower = flowers[random.randrange(0, len(flowers))]
                    interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, ground_block)
                    if plot[x, z] == 6:
                        for y in range(y1 + 2, y1 + height + 1):
                            interfaceUtils.placeBlockBatched(x_pos, y, z_pos, wall)
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, log)
                        interfaceUtils.placeBlockBatched(x_pos, y1, z_pos,
                                                         "minecraft:acacia_door[half=lower,facing=north,hinge=left]")
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 1, z_pos,
                                                         "minecraft:acacia_door[half=upper,facing=north,hinge=left]")

                        interfaceUtils.placeBlockBatched(x_pos, y1 + 2, z_pos, glass)
                    if plot[x, z] == 1:
                        for y in range(y1, y1 + height + 1):
                            interfaceUtils.placeBlockBatched(x_pos, y, z_pos, wall)
                    if plot[x, z] == 2 or plot[x, z] == 7 or plot[x, z] == 8:
                        carpet = self.utils.blockColor(x, z, carpets)
                        interfaceUtils.placeBlockBatched(x_pos, y1, z_pos, carpet)
                        interfaceUtils.placeBlockBatched(x_pos, y1 + height, z_pos, roof)
                    if plot[x, z] == 3:
                        for y in range(y1, y1 + height + 1):
                            interfaceUtils.placeBlockBatched(x_pos, y, z_pos, corner)
                    if plot[x, z] == 4:
                        for y in range(y1, y1 + height + 1):
                            interfaceUtils.placeBlockBatched(x_pos, y, z_pos, wall)
                            interfaceUtils.placeBlockBatched(x_pos, y1 + 1, z_pos, glass)
                            interfaceUtils.placeBlockBatched(x_pos, y1 + 2, z_pos, glass)
                            interfaceUtils.placeBlockBatched(x_pos, y1 + 3, z_pos, glass)

                    if plot[x, z] == 7:
                        if x % 2 == 0:
                            if height >= 5:
                                interfaceUtils.placeBlockBatched(x_pos, y1 + height - 1, z_pos, 'minecraft:chain')
                                interfaceUtils.placeBlockBatched(x_pos, y1 + height - 2, z_pos, 'minecraft:lantern')
                            else:
                                interfaceUtils.placeBlockBatched(x_pos, y1 + height - 1, z_pos, 'minecraft:lantern')
                        interfaceUtils.placeBlockBatched(x_pos, y1, z_pos, 'minecraft:fletching_table')
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 1, z_pos, f'potted_{flower}')

                    if plot[x, z] == 8:
                        if z % 2 == 0:
                            if height >= 5:
                                interfaceUtils.placeBlockBatched(x_pos, y1 + height - 1, z_pos, 'minecraft:chain')
                                interfaceUtils.placeBlockBatched(x_pos, y1 + height - 2, z_pos, 'minecraft:lantern')
                            else:
                                interfaceUtils.placeBlockBatched(x_pos, y1 + height - 1, z_pos, 'minecraft:lantern')
                        interfaceUtils.placeBlockBatched(x_pos, y1, z_pos, 'minecraft:fletching_table')
                        interfaceUtils.placeBlockBatched(x_pos, y1 + 1, z_pos, f'potted_{flower}')
