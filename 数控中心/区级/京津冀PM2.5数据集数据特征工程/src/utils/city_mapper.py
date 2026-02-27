"""城市映射工具。

负责从 `config/cities.json` 加载城市列表，并提供常用的映射方法，例如中文名->拼音。
"""

import json
import os
from config.settings import BASE_DIR


def get_all_cities():
    """从 `config/cities.json` 加载城市列表并返回原始字典结构。

    返回格式为省份分组的字典，值为包含 `name` 和 `pinyin` 的列表。
    """
    path = os.path.join(BASE_DIR, 'config', 'cities.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"已加载城市数据，共{sum(len(cities) for cities in data.values())}个城市")
    return data


def get_pinyin_map():
    """返回中文名到拼音的映射字典。"""
    data = get_all_cities()
    mapping = {}
    for province, cities in data.items():
        for c in cities:
            mapping[c['name']] = c['pinyin']
    return mapping

def get_city_code_map():
    """返回中文名到城市编码的映射字典（从 config/city_codes.json 加载）"""
    path = os.path.join(BASE_DIR, 'config', 'city_codes.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    mapping = {}
    for province, cities in data.items():
        for c in cities:
            mapping[c['name']] = c['code']
    print(f"已加载城市编码映射，共{len(mapping)}个城市")
    return mapping