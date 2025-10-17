import requests
from ..models.item import Item

url = "https://www.jiandaoyun.com/_/data_process/admin/data/find"

payload = "{\r\n    \"appId\": \"68c26aba501fed5e4735079d\",\r\n    \"entryId\": \"68c272f1cbade2668177ac0a\",\r\n    \"filter\": {\r\n        \"cond\": [],\r\n        \"rel\": \"and\"\r\n    },\r\n    \"skip\": 0,\r\n    \"fields\": [\r\n        {\r\n            \"id\": \"68c272f1cbade2668177ac0a\",\r\n            \"form\": \"68c272f1cbade2668177ac0a\",\r\n            \"text\": \"流水号\",\r\n            \"labelHidden\": false,\r\n            \"lineWidth\": 12,\r\n            \"name\": \"_widget_1757573876116\",\r\n            \"type\": \"sn\"\r\n        },\r\n        {\r\n            \"id\": \"68c272f1cbade2668177ac0a\",\r\n            \"form\": \"68c272f1cbade2668177ac0a\",\r\n            \"text\": \"产品名称\",\r\n            \"labelHidden\": false,\r\n            \"lineWidth\": 12,\r\n            \"name\": \"_widget_1757573876115\",\r\n            \"type\": \"text\"\r\n        },\r\n        {\r\n            \"id\": \"68c272f1cbade2668177ac0a\",\r\n            \"form\": \"68c272f1cbade2668177ac0a\",\r\n            \"text\": \"价格\",\r\n            \"labelHidden\": false,\r\n            \"lineWidth\": 12,\r\n            \"name\": \"_widget_1757573876133\",\r\n            \"type\": \"number\",\r\n            \"precision\": null,\r\n            \"displayMode\": \"number\",\r\n            \"thousandsSeparator\": false\r\n        },\r\n        {\r\n            \"id\": \"68c272f1cbade2668177ac0a\",\r\n            \"form\": \"68c272f1cbade2668177ac0a\",\r\n            \"text\": \"押金\",\r\n            \"labelHidden\": false,\r\n            \"lineWidth\": 12,\r\n            \"name\": \"_widget_1757573876134\",\r\n            \"type\": \"number\",\r\n            \"precision\": null,\r\n            \"displayMode\": \"number\",\r\n            \"thousandsSeparator\": false\r\n        },\r\n        {\r\n            \"id\": \"68c272f1cbade2668177ac0a\",\r\n            \"form\": \"68c272f1cbade2668177ac0a\",\r\n            \"text\": \"标签\",\r\n            \"labelHidden\": false,\r\n            \"lineWidth\": 12,\r\n            \"name\": \"_widget_1757573876117\",\r\n            \"type\": \"combocheck\",\r\n            \"colorEnable\": false,\r\n            \"async\": {\r\n                \"data\": {\r\n                    \"formId\": \"68c27296d42e33556463596e\",\r\n                    \"field\": \"_widget_1757573783497\"\r\n                }\r\n            },\r\n            \"allowAddOptions\": false\r\n        },\r\n        {\r\n            \"id\": \"68c272f1cbade2668177ac0a\",\r\n            \"form\": \"68c272f1cbade2668177ac0a\",\r\n            \"text\": \"主图\",\r\n            \"labelHidden\": false,\r\n            \"lineWidth\": 12,\r\n            \"name\": \"_widget_1757573876135\",\r\n            \"type\": \"image\",\r\n            \"showStyle\": \"card\"\r\n        },\r\n        {\r\n            \"id\": \"68c272f1cbade2668177ac0a\",\r\n            \"form\": \"68c272f1cbade2668177ac0a\",\r\n            \"text\": \"列表图\",\r\n            \"labelHidden\": false,\r\n            \"lineWidth\": 12,\r\n            \"name\": \"_widget_1757573876136\",\r\n            \"type\": \"image\",\r\n            \"showStyle\": \"card\"\r\n        },\r\n        {\r\n            \"id\": \"68c272f1cbade2668177ac0a\",\r\n            \"form\": \"68c272f1cbade2668177ac0a\",\r\n            \"name\": \"creator\",\r\n            \"type\": \"user\",\r\n            \"text\": \"提交人\"\r\n        },\r\n        {\r\n            \"id\": \"68c272f1cbade2668177ac0a\",\r\n            \"form\": \"68c272f1cbade2668177ac0a\",\r\n            \"name\": \"createTime\",\r\n            \"type\": \"datetime\",\r\n            \"format\": \"yyyy-MM-dd HH:mm:ss\",\r\n            \"text\": \"提交时间\"\r\n        },\r\n        {\r\n            \"id\": \"68c272f1cbade2668177ac0a\",\r\n            \"form\": \"68c272f1cbade2668177ac0a\",\r\n            \"name\": \"updateTime\",\r\n            \"type\": \"datetime\",\r\n            \"format\": \"yyyy-MM-dd HH:mm:ss\",\r\n            \"text\": \"更新时间\"\r\n        }\r\n    ],\r\n    \"limit\": 300,\r\n    \"sort\": []\r\n}"
headers = {
    'Cookie': 'AGL_USER_ID=39ef2178-777b-4329-ac49-a89ebbbebd21; _ga=GA1.1.536251028.1747904456; Hm_lvt_de47dd1629940fe88b02865de93dd9fe=1760324311; HMACCOUNT=FEE33F4837A93EF9; _ga_JTDW9M3LHZ=GS2.1.s1760324311$o12$g0$t1760324311$j60$l0$h0; _clck=reyl0z%5E2%5Eg04%5E0%5E1968; _csrf=s%3AFKLiIibXRwPuHB1bYCHzLIzj.z%2BxJaY2R2%2FQlwfT8ak3Mo7kB6msEQN2i02uwH235Tu0; auth_token=s%3A.9uztgExtmqUJXHCi00hv9SGq6eVYSvH%2BxQSwrox1Yls; _clsk=izlf6n%5E1760324311941%5E1%5E1%5Es.clarity.ms%2Fcollect; Hm_lpvt_de47dd1629940fe88b02865de93dd9fe=1760324312; GSuvNKHqfvX2r6v7P8HkZv2bow=s%3A1lcLcDdrRJR0qKsaEmUuQSiLarC9cXSg.J75S0g1u3U4aSOTtM%2FRhkiR4SxBh2y9LCNI2Ho9rUUg; JDY_SID=s%3AlvB6cNujLd00_xAPZDRVqVehXoBhtX8w.Vw14dcn%2BSfeGxs8uZNd0P6wDnL8B3qwCUqcVnExTTPI; fx-lang=zh_cn',
    'X-Csrf-Token': 'zLlSgJ0j-PpJ6mLxNuONJF3PfRPNaxDV76lI',
    'Content-Type': 'application/json'
}


class Product:

    @staticmethod
    def get_product_list():
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.json())
        data = response.json()["data"]
        res = []
        for d in data:
            code = d["_widget_1757573876116"]
            name = d["_widget_1757573876115"]
            price = d["_widget_1757573876133"]
            dd = d["_widget_1757573876134"]
            tags = d["_widget_1757573876117"]
            image = d["_widget_1757573876135"]
            image_url = ""
            if len(image) > 0:
                image_url = image[0]["url"]
                thumb = image[0]["thumbUrl"]
            image_list = d["_widget_1757573876136"]
            image_list_url = []
            if len(image_list) > 0:
                for i in image_list:
                    image_list_url.append(i["url"])
            item = Item(code, name, image_url, thumb, image_list_url, tags)
            res.append(item)
        return res
