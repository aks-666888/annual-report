#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intake: 从零散材料自动归类成报告数据草稿
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

def extract(text: str) -> Dict[str, Any]:
    """从零散文本中提取并归类数据"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # 初始化各区块
    result = {
        "meta": {"title": "", "subtitle": "", "period": "", "accent": "violet", "preset": "dashboard"},
        "metrics": [],
        "growth": {"caption": "", "labels": [], "series": []},
        "milestones": [],
        "features": [],
        "team": [],
        "outlook": [],
        "_hint": []
    }

    consumed = set()  # 标记已消费的行索引

    # 1. 检测标题（第一行通常含"年度/复盘/报告"）
    if lines and any(kw in lines[0] for kw in ['年度', '复盘', '报告', '回顾']):
        result["meta"]["title"] = lines[0]
        consumed.add(0)

    # 2. 检测时间段（含"2025年/今年/去年"等）
    for i, line in enumerate(lines):
        if i in consumed:
            continue
        if re.search(r'202[0-9]年|今年|去年|本季度|上半年|下半年', line):
            result["meta"]["period"] = line
            consumed.add(i)
            break

    # 3. 抽指标（纯数字+单位，不含"月"字）
    for i, line in enumerate(lines):
        if i in consumed:
            continue
        # 跳过明显是增长行（以"1月/2月/Q1"开头）
        if re.match(r'^[1-9一二三四]月|^Q[1-4]', line):
            continue
        # 剥括号内容（如"（单位 万）"）
        clean_line = re.sub(r'（[^）]*）', '', line)
        # 匹配：数字 + 可选单位 + 可选同比/增长率
        match = re.search(r'([0-9.,]+)\s*([万亿千万%]?)\s*(?:，?同比\s*([+-][0-9.,]+%))?', clean_line)
        if match:
            value_str, unit, delta = match.groups()
            # 提取标签（前面的文字）
            label_part = line.split(match.group(0))[0].strip('，、:')
            if label_part:
                value = float(value_str.replace(',', ''))
                metric = {
                    "label": label_part,
                    "value": value,
                    "unit": unit or ""
                }
                if delta:
                    metric["delta"] = delta
                    # 尝试提取上年值（"去年 450"）
                    prev_match = re.search(r'去年\s*([0-9.,]+)', line)
                    if prev_match:
                        metric["prev"] = float(prev_match.group(1).replace(',', ''))
                result["metrics"].append(metric)
                consumed.add(i)

    # 4. 抽增长曲线（月份+数值序列）
    for i, line in enumerate(lines):
        if i in consumed:
            continue
        if '走势' in line or '增长' in line or '月活' in line:
            # 检查后续行是否是序列
            data = []
            labels = []
            for j in range(i+1, min(i+13, len(lines))):
                if j in consumed:
                    continue
                seq_match = re.search(r'([1-9]|1[0-2])月\s*([0-9.,]+)', lines[j])
                if seq_match:
                    labels.append(seq_match.group(1) + '月')
                    data.append(float(seq_match.group(2).replace(',', '')))
                    consumed.add(j)
            if len(data) >= 3:
                result["growth"]["caption"] = "月活跃用户（MAU）"
                result["growth"]["labels"] = labels
                result["growth"]["series"] = [{
                    "label": "2025",
                    "data": data,
                    "color": "#c2ef4e"
                }]
                result["_hint"].append("增长曲线已自动提取，建议补充 caption（默认'月活跃用户'）和可选的往年对比数据")

    # 5. 抽里程碑（季度+事件）
    for i, line in enumerate(lines):
        if i in consumed:
            continue
        q_match = re.search(r'Q([1-4])[:：]?\s*(.+)', line)
        if q_match:
            quarter = f"Q{q_match.group(1)}"
            detail = q_match.group(2)
            # 尝试提取标题（第一个句号前的内容）
            title_match = re.match(r'([^，。]+)', detail)
            title = title_match.group(1) if title_match else detail
            result["milestones"].append({
                "quarter": quarter,
                "title": title,
                "detail": detail
            })
            consumed.add(i)

    # 6. 抽功能分布（功能+占比）
    for i, line in enumerate(lines):
        if i in consumed:
            continue
        if '功能' in line or '使用' in line:
            # 检查后续行是否是占比序列
            for j in range(i+1, min(i+10, len(lines))):
                if j in consumed:
                    continue
                feat_match = re.search(r'([^，、]+?)\s*([0-9.]+)%', lines[j])
                if feat_match:
                    result["features"].append({
                        "label": feat_match.group(1).strip(),
                        "value": float(feat_match.group(2))
                    })
                    consumed.add(j)
            if result["features"]:
                result["_hint"].append("功能分布已自动提取，建议检查标签是否准确")

    # 7. 抽团队亮点（职能+成就）
    for i, line in enumerate(lines):
        if i in consumed:
            continue
        team_match = re.match(r'(工程|产品|设计|运营|市场|销售)[:：]\s*(.+)', line)
        if team_match:
            result["team"].append({
                "label": team_match.group(1),
                "achievement": team_match.group(2)
            })
            consumed.add(i)

    # 8. 抽展望（明年方向）
    for i, line in enumerate(lines):
        if i in consumed:
            continue
        if '明年' in line or '展望' in line or '计划' in line:
            # 尝试分离多个方向（逗号、顿号分隔）
            parts = re.split(r'[，、。]', line)
            for part in parts:
                part = part.strip()
                if len(part) > 2 and not any(kw in part for kw in ['明年', '展望', '计划', '将']):
                    result["outlook"].append({
                        "title": part,
                        "detail": ""
                    })
            if result["outlook"]:
                result["_hint"].append("展望已自动提取，建议补充每项的详细说明")

    # 9. 提示 agent 复核
    if not result["metrics"]:
        result["_hint"].append("未检测到核心指标，建议手动补充至少1-3个关键指标（如用户数、收入、NPS）")
    if not result["growth"]["series"]:
        result["_hint"].append("未检测到增长曲线，建议手动补充月度/季度数据序列")
    if not result["milestones"]:
        result["_hint"].append("未检测到里程碑，建议手动补充关键事件+季度/时间")

    return result

def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("用法: python intake.py <输入文件> <输出文件>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # 读取输入
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 提取数据
    data = extract(text)

    # 写入输出
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 草稿已生成: {output_path}")
    print(f"   指标: {len(data['metrics'])} 个")
    print(f"   增长: {len(data['growth']['series'])} 条序列")
    print(f"   里程碑: {len(data['milestones'])} 个")
    print(f"   功能: {len(data['features'])} 项")
    print(f"   团队: {len(data['team'])} 个")
    print(f"   展望: {len(data['outlook'])} 项")
    if data["_hint"]:
        print(f"\n💡 提示: {len(data['_hint'])} 条需 agent 复核")

if __name__ == '__main__':
    main()
