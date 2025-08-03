#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
柯南侦探英语冒险章节拆分脚本
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
    <title>{title} - 柯南侦探英语冒险：杨乐北的单词探案记</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', 'SimSun', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
            max-width: 210mm;
            margin: 0 auto;
        }}
        
        .container {{
            max-width: 180mm;
            margin: 0 auto;
            background: white;
            padding: 30px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 10px;
        }}
        
        .chapter-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 20px 0;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
        }}
        
        .chapter-nav a {{
            color: white;
            text-decoration: none;
            padding: 8px 15px;
            border-radius: 4px;
            background: rgba(255,255,255,0.2);
            transition: background 0.3s;
        }}
        
        .chapter-nav a:hover {{
            background: rgba(255,255,255,0.3);
        }}
        
        .chapter-nav a.disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        .back-link {{
            background: #28a745;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            margin: 10px 0;
        }}
        
        .back-link:hover {{
            background: #218838;
        }}
        
        .chapter {{
            margin-bottom: 40px;
            page-break-inside: avoid;
        }}
        
        .chapter-title {{
            color: #495057;
            font-size: 1.8em;
            margin-bottom: 20px;
            border-bottom: 2px solid #6c757d;
            padding-bottom: 10px;
        }}
        
        .section-title {{
            color: #495057;
            font-size: 1.4em;
            margin: 25px 0 15px 0;
            border-left: 3px solid #6c757d;
            padding-left: 15px;
        }}
        
        .magic-box {{
            background: #f3e5f5;
            border: 2px solid #9c27b0;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        .story-box {{
            background: #fff3cd;
            border: 2px solid #ffeaa7;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        .word-box {{
            background: #d4edda;
            border: 2px solid #c3e6cb;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        .game-box {{
            background: #f8d7da;
            border: 2px solid #f5c6cb;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        .adventure-box {{
            background: #d1ecf1;
            border: 2px solid #bee5eb;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        .highlight {{
            background: #fff3cd;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: bold;
        }}
        
        .english-word {{
            color: #e74c3c;
            font-weight: bold;
            font-size: 1.1em;
        }}
        
        .chinese-meaning {{
            color: #27ae60;
            font-weight: bold;
        }}
        
        .magic {{
            color: #9c27b0;
            font-weight: bold;
        }}
        
        .conan {{
            color: #e67e22;
            font-weight: bold;
        }}
        
        .yang-lebei {{
            color: #3498db;
            font-weight: bold;
        }}
        
        .yang-letian {{
            color: #e74c3c;
            font-weight: bold;
        }}
        
        .yang-leda {{
            color: #f39c12;
            font-weight: bold;
        }}
        
        .adventure {{
            color: #f39c12;
            font-weight: bold;
        }}
        
        .word-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .word-card {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .word-card .english {{
            font-size: 1.2em;
            font-weight: bold;
            color: #e74c3c;
            margin-bottom: 5px;
        }}
        
        .word-card .chinese {{
            color: #27ae60;
            font-weight: bold;
        }}
        
        .word-card .example {{
            font-style: italic;
            color: #666;
            margin-top: 8px;
            font-size: 0.9em;
        }}
        
        .mission-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .mission-card h4 {{
            color: white;
            margin-bottom: 10px;
        }}
        
        @media print {{
            .chapter-nav, .back-link {{
                display: none;
            }}
            
            @page {{
                margin: 20mm 15mm 20mm 15mm;
                size: A4 portrait;
            }}
            
            body {{
                margin: 0;
                padding: 0;
                font-size: 11pt;
                line-height: 1.5;
                background-color: white;
                max-width: none;
            }}
            
            .container {{
                max-width: none;
                margin: 0;
                padding: 0;
                background-color: white;
                box-shadow: none;
                border-radius: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-link">📖 返回总目录</a>
        <a href="index.html" class="back-link">📚 返回章节目录</a>
        
        <div class="chapter-nav">
            <a href="{prev_link}" class="{prev_class}">⬅️ 上一章</a>
            <span>{title}</span>
            <a href="{next_link}" class="{next_class}">下一章 ➡️</a>
        </div>
        
        {content}
        
        <div class="chapter-nav">
            <a href="{prev_link}" class="{prev_class}">⬅️ 上一章</a>
            <a href="index.html" class="back-link">📚 返回章节目录</a>
            <a href="{next_link}" class="{next_class}">下一章 ➡️</a>
        </div>
    </div>
</body>
</html>'''

def split_chapters():
    """拆分章节"""
    # 章节信息 - 根据grep搜索结果确定的行号
    chapters = [
        {"num": 1, "title": "魔法学院的入学考试", "start": 685, "end": 1940},
        {"num": 2, "title": "颜色单词的魔法咒语", "start": 1941, "end": 3056},
        {"num": 3, "title": "数字单词的密码破解", "start": 3057, "end": 4033},
        {"num": 4, "title": "罗小黑的奇妙相遇", "start": 4293, "end": 4663},
        {"num": 5, "title": "魔法生物的语言", "start": 4664, "end": 5504},
        {"num": 6, "title": "魔法地图的探索", "start": 5505, "end": 6484},
        {"num": 7, "title": "魔法图书馆的秘密", "start": 6485, "end": 7525},
        {"num": 8, "title": "魔法竞技场的挑战", "start": 7526, "end": 8732},
        {"num": 9, "title": "魔法天气的预测", "start": 8733, "end": 9743},
        {"num": 10, "title": "魔法时间的旅行", "start": 9744, "end": 10925},
        {"num": 11, "title": "最终魔法考试", "start": 10926, "end": -1},
    ]
    
    # 附录信息
    appendix = {"title": "魔法词典和参考答案", "start": 4034, "end": 4292}
    
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
        
        # 清理章节内容
        chapter_content = '\n'.join(chapter_lines)
        
        # 确保章节内容格式正确
        if not chapter_content.strip().startswith('<div class="chapter">'):
            chapter_content = f'        <div class="chapter">\n{chapter_content}\n        </div>'
        
        # 设置导航链接
        prev_link = f"chapter{i:02d}.html" if i > 0 else "#"
        prev_class = "" if i > 0 else "disabled"
        next_link = f"chapter{i+2:02d}.html" if i < len(chapters) - 1 else "appendix.html"
        next_class = ""
        
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
    
    # 处理附录
    print("处理附录：魔法词典和参考答案...")
    start_line = appendix['start'] - 1
    end_line = appendix['end']
    appendix_lines = lines[start_line:end_line]
    appendix_content = '\n'.join(appendix_lines)
    
    if not appendix_content.strip().startswith('<div class="chapter">'):
        appendix_content = f'        <div class="chapter">\n{appendix_content}\n        </div>'
    
    appendix_html = get_chapter_template().format(
        title=f"附录：{appendix['title']}",
        content=appendix_content,
        prev_link=f"chapter{len(chapters):02d}.html",
        prev_class="",
        next_link="#",
        next_class="disabled"
    )
    
    write_file("chapters/appendix.html", appendix_html)
    print("  → 已创建 chapters/appendix.html")
    
    print("章节拆分完成！")

def create_chapter_index():
    """创建章节目录"""
    index_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>章节目录 - 柯南侦探英语冒险：杨乐北的单词探案记</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', 'SimSun', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 10px;
        }
        
        .title {
            text-align: center;
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 30px;
        }
        
        .chapter-list {
            list-style: none;
            padding: 0;
        }
        
        .chapter-item {
            margin: 15px 0;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .chapter-item a {
            color: white;
            text-decoration: none;
            font-size: 1.2em;
            display: block;
        }
        
        .chapter-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.3s;
        }
        
        .back-link {
            background: #28a745;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            margin: 20px 0;
        }
        
        .back-link:hover {
            background: #218838;
        }
        
        .stats {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-link">📖 返回总目录</a>
        
        <h1 class="title">柯南侦探英语冒险：杨乐北的单词探案记</h1>
        
        <div class="stats">
            <p><strong>📚 章节总数：</strong>11章 + 1个附录</p>
            <p><strong>🎯 学习目标：</strong>掌握小学阶段核心英语单词</p>
            <p><strong>👦 主角：</strong>杨乐北（10岁，小学五年级）</p>
        </div>
        
        <ul class="chapter-list">
            <li class="chapter-item">
                <a href="chapters/chapter01.html">✨ 第一章：魔法学院的入学考试</a>
            </li>
            <li class="chapter-item">
                <a href="chapters/chapter02.html">🌈 第二章：颜色单词的魔法咒语</a>
            </li>
            <li class="chapter-item">
                <a href="chapters/chapter03.html">🔢 第三章：数字单词的密码破解</a>
            </li>
            <li class="chapter-item">
                <a href="chapters/chapter04.html">🐱 第四章：罗小黑的奇妙相遇</a>
            </li>
            <li class="chapter-item">
                <a href="chapters/chapter05.html">🦄 第五章：魔法生物的语言</a>
            </li>
            <li class="chapter-item">
                <a href="chapters/chapter06.html">🗺️ 第六章：魔法地图的探索</a>
            </li>
            <li class="chapter-item">
                <a href="chapters/chapter07.html">📚 第七章：魔法图书馆的秘密</a>
            </li>
            <li class="chapter-item">
                <a href="chapters/chapter08.html">🏟️ 第八章：魔法竞技场的挑战</a>
            </li>
            <li class="chapter-item">
                <a href="chapters/chapter09.html">🌦️ 第九章：魔法天气的预测</a>
            </li>
            <li class="chapter-item">
                <a href="chapters/chapter10.html">⏰ 第十章：魔法时间的旅行</a>
            </li>
            <li class="chapter-item">
                <a href="chapters/chapter11.html">🎓 第十一章：最终魔法考试</a>
            </li>
            <li class="chapter-item">
                <a href="chapters/appendix.html">📋 附录：魔法词典和参考答案</a>
            </li>
        </ul>
        
        <a href="../index.html" class="back-link">📖 返回总目录</a>
    </div>
</body>
</html>'''
    
    write_file("chapters/index.html", index_content)
    print("已创建章节目录 chapters/index.html")

if __name__ == "__main__":
    split_chapters()
    create_chapter_index()
