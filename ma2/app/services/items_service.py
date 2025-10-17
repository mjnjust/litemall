from ..integration.product import Product


class ItemService:
    @staticmethod
    def list_items(page, page_size):
        data = Product.get_product_list()
        total = len(data)
        res = data[(page - 1) * page_size:page * page_size]
        return {
            "total": total,
            "data": res
        }
