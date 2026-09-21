#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF 注释提取工具
将 PDF 文件中的所有注释导出为 XML 格式
"""

import sys
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom


def parse_pdf_annotations(pdf_path: str) -> list[dict]:
    """
    解析 PDF 文件中的注释

    Args:
        pdf_path: PDF 文件路径

    Returns:
        包含所有注释信息的字典列表
    """
    try:
        import pymupdf
    except ImportError:
        print("错误：请先安装 PyMuPDF 库")
        print("使用命令：pip install PyMuPDF")
        sys.exit(1)

    annotations = []

    try:
        with pymupdf.open(pdf_path) as doc:
            for page_num, page in enumerate(doc.pages(), start=1):
                # 获取页面注释
                annots = page.annots()

                if annots is not None:
                    for annot in annots:
                        info = annot.info if hasattr(annot, 'info') else {}
                        annot_info = {
                            'page': page_num,
                            'type': annot.type[0],
                            'subtype': annot.type[1],
                            'content': info.get('content', ''),
                            'subject': info.get('subject', ''),
                            'rect': annot.rect,
                            'created': info.get('created', ''),
                            'modified': info.get('modified', ''),
                            'color': list(annot.colors.get('stroke') or annot.colors.get('fill') or []) if annot.colors else None,
                            'opacity': annot.opacity
                        }
                        annotations.append(annot_info)

    except Exception as e:
        print(f"解析 PDF 失败：{e}")
        sys.exit(1)

    return annotations


def create_xml_tree(annotations: list[dict]) -> ET.Element:
    """
    创建注释的 XML 树结构

    Args:
        annotations: 注释信息列表

    Returns:
        ElementTree 根元素
    """
    root = ET.Element('pdf_annotations')

    # 添加元数据
    metadata = ET.SubElement(root, 'metadata')
    timestamp = ET.SubElement(metadata, 'export_time')
    from datetime import datetime
    timestamp.text = datetime.now().isoformat()

    count = ET.SubElement(metadata, 'annotation_count')
    count.text = str(len(annotations))

    # 添加每个注释
    for i, annot in enumerate(annotations):
        annot_elem = ET.SubElement(root, 'annotation')
        annot_elem.set('id', str(i + 1))

        ET.SubElement(annot_elem, 'page').text = str(annot['page'])
        ET.SubElement(annot_elem, 'type').text = str(annot['type'])
        ET.SubElement(annot_elem, 'subtype').text = str(annot['subtype'])

        if annot['content']:
            ET.SubElement(annot_elem, 'content').text = annot['content']

        if annot['subject']:
            ET.SubElement(annot_elem, 'subject').text = annot['subject']

        if annot['rect']:
            rect_elem = ET.SubElement(annot_elem, 'rect')
            rect_elem.set('x0', str(annot['rect'].x0))
            rect_elem.set('y0', str(annot['rect'].y0))
            rect_elem.set('x1', str(annot['rect'].x1))
            rect_elem.set('y1', str(annot['rect'].y1))

        if annot['created']:
            ET.SubElement(annot_elem, 'created').text = annot['created']

        if annot['modified']:
            ET.SubElement(annot_elem, 'modified').text = annot['modified']

        if annot['color']:
            color_elem = ET.SubElement(annot_elem, 'color')
            color_vals = annot['color']
            if len(color_vals) >= 3:
                color_elem.set('r', str(int(color_vals[0] * 255)))
                color_elem.set('g', str(int(color_vals[1] * 255)))
                color_elem.set('b', str(int(color_vals[2] * 255)))
                if len(color_vals) >= 4:
                    color_elem.set('a', str(round(color_vals[3], 2)))
            elif len(color_vals) == 1:
                color_elem.set('gray', str(int(color_vals[0] * 255)))

        if annot['opacity'] is not None:
            ET.SubElement(annot_elem, 'opacity').text = str(annot['opacity'])

    return root


def prettify_xml(elem: ET.Element) -> str:
    """
    美化 XML 输出

    Args:
        elem: XML 元素

    Returns:
        格式化后的 XML 字符串
    """
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)

    # 获取缩进字符串（2 个空格）
    return reparsed.toprettyxml(indent="  ")


def export_annotations_as_xml(
    pdf_path: str,
    output_path: str | None = None,
    encoding: str = 'utf-8'
) -> str:
    """
    将 PDF 注释导出为 XML 文件

    Args:
        pdf_path: 输入的 PDF 文件路径
        output_path: 输出的 XML 文件路径（默认与 PDF 同目录，同名 .xml 后缀）
        encoding: XML 文件编码

    Returns:
        输出的 XML 文件路径
    """
    # 如果未指定输出路径，默认保存在 PDF 同目录下
    if output_path is None:
        pdf_file = Path(pdf_path)
        output_path = str(pdf_file.with_suffix('.xml'))

    # 解析 PDF 注释
    print(f"正在解析 PDF 文件：{pdf_path}")
    annotations = parse_pdf_annotations(pdf_path)
    print(f"找到 {len(annotations)} 条注释")

    # 创建 XML 树
    root = create_xml_tree(annotations)

    # 转换为格式化字符串
    xml_string = prettify_xml(root)

    # 写入文件
    with open(output_path, 'w', encoding=encoding) as f:
        f.write(xml_string)

    print(f"XML 文件已保存至：{output_path}")
    return output_path


if __name__ == '__main__':
    # 命令行参数处理
    if len(sys.argv) < 2:
        print("用法：python pdf_annotations_to_xml.py <pdf 文件或文件夹路径> [输出 xml 路径]")
        print("")
        print("示例:")
        print("  python pdf_annotations_to_xml.py document.pdf")
        print("  python pdf_annotations_to_xml.py document.pdf comments.xml")
        print("  python pdf_annotations_to_xml.py ./pdf_folder/")
        sys.exit(1)

    input_path = sys.argv[1]
    output_xml = sys.argv[2] if len(sys.argv) > 2 else None

    # 检查输入路径是否存在
    if not os.path.exists(input_path):
        print(f"错误：路径不存在：{input_path}")
        sys.exit(1)

    # 判断是文件还是文件夹
    if os.path.isdir(input_path):
        # 文件夹：处理所有 PDF 文件
        pdf_folder = Path(input_path)
        # Windows 文件系统不区分大小写，只匹配小写即可
        pdf_files = list(pdf_folder.glob('*.pdf'))

        if not pdf_files:
            print(f"文件夹中没有找到 PDF 文件：{input_path}")
            sys.exit(0)

        print(f"找到 {len(pdf_files)} 个 PDF 文件")
        for pdf_file in pdf_files:
            print(f"\n处理：{pdf_file.name}")
            export_annotations_as_xml(str(pdf_file))

        print(f"\n完成！共处理 {len(pdf_files)} 个文件")
    else:
        # 单个文件
        export_annotations_as_xml(input_path, output_xml)
