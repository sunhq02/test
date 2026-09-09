#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import csv


def xml2list(xml_path: str) -> list[tuple[float, float]]:
    """
    从 XML 文件中提取距离数据，两两配对返回。

    Args:
        xml_path: XML 文件路径

    Returns:
        配对数据的列表，每个元素是一个 tuple，例如：[(数据1, 数据2), (数据3, 数据4), ...]
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    annotations = sorted(root.findall('annotation'), key=lambda a: int(a.get('id')))
    raw_data = []
    for annot in annotations:
        content = annot.findtext('content', '')
        match = re.search(r'距离.*?(\d+\.?\d*)\s*微米', content, re.DOTALL)
        if match:
            raw_data.append(float(match.group(1)))

    # 两两配对
    result = []
    for i in range(0, len(raw_data), 2):
        pair = raw_data[i:i+2]
        if len(pair) == 2:
            result.append((pair[0], pair[1]))
        else:
            # 奇数个数据时，最后一个单独成对（第二个值为 None）
            result.append((pair[0], None))

    return result


def xml2csv(input_path: str, output_csv: str = 'output.csv') -> str:
    """
    对路径下所有 XML 文件调用 xml2list，并将结果保存到 CSV 文件。
    每个 XML 文件的数据占两列，每两个 XML 文件之间间隔 2 列。

    Args:
        input_path: XML 文件所在的路径（文件夹或单个文件）
        output_csv: 输出的 CSV 文件路径

    Returns:
        输出的 CSV 文件路径
    """
    # 获取所有 XML 文件
    xml_path = Path(input_path)
    if xml_path.is_file():
        xml_files = [xml_path]
    else:
        xml_files = list(xml_path.glob('*.xml'))

    if not xml_files:
        print(f"未找到 XML 文件：{input_path}")
        return output_csv

    print(f"找到 {len(xml_files)} 个 XML 文件")

    # 提取所有 XML 的数据
    all_data = []
    max_rows = 0
    for xml_file in xml_files:
        data = xml2list(str(xml_file))
        all_data.append(data)
        max_rows = max(max_rows, len(data))
        print(f"  {xml_file.name}: {len(data)} 对数据")

    # 构建 CSV 行数据
    rows = []
    for row_idx in range(max_rows):
        row = []
        for data in all_data:
            # 添加当前 XML 的数据（两列）
            if row_idx < len(data):
                row.extend(data[row_idx])
            else:
                row.extend(['', ''])  # 不足的行用空值填充
            # 添加间隔列（每个 XML 数据块后）
            row.extend(['', ''])

        # 移除最后的间隔列（最后一个 XML 不需要）
        row = row[:-2]
        rows.append(row)

    # 写入 CSV 文件
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"CSV 文件已保存至：{output_csv}")
    return output_csv


if __name__ == '__main__':
    import sys

    # 命令行参数处理
    if len(sys.argv) == 1:
        # 无参数，默认处理当前文件夹
        input_path = '.'
        output_csv = 'output.csv'
    elif len(sys.argv) == 2:
        # 一个参数：输入路径
        input_path = sys.argv[1]
        output_csv = 'output.csv'
    else:
        # 两个及以上参数：输入路径和输出文件
        input_path = sys.argv[1]
        output_csv = sys.argv[2]

    xml2csv(input_path, output_csv)