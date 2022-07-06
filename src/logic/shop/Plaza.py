
from src.model.Item import Item
from src.logic.shop.BaseShop import BaseShop
from src.model.SearchKeywordsPlaza import SearchKeywordsPlaza
from bs4.element import ResultSet, PageElement
from bs4 import BeautifulSoup


class Plaza(BaseShop):
    baseUrl: str = 'https://www.plazastyle.com'
    pageUrls: list[str] = []
    pageUrlsWithKeyword: list[str] = [
        '/ec/proList/doSearch/srDispProductList/%20/1/%20/${keyword}/1/0/0/1/%20/%20/%20/4/40/0/0?jp=on&wd=%20']
    searchKeywords: list[str] = SearchKeywordsPlaza.get()
    fileName: str = 'plaza.csv'
    shopName: str = 'Plaza'

    def __init__(self) -> None:
        super().__init__(self.baseUrl, self.pageUrls,
                         self.pageUrlsWithKeyword, self.fileName)

    def _getItemListElement(self, soup: BeautifulSoup) -> ResultSet[PageElement]:
        return soup.select('ul[class="item"] li')

    def _generateItem(self, itemElement: PageElement) -> Item:
        photoElement = itemElement.select_one('p.photo')
        imgElement: PageElement = photoElement.find('img')

        url = self.baseUrl + photoElement.find('a')['href']
        id = url.split('/')[-1]
        label = imgElement['alt']
        image = self.baseUrl + imgElement['src']
        discount = '??%'
        price = itemElement.find('p', class_='price price-sale').get_text()

        return Item(id, label, price, image, url, discount, False, self.shopName)

    def _isNotAvailable(self, item):
        return item.select_one('p.photo') == None

    def _getNextUrl(self, soup, pageUrl):
        nextElement = soup.select_one('li.next')
        return self.baseUrl + nextElement.find('a')['href'] if nextElement is not None else None
