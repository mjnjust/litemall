from dataclasses import dataclass

from ..models.item import Item


@dataclass
class Good(Item):
    # 尺码
    size: str
    # 价格
    price: int
    # 押金
    deposit: int
    # 类型
    item: Item

    def __init__(self, size, price, deposit, item):
        self.item = item
        self.size = size
        self.price = price
        self.deposit = deposit
        super().__init__(item.code, item.name,item.image, item.thumb, item.list_images,item.tags)

    def to_dist(self):
        dist = self.item.to_dist()
        dist["size"] = self.size
        dist["price"] = self.price
        dist["deposit"] = self.deposit
        return dist
