import pandas as pd
from src.logic.shop.PerfectWorld import PerfectWorld
from src.logic.shop.Hopely import Hopely
from src.logic.shop.VillageVanguard import VillageVanguard
from src.logic.shop.Magaseek import Magaseek
from src.logic.shop.Plaza import Plaza
from src.logic.shop.World import World
from src.logic.shop.OIOI import OIOI
from src.model.Command import Command


class ItemSearch:
    rowNumber = 500

    def searchItems(self, keyword):
        PerfectWorld().getWithKeyword(keyword)

    def search(self, keyword, offset=0, filterWord=None):
        self.searchItems(keyword)

        offset = int(offset) if offset is not None else 0
        listItemTemp = ''
        listItem = ''
        listItems = ''
        with open('src/template/listItem.html', encoding='utf8') as f:
            listItemTemp = f.read()

        # dataFileList = [PerfectWorld.fileName,
        #                 Hopely.fileName, VillageVanguard.fileName, Magaseek.fileName,
        #                 Plaza.fileName, World.fileName, OIOI.fileName]

        dataFileList = [PerfectWorld.fileName]

        dfList = []
        for dataFile in dataFileList:
            dfList.append(pd.read_csv('data/' + dataFile))

        df = pd.concat(dfList)
        if filterWord != None:
            words = filterWord.split()
            regex = '.*' + '.*|.*'.join(words) + '.*'
            df = df[df.label.str.match(regex)]

        # Remove 0% data
        df = df[df.discount != '0%']
        df = df.sort_values(by='isNew', ascending=False)

        startRow = offset * self.rowNumber
        endRow = startRow + self.rowNumber
        df = df[startRow:endRow]

        for index, data in df.iterrows():
            listItem = listItemTemp
            listItem = listItem.replace('${URL}', data.url)
            listItem = listItem.replace('${IMAGE}', data.image)
            listItem = listItem.replace('${LABEL}', data.label)
            listItem = listItem.replace('${PRICE}', str(data.price))
            listItem = listItem.replace('${DISCOUNT}', data.discount)
            listItem = listItem.replace(
                '${ISNEW}', '[NEW]' if data.isNew else '')
            listItem = listItem.replace('${SHOP}', data.shop)
            listItems += listItem

        return listItems
