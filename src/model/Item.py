from typing import Text


class Item:
    def __init__(self, id, label, price, image, url, discount, isNew, shop):
        self.id = id
        self.label = label
        self.price = price
        self.image = image
        self.url = url
        self.discount = discount
        self.isNew = isNew
        self.shop = shop

    def convertToCSV(self):
        return [self.id, self.label, self.price, self.image, self.url, self.discount, self.isNew, self.shop]

    def getHeader():
        return ['id', 'label', 'price', 'image', 'url', 'discount', 'isNew', 'shop']
