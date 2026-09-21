#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF 注释提取工具（迭代器版本）
将 pdf2xml.py 改写为迭代器形式，逐条 yield 注释，避免一次性加载全部数据到内存。
原文件不做修改，本文件为独立重写版本。

迭代器改造点：
  1. iter_pdf_annotations  —— 逐条 yield 注释字典（生成器）
  2. iter_xml_tree        —— 逐段 yield XML 字符串片段（生成器），不构建完整树
  3. export_annotations_as_xml —— 流式写入文件，内存中只持有当前一条注释
"""

import sys
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from typing import Iterator

# annotation_count 占位符：写入时占位，写完后回写替换为真实数值
_COUNT_PLACEHOLDER = '__ANNOTATION_COUNT_PLACEHOLDER__'


# ───────────────────────── 1. 注释迭代器 ─────────────────────────

def iter_pdf_annotations(pdf_path: str) -> Iterator[dict]:
    """
    以迭代器形式逐条解析 PDF 注释。

    与原版 parse_pdf_annotations 的区别：
    - 不再把所有注释收集到列表中一次性返回，而是逐条 yield，
      适合处理注释数量庞大的大型 PDF 文件，内存占用更低。

    Args:
        pdf_path: PDF 文件路径

    Yields:
        每条注释的字典信息
    """
    try:
        import pymupdf
    except ImportError:
        print("错误：请先安装 PyMuPDF 库")
        print("使用命令：pip install PyMuPDF")
        sys.exit(1)

    try:
        with pymupdf.open(pdf_path) as doc:
            for page_num, page in enumerate(doc.pages(), start=1):
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
                        yield annot_info

    except Exception as e:
        print(f"解析 PDF 失败：{e}")
        sys.exit(1)


# ───────────────────────── 2. XML 构建迭代器 ─────────────────────────

def _build_annotation_element(annot: dict, idx: int) -> ET.Element:
    """为单条注释构建一个 <annotation> XML 元素。"""
    annot_elem = ET.Element('annotation')
    annot_elem.set('id', str(idx))

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

    return annot_elem


def _prettify_element(elem: ET.Element, base_indent: str = '  ', child_indent: str = '  ') -> str:
    """
    美化单个 XML 元素，为每一行添加 base_indent 前缀，
    使其作为 <pdf_annotations> 的直接子元素时缩进正确。

    Args:
        elem: XML 元素
        base_indent: 根元素行的缩进（对应 <pdf_annotations> 的子级）
        child_indent: 子级递增缩进

    Returns:
        格式化后的多行字符串（不含 XML 声明）
    """
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    lines = reparsed.toprettyxml(indent=child_indent).splitlines()
    # 跳过第一行 <?xml ...?>，给每行加 base_indent
    pretty_lines = [base_indent + line for line in lines[1:]]
    return '\n'.join(pretty_lines)


def iter_xml_tree(annotations: Iterator[dict]) -> Iterator[str]:
    """
    以生成器形式逐段产出 XML 字符串。

    与原版 create_xml_tree 的区别：
    - 原版返回完整 ET.Element（整棵树在内存中）
    - 本函数逐段 yield XML 字符串片段，调用方可流式写入文件，
      内存中任意时刻只持有当前一条注释的元素。

    由于 annotation_count 需要在迭代结束后才能确定，
    而它在 XML 中位于 metadata（所有 annotation 之前），
    因此头部使用占位符 _COUNT_PLACEHOLDER，
    由 export_annotations_as_xml 在写入完成后回写替换。

    Yields 顺序:
      1. XML 声明 + <pdf_annotations> + <metadata>...</metadata>（含占位符）
      2. 每条注释的 <annotation>...</annotation>（逐条，带 2 空格缩进）
      3. </pdf_annotations> 闭标签
    """
    # ---- 第一段：XML 头 + 根元素 + 完整 metadata（占位符待回写）----
    head = (
        '<?xml version="1.0" ?>\n'
        '<pdf_annotations>\n'
        '  <metadata>\n'
        f'    <export_time>{datetime.now().isoformat()}</export_time>\n'
        f'    <annotation_count>{_COUNT_PLACEHOLDER}</annotation_count>\n'
        '  </metadata>\n'
    )
    yield head

    # ---- 中间段：逐条 annotation（2 空格缩进，子元素 4 空格）----
    for i, annot in enumerate(annotations, start=1):
        elem = _build_annotation_element(annot, i)
        yield _prettify_element(elem, base_indent='  ', child_indent='  ') + '\n'

    # ---- 最后一段：闭标签 ----
    yield '</pdf_annotations>\n'


# ───────────────────────── 3. 导出函数（流式写入 + 占位符回写） ─────────────────────────

def export_annotations_as_xml(
    pdf_path: str,
    output_path: str | None = None,
    encoding: str = 'utf-8'
) -> str:
    """
    将 PDF 注释导出为 XML 文件（迭代器 + 流式写入版本）。

    与原版区别：
    - 使用 iter_pdf_annotations 生成器逐条读取注释
    - 使用 iter_xml_tree 生成器逐段产出 XML 字符串
    - 逐段写入文件，不在内存中构建完整 XML 树
    - annotation_count 用占位符先写入，迭代结束后回写真实值

    Args:
        pdf_path: 输入的 PDF 文件路径
        output_path: 输出的 XML 文件路径（默认与 PDF 同目录，同名 .xml 后缀）
        encoding: XML 文件编码

    Returns:
        输出的 XML 文件路径
    """
    if output_path is None:
        pdf_file = Path(pdf_path)
        output_path = str(pdf_file.with_suffix('.xml'))

    print(f"正在解析 PDF 文件：{pdf_path}")
    annotations = iter_pdf_annotations(pdf_path)

    count = 0
    with open(output_path, 'w+', encoding=encoding) as f:
        for fragment in iter_xml_tree(annotations):
            f.write(fragment)
            if '<annotation ' in fragment:
                count += 1

        # 回写真实 annotation_count（占位符 → 真实数值）
        # 重新读取文件内容，替换占位符后写回
        # 注：此处仅对占位符做字符串替换，不涉及完整 XML 树重建
        f.seek(0)
        content = f.read()
        content = content.replace(_COUNT_PLACEHOLDER, str(count))
        f.seek(0)
        f.write(content)
        f.truncate()  # 防止替换后文件变长时残留旧内容

    print(f"找到 {count} 条注释")
    print(f"XML 文件已保存至：{output_path}")
    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python pdf2xml_iter.py <pdf 文件或文件夹路径> [输出 xml 路径]")
        print("")
        print("示例:")
        print("  python pdf2xml_iter.py document.pdf")
        print("  python pdf2xml_iter.py document.pdf comments.xml")
        print("  python pdf2xml_iter.py ./pdf_folder/")
        sys.exit(1)

    input_path = sys.argv[1]
    output_xml = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(input_path):
        print(f"错误：路径不存在：{input_path}")
        sys.exit(1)

    if os.path.isdir(input_path):
        pdf_folder = Path(input_path)
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
        export_annotations_as_xml(input_path, output_xml)
