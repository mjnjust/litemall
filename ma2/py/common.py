import re
from pypinyin import lazy_pinyin
import logging
from datetime import datetime, timedelta
def read_file_to_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

lockDayMap = {
    "江苏省": 2,
    "上海市": 2,
    "浙江省": 2,
    "安徽省": 2,
    "山东省": 2,
    "北京市": 3,
    "天津市": 3,
    "河北省": 3,
    "山西省": 3,
    "福建省": 3,
    "江西省": 3,
    "河南省": 3,
    "湖北省": 3,
    "湖南省": 3,
    "广东省": 3,
    "广西省": 3,
    "重庆市": 3,
    "四川省": 3,
    "贵州省": 3,
    "云南省": 3,
    "陕西省": 3,
    "辽宁省": 3,
    "吉林省": 3,
    "黑龙江省": 4
}
num_mapping = {
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
    '十': 10,
}

item_json = read_file_to_string("item.json")
category_json = read_file_to_string("category.json")
item_detail_json = read_file_to_string("item_detail.json")
hat_detail_json = read_file_to_string("hat_detail.json")

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', filename='my_log.log')

# 中文数字到阿拉伯数字的映射表
CHINESE_NUM_MAP1 = {
    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
}
CHINESE_NUM_MAP2 = {
    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 0
}


def chinese_num_to_arabic(chinese_num):
    """将中文数字转换为阿拉伯数字（直接拼接模式）"""
    num_str = ''
    if len(chinese_num) == 1:
        for char in chinese_num:
            num_str += str(CHINESE_NUM_MAP1.get(char, 0))
        return int(num_str) if num_str else 0
    elif len(chinese_num) == 2:
        if chinese_num.startswith("十"):
            return 10 + int(CHINESE_NUM_MAP2.get(chinese_num[1]))
        else:
            for char in chinese_num:
                num_str += str(CHINESE_NUM_MAP2.get(char, 0))
            return int(num_str) if num_str else 0
    else:
        return 100


def log(message):
    """Logs a message with timestamp and level."""
    logging.error(message)
    print(message)


def generate_date_range(yymmdd: int, delta: int):
    # 将输入的YYMMDD格式转换为字符串，然后转换为日期对象
    date_str = str(yymmdd)
    base_date = datetime.strptime(date_str, "%y%m%d")

    # 生成日期范围
    date_range = []
    for i in range(-delta, delta + 1):
        new_date = base_date + timedelta(days=i)
        date_range.append(new_date.strftime("%y%m%d"))

    return date_range


def isoTZtoYYMMDD(isoDate):
    useDay = isoDate
    dt = datetime.strptime(useDay, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt + timedelta(hours=8)

    formatted = dt.strftime("%y%m%d")
    useDay = int(formatted)
    return useDay