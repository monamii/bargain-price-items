from pandas.core.frame import DataFrame
import requests
from bs4.element import ResultSet, Tag
from bs4 import BeautifulSoup
from src.model.Item import Item
from src.model.SearchKeywords import SearchKeywords
import csv
import re
import pandas as pd
from abc import ABC, abstractmethod
from shutil import move
from typing import Optional


class BaseShop(ABC):
    filePath: str = 'data/'
    searchKeywords: list[str] = SearchKeywords.get()

    def __init__(self, baseUrl: str, pageUrls: list[str], pageUrlsWithKeyword: list[str], fileName: str) -> None:
        self.baseUrl: str = baseUrl
        self.pageUrls: list[str] = pageUrls
        self.pageUrlsWithKeyword: list[str] = pageUrlsWithKeyword
        self.fileName: str = fileName

    def getWithKeyword(self, keyword):
        self.searchKeywords = [keyword]
        self.get()

    def get(self):

        plainDataList = []
        dataFilePath = self.filePath + self.fileName
        prevDataFilePath = dataFilePath + '.PREV'
        move(dataFilePath, prevDataFilePath)
        prevDataDf: DataFrame = pd.read_csv(prevDataFilePath)

        pageUrls: list[str] = self.__getAllPageUrls()
        for pageUrl in pageUrls:
            url = self.baseUrl + pageUrl
            itemList = self.__generateItemList(url, prevDataDf)
            plainDataList.extend(itemList)

        # Remove duplicated items
        idSet = set()
        dataList = []
        for data in plainDataList:
            if not data.id in idSet:
                dataList.append(data)
                idSet.add(data.id)

        with open(dataFilePath, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(Item.getHeader())
            for data in dataList:
                writer.writerow(data.convertToCSV())

    def __generateItemList(self, pageUrl: str, prevDataDf):
        # index = 0

        itemList: list[Item] = []
        while pageUrl is not None:
            print(pageUrl)

            response = requests.get(pageUrl)
            soup = BeautifulSoup(response.text, 'html.parser')
            itemListElement = self._getItemListElement(soup)
            for itemElement in itemListElement:
                if self._isNotAvailable(itemElement):
                    continue
                item = self._generateItem(itemElement)
                item.isNew = not item.id in prevDataDf.id.values
                itemList.append(item)

            pageUrl = self._getNextUrl(soup, pageUrl)
            # index += 1
            # if index > 2:
            #     break
        return itemList

    def __getAllPageUrls(self) -> list[str]:
        result: list[str] = []
        result.extend(self.pageUrls)
        for pageUrlWithKeyword in self.pageUrlsWithKeyword:
            for searchKeyword in self.searchKeywords:
                url: str = re.sub('\$\{keyword\}', searchKeyword,
                                  pageUrlWithKeyword)
                result.append(url)

        return result

    @abstractmethod
    def _generateItem(self, itemElement: Tag) -> Item:
        pass

    @abstractmethod
    def _isNotAvailable(self, itemElement: Tag) -> bool:
        pass

    @abstractmethod
    def _getItemListElement(self, soup: BeautifulSoup) -> ResultSet[Tag]:
        pass

    @abstractmethod
    def _getNextUrl(self, soup: BeautifulSoup, pageUrl: str) -> Optional[str]:
        pass
