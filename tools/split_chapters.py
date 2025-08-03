#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节拆分脚本
自动将长HTML文件按章节拆分为独立文件
"""

import re
import os

def read_file(filename):
    """读取HTML文件"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filename, content):
    """写入文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def get_chapter_template():
    """获取章节模板"""
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 柯南侦探英语冒险</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-link">📖 返回目录</a>
        
        <div class="chapter-nav">
            <a href="{prev_link}" class="{prev_class}">⬅️ 上一章</a>
            <span>{title}</span>
            <a href="{next_link}" class="{next_class}">下一章 ➡️</a>
        </div>
        
        {content}
        
        <div class="chapter-nav">
            <a href="{prev_link}" class="{prev_class}">⬅️ 上一章</a>
            <a href="../index.html" class="back-link">📖 返回目录</a>
            <a href="{next_link}" class="{next_class}">下一章 ➡️</a>
        </div>
    </div>
</body>
</html>'''

def split_chapters():
    """拆分章节"""
    # 章节信息
    chapters = [
        {"num": 1, "title": "魔法学院的入学考试", "start": 685, "end": 1940},
        {"num": 2, "title": "颜色单词的魔法咒语", "start": 1941, "end": 3056},
        {"num": 3, "title": "数字单词的密码破解", "start": 3057, "end": 4292},
        {"num": 4, "title": "罗小黑的奇妙相遇", "start": 4293, "end": 4663},
        {"num": 5, "title": "魔法生物的语言", "start": 4664, "end": 5504},
        {"num": 6, "title": "魔法地图的探索", "start": 5505, "end": 6484},
        {"num": 7, "title": "魔法图书馆的秘密", "start": 6485, "end": 7525},
        {"num": 8, "title": "魔法竞技场的挑战", "start": 7526, "end": 8732},
        {"num": 9, "title": "魔法天气的预测", "start": 8733, "end": 9743},
        {"num": 10, "title": "魔法时间的旅行", "start": 9744, "end": 10925},
        {"num": 11, "title": "最终魔法考试", "start": 10926, "end": -1},
    ]
    
    # 读取原文件
    print("读取原HTML文件...")
    content = read_file("柯南侦探英语冒险：杨乐北的单词探案记.html")
    lines = content.split('\n')
    
    # 创建chapters目录
    os.makedirs("chapters", exist_ok=True)
    
    # 处理每个章节
    for i, chapter in enumerate(chapters):
        print(f"处理第{chapter['num']}章：{chapter['title']}...")
        
        # 提取章节内容
        start_line = chapter['start'] - 1  # 转换为0索引
        end_line = chapter['end'] if chapter['end'] != -1 else len(lines)
        chapter_lines = lines[start_line:end_line]
        
        # 清理章节内容，移除多余的div标签
        chapter_content = '\n'.join(chapter_lines)
        
        # 移除开头的空白div和结尾可能的div
        chapter_content = re.sub(r'^\s*<div class="chapter">\s*', '', chapter_content)
        chapter_content = re.sub(r'\s*</div>\s*$', '', chapter_content)
        
        # 确保内容以章节div开始
        if not chapter_content.strip().startswith('<div class="chapter">'):
            chapter_content = f'        <div class="chapter">\n{chapter_content}\n        </div>'
        
        # 设置导航链接
        prev_link = f"chapter{i:02d}.html" if i > 0 else "#"
        prev_class = "" if i > 0 else "disabled"
        next_link = f"chapter{i+2:02d}.html" if i < len(chapters) - 1 else "#"
        next_class = "" if i < len(chapters) - 1 else "disabled"
        
        # 生成章节HTML
        chapter_html = get_chapter_template().format(
            title=f"第{chapter['num']}章：{chapter['title']}",
            content=chapter_content,
            prev_link=prev_link,
            prev_class=prev_class,
            next_link=next_link,
            next_class=next_class
        )
        
        # 写入文件
        filename = f"chapters/chapter{chapter['num']:02d}.html"
        write_file(filename, chapter_html)
        print(f"  → 已创建 {filename}")
    
    print("章节拆分完成！")

if __name__ == "__main__":
    split_chapters()