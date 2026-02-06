from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import requests
import common

app = Flask(__name__)
CORS(app)

url = "https://www.jiandaoyun.com/_/data_process/admin/data/find"
headers = {
    'Cookie': 'AGL_USER_ID=39ef2178-777b-4329-ac49-a89ebbbebd21; _ga=GA1.1.536251028.1747904456; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%225eddb0177bdfd800064513a5%22%2C%22first_id%22%3A%2219b063a21168e2-08a979030520848-26001851-2073600-19b063a211710c6%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTliMDYzYTIxMTY4ZTItMDhhOTc5MDMwNTIwODQ4LTI2MDAxODUxLTIwNzM2MDAtMTliMDYzYTIxMTcxMGM2IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiNWVkZGIwMTc3YmRmZDgwMDA2NDUxM2E1In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%225eddb0177bdfd800064513a5%22%7D%7D; _clck=reyl0z%5E2%5Eg1w%5E0%5E1968; Hm_lvt_de47dd1629940fe88b02865de93dd9fe=1768812040; HMACCOUNT=FEE33F4837A93EF9; _csrf=s%3AGVCso0MhHLxFI9Xorj6jgccK.F5U3szjSKPbAJDaPK6YNU5YLvQmM2UYEDLCb7NXDYfU; auth_token=s%3A.9uztgExtmqUJXHCi00hv9SGq6eVYSvH%2BxQSwrox1Yls; _ga_JTDW9M3LHZ=GS2.1.s1768812040$o23$g0$t1768812041$j59$l0$h0; Hm_lpvt_de47dd1629940fe88b02865de93dd9fe=1768812042; GSuvNKHqfvX2r6v7P8HkZv2bow=s%3AeV7fyYRdkrVfJodeOykEWFPD81t9zbaq.zrFPuq%2B6waRcSivnHBkwZJevNiyu88UKy0j3DXz1sMg; JDY_SID=s%3AZ0OM9nVdnRpxz_1uwJUQz9um_FzBA9rr.NuRc3M2829%2BhGT%2Fl3caCu%2FTDrO6lFMlkbze4vcrpgBc; fx-lang=zh_cn',
    'x-csrf-token': 'rBWnkHN8-n3y4hV_sSFuxzNPPjAR8X18-IC4',
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
    payload = common.category_json
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    json_data = response.json()
    listData = json_data.get("data")
    res = []
    for d in listData:
        item = {
            "id": d["_widget_1763359182895"],
            "name": d["_widget_1763357882073"],
            "img": d["_widget_1763357882074"][0]["previewUrl"],
            "sort": d["_widget_1763368849561"]
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

    all_items = get_items(cat_id)
    if date is None:
        common.log(f"query all , cat:{cat_id}")
        return jsonify(all_items)
    else:
        date = date.replace("-", "")
        date = date[2:]
        map_items = {}
        for item in all_items:
            map_items[f"{item['name']}"] = item

        lock_nums = common.lockDayMap.get(province)
        if lock_nums is None:
            lock_nums = 3
        try_lock_days = common.generate_date_range(date, lock_nums)

        if size is None or size == 'None':
            common.log(f"query without size , cat:{cat_id},date:{date},address:{province}-{city}")
            tmp_res = get_date_useful_items(map_items, date, try_lock_days)
            res = []
            for tmp in tmp_res:
                if tmp["nums"]["idle_stock"] > 0:
                    res.append(tmp)
            return jsonify(res)
        else:
            common.log(f"query by size , cat:{cat_id},date:{date},address:{province}-{city},size:{size}")
            tmp_res = get_size_useful_items(map_items, date, province, city, size)
            res = []
            for tmp in tmp_res:
                if tmp["idle_stock"] > 0:
                    res.append(tmp)
            return jsonify(res)


def get_all_items(cat_id):
    items = get_items(cat_id)
    return items


def get_size_useful_items(items, date, province, city, size):
    orders = get_orders()
    for order in orders:
        item_name = order["itemName"]
        locked_days = order["lockDay"]
        common.log(item_name)
        common.log(locked_days)

    return orders


def get_date_useful_items(items, use_day, try_lock_days):
    orders = get_orders()
    for order in orders:
        item_name = order["itemName"]
        locked_days = order["lockDay"]
        if item_name not in items:
            continue
        item = items[item_name]
        intersection = list(set(try_lock_days) & set(locked_days))
        if len(intersection) > 0:
            item['nums']["idle_stock"] = item['nums']["idle_stock"] - 1
            key = f'{order["user"]}_{order["province"]}_{order["useDay"]}'
            item["conflicted"].append({
                "key": key
            })
        else:
            key = f'{order["user"]}_{order["province"]}_{order["useDay"]}'
            if int(use_day) < int(order["useDay"]):
                item["continued"].append({
                    "key": key
                })
                common.log(f'continued with order {key}')
            else:
                item["returned"].append({
                    "key": key
                })
                common.log(f'returned with order {key}')
    values = list(items.values())
    values = sorted(values, key=lambda x: x['sort'])
    return values


def get_items(cat_id):
    payload = common.item_json
    payload = payload.replace("${value}", cat_id)
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    print(response)
    json_data = response.json()
    listData = json_data.get("data")
    res = []
    for d in listData:
        item = convert_item_data(d)
        res.append(item)
    res = sorted(res, key=lambda x: x['sort'])
    return res


def get_orders():
    payload = json.dumps({
        "appId": "67f7b5e44bb87e55f5a8c699",
        "entryId": "67f7b5e741db931a0b8c63fa",
        "filter": {
            "cond": [
                {
                    "type": "text",
                    "method": "ne",
                    "value": [
                        "完成"
                    ],
                    "entryId": "67f7b5e741db931a0b8c63fa",
                    "field": "_widget_1744287207908"
                }
            ],
            "rel": "and"
        },
        "skip": 0,
        "fields": [
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "name": "label",
                "type": "text",
                "text": "标题"
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "描述",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1763770854820",
                "type": "textarea"
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "来源",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1744287760630",
                "type": "combo",
                "colorEnable": False,
                "items": [
                    {
                        "value": "闲鱼【一眼风华】",
                        "text": "闲鱼【一眼风华】"
                    },
                    {
                        "value": "闲鱼【南柚记】",
                        "text": "闲鱼【南柚记】"
                    }
                ]
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "用户名",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1744287207906",
                "type": "text"
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "使用日期",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1744287207902",
                "type": "datetime",
                "format": "yyyy-MM-dd"
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "锁期",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1747105154404",
                "type": "number",
                "precision": None,
                "displayMode": "number",
                "thousandsSeparator": False
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "关联衣物",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1746403048270",
                "type": "combo",
                "colorEnable": False,
                "async": {
                    "data": {
                        "formId": "6814c756e30726893512cd7f",
                        "field": "_widget_1746242293714"
                    }
                }
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "备注",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1744287207912",
                "type": "textarea"
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "衣物",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1744287207916",
                "type": "text"
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "衣物图片",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1744287207917",
                "type": "image",
                "showStyle": "card"
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "帽子",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1746341421477",
                "type": "combo",
                "colorEnable": False,
                "async": {
                    "data": {
                        "formId": "68158a05eb085d16c79f45cd",
                        "field": "_widget_1746242055521"
                    }
                }
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "帽子图片",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1746341421482",
                "type": "image",
                "showStyle": "card"
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "学士服",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1746976016884",
                "type": "radiogroup",
                "colorEnable": False,
                "items": [
                    {
                        "value": "学士服",
                        "text": "学士服"
                    },
                    {
                        "value": "硕士服",
                        "text": "硕士服"
                    },
                    {
                        "value": "不需要",
                        "text": "不需要",
                        "color": "#46C26F"
                    }
                ]
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "垂布颜色",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1746976016891",
                "type": "combo",
                "colorEnable": False,
                "items": [
                    {
                        "value": "粉领",
                        "text": "粉领",
                        "selected": True
                    },
                    {
                        "value": "黄领",
                        "text": "黄领",
                        "selected": False
                    },
                    {
                        "value": "灰领",
                        "text": "灰领",
                        "selected": False
                    },
                    {
                        "value": "白领",
                        "text": "白领",
                        "color": "#A2C204",
                        "selected": False
                    },
                    {
                        "value": "绿领",
                        "text": "绿领",
                        "color": "#00AED1",
                        "selected": False
                    }
                ]
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "地址",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1744287207903",
                "type": "address",
                "needDetail": True
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "实收",
                "labelHidden": False,
                "lineWidth": 4,
                "name": "_widget_1744287207918",
                "type": "number",
                "precision": None,
                "displayMode": "number",
                "thousandsSeparator": False
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "运费",
                "labelHidden": False,
                "lineWidth": 4,
                "name": "_widget_1744287207907",
                "type": "number",
                "precision": None,
                "displayMode": "number",
                "thousandsSeparator": False
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "获利",
                "labelHidden": False,
                "lineWidth": 4,
                "name": "_widget_1744287207919",
                "type": "number",
                "precision": None,
                "displayMode": "number",
                "thousandsSeparator": False
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "状态",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1744287207908",
                "type": "combo",
                "colorEnable": False,
                "items": [
                    {
                        "value": "待发货",
                        "text": "待发货",
                        "selected": True
                    },
                    {
                        "value": "已发货",
                        "text": "已发货",
                        "selected": False
                    },
                    {
                        "value": "完成",
                        "text": "完成",
                        "selected": False
                    }
                ]
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "text": "寄出单号",
                "labelHidden": False,
                "lineWidth": 12,
                "name": "_widget_1744287760627",
                "type": "text"
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "name": "creator",
                "type": "user",
                "text": "提交人"
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "name": "createTime",
                "type": "datetime",
                "format": "yyyy-MM-dd HH:mm:ss",
                "text": "提交时间"
            },
            {
                "id": "67f7b5e741db931a0b8c63fa",
                "form": "67f7b5e741db931a0b8c63fa",
                "name": "updateTime",
                "type": "datetime",
                "format": "yyyy-MM-dd HH:mm:ss",
                "text": "更新时间"
            }
        ],
        "limit": 20,
        "sort": []
    })
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    json_data = response.json()
    listData = json_data.get("data")
    res = []
    for data in listData:
        useDay = data['_widget_1744287207902']
        dt = datetime.strptime(useDay, "%Y-%m-%dT%H:%M:%S.%fZ")
        dt = dt + timedelta(hours=8)
        formatted = dt.strftime("%y%m%d")
        useDay = int(formatted)
        province = data['_widget_1744287207903']['province']
        lockDayNums = data.get('_widget_1747105154404')
        if lockDayNums is None:
            lockDayNums = common.lockDayMap.get(province)
            if lockDayNums is None:
                lockDayNums = 3
        lockDay = common.generate_date_range(useDay, lockDayNums)
        itemName = data.get('_widget_1746403048270')
        itemTag = data.get('_widget_1746403048270')
        hatItem = data.get('_widget_1746341421477')
        user = f'{data["_widget_1744287207906"]}'
        item = {
            "orderId": data["_id"],
            "source": f'{data["_widget_1744287760630"]}',
            "user": user,
            "useDay": useDay,
            "province": province,
            "mask": '',
            "lockDay": lockDay,
            "itemName": itemName,
            "itemTag": itemTag,
            "hatItem": hatItem,
            "size": "M"
        }
        res.append(item)
        common.log(f'order信息 ->{itemName}, {province} , {user} , {useDay} , 锁{2 * lockDayNums + 1}天')
    return res


@app.route('/api/item_detail', methods=['GET'])
def item_detail():
    id = request.args.get('id')
    date = request.args.get('date')
    province = request.args.get('province')
    city = request.args.get('city')
    size = request.args.get('size')
    payload = common.item_detail_json
    payload = payload.replace("${value}", id)

    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    json_data = response.json()
    listData = json_data.get("data")
    res = []
    if len(listData) > 0:
        dd = listData[0]
        if "_widget_1765528377780" in dd:
            hat_cat = dd["_widget_1765528377780"]
            hat_payload = common.hat_detail_json
            hat_payload = hat_payload.replace("${value}", hat_cat)
            hat_response = requests.request("POST", url, headers=headers, data=hat_payload.encode("utf-8"))
            hat_json_data = hat_response.json()
            hat_listData = hat_json_data.get("data")
            for xs in hat_listData:
                item = {
                    "id": xs['_widget_1746342147352'],
                    "url": xs['_widget_1746242055522'][0]["previewUrl"],
                    "title": xs['_widget_1746242055521'],
                    "text": hat_cat,
                    "total_stock": 1,
                    "idle_stock": 1,
                    "sort": xs.get("_widget_1765875090525", 100)
                }
                if "_widget_1765864554528" in xs:
                    item["total_stock"] = xs["_widget_1765864554528"]
                    item["idle_stock"] = xs["_widget_1765864554528"]
                item["continued"] = []
                item["returned"] = []
                item["conflicted"] = []
                res.append(item)
            if date is None:
                return jsonify(res)
            else:
                date = date.replace("-", "")
                date = date[2:]
                lock_nums = common.lockDayMap.get(province)
                if lock_nums is None:
                    lock_nums = 3
                try_lock_days = common.generate_date_range(date, lock_nums)
                tmp_res = get_useful_hats(res, date, try_lock_days)
                res = []
                for tmp in tmp_res:
                    if tmp["idle_stock"] > 0:
                        res.append(tmp)
                return jsonify(res)
        else:
            res = load_ma(dd)
            return jsonify(res)


def get_useful_hats(hat_list, use_day, try_lock_days):
    orders = get_orders()
    hat_map = {}
    for h in hat_list:
        hat_map[f"{h['title']}"] = h
    for order in orders:
        if "hatItem" in order:
            hat_title = order["hatItem"]
            if hat_title in hat_map:
                hat = hat_map[f"{hat_title}"]
                locked_days = order["lockDay"]
                intersection = list(set(try_lock_days) & set(locked_days))
                if len(intersection) > 0:
                    hat["idle_stock"] = hat["idle_stock"] - 1
                    key = f'{order["user"]}_{order["province"]}_{order["useDay"]}'
                    hat["conflicted"].append({
                        "key": key
                    })
                else:
                    key = f'{order["user"]}_{order["province"]}_{order["useDay"]}'
                    if int(use_day) < int(order["useDay"]):
                        hat["continued"].append({
                            "key": key
                        })
                        common.log(f'continued with order {key}')
                    else:
                        hat["returned"].append({
                            "key": key
                        })
                        common.log(f'returned with order {key}')
    values = list(hat_map.values())
    values = sorted(values, key=lambda x: x['sort'])
    return values


def load_ma(dd):
    res = []
    for d in dd["_widget_1746192214992"]:
        item = {
            "id": dd["_widget_1763770024462"],
            "url": d["previewUrl"],
            "title": dd.get("_widget_1746242293714", ""),
            "text": dd.get("_widget_1763770891928", dd.get("_widget_1746242293714", ""))
        }
        res.append(item)
    return res


def convert_hat_data(item):
    res = {
        "id": item["_widget_1763770024462"],
        "name": item["_widget_1746242293714"],
        "img": item["_widget_1746192214992"][0]["previewUrl"],
        "sort": item["_widget_1763793130332"],
        "conflicted": [],
        "continued": [],
        "returned": [],
        "zujin": 0,
        "yajin": 0,
        "desc": f"{item['name']},租金{item['zujin']},押金{item['yajin']}",
        "nums": {
            "total_stock": 0,
            "idle_stock": 0
        }
    }
    return res


def get_all_itemss(cat_id):
    payload = json.dumps()
    payload = payload.replace("${value}", cat_id)
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    json_data = response.json()
    listData = json_data.get("data")


def convert_item_data(item):
    res = {
        "id": item["_widget_1763770024462"],
        "name": item["_widget_1746242293714"],
        "img": item.get("_widget_1746192214992", [{"previewUrl": ""}])[0]["previewUrl"],
        "sort": item["_widget_1763793130332"],
        "conflicted": [],
        "continued": [],
        "returned": [],
        "zujin": item.get("_widget_1748412001178", 0),
        "yajin": item.get("_widget_1748412001179", 0),
        "nums": {
            "total_stock": 1,
            "idle_stock": 1
        },
        "nums_S": {
            "total_stock": 0,
            "idle_stock": 0
        },
        "nums_M": {
            "total_stock": 0,
            "idle_stock": 0
        },
        "nums_L": {
            "total_stock": 0,
            "idle_stock": 0
        },
    }
    res["desc"] = f"{res['name']},租金{res['zujin']},押金{res['yajin']}",
    if "_widget_1765781927469" in item:
        total = 0
        for st in item["_widget_1765781927469"]:
            flag = st["_widget_1765781927471"]
            v = st["_widget_1765781927473"]
            if flag == 'S':
                res["nums_S"] = {
                    "total_stock": v,
                    "idle_stock": v
                }
            elif flag == 'M':
                res["nums_M"] = {
                    "total_stock": v,
                    "idle_stock": v
                }
            elif flag == 'L':
                res["nums_L"] = {
                    "total_stock": v,
                    "idle_stock": v
                }
            total = total + v
        res["nums"] = {
            "total_stock": total,
            "idle_stock": total
        }
    return res


if __name__ == '__main__':
    print(1111)
    app.run(host='0.0.0.0', port=5000)
