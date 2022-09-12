import interfaceUtils
from userUtils import UserUtilities


class Fence:
    def __init__(self, area):
        self.area = area
        self.utils = UserUtilities(area)

    # Build fence around the build area
    def build(self, area, heightmapGround):

        # build a fence around the perimeter
        for x in range(area[0], area[0] + area[2]):
            z = area[1]
            y = self.utils.heightAt(x, z, heightmapGround)
            interfaceUtils.placeBlockBatched(x, y - 1, z, "cobblestone")
            interfaceUtils.placeBlockBatched(x, y, z, "oak_fence")
            if x % 2 == 0:
                interfaceUtils.placeBlockBatched(x, y + 1, z, 'minecraft:lantern')

        for z in range(area[1], area[1] + area[3]):
            x = area[0]
            y = self.utils.heightAt(x, z, heightmapGround)
            interfaceUtils.placeBlockBatched(x, y - 1, z, "cobblestone")
            interfaceUtils.placeBlockBatched(x, y, z, "oak_fence")
            if z % 2 == 0:
                interfaceUtils.placeBlockBatched(x, y + 1, z, 'minecraft:lantern')
        for x in range(area[0], area[0] + area[2]):
            z = area[1] + area[3] - 1
            y = self.utils.heightAt(x, z, heightmapGround)
            interfaceUtils.placeBlockBatched(x, y - 1, z, "cobblestone")
            interfaceUtils.placeBlockBatched(x, y, z, "oak_fence")

            if x % 2 == 0:
                interfaceUtils.placeBlockBatched(x, y + 1, z, 'minecraft:soul_lantern')
        for z in range(area[1], area[1] + area[3]):
            x = area[0] + area[2] - 1
            y = self.utils.heightAt(x, z, heightmapGround)
            interfaceUtils.placeBlockBatched(x, y - 1, z, "cobblestone")
            interfaceUtils.placeBlockBatched(x, y, z, "oak_fence")
            if z % 2 == 0:
                interfaceUtils.placeBlockBatched(x, y + 1, z, 'minecraft:soul_lantern')
