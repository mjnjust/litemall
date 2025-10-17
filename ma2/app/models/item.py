from dataclasses import dataclass


@dataclass
class Item:
    # 编码
    code: str
    # 名称
    name: str
    # 主图
    image: str
    # 缩略图
    thumb: str
    # 列表图
    list_images: []
    # 标签
    tags: []

    def to_dist(self):
        return {
            "code": self.code,
            "name": self.name,
            "image": self.image,
            "thumb": self.thumb,
            "list_images": self.list_images,
            "tags": self.tags
        }
