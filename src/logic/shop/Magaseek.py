from bs4.element import ResultSet, Tag
from bs4 import BeautifulSoup
from src.model.Item import Item
from src.logic.shop.BaseShop import BaseShop
import re
from typing import Optional


class Magaseek(BaseShop):
    # https://www.magaseek.com/fw/list/dp_2-tr_f-fw_%E3%82%B9%E3%83%8C%E3%83%BC%E3%83%94%E3%83%BC
    baseUrl: str = 'https://www.magaseek.com'
    pageUrls: list[str] = []
    pageUrlsWithKeyword: list[str] = ['/fw/list/sk_2-tr_f-fw_${keyword}']
    fileName: str = 'magaseek.csv'
    shopName: str = 'Magaseek'

    def __init__(self) -> None:
        super().__init__(self.baseUrl, self.pageUrls,
                         self.pageUrlsWithKeyword, self.fileName)

    def _getItemListElement(self, soup: BeautifulSoup) -> ResultSet[Tag]:
        return soup.find_all('div', class_='pack')

    def _generateItem(self, itemTag: Tag) -> Item:
        productElement: Tag = itemTag.find('p', class_='product-pic')
        linkElement = productElement.find('a')
        imgElement = linkElement.find('img')

        id: str = itemTag.attrs['data-mgnocolor']
        url: str = self.baseUrl + linkElement.attrs['href']
        label = imgElement.attrs['alt']
        image = imgElement.attrs['data-original']
        priceString = itemTag.select_one('p.price').get_text()
        price = priceString.split('&nbsp;')[0]
        discount = re.search('\d+\%', priceString)
        discount = discount.group() if discount is not None else '0%'

        return Item(id, label, price, image, url, discount, False, self.shopName)

    def _isNotAvailable(self, itemTag: Tag):
        # Never be unavailable since items are filtered by a stock available
        return False

    def _getNextUrl(self, soup: BeautifulSoup, pageUrl: str) -> Optional[str]:
        nextElement = soup.find('li', class_='next')
        aElement = nextElement.find('a') if nextElement is not None else None
        return self.baseUrl + aElement.attrs['href'] if aElement is not None else None
