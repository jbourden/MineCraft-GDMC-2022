import interfaceUtils
from userUtils import UserUtilities


class Fountain:
    def _init__(self,area):
        self.utils = UserUtilities(area)

    # build a fountain in the build area with a given location
    def build(self,x1, y1, z1, x2, z2, fountain, heightmapGround, heightmapTree):
        self.utils.clean_plot((x1, z1, x2, z2), y1, heightmapTree)
        self.fill_plot(x1, x2, y1, z1, z2, heightmapGround)
        for x in range(fountain.shape[0]):
            for z in range(fountain.shape[1]):
                x_pos, z_pos = x1 + x, z1 + z
                if fountain[x, z] == 0:
                    interfaceUtils.setBlock(x_pos, y1 - 1, z_pos, "glowstone")
                if fountain[x, z] == 1:
                    interfaceUtils.setBlock(x_pos, y1 - 1, z_pos, "stone_bricks")
                    interfaceUtils.setBlock(x_pos, y1, z_pos, "soul_lantern")
                if fountain[x, z] == 2:
                    interfaceUtils.setBlock(x_pos, y1, z_pos, "glowstone")
                if fountain[x, z] == 3:
                    interfaceUtils.setBlock(x_pos, y1, z_pos, "glowstone")
                    interfaceUtils.setBlock(x_pos, y1 + 1, z_pos, "glowstone")
                    interfaceUtils.setBlock(x_pos, y1 + 2, z_pos, "water")

