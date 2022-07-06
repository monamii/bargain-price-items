
from src.model.Item import Item
import re
from bs4.element import ResultSet, PageElement
from bs4 import BeautifulSoup
from src.logic.shop.BaseShop import BaseShop


class PerfectWorld(BaseShop):
    baseUrl: str = 'https://perfectworld.shop'
    pageUrls: list[str] = ['?mode=srh&sort=n&keyword=%A5%BB%A1%BC%A5%EB',
                           '?mode=srh&sort=n&keyword=%B2%F1%B0%F7%CD%CD%B8%C2%C4%EA']
    pageUrlsWithKeyword: list[str] = []
    fileName: str = 'perfectWorld.csv'
    shopName: str = 'PerfectWorld'

    def __init__(self) -> None:
        super().__init__(self.baseUrl, self.pageUrls,
                         self.pageUrlsWithKeyword, self.fileName)

    def _getItemListElement(self, soup: BeautifulSoup) -> ResultSet[PageElement]:
        return soup.find_all('li', class_='prd_lst_unit prd_lst_unit_s')

    def _generateItem(self, itemElement: PageElement) -> Item:
        priceElement = itemElement.find(
            'span', class_='prd_lst_price prd_lst_span')
        linkElement = itemElement.find('a', class_='prd_lst_link')
        imgElement = linkElement.find('img')

        url = self.baseUrl + linkElement['href']
        id = url.partition('?pid=')[2]
        label = imgElement['alt']
        image = imgElement['src']
        discount = re.search('\d\d％', label).group() if re.search(
            '\d\d％', label) is not None else re.search('\d\d%', label).group()
        price = priceElement.get_text()

        return Item(id, label, price, image, url, discount, False, self.shopName)

    def _isNotAvailable(self, item):
        return item.find('span', class_='prd_lst_soldout prd_lst_span') is not None

    def _getNextUrl(self, soup, pageUrl):
        nextElement = soup.find('li', class_='prd_lst_pager_next')
        return self.baseUrl + nextElement.find('a')['href'] if nextElement.find('a') is not None else None
