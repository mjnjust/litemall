from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import requests

app = Flask(__name__)
CORS(app)

url = "https://www.jiandaoyun.com/_/data_process/admin/data/find"
headers = {
    'clientId': '84261d495c414e',
    'clientSecret': '2112f4b855264ad7b1a4209737fc7836',
    'Cookie': 'AGL_USER_ID=39ef2178-777b-4329-ac49-a89ebbbebd21; _ga=GA1.1.536251028.1747904456; sajssdk_2015_cross_new_user=1; Hm_lvt_de47dd1629940fe88b02865de93dd9fe=1764205859,1765336032; HMACCOUNT=FEE33F4837A93EF9; _ga_JTDW9M3LHZ=GS2.1.s1765336032$o16$g0$t1765336032$j60$l0$h0; _clck=reyl0z%5E2%5Eg1q%5E0%5E1968; _csrf=s%3AUABgH7iMIx_OyhXhVFBU5IV2.GWyhK5WzqtYUsArTkPE%2B5VrpKALIBNGf8nk5fNTGenE; auth_token=s%3A.9uztgExtmqUJXHCi00hv9SGq6eVYSvH%2BxQSwrox1Yls; Hm_lpvt_de47dd1629940fe88b02865de93dd9fe=1765336033; GSuvNKHqfvX2r6v7P8HkZv2bow=s%3ATwc5nPN3Tgq7mh2spWyp2iIiU5jPmdMh.9hkGposL6eS2bJlxpXUQZqTR8MjjMZcXwcuwu9feuu4; JDY_SID=s%3AYwm9dwYO4v4u8UcFlu4p4-pMs5_wgfju.I9AhkCBGXh1pFtZpkUyos%2FmilJ%2Bg4fX%2FK6DBCsoj7nQ; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%225eddb0177bdfd800064513a5%22%2C%22first_id%22%3A%2219b063a21168e2-08a979030520848-26001851-2073600-19b063a211710c6%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTliMDYzYTIxMTY4ZTItMDhhOTc5MDMwNTIwODQ4LTI2MDAxODUxLTIwNzM2MDAtMTliMDYzYTIxMTcxMGM2IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiNWVkZGIwMTc3YmRmZDgwMDA2NDUxM2E1In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%225eddb0177bdfd800064513a5%22%7D%7D; fx-lang=zh_cn',
    'x-csrf-token':'ZzGkUxUW-GW4w2ZCuDHFWCkvkqgk39ViidxE',
    'Content-Type': 'application/json',
    'X-Jdy-Ver': '10.11.6'
}


@app.route('/api/data', methods=['GET'])
def get_data():
    with open('city.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    return jsonify(data)


@app.route('/api/cat', methods=['GET'])
def get_cat():
    payload = json.dumps({
  "appId": "67f7b5e44bb87e55f5a8c699",
  "entryId": "6920fcf62dc8c36caac4afeb",
  "filter": {
    "cond": [],
    "rel": "and"
  },
  "skip": 0,
  "fields": [
    {
      "id": "6920fcf62dc8c36caac4afeb",
      "form": "6920fcf62dc8c36caac4afeb",
      "text": "分类编码",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1763359182895",
      "type": "sn"
    },
    {
      "id": "6920fcf62dc8c36caac4afeb",
      "form": "6920fcf62dc8c36caac4afeb",
      "text": "分类名称",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1763357882073",
      "type": "text"
    },
    {
      "id": "6920fcf62dc8c36caac4afeb",
      "form": "6920fcf62dc8c36caac4afeb",
      "text": "图片",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1763357882074",
      "type": "image",
      "showStyle": "card"
    },
    {
      "id": "6920fcf62dc8c36caac4afeb",
      "form": "6920fcf62dc8c36caac4afeb",
      "text": "排序",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1763368849561",
      "type": "number",
      "precision": None,
      "displayMode": "number",
      "thousandsSeparator": False
    },
    {
      "id": "6920fcf62dc8c36caac4afeb",
      "form": "6920fcf62dc8c36caac4afeb",
      "name": "creator",
      "type": "user",
      "text": "提交人"
    },
    {
      "id": "6920fcf62dc8c36caac4afeb",
      "form": "6920fcf62dc8c36caac4afeb",
      "name": "createTime",
      "type": "datetime",
      "format": "yyyy-MM-dd HH:mm:ss",
      "text": "提交时间"
    },
    {
      "id": "6920fcf62dc8c36caac4afeb",
      "form": "6920fcf62dc8c36caac4afeb",
      "name": "updateTime",
      "type": "datetime",
      "format": "yyyy-MM-dd HH:mm:ss",
      "text": "更新时间"
    }
  ],
  "limit": 200,
  "sort": []
})
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    json_data = response.json()
    listData = json_data.get("data")
    res = []
    for d in listData:
        item = {
            "id": d["_widget_1763359182895"],
            "name": d["_widget_1763357882073"],
            "img": d["_widget_1763357882074"][0]["previewUrl"],
            "sort":d["_widget_1763368849561"]
        }
        res.append(item)
    res = sorted(res, key=lambda x: x['sort'])
    return jsonify(res)


@app.route('/api/cat_items', methods=['GET'])
def get_cat_items():
    cat_id = request.args.get('cat')
    date = request.args.get('date')
    province = request.args.get('province')
    city = request.args.get('city')
    size = request.args.get('size')

    payload = json.dumps({
  "appId": "67f7b5e44bb87e55f5a8c699",
  "entryId": "6814c756e30726893512cd7f",
  "filter": {
    "cond": [
      {
        "type": "text",
        "method": "in",
        "value": [
          "${value}"
        ],
        "entryId": "6814c756e30726893512cd7f",
        "hasEmpty": False,
        "field": "_widget_1763769901148"
      }
    ],
    "rel": "and"
  },
  "skip": 0,
  "fields": [
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "name": "label",
      "type": "text",
      "text": "标题"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "流水号",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1763770024462",
      "type": "sn"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "款式",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1746242293714",
      "type": "text"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "排序",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1763793130332",
      "type": "number",
      "precision": None,
      "displayMode": "number",
      "thousandsSeparator": False
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "库存",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1747050215076",
      "type": "number",
      "precision": None,
      "displayMode": "number",
      "thousandsSeparator": False
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "描述",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1763770891928",
      "type": "textarea"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "分类",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1763769901146",
      "type": "combo",
      "colorEnable": False,
      "async": {
        "data": {
          "formId": "6920fcf62dc8c36caac4afeb",
          "field": "_widget_1763357882073"
        }
      }
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "分类编码",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1763769901148",
      "type": "text"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "分类无用",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1748412374678",
      "type": "combo",
      "colorEnable": False,
      "items": [
        {
          "value": "粉色",
          "text": "粉色"
        },
        {
          "value": "蓝色",
          "text": "蓝色"
        },
        {
          "value": "紫色",
          "text": "紫色"
        },
        {
          "value": "黄色",
          "text": "黄色",
          "color": "#A2C204"
        },
        {
          "value": "绿色",
          "text": "绿色",
          "color": "#00AED1"
        },
        {
          "value": "红色",
          "text": "红色",
          "color": "#5865F5"
        }
      ]
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "租金",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1748412001179",
      "type": "number",
      "precision": None,
      "displayMode": "number",
      "thousandsSeparator": False
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "押金",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1748412001178",
      "type": "number",
      "precision": None,
      "displayMode": "number",
      "thousandsSeparator": False
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "图片",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1746192214992",
      "type": "image",
      "showStyle": "card"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "name": "creator",
      "type": "user",
      "text": "提交人"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "name": "createTime",
      "type": "datetime",
      "format": "yyyy-MM-dd HH:mm:ss",
      "text": "提交时间"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "name": "updateTime",
      "type": "datetime",
      "format": "yyyy-MM-dd HH:mm:ss",
      "text": "更新时间"
    }
  ],
  "limit": 100,
  "sort": [
    {
      "_widget_1746242293714": 1
    },
    {
      "_widget_1763770024462": 1
    }
  ]
})
    payload = payload.replace("${value}", cat_id)
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    json_data = response.json()
    listData = json_data.get("data")
    res = []
    for d in listData:
        item = {
            "id": d["_widget_1763770024462"],
            "name": d["_widget_1746242293714"],
            "img": d["_widget_1746192214992"][0]["previewUrl"],
            "sort": d["_widget_1763793130332"]
        }
        res.append(item)
    res = sorted(res, key=lambda x: x['sort'])
    return jsonify(res)


@app.route('/api/item_detail', methods=['GET'])
def item_detail():
    id = request.args.get('id')
    payload = json.dumps({
  "appId": "67f7b5e44bb87e55f5a8c699",
  "entryId": "6814c756e30726893512cd7f",
  "filter": {
    "cond": [
      {
        "type": "text",
        "method": "in",
        "value": [
          "${value}"
        ],
        "entryId": "6814c756e30726893512cd7f",
        "hasEmpty": False,
        "field": "_widget_1763770024462"
      }
    ],
    "rel": "and"
  },
  "skip": 0,
  "fields": [
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "name": "label",
      "type": "text",
      "text": "标题"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "描述",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1763770891928",
      "type": "textarea"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "流水号",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1763770024462",
      "type": "sn"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "款式",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1746242293714",
      "type": "text"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "库存",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1747050215076",
      "type": "number",
      "precision": None,
      "displayMode": "number",
      "thousandsSeparator": False
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "分类",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1763769901146",
      "type": "combo",
      "colorEnable": False,
      "async": {
        "data": {
          "formId": "6920fcf62dc8c36caac4afeb",
          "field": "_widget_1763357882073"
        }
      }
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "分类编码",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1763769901148",
      "type": "text"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "分类无用",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1748412374678",
      "type": "combo",
      "colorEnable": False,
      "items": [
        {
          "value": "粉色",
          "text": "粉色"
        },
        {
          "value": "蓝色",
          "text": "蓝色"
        },
        {
          "value": "紫色",
          "text": "紫色"
        },
        {
          "value": "黄色",
          "text": "黄色",
          "color": "#A2C204"
        },
        {
          "value": "绿色",
          "text": "绿色",
          "color": "#00AED1"
        },
        {
          "value": "红色",
          "text": "红色",
          "color": "#5865F5"
        }
      ]
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "租金",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1748412001179",
      "type": "number",
      "precision": None,
      "displayMode": "number",
      "thousandsSeparator": False
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "押金",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1748412001178",
      "type": "number",
      "precision": None,
      "displayMode": "number",
      "thousandsSeparator": False
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "text": "图片",
      "labelHidden": False,
      "lineWidth": 12,
      "name": "_widget_1746192214992",
      "type": "image",
      "showStyle": "card"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "name": "creator",
      "type": "user",
      "text": "提交人"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "name": "createTime",
      "type": "datetime",
      "format": "yyyy-MM-dd HH:mm:ss",
      "text": "提交时间"
    },
    {
      "id": "6814c756e30726893512cd7f",
      "form": "6814c756e30726893512cd7f",
      "name": "updateTime",
      "type": "datetime",
      "format": "yyyy-MM-dd HH:mm:ss",
      "text": "更新时间"
    }
  ],
  "limit": 100,
  "sort": [
    {
      "_widget_1746242293714": 1
    }
  ]
})
    payload = payload.replace("${value}", id)

    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    json_data = response.json()
    listData = json_data.get("data")
    res = []
    if len(listData) > 0:
        dd = listData[0]
        for d in dd["_widget_1746192214992"]:
            item = {
                "id": dd["_widget_1763770024462"],
                "url": d["previewUrl"],
                "title": dd["_widget_1746242293714"],
                "text": dd["_widget_1746242293714"]
            }
            res.append(item)
    return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
