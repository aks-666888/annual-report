#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Annual Report Generator
从 JSON 数据生成单文件零依赖的交互式年度报告
"""

import json
import sys
import os
from pathlib import Path

def load_template(template_path: str) -> str:
    """加载 HTML 模板"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def inject_data(template: str, data: dict) -> str:
    """将数据注入模板"""
    # 将数据转换为 JSON 字符串
    data_json = json.dumps(data, ensure_ascii=False, indent=2)

    # 找到模板中的 DATA 占位符并替换
    template = template.replace('const DATA = {', 'const DATA = ' + data_json + '; // Replaced placeholder: {')

    return template

def generate(data_path: str, output_path: str, template_path: str = None) -> str:
    """
    生成报告

    Args:
        data_path: JSON 数据文件路径
        output_path: 输出 HTML 文件路径
        template_path: 模板文件路径（可选，默认使用同级目录的 report-template.html）

    Returns:
        生成的 HTML 内容
    """
    # 确定模板路径
    if template_path is None:
        script_dir = Path(__file__).parent
        template_path = script_dir.parent / 'templates' / 'report-template.html'

    # 加载数据
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 加载模板
    template = load_template(str(template_path))

    # 注入数据
    html = inject_data(template, data)

    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return html

def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("用法: python generate.py <数据文件> <输出文件> [模板文件]")
        sys.exit(1)

    data_path = sys.argv[1]
    output_path = sys.argv[2]
    template_path = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        html = generate(data_path, output_path, template_path)
        print(f"✅ 报告已生成: {output_path}")
        print(f"   大小: {len(html):,} 字节")
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
