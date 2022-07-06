
from src.model.Item import Item
from src.logic.shop.BaseShop import BaseShop
from bs4.element import ResultSet, PageElement
from bs4 import BeautifulSoup
import re


class OIOI(BaseShop):
    baseUrl: str = 'https://search-voi.0101.co.jp'
    pageUrls: list[str] = []
    pageUrlsWithKeyword: list[str] = ['/freeword/?q=${keyword}&sale=1&page=1']
    fileName: str = 'oioi.csv'
    shopName: str = 'OIOI'

    def __init__(self) -> None:
        super().__init__(self.baseUrl, self.pageUrls,
                         self.pageUrlsWithKeyword, self.fileName)

    def _getItemListElement(self, soup: BeautifulSoup) -> ResultSet[PageElement]:
        return soup.find_all('li', class_='itemContainer__list__item -two')

    def _generateItem(self, itemElement: PageElement) -> Item:
        aElement = itemElement.select_one('a', class_='item__image')
        imgElement: PageElement = aElement.find(
            'img', class_='image-contents__image')

        url = aElement['href']
        id = itemElement.find('div', class_='item')['data-productid']
        label = imgElement['alt']
        # image = imgElement['data-src']
        image = label
        discount = itemElement.find(
            'li', class_='labels__list__label -sale').get_text()
        price = itemElement.find(
            'span', class_='summary__price-info__num').get_text()

        return Item(id, label, price, image, url, discount, False, self.shopName)

    def _isNotAvailable(self, item):
        # Never be unavailable since items are filtered by a stock available
        return False

    def _getNextUrl(self, soup, pageUrl: str):
        nextElement = soup.find('button', class_="button-wrapper__button")
        if(nextElement is None or nextElement['disabled'] is not None):
            return None

        currentPage = int(pageUrl.split("&page=")[1])
        return re.sub('page=\d+', 'page=' + str(currentPage+1), pageUrl)
