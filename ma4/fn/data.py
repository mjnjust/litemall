from flask import Blueprint, request, jsonify
import json
import os
from flask import Flask, request, jsonify
from datetime import datetime
import requests
import re

data_bp = Blueprint('data', __name__, url_prefix='/fn')

DATA_FILE = 'data.json'

class TencentFinanceAPI:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.base_url = "http://qt.gtimg.cn/q="

    def get_stock_data(self, stock_codes):
        """
        获取股票实时数据
        stock_codes: 股票代码列表，如 ['sh600519', 'sz000001']
        """
        if isinstance(stock_codes, list):
            codes_str = ','.join(stock_codes)
        else:
            codes_str = stock_codes

        url = f"{self.base_url}{codes_str}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'gbk'  # 腾讯接口使用GBK编码
            data = response.text

            return self.parse_stock_data(data)
        except Exception as e:
            print(f"获取数据失败: {e}")
            return None

    def parse_stock_data(self, raw_data):
        """
        解析股票数据
        数据格式: v_sh600519="1~贵州茅台~600519~1675.00~...";
        """
        stocks = []

        # 分割每只股票的数据
        lines = raw_data.strip().split(';')

        for line in lines:
            if not line:
                continue

            # 提取数据部分
            match = re.search(r'="(.*)"', line)
            if not match:
                continue

            data_str = match.group(1)
            fields = data_str.split('~')

            if len(fields) < 49:  # 确保有足够字段
                continue

            # 解析主要字段（腾讯财经字段说明见下表）
            stock_info = {
                # 基础信息
                'code': fields[2],  # 股票代码
                'name': fields[1],  # 股票名称
                'current_price': fields[3],  # 当前价格

                # 今日行情
                'open_price': fields[5],  # 今开
                'close_price': fields[4],  # 昨收
                'high_price': fields[33],  # 最高
                'low_price': fields[34],  # 最低

                # 买卖盘
                'bid_price': fields[9],  # 买一价
                'bid_volume': fields[10],  # 买一量（手）
                'ask_price': fields[19],  # 卖一价
                'ask_volume': fields[20],  # 卖一量（手）

                # 成交信息
                'volume': fields[6],  # 成交量（手）
                'turnover': fields[37],  # 成交额（万）
                'time': fields[30],  # 时间

                # 涨跌信息
                'change': fields[31],  # 涨跌额
                'change_percent': fields[32],  # 涨跌幅%

                # 其他指标
                'pe_ratio': fields[39],  # 市盈率
                'pb_ratio': fields[46],  # 市净率
                'total_market_cap': fields[45],  # 总市值
                'circulation_market_cap': fields[44],  # 流通市值
                'turnover_rate': fields[38],  # 换手率

                # 涨跌停
                'limit_up': fields[47],  # 涨停价
                'limit_down': fields[48],  # 跌停价
            }

            stocks.append(stock_info)

        return stocks

    def get_fund_data(self, fund_codes):
        """
        获取基金数据
        fund_codes: 基金代码列表，如 ['of161725', 'of110022']
        """
        if isinstance(fund_codes, list):
            codes_str = ','.join(fund_codes)
        else:
            codes_str = fund_codes

        url = f"{self.base_url}{codes_str}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'gbk'
            data = response.text

            return self.parse_fund_data(data)
        except Exception as e:
            print(f"获取基金数据失败: {e}")
            return None

    def parse_fund_data(self, raw_data):
        """
        解析基金数据
        """
        funds = []
        lines = raw_data.strip().split(';')

        for line in lines:
            if not line:
                continue

            match = re.search(r'="(.*)"', line)
            if not match:
                continue

            data_str = match.group(1)
            fields = data_str.split('~')

            if len(fields) < 40:
                continue

            fund_info = {
                # 基础信息
                'code': fields[0],  # 基金代码
                'name': fields[1],  # 基金名称

                # 净值信息
                'net_value': fields[3],  # 最新净值
                'yesterday_value': fields[4],  # 昨收净值
                'change': fields[5],  # 涨跌额
                'change_percent': fields[6],  # 涨跌幅%

                # 时间
                'date': fields[2],  # 净值日期
                'time': fields[30],  # 更新时间

                # 估值信息（盘中实时）
                'estimated_value': fields[32],  # 估算净值
                'estimated_change_percent': fields[33],  # 估算涨跌幅%

                # 费率信息
                'purchase_rate': fields[20],  #
                'redemption_rate': fields[21],  #

                # 规模信息
                'total_net_assets': fields[23],  #

                # 其他
                'nav_date': fields[24],  #
                'this_year_return': fields[25],
            }

            funds.append(fund_info)

        return funds


def analyse(current_price, chengben_price, chengben_nums, target_lv):
    nums = 0
    while (True):
        current_chengben1 = chengben_price * chengben_nums
        current_chengben2 = float(current_price) * nums
        shouxufei = max(float(current_chengben2) * 0.0005, 5)
        chenben = current_chengben1 + current_chengben2 + shouxufei
        jiazhi = float(current_price) * (int(chengben_nums) + int(nums))
        lv = (jiazhi - chenben) / chenben
        if abs(lv) < target_lv:
            return {
                "current_price":current_price,
                "new_nums": nums,
                "new_chengben": current_chengben2
            }
        nums = nums + 100


def analyse_code(code, chengben_price, chengben_nums, target_lv):
    api = TencentFinanceAPI()
    stock = api.get_stock_data(code)
    current_price = stock[0]['current_price']
    res = analyse(current_price, chengben_price, chengben_nums, target_lv)
    shouyi = (float(current_price) - float(chengben_price))/float(chengben_price)*100
    shouyi = format(shouyi, ".3f")
    res['shouyi'] = shouyi
    res['name'] = stock[0]['name']
    return res

def load_data():
    """从文件加载数据"""
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_data(data):
    """保存数据到文件"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@data_bp.route('/api/record', methods=['POST'])
def record_data():
    """
    记录数据接口
    参数：
    - code: 唯一标识码 (必需)
    - chengben_price: 成本价格 (必需)
    - chengben_nums: 成本数量 (必需)
    """
    try:
        # 获取请求参数
        code = request.form.get('code')
        code = str(code)
        chengben_price = request.form.get('chengben_price')
        chengben_nums = request.form.get('chengben_nums')

        # 验证必需参数
        if not code:
            return jsonify({
                'status': 'error',
                'message': '参数code不能为空'
            }), 400

        if chengben_price is None or chengben_nums is None:
            return jsonify({
                'status': 'error',
                'message': '参数chengben_price和chengben_nums不能为空'
            }), 400

        # 转换为数值类型
        try:
            price = float(chengben_price)
            nums = int(chengben_nums) if '.' not in chengben_nums else float(chengben_nums)
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': '参数chengben_price应为数字，chengben_nums应为整数或浮点数'
            }), 400

        # 加载现有数据
        data = load_data()

        # 创建或更新记录
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if code in data:
            # 更新现有记录
            action = 'updated'
            data[code]['chengben_price'] = price
            data[code]['chengben_nums'] = nums
            data[code]['update_time'] = time_now
            data[code]['update_count'] = data[code].get('update_count', 0) + 1
        else:
            # 创建新记录
            action = 'created'
            data[code] = {
                'code': code,
                'chengben_price': price,
                'chengben_nums': nums,
                'create_time': time_now,
                'update_time': time_now,
                'update_count': 0
            }
        # 保存数据
        save_data(data)

        print(1231234)
        return jsonify({
            'status': 'success',
            'action': action,
            'code': code,
            'data': data[code]
        })

    except Exception as e:
        print(e)
        return jsonify({
            'status': 'error',
            'message': f'服务器内部错误: {str(e)}'
        }), 500


@data_bp.route('/api/query/<code>', methods=['GET'])
def query_data(code):
    """查询指定code的数据"""
    try:
        data = load_data()

        if code in data:
            return jsonify({
                'status': 'success',
                'data': data[code]
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'未找到code为{code}的记录'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'查询失败: {str(e)}'
        }), 500


@data_bp.route('/api/query_all', methods=['GET'])
def query_all():
    """查询所有数据"""
    try:
        data = load_data()
        for d in data:
            name = d
            value = data[d]
            res = analyse_code(name, value['chengben_price'], value['chengben_nums'], 0.05)
            data[d]['new_nums'] = res['new_nums']
            data[d]['new_chengben'] = res['new_chengben']
            data[d]['current_price'] = res['current_price']
            data[d]['shouyi'] = res['shouyi']
            data[d]['name'] = res['name']

        # 统计数据
        total_records = len(data)
        codes = list(data.keys())

        return jsonify({
            'status': 'success',
            'total_records': total_records,
            'codes': codes,
            'data': data
        })
    except Exception as e:
        print(e)
        return jsonify({
            'status': 'error',
            'message': f'查询失败: {str(e)}'
        }), 500


@data_bp.route('/api/delete/<code>', methods=['DELETE'])
def delete_data(code):
    """删除指定code的数据"""
    try:
        data = load_data()

        if code in data:
            deleted_data = data.pop(code)
            save_data(data)

            return jsonify({
                'status': 'success',
                'message': f'已删除code为{code}的记录',
                'deleted_data': deleted_data
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'未找到code为{code}的记录'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'删除失败: {str(e)}'
        }), 500


@data_bp.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    try:
        data = load_data()

        if not data:
            return jsonify({
                'status': 'success',
                'message': '暂无数据',
                'total_records': 0
            })

        # 计算一些基本统计
        total_items = sum(item.get('chengben_nums', 0) for item in data.values())
        total_value = sum(item.get('chengben_price', 0) * item.get('chengben_nums', 0)
                          for item in data.values())

        return jsonify({
            'status': 'success',
            'total_records': len(data),
            'total_items': total_items,
            'total_value': round(total_value, 2),
            'avg_price': round(total_value / total_items, 2) if total_items > 0 else 0
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取统计失败: {str(e)}'
        }), 500


@data_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'service': 'data_recorder',
        'timestamp': datetime.now().isoformat()
    })

