from src.model.Command import Command
from src.logic.shop.PerfectWorld import PerfectWorld
from src.logic.shop.Hopely import Hopely
from src.logic.shop.VillageVanguard import VillageVanguard
from src.logic.shop.Magaseek import Magaseek
from src.logic.shop.Plaza import Plaza
from src.logic.shop.World import World
from src.logic.shop.OIOI import OIOI
import sys


def main(command):
    if Command.ALL == command:
        PerfectWorld().get()
        Hopely().get()
        VillageVanguard().get()
        Magaseek().get()
        Plaza().get()
        World().get()
        OIOI().get()
    elif Command.PERFECT_WORLD == command:
        PerfectWorld().get()
    elif Command.HOPLEY == command:
        Hopely().get()
    elif Command.VILLAGE_VANGUARD == command:
        VillageVanguard().get()
    elif Command.MEGASEEK == command:
        Magaseek().get()
    elif Command.PLAZA == command:
        Plaza().get()
    elif Command.WORLD == command:
        World().get()
    elif Command.OIOI == command:
        OIOI().get()
    else:
        print('Unknown command')


if __name__ == "__main__":
    main(sys.argv[1])
