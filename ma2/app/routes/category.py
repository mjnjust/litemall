import json

from flask import Blueprint, request, jsonify

category_bp = Blueprint('ca', __name__)

cat_payload="{\r\n    \"errno\": 0,\r\n    \"data\": {\r\n        \"currentCategory\": {\r\n            \"id\": 1005001,\r\n            \"name\": \"餐厨\",\r\n            \"keywords\": \"\",\r\n            \"desc\": \"爱，囿于厨房\",\r\n            \"pid\": 0,\r\n            \"iconUrl\": \"http://yanxuan.nosdn.127.net/ad8b00d084cb7d0958998edb5fee9c0a.png\",\r\n            \"picUrl\": \"http://yanxuan.nosdn.127.net/3708dbcb35ad5abf9e001500f73db615.png\",\r\n            \"level\": \"L1\",\r\n            \"sortOrder\": 3,\r\n            \"addTime\": \"2018-02-01 00:00:00\",\r\n            \"updateTime\": \"2018-02-01 00:00:00\",\r\n            \"deleted\": false\r\n        },\r\n        \"categoryList\": [\r\n            {\r\n                \"id\": 1005000,\r\n                \"name\": \"居家\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"回家，放松身心\",\r\n                \"pid\": 0,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/a45c2c262a476fea0b9fc684fed91ef5.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/e8bf0cf08cf7eda21606ab191762e35c.png\",\r\n                \"level\": \"L1\",\r\n                \"sortOrder\": 2,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1005001,\r\n                \"name\": \"餐厨\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"爱，囿于厨房\",\r\n                \"pid\": 0,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/ad8b00d084cb7d0958998edb5fee9c0a.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/3708dbcb35ad5abf9e001500f73db615.png\",\r\n                \"level\": \"L1\",\r\n                \"sortOrder\": 3,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1005002,\r\n                \"name\": \"饮食\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"好吃，高颜值美食\",\r\n                \"pid\": 0,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/c9280327a3fd2374c000f6bf52dff6eb.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/fb670ff3511182833e5b035275e4ac09.png\",\r\n                \"level\": \"L1\",\r\n                \"sortOrder\": 9,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1008000,\r\n                \"name\": \"配件\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"配角，亦是主角\",\r\n                \"pid\": 0,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/11abb11c4cfdee59abfb6d16caca4c6a.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/02f9a44d05c05c0dd439a5eb674570a2.png\",\r\n                \"level\": \"L1\",\r\n                \"sortOrder\": 4,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1010000,\r\n                \"name\": \"服装\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"贴身的，要亲肤\",\r\n                \"pid\": 0,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/28a685c96f91584e7e4876f1397767db.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/622c8d79292154017b0cbda97588a0d7.png\",\r\n                \"level\": \"L1\",\r\n                \"sortOrder\": 5,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1011000,\r\n                \"name\": \"婴童\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"爱，从心开始\",\r\n                \"pid\": 0,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/1ba9967b8de1ac50fad21774a4494f5d.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/9cc0b3e0d5a4f4a22134c170f10b70f2.png\",\r\n                \"level\": \"L1\",\r\n                \"sortOrder\": 7,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1012000,\r\n                \"name\": \"杂货\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"解忧，每个烦恼\",\r\n                \"pid\": 0,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/c2a3d6349e72c35931fe3b5bcd0966be.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/547853361d29a37282f377b9a755dd37.png\",\r\n                \"level\": \"L1\",\r\n                \"sortOrder\": 8,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1013001,\r\n                \"name\": \"洗护\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"亲肤之物，严选天然\",\r\n                \"pid\": 0,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/9fe068776b6b1fca13053d68e9c0a83f.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/1526ab0f5982722adbc8726f9f2a338c.png\",\r\n                \"level\": \"L1\",\r\n                \"sortOrder\": 6,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1019000,\r\n                \"name\": \"志趣\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"周边精品，共享热爱\",\r\n                \"pid\": 0,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/7093cfecb9dde1dd3eaf459623df4071.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/1706e24a5e605870ba3b37ff5f49aa18.png\",\r\n                \"level\": \"L1\",\r\n                \"sortOrder\": 10,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            }\r\n        ],\r\n        \"currentSubCategory\": [\r\n            {\r\n                \"id\": 1005007,\r\n                \"name\": \"锅具\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"一口好锅，炖煮生活一日三餐\",\r\n                \"pid\": 1005001,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/4aab4598017b5749e3b63309d25e9f6b.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/d2db0d1d0622c621a8aa5a7c06b0fc6d.png\",\r\n                \"level\": \"L2\",\r\n                \"sortOrder\": 1,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1005008,\r\n                \"name\": \"餐具\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"餐桌上的舞蹈\",\r\n                \"pid\": 1005001,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/f109afbb7e7a00c243c1da29991a5aa3.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/695ed861a63d8c0fc51a51f42a5a993b.png\",\r\n                \"level\": \"L2\",\r\n                \"sortOrder\": 4,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1005009,\r\n                \"name\": \"清洁\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"环保便利，聪明之选\",\r\n                \"pid\": 1005001,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/e8b67fe8b8db2ecc2e126a0aa631def0.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/3a40faaef0a52627357d98ceed7a3c45.png\",\r\n                \"level\": \"L2\",\r\n                \"sortOrder\": 9,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1007000,\r\n                \"name\": \"杯壶\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"精工生产制作，匠人手艺\",\r\n                \"pid\": 1005001,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/0b244d3575b737c8f0ed7e84c5c4abd2.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/ec53828a3814171079178a59fb2593da.png\",\r\n                \"level\": \"L2\",\r\n                \"sortOrder\": 2,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1008011,\r\n                \"name\": \"清洁保鲜\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"真空保鲜，美味不限时\",\r\n                \"pid\": 1005001,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/dc4d6c35b9f4abb42d2eeaf345710589.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/04cd632e1589adcc4345e40e8ad75d2b.png\",\r\n                \"level\": \"L2\",\r\n                \"sortOrder\": 6,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1008012,\r\n                \"name\": \"功能厨具\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"下厨省力小帮手\",\r\n                \"pid\": 1005001,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/22db4ccbf52dc62c723ac83aa587812a.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/5b94463017437467a93ae4af17c2ba4f.png\",\r\n                \"level\": \"L2\",\r\n                \"sortOrder\": 3,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1008013,\r\n                \"name\": \"茶具咖啡具\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"先进工艺制造，功夫体验\",\r\n                \"pid\": 1005001,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/9ea192cd2719c8348f42ec17842ba763.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/be3ba4056e274e311d1c23bd2931018d.png\",\r\n                \"level\": \"L2\",\r\n                \"sortOrder\": 5,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1013005,\r\n                \"name\": \"刀剪砧板\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"传统工艺 源自中国刀城\",\r\n                \"pid\": 1005001,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/9d481ea4c2e9e6eda35aa720d407332e.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/555afbfe05dab48c1a3b90dcaf89b4f2.png\",\r\n                \"level\": \"L2\",\r\n                \"sortOrder\": 7,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            },\r\n            {\r\n                \"id\": 1023000,\r\n                \"name\": \"厨房小电\",\r\n                \"keywords\": \"\",\r\n                \"desc\": \"厨房里的省心小电器\",\r\n                \"pid\": 1005001,\r\n                \"iconUrl\": \"http://yanxuan.nosdn.127.net/521bd0c02d283b80ba49e73ca84df250.png\",\r\n                \"picUrl\": \"http://yanxuan.nosdn.127.net/c09d784ba592e4fadabbaef6b2e95a95.png\",\r\n                \"level\": \"L2\",\r\n                \"sortOrder\": 8,\r\n                \"addTime\": \"2018-02-01 00:00:00\",\r\n                \"updateTime\": \"2018-02-01 00:00:00\",\r\n                \"deleted\": false\r\n            }\r\n        ]\r\n    },\r\n    \"errmsg\": \"成功\"\r\n}"
home_payload='''
{
    "errno": 0,
    "data": {
        "newGoodsList": [
            {
                "id": 1181000,
                "name": "母亲节礼物-舒适安睡组合",
                "brief": "安心舒适是最好的礼物",
                "picUrl": "http://yanxuan.nosdn.127.net/1f67b1970ee20fd572b7202da0ff705d.png",
                "isNew": true,
                "isHot": false,
                "counterPrice": 2618.00,
                "retailPrice": 2598.00
            },
            {
                "id": 1116011,
                "name": "蔓越莓曲奇 200克",
                "brief": "酥脆奶香，甜酸回味",
                "picUrl": "http://yanxuan.nosdn.127.net/767b370d07f3973500db54900bcbd2a7.png",
                "isNew": true,
                "isHot": true,
                "counterPrice": 56.00,
                "retailPrice": 36.00
            },
            {
                "id": 1127047,
                "name": "趣味粉彩系列笔记本",
                "brief": "粉彩色泽，记录生活",
                "picUrl": "http://yanxuan.nosdn.127.net/6c03ca93d8fe404faa266ea86f3f1e43.png",
                "isNew": true,
                "isHot": false,
                "counterPrice": 49.00,
                "retailPrice": 29.00
            },
            {
                "id": 1135002,
                "name": "宫廷奢华真丝四件套",
                "brief": "100%桑蚕丝，丝滑润肤",
                "picUrl": "http://yanxuan.nosdn.127.net/45548f26cfd0c7c41e0afc3709d48286.png",
                "isNew": true,
                "isHot": false,
                "counterPrice": 2619.00,
                "retailPrice": 2599.00
            },
            {
                "id": 1152161,
                "name": "竹语丝麻印花四件套",
                "brief": "3重透气，清爽柔滑",
                "picUrl": "http://yanxuan.nosdn.127.net/977401e75113f7c8334c4fb5b4bf6215.png",
                "isNew": true,
                "isHot": false,
                "counterPrice": 479.00,
                "retailPrice": 459.00
            },
            {
                "id": 1166008,
                "name": "Carat钻石 不粘厨具组合",
                "brief": "钻石涂层，不粘锅锅具组",
                "picUrl": "http://yanxuan.nosdn.127.net/615a16e899e01efb780c488df4233f48.png",
                "isNew": true,
                "isHot": false,
                "counterPrice": 479.00,
                "retailPrice": 459.00
            }
        ],
        "couponList": [
            {
                "id": 1,
                "name": "限时满减券",
                "desc": "全场通用",
                "tag": "无限制",
                "discount": 5.00,
                "min": 99.00,
                "days": 10
            },
            {
                "id": 2,
                "name": "限时满减券",
                "desc": "全场通用",
                "tag": "无限制",
                "discount": 10.00,
                "min": 99.00,
                "days": 10
            }
        ],
        "channel": [
            {
                "id": 1005000,
                "name": "居家",
                "iconUrl": "http://yanxuan.nosdn.127.net/a45c2c262a476fea0b9fc684fed91ef5.png"
            },
            {
                "id": 1005001,
                "name": "餐厨",
                "iconUrl": "http://yanxuan.nosdn.127.net/ad8b00d084cb7d0958998edb5fee9c0a.png"
            },
            {
                "id": 1005002,
                "name": "饮食",
                "iconUrl": "http://yanxuan.nosdn.127.net/c9280327a3fd2374c000f6bf52dff6eb.png"
            },
            {
                "id": 1008000,
                "name": "配件",
                "iconUrl": "http://yanxuan.nosdn.127.net/11abb11c4cfdee59abfb6d16caca4c6a.png"
            },
            {
                "id": 1010000,
                "name": "服装",
                "iconUrl": "http://yanxuan.nosdn.127.net/28a685c96f91584e7e4876f1397767db.png"
            },
            {
                "id": 1011000,
                "name": "婴童",
                "iconUrl": "http://yanxuan.nosdn.127.net/1ba9967b8de1ac50fad21774a4494f5d.png"
            },
            {
                "id": 1012000,
                "name": "杂货",
                "iconUrl": "http://yanxuan.nosdn.127.net/c2a3d6349e72c35931fe3b5bcd0966be.png"
            },
            {
                "id": 1013001,
                "name": "洗护",
                "iconUrl": "http://yanxuan.nosdn.127.net/9fe068776b6b1fca13053d68e9c0a83f.png"
            },
            {
                "id": 1019000,
                "name": "志趣",
                "iconUrl": "http://yanxuan.nosdn.127.net/7093cfecb9dde1dd3eaf459623df4071.png"
            }
        ],
        "grouponList": [],
        "banner": [],
        "brandList": [
            {
                "id": 1001000,
                "name": "MUJI制造商",
                "desc": "严选精选了MUJI制造商和生产原料，n用几乎零利润的价格，剔除品牌溢价，n让用户享受原品牌的品质生活。",
                "picUrl": "http://yanxuan.nosdn.127.net/1541445967645114dd75f6b0edc4762d.png",
                "floorPrice": 12.90
            },
            {
                "id": 1001002,
                "name": "内野制造商",
                "desc": "严选从世界各地挑选毛巾，最终选择了为日本内野代工的工厂，追求毛巾的柔软度与功能性。品质比肩商场几百元的毛巾。",
                "picUrl": "http://yanxuan.nosdn.127.net/8ca3ce091504f8aa1fba3fdbb7a6e351.png",
                "floorPrice": 29.00
            },
            {
                "id": 1001003,
                "name": "Adidas制造商",
                "desc": "严选找到为Adidas等品牌制造商，n选取优质原材料，与厂方一起设计，n为你提供好的理想的运动装备。",
                "picUrl": "http://yanxuan.nosdn.127.net/335334d0deaff6dc3376334822ab3a2f.png",
                "floorPrice": 49.00
            },
            {
                "id": 1001007,
                "name": "优衣库制造商",
                "desc": "严选找到日本知名服装UNIQLO的制造商，n选取优质长绒棉和精梳工艺，n与厂方一起设计，为你提供理想的棉袜。",
                "picUrl": "http://yanxuan.nosdn.127.net/0d72832e37e7e3ea391b519abbbc95a3.png",
                "floorPrice": 29.00
            }
        ],
        "hotGoodsList": [
            {
                "id": 1152008,
                "name": "魔兽世界 部落 护腕 一只",
                "brief": "吸汗、舒适、弹性、防护、耐用",
                "picUrl": "http://yanxuan.nosdn.127.net/203cb83d93606865e3ddde57b69b9e9a.png",
                "isNew": false,
                "isHot": true,
                "counterPrice": 49.00,
                "retailPrice": 29.00
            },
            {
                "id": 1152009,
                "name": "魔兽世界 联盟 护腕 一只",
                "brief": "吸汗、舒适、弹性、防护、耐用",
                "picUrl": "http://yanxuan.nosdn.127.net/ae6d41117717387b82dcaf1dfce0cd97.png",
                "isNew": false,
                "isHot": true,
                "counterPrice": 49.00,
                "retailPrice": 29.00
            },
            {
                "id": 1152031,
                "name": "魔兽世界-伊利丹颈枕眼罩套装",
                "brief": "差旅好伴侣",
                "picUrl": "http://yanxuan.nosdn.127.net/fd6e78a397bd9e9804116a36f0270b0a.png",
                "isNew": false,
                "isHot": true,
                "counterPrice": 119.00,
                "retailPrice": 99.00
            },
            {
                "id": 1022000,
                "name": "意式毛线绣球四件套",
                "brief": "浪漫毛线绣球，简约而不简单",
                "picUrl": "http://yanxuan.nosdn.127.net/5350e35e6f22165f38928f3c2c52ac57.png",
                "isNew": false,
                "isHot": true,
                "counterPrice": 319.00,
                "retailPrice": 299.00
            },
            {
                "id": 1011004,
                "name": "色织精梳AB纱格纹空调被",
                "brief": "加大加厚，双色精彩",
                "picUrl": "http://yanxuan.nosdn.127.net/0984c9388a2c3fd2335779da904be393.png",
                "isNew": false,
                "isHot": true,
                "counterPrice": 219.00,
                "retailPrice": 199.00
            },
            {
                "id": 1084003,
                "name": "纯棉美式绞花针织盖毯",
                "brief": "美式提花，温暖舒适",
                "picUrl": "http://yanxuan.nosdn.127.net/cf40c167e7054fe184d49f19121f63c7.png",
                "isNew": false,
                "isHot": true,
                "counterPrice": 219.00,
                "retailPrice": 199.00
            }
        ],
        "topicList": [
            {
                "id": 264,
                "title": "设计师们推荐的应季好物",
                "subtitle": "原创设计春款系列上新",
                "price": 29.90,
                "readCount": "77.7k",
                "picUrl": "https://yanxuan.nosdn.127.net/14918201901050274.jpg"
            },
            {
                "id": 266,
                "title": "一条丝巾就能提升时髦度",
                "subtitle": "不知道大家对去年G20时，严选与国礼制造商一起推出的《凤凰于飞》等几款丝巾是否还...",
                "price": 0.00,
                "readCount": "35.0k",
                "picUrl": "https://yanxuan.nosdn.127.net/14919007135160213.jpg"
            },
            {
                "id": 268,
                "title": "米饭好吃的秘诀：会呼吸的锅",
                "subtitle": "今年1月份，我们联系到了日本伊贺地区的长谷园，那里有着180年伊贺烧历史的窑厂。...",
                "price": 0.00,
                "readCount": "33.3k",
                "picUrl": "https://yanxuan.nosdn.127.net/14920623353130483.jpg"
            },
            {
                "id": 271,
                "title": "选式新懒人",
                "subtitle": "懒出格调，懒出好生活。",
                "price": 15.00,
                "readCount": "57.7k",
                "picUrl": "https://yanxuan.nosdn.127.net/14924199099661697.jpg"
            }
        ],
        "floorGoodsList": [
            {
                "name": "居家",
                "goodsList": [
                    {
                        "id": 1110016,
                        "name": "天然硅胶宠物除毛按摩刷",
                        "brief": "顺滑平面，猫狗通用，去除死毛",
                        "picUrl": "http://yanxuan.nosdn.127.net/3bd73b7279a83d1cbb50c0e45778e6d6.png",
                        "isNew": false,
                        "isHot": false,
                        "counterPrice": 59.00,
                        "retailPrice": 39.00
                    },
                    {
                        "id": 1110017,
                        "name": "耐用材料猫咪护理清洁套装",
                        "brief": "精致钢材，美容清洁",
                        "picUrl": "http://yanxuan.nosdn.127.net/534231583f82572398ec84bad425cdaf.png",
                        "isNew": false,
                        "isHot": false,
                        "counterPrice": 99.00,
                        "retailPrice": 79.00
                    },
                    {
                        "id": 1110018,
                        "name": "耐用狗狗清洁美容护理套装",
                        "brief": "精致钢材，耐咬美容",
                        "picUrl": "http://yanxuan.nosdn.127.net/d93aa5d6e7a296101cf4cb72613aeda6.png",
                        "isNew": false,
                        "isHot": false,
                        "counterPrice": 99.00,
                        "retailPrice": 79.00
                    },
                    {
                        "id": 1110019,
                        "name": "宠物合金钢安全除菌指甲护理组合",
                        "brief": "猫狗皆可用，保护家具",
                        "picUrl": "http://yanxuan.nosdn.127.net/1e7e392b6fc9da99dc112197b7444eec.png",
                        "isNew": false,
                        "isHot": false,
                        "counterPrice": 89.00,
                        "retailPrice": 69.00
                    }
                ],
                "id": 1005000
            },
            {
                "name": "餐厨",
                "goodsList": [
                    {
                        "id": 1023003,
                        "name": "100年传世珐琅锅 全家系列",
                        "brief": "特质铸铁，大容量全家共享",
                        "picUrl": "http://yanxuan.nosdn.127.net/c39d54c06a71b4b61b6092a0d31f2335.png",
                        "isNew": false,
                        "isHot": false,
                        "counterPrice": 418.00,
                        "retailPrice": 398.00
                    },
                    {
                        "id": 1073008,
                        "name": "铸铁珐琅牛排煎锅",
                        "brief": "沥油隔水，煎出外焦里嫩",
                        "picUrl": "http://yanxuan.nosdn.127.net/619e46411ccd62e5c0f16692ee1a85a0.png",
                        "isNew": false,
                        "isHot": false,
                        "counterPrice": 169.00,
                        "retailPrice": 149.00
                    },
                    {
                        "id": 1051000,
                        "name": "Carat钻石炒锅30cm",
                        "brief": "安全涂层，轻便无烟",
                        "picUrl": "http://yanxuan.nosdn.127.net/e564410546a11ddceb5a82bfce8da43d.png",
                        "isNew": false,
                        "isHot": false,
                        "counterPrice": 200.00,
                        "retailPrice": 180.00
                    },
                    {
                        "id": 1051001,
                        "name": "Carat钻石煎锅28cm",
                        "brief": "耐磨涂层，导热迅速",
                        "picUrl": "http://yanxuan.nosdn.127.net/f53ed57d9e23fda7e24dfd0e0a50c5d1.png",
                        "isNew": false,
                        "isHot": false,
                        "counterPrice": 179.00,
                        "retailPrice": 159.00
                    }
                ],
                "id": 1005001
            },
            {
                "name": "饮食",
                "goodsList": [
                    {
                        "id": 1045000,
                        "name": "绿茶蛋黄酥 200克/4枚入",
                        "brief": "香甜茶食，果腹优选",
                        "picUrl": "http://yanxuan.nosdn.127.net/b2adc3fd9b84a289a1be03e8ee400e61.png",
                        "isNew": false,
                        "isHot": false,
                        "counterPrice": 48.00,
                        "retailPrice": 28.00
                    },
                    {
                        "id": 1116011,
                        "name": "蔓越莓曲奇 200克",
                        "brief": "酥脆奶香，甜酸回味",
                        "picUrl": "http://yanxuan.nosdn.127.net/767b370d07f3973500db54900bcbd2a7.png",
                        "isNew": true,
                        "isHot": true,
                        "counterPrice": 56.00,
                        "retailPrice": 36.00
                    },
                    {
                        "id": 1070000,
                        "name": "星云酥 180克/3颗",
                        "brief": "酥饼界的小仙女",
                        "picUrl": "http://yanxuan.nosdn.127.net/8392725765cdd57fdae3f173877f4bda.png",
                        "isNew": false,
                        "isHot": false,
                        "counterPrice": 46.00,
                        "retailPrice": 26.00
                    },
                    {
                        "id": 1155015,
                        "name": "绿豆糕 80克（4枚入）",
                        "brief": "细腻松软，入口绵柔",
                        "picUrl": "http://yanxuan.nosdn.127.net/66b9f1638c0517d179262f14ed1345f9.png",
                        "isNew": true,
                        "isHot": false,
                        "counterPrice": 32.90,
                        "retailPrice": 12.90
                    }
                ],
                "id": 1005002
            },
            {
                "name": "配件",
                "goodsList": [
                    {
                        "id": 1085019,
                        "name": "20寸 纯PC“铝框”（非全铝）登机箱",
                        "brief": "铝质包角，牢固抗摔",
                        "picUrl": "http://yanxuan.nosdn.127.net/65c955a7a98e84d44ca30bb88a591eac.png",
                        "isNew": false,
                        "isHot": false,
                        "counterPrice": 369.00,
                        "retailPrice": 349.00
                    },
                    {
                        "id": 1086052,
                        "name": "20寸 铝镁合金登机箱",
                        "brief": "时尚金属箱，奢品质感",
                        "picUrl": "http://yanxuan.nosdn.127.net/93171a281c4ed272c007a050816e6f6c.png",
                        "isNew": false,
                        "isHot": false,
                        "counterPrice": 879.00,
                        "retailPrice": 859.00
                    },
                    {
                        "id": 1152101,
                        "name": "魔兽世界 部落 奥格瑞玛 拉杆箱 可登机",
                        "brief": "18寸，可携带登机",
                        "picUrl": "http://yanxuan.nosdn.127.net/c1c62211a17b71a634fa0c705d11fb42.png",
                        "isNew": false,
                        "isHot": true,
                        "counterPrice": 908.00,
                        "retailPrice": 888.00
                    },
                    {
                        "id": 1114011,
                        "name": "104升 纯PC拉链斜纹拉杆箱",
                        "brief": "104升的体积，90升的价格",
                        "picUrl": "http://yanxuan.nosdn.127.net/196b5ce11930b4eadaec563cb0406634.png",
                        "isNew": false,
                        "isHot": false,
                        "counterPrice": 319.00,
                        "retailPrice": 299.00
                    }
                ],
                "id": 1008000
            }
        ]
    },
    "errmsg": "成功"
}
'''
@category_bp.route('/catalog/index', methods=['GET'])
def get_items():
    return jsonify(json.loads(cat_payload))

@category_bp.route('/home/index', methods=['GET'])
def home_index():
    return jsonify(json.loads(home_payload))