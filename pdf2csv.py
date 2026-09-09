#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PDF → XML → CSV 一键处理入口，依次调用 pdf2xml.py 和 xml2csv.py。"""
import sys
import os

if __name__ == '__main__':
    # --- 步骤 1: PDF → XML ---
    print("=" * 50)
    print("步骤 1: 提取 PDF 注释为 XML")
    print("=" * 50)

    # 导入 pdf2xml 并调用其主函数
    from pdf2xml import export_annotations_as_xml

    input_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    if not os.path.exists(input_path):
        print(f"错误：路径不存在：{input_path}")
        sys.exit(1)

    input_dir = input_path if os.path.isdir(input_path) else None

    if input_dir:
        from pathlib import Path
        pdf_files = sorted(Path(input_dir).glob('*.pdf'))
        if not pdf_files:
            print(f"未找到 PDF 文件：{input_path}")
            sys.exit(0)
        print(f"找到 {len(pdf_files)} 个 PDF 文件\n")
        xml_files = []
        for pdf_file in pdf_files:
            print(f"处理：{pdf_file.name}")
            xml_path = export_annotations_as_xml(str(pdf_file))
            xml_files.append(xml_path)
            print()
    else:
        output_xml = sys.argv[2] if len(sys.argv) > 2 else None
        xml_files = [export_annotations_as_xml(input_path, output_xml)]

    # --- 步骤 2: XML → CSV ---
    print("=" * 50)
    print("步骤 2: 将 XML 转换为 CSV")
    print("=" * 50)

    from xml2csv import xml2csv

    if len(xml_files) == 1:
        output_csv = sys.argv[2] if len(sys.argv) > 2 and not input_dir else 'output.csv'
    else:
        output_csv = 'output.csv'

    # xml2csv 期望一个文件夹路径或单个文件路径
    if len(xml_files) == 1:
        xml2csv(xml_files[0], output_csv)
    else:
        # 多个 XML：用第一个所在的文件夹
        from pathlib import Path
        folder = str(Path(xml_files[0]).parent)
        xml2csv(folder, output_csv)

    print("\n全部完成！")
