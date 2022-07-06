import requests
from bs4.element import ResultSet, PageElement
from bs4 import BeautifulSoup
from src.model.Item import Item
from src.logic.shop.BaseShop import BaseShop
import re


class VillageVanguard(BaseShop):
    baseUrl: str = 'https://vvstore.jp'
    pageUrls: list[str] = [
        '/s/category/c1s118/?sort=6&rows=20&page=1&sale=1&stock=1']
    pageUrlsWithKeyword: list[str] = [
        '/s/search/q=${keyword}/?sort=6&rows=20&page=1&sale=1&stock=1']
    fileName: str = 'villageVanguard.csv'
    shopName: str = 'VillageVanguard'

    def __init__(self) -> None:
        super().__init__(self.baseUrl, self.pageUrls,
                         self.pageUrlsWithKeyword, self.fileName)

    def _getItemListElement(self, soup: BeautifulSoup) -> ResultSet[PageElement]:
        return soup.select('.bigsquare,.smallsquare')

    def _generateItem(self, itemElement: PageElement) -> Item:
        linkElement = itemElement.find('a')
        imgElement = linkElement.find('span', class_='pic').find('img')

        url = self.baseUrl + linkElement['href']
        id = linkElement.find('input', {'name': 'ga_item'}).get('id')
        label = linkElement.find('span', class_='label').get_text()
        image = 'https:' + imgElement['src']
        price = linkElement.find(
            'span', class_='pricefukidashi').find('strong').get_text()
        discountNum = 100 - int(price) * \
            100 // int(self.__getDiscount(linkElement['href']))
        discount = str(discountNum) + '%'

        return Item(id, label, price, image, url, discount, False, self.shopName)

    def _isNotAvailable(self, item):
        # Never be unavailable since items are filtered by a stock available
        return False

    def _getNextUrl(self, soup, pageUrl):
        nextElement = soup.find('input', class_='next')
        if nextElement is None:
            return None

        currentPage = soup.find('input', {'name': 'page'}).get('value')
        nextPage = int(currentPage) + 1
        return re.sub('page=\d+', 'page=' + str(nextPage), pageUrl)

    def __getDiscount(self, detailUrl):
        response = requests.get(self.baseUrl + detailUrl)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find('li', class_='price').find('strong', class_='txtprice').get_text()
