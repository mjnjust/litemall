import os
from typing import List, Dict, Any, Optional, Union
from peewee import *
from datetime import datetime
import logging
from flask import Blueprint, request, jsonify
from ..services.items_service import ItemService

items_bp = Blueprint('items', __name__)

@items_bp.route('/list', methods=['GET'])
def get_items():
    total = 100;
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=10, type=int)
    data = ItemService.list_items(page, page_size)
    return jsonify(data)
