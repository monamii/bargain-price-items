
from src.model.Item import Item
from src.logic.shop.BaseShop import BaseShop
from bs4.element import ResultSet, PageElement
from bs4 import BeautifulSoup


class World(BaseShop):
    baseUrl: str = 'https://store.world.co.jp'
    pageUrls: list[str] = []
    pageUrlsWithKeyword: list[str] = [
        '/search?fr=${keyword}&st=1&sst1=3']
    fileName: str = 'world.csv'
    shopName: str = 'World'

    def __init__(self) -> None:
        super().__init__(self.baseUrl, self.pageUrls,
                         self.pageUrlsWithKeyword, self.fileName)

    def _getItemListElement(self, soup: BeautifulSoup) -> ResultSet[PageElement]:
        return soup.select('div.block_item')

    def _generateItem(self, itemElement: PageElement) -> Item:
        aElement = itemElement.select_one(
            'a', class_='search-result__item--link')
        imgElement: PageElement = aElement.find('img')
        priceElement: PageElement = itemElement.find(
            'div', class_="wrap_price")

        url = aElement['href']
        id = url.split('/')[-1]
        label = imgElement['alt']
        image = self.baseUrl + imgElement['src']
        discount = priceElement.find(
            'p', class_='txt_sale-rate').find('em').get_text()
        price = priceElement.find(
            'p', class_='txt_sale-price').find('em').get_text()

        return Item(id, label, price, image, url, discount, False, self.shopName)

    def _isNotAvailable(self, item):
        # Never be unavailable since items are filtered by a stock available
        return False

    def _getNextUrl(self, soup, pageUrl):
        nextElement = soup.find('li', class_="search-result__paging__last")
        isNotNone = (nextElement is not None) and (
            nextElement.find('a') is not None)
        return nextElement.find('a')['href'] if isNotNone else None
