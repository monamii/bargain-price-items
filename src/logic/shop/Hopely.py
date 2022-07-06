
from src.model.Item import Item
from src.logic.shop.BaseShop import BaseShop
from bs4.element import ResultSet, PageElement
from bs4 import BeautifulSoup


class Hopely(BaseShop):
    baseUrl: str = 'https://hopely.jp'
    pageUrls: list[str] = ['/item/search?type=new&parent_category=23']
    pageUrlsWithKeyword: list[str] = []
    fileName: str = 'hopely.csv'
    shopName: str = 'Hopely'

    def __init__(self) -> None:
        super().__init__(self.baseUrl, self.pageUrls,
                         self.pageUrlsWithKeyword, self.fileName)

    def _getItemListElement(self, soup: BeautifulSoup) -> ResultSet[PageElement]:
        return soup.select('.m-items .unit')

    def _generateItem(self, itemElement: PageElement) -> Item:
        imgElement = itemElement.find('p', class_='fig').find('img')
        linkElement = itemElement.find('a', class_='text')
        priceElement = linkElement.find('p', class_='price')

        url = self.baseUrl + linkElement['href']
        id = url.partition('/item/')[2]
        label = linkElement.find('h3', class_='name').get_text()
        image = self.baseUrl + imgElement['src']
        discount = itemElement.find('li', class_='is_red').get_text()
        price = priceElement.get_text()

        return Item(id, label, price, image, url, discount, False, self.shopName)

    def _isNotAvailable(self, item):
        return item.find('li', class_='is_gray') is not None

    def _getNextUrl(self, soup, pageUrl):
        nextElement = soup.find('p', class_='next')
        return self.baseUrl + nextElement.find('a')['href'] if nextElement is not None else None
