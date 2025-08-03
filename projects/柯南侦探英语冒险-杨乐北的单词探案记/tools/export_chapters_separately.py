#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分章节PDF导出工具
将每个章节分别导出为独立的PDF文件
"""

import os
import sys
from pathlib import Path
import re
from bs4 import BeautifulSoup
from datetime import datetime

try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError:
    print("❌ 请先安装依赖: pip install weasyprint")
    print("   如果安装失败，请使用浏览器打印功能")
    sys.exit(1)

class ChapterPDFExporter:
    def __init__(self, book_format="16k"):
        self.base_dir = Path(__file__).parent.parent
        self.chapters_dir = self.base_dir / "chapters"
        self.output_dir = self.base_dir / "output" / "chapters_pdf"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 书籍尺寸配置
        self.formats = {
            "16k": {"size": "185mm 260mm", "margin": "15mm", "name": "16开本(185×260mm)"},
            "32k": {"size": "130mm 185mm", "margin": "12mm", "name": "大32开(130×185mm)"},
            "a5": {"size": "A5", "margin": "15mm", "name": "A5(148×210mm)"},
            "a4": {"size": "A4", "margin": "20mm", "name": "A4(210×297mm)"}
        }
        
        format_config = self.formats.get(book_format, self.formats["16k"])
        self.page_size = format_config["size"]
        self.margin = format_config["margin"]
        self.format_name = format_config["name"]
        
        # 章节文件列表
        self.chapter_files = [
            {"file": "chapter01.html", "title": "第01章-魔法学院的入学考试"},
            {"file": "chapter02.html", "title": "第02章-颜色单词的魔法咒语"},
            {"file": "chapter03.html", "title": "第03章-数字单词的密码破解"},
            {"file": "chapter04.html", "title": "第04章-罗小黑的奇妙相遇"},
            {"file": "chapter05.html", "title": "第05章-魔法生物的语言"},
            {"file": "chapter06.html", "title": "第06章-魔法地图的探索"},
            {"file": "chapter07.html", "title": "第07章-魔法图书馆的秘密"},
            {"file": "chapter08.html", "title": "第08章-魔法竞技场的挑战"},
            {"file": "chapter09.html", "title": "第09章-魔法天气的预测"},
            {"file": "chapter10.html", "title": "第10章-魔法时间的旅行"},
            {"file": "chapter11.html", "title": "第11章-最终魔法考试"},
            {"file": "appendix.html", "title": "附录-魔法词典和参考答案"},
        ]

    def get_enhanced_css(self):
        """获取增强的打印CSS样式"""
        return f"""
        @page {{
            size: {self.page_size};
            margin: {self.margin};
        }}
        
        body {{
            font-family: 'Microsoft YaHei', 'SimSun', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: #333;
            font-size: 11pt;
        }}
        
        .container {{
            max-width: none;
            margin: 0;
            padding: 0;
            background-color: white;
            box-shadow: none;
            border-radius: 0;
        }}
        
        .chapter-nav, .back-link {{
            display: none !important;
        }}
        
        .chapter-title {{
            color: #495057;
            font-size: 18pt;
            margin-bottom: 15pt;
            border-bottom: 2pt solid #6c757d;
            padding-bottom: 8pt;
            page-break-after: avoid;
        }}
        
        .section-title {{
            color: #495057;
            font-size: 14pt;
            margin: 20pt 0 12pt 0;
            border-left: 3pt solid #6c757d;
            padding-left: 12pt;
            page-break-after: avoid;
        }}
        
        .magic-box {{
            background: #f3e5f5;
            border: 2pt solid #9c27b0;
            padding: 15pt;
            border-radius: 6pt;
            margin: 15pt 0;
            page-break-inside: avoid;
        }}
        
        .story-box {{
            background: #fff3cd;
            border: 2pt solid #ffeaa7;
            padding: 15pt;
            border-radius: 6pt;
            margin: 15pt 0;
            page-break-inside: avoid;
        }}
        
        .word-box {{
            background: #d4edda;
            border: 2pt solid #c3e6cb;
            padding: 15pt;
            border-radius: 6pt;
            margin: 15pt 0;
            page-break-inside: avoid;
        }}
        
        .game-box {{
            background: #f8d7da;
            border: 2pt solid #f5c6cb;
            padding: 15pt;
            border-radius: 6pt;
            margin: 15pt 0;
            page-break-inside: avoid;
        }}
        
        .adventure-box {{
            background: #d1ecf1;
            border: 2pt solid #bee5eb;
            padding: 15pt;
            border-radius: 6pt;
            margin: 15pt 0;
            page-break-inside: avoid;
        }}
        
        .highlight {{
            background: #fff3cd;
            padding: 2pt 4pt;
            border-radius: 3pt;
            font-weight: bold;
        }}
        
        .english-word {{
            color: #e74c3c;
            font-weight: bold;
            font-size: 12pt;
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
            grid-template-columns: repeat(2, 1fr);
            gap: 10pt;
            margin: 15pt 0;
        }}
        
        .word-card {{
            background: white;
            border: 1pt solid #e9ecef;
            border-radius: 6pt;
            padding: 12pt;
            box-shadow: 0 1pt 2pt rgba(0,0,0,0.1);
            page-break-inside: avoid;
        }}
        
        .word-card .english {{
            font-size: 12pt;
            font-weight: bold;
            color: #e74c3c;
            margin-bottom: 4pt;
        }}
        
        .word-card .chinese {{
            color: #27ae60;
            font-weight: bold;
        }}
        
        .word-card .example {{
            font-style: italic;
            color: #666;
            margin-top: 6pt;
            font-size: 10pt;
        }}
        
        .mission-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 6pt;
            padding: 15pt;
            margin: 12pt 0;
            page-break-inside: avoid;
        }}
        
        .mission-card h4 {{
            color: white;
            margin-bottom: 8pt;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            page-break-inside: avoid;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            page-break-after: avoid;
        }}
        
        p {{
            orphans: 2;
            widows: 2;
        }}
        """

    def read_html_file(self, file_path):
        """读取HTML文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ 读取文件 {file_path} 时出错: {e}")
            return None

    def process_html_for_pdf(self, html_content):
        """处理HTML内容，优化PDF输出"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 移除导航元素
        for element in soup.find_all(['div'], class_=['chapter-nav']):
            element.decompose()
        
        for element in soup.find_all(['a'], class_=['back-link']):
            element.decompose()
        
        # 移除脚本
        for script in soup.find_all('script'):
            script.decompose()
        
        # 处理图片路径
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src.startswith('../'):
                # 转换为绝对路径
                img_path = self.base_dir / src[3:]  # 去掉 '../'
                if img_path.exists():
                    img['src'] = str(img_path.resolve())
        
        return str(soup)

    def export_single_chapter(self, chapter_info):
        """导出单个章节"""
        file_path = self.chapters_dir / chapter_info['file']
        
        if not file_path.exists():
            print(f"❌ 文件不存在: {file_path}")
            return False
        
        print(f"📖 正在处理: {chapter_info['title']}")
        
        # 读取HTML内容
        html_content = self.read_html_file(file_path)
        if not html_content:
            return False
        
        # 处理HTML内容
        processed_html = self.process_html_for_pdf(html_content)
        
        # 创建完整的HTML文档
        full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{chapter_info['title']} - 柯南侦探英语冒险</title>
    <style>
        {self.get_enhanced_css()}
    </style>
</head>
<body>
    {processed_html}
</body>
</html>"""
        
        # 生成PDF
        output_file = self.output_dir / f"{chapter_info['title']}.pdf"
        
        try:
            # 配置字体
            font_config = FontConfiguration()
            
            html_doc = HTML(string=full_html, base_url=str(self.base_dir))
            html_doc.write_pdf(str(output_file), font_config=font_config)
            
            print(f"✅ 已生成: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ 导出失败 {chapter_info['title']}: {e}")
            return False

    def export_all_chapters(self):
        """导出所有章节"""
        print("🚀 开始分章节PDF导出...")
        print(f"📖 书籍格式: {self.format_name}")
        print(f"📁 输出目录: {self.output_dir}")
        print("=" * 50)
        
        success_count = 0
        total_count = len(self.chapter_files)
        
        for chapter_info in self.chapter_files:
            if self.export_single_chapter(chapter_info):
                success_count += 1
            print("-" * 30)
        
        print("=" * 50)
        print(f"🎉 导出完成! 成功: {success_count}/{total_count}")
        print(f"📁 所有PDF文件保存在: {self.output_dir}")
        
        if success_count > 0:
            print("\n📋 导出的文件列表:")
            for pdf_file in sorted(self.output_dir.glob("*.pdf")):
                print(f"   📄 {pdf_file.name}")

    def create_browser_print_versions(self):
        """创建用于浏览器打印的单章节HTML版本"""
        print("🌐 创建浏览器打印版本...")
        
        browser_output_dir = self.output_dir / "browser_print"
        browser_output_dir.mkdir(exist_ok=True)
        
        for chapter_info in self.chapter_files:
            file_path = self.chapters_dir / chapter_info['file']
            
            if not file_path.exists():
                continue
            
            html_content = self.read_html_file(file_path)
            if not html_content:
                continue
            
            # 处理HTML内容
            processed_html = self.process_html_for_pdf(html_content)
            
            # 创建优化的浏览器打印版本
            browser_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{chapter_info['title']} - 打印版</title>
    <style>
        {self.get_enhanced_css()}
        
        /* 浏览器打印特有样式 */
        @media screen {{
            body {{
                max-width: 210mm;
                margin: 20px auto;
                padding: 20px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
            }}
            
            .print-hint {{
                background: #e3f2fd;
                border: 2px solid #2196f3;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                text-align: center;
                font-weight: bold;
                color: #1976d2;
            }}
        }}
        
        @media print {{
            .print-hint {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="print-hint">
        💡 按 Ctrl+P 打印此章节，选择"保存为PDF"即可导出PDF文件
    </div>
    {processed_html}
</body>
</html>"""
            
            # 保存文件
            output_file = browser_output_dir / f"{chapter_info['title']}-打印版.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(browser_html)
            
            print(f"✅ 已创建浏览器打印版: {output_file}")
        
        print(f"🌐 浏览器打印版本保存在: {browser_output_dir}")
        print("💡 使用方法：打开HTML文件，按Ctrl+P，选择'保存为PDF'")

def main():
    """主函数"""
    print("柯南侦探英语冒险 - 分章节PDF导出工具")
    print("=" * 60)
    
    # 选择书籍格式
    print("📖 请选择书籍页面格式:")
    print("1. 16开本 (185×260mm) - 推荐，适合儿童读物")
    print("2. 大32开 (130×185mm) - 便携，成本低")
    print("3. A5 (148×210mm) - 国际标准")
    print("4. A4 (210×297mm) - 通用打印纸")
    
    format_choice = input("请选择页面格式 (1/2/3/4，默认为1): ").strip() or "1"
    format_map = {"1": "16k", "2": "32k", "3": "a5", "4": "a4"}
    book_format = format_map.get(format_choice, "16k")
    
    exporter = ChapterPDFExporter(book_format)
    
    print(f"✅ 已选择: {exporter.format_name}")
    print("-" * 60)
    
    # 显示导出方式选项
    print("请选择导出方式:")
    print("1. Python WeasyPrint 导出 (推荐，需要安装依赖)")
    print("2. 创建浏览器打印版本 (简单，任何浏览器都可用)")
    print("3. 同时创建两种版本")
    
    choice = input("请输入选择 (1/2/3，默认为3): ").strip() or "3"
    
    print("-" * 60)
    
    if choice in ["1", "3"]:
        try:
            exporter.export_all_chapters()
        except Exception as e:
            print(f"❌ WeasyPrint导出失败: {e}")
            print("建议使用浏览器打印方式")
    
    if choice in ["2", "3"]:
        exporter.create_browser_print_versions()
    
    print("\n" + "=" * 60)
    print("🎉 所有操作完成!")

if __name__ == "__main__":
    main()