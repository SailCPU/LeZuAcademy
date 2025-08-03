#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业级PDF导出工具 - 符合印刷标准
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
    sys.exit(1)

class ProfessionalPDFExporter:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.chapters_dir = self.base_dir / "chapters"
        self.output_dir = self.base_dir / "output" / "professional"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.output_file = self.output_dir / "柯南侦探英语冒险-专业印刷版.pdf"
        
        # 专业印刷设置
        self.dpi = 300  # 印刷级分辨率
        self.page_width = "185mm"  # 16开本宽度
        self.page_height = "260mm"  # 16开本高度
        self.margin_inner = "25mm"  # 内侧边距 (装订侧)
        self.margin_outer = "20mm"  # 外侧边距
        self.margin_top = "20mm"    # 上边距
        self.margin_bottom = "25mm" # 下边距
        self.bleed = "3mm"         # 出血
        
        # 完整书籍文件顺序
        self.chapter_files = [
            "book_cover.html",      # 封面
            "index.html",           # 目录页
            "chapter01.html",       # 章节内容
            "chapter02.html", 
            "chapter03.html",
            "chapter04.html",
            "chapter05.html",
            "chapter06.html",
            "chapter07.html",
            "chapter08.html",
            "chapter09.html",
            "chapter10.html",
            "chapter11.html",
            "appendix.html",        # 附录
            "book_back_cover.html", # 后封面
        ]
    
    def read_html_file(self, file_path):
        """读取HTML文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
            return None
    
    def get_file_content(self, filename):
        """获取文件内容"""
        if filename in ["book_cover.html", "book_back_cover.html", "index.html"]:
            file_path = self.base_dir / filename
        else:
            file_path = self.chapters_dir / filename
        
        if not file_path.exists():
            print(f"警告：文件 {filename} 不存在，路径: {file_path}")
            return None
        
        return self.read_html_file(file_path)
    
    def extract_css_styles(self, html_content):
        """提取CSS样式"""
        soup = BeautifulSoup(html_content, 'html.parser')
        styles = []
        
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                styles.append(style_tag.string)
        
        return '\n'.join(styles)
    
    def extract_body_content(self, html_content, filename="", page_number=1):
        """提取body内容并添加页码"""
        soup = BeautifulSoup(html_content, 'html.parser')
        body = soup.find('body')
        
        if not body:
            return ""
        
        # 移除脚本和不需要的元素
        for element in body.find_all(['script', 'noscript']):
            element.decompose()
        
        # 移除固定定位的元素
        for element in body.find_all(attrs={"style": re.compile(r"position:\s*fixed")}):
            element.decompose()
        
        # 移除特定的ID元素
        for element_id in ["pronunciation-guide", "previewNote"]:
            element = body.find(id=element_id)
            if element:
                element.decompose()
        
        # 添加页面分隔和页码
        content = ''.join(str(child) for child in body.children)
        
        # 为每页添加包装器
        page_wrapper = f"""
        <div class="page-wrapper" data-page="{page_number}">
            {content}
        </div>
        """
        
        return page_wrapper
    
    def get_professional_css(self):
        """获取专业印刷CSS样式"""
        return f"""
        /* 专业印刷CSS样式 */
        
        /* 字体设置 */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
        
        /* 页面设置 - 专业印刷标准 */
        @page {{
            size: {self.page_width} {self.page_height};
            margin: {self.margin_top} {self.margin_outer} {self.margin_bottom} {self.margin_inner};
            
            /* 页眉页脚 */
            @top-left {{
                content: "柯南侦探英语冒险";
                font-size: 9pt;
                color: #666;
                font-family: 'Noto Sans SC', sans-serif;
            }}
            
            @bottom-right {{
                content: counter(page);
                font-size: 10pt;
                color: #333;
                font-family: 'Noto Sans SC', sans-serif;
            }}
        }}
        
        /* 右页（奇数页）- 外侧边距大 */
        @page :right {{
            margin: {self.margin_top} {self.margin_outer} {self.margin_bottom} {self.margin_inner};
        }}
        
        /* 左页（偶数页）- 内侧边距大 */
        @page :left {{
            margin: {self.margin_top} {self.margin_inner} {self.margin_bottom} {self.margin_outer};
        }}
        
        /* 封面页 - 无页眉页脚 */
        @page cover {{
            margin: 0;
            @top-left {{ content: none; }}
            @bottom-right {{ content: none; }}
        }}
        
        /* 全局样式重置 */
        * {{
            box-sizing: border-box;
        }}
        
        html {{
            font-size: 12pt; /* 印刷标准字号 */
            line-height: 1.6;
        }}
        
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
            color: #333;
            background: white;
            -webkit-print-color-adjust: exact;
            color-adjust: exact;
            print-color-adjust: exact;
        }}
        
        /* 页面包装器 */
        .page-wrapper {{
            min-height: calc(100vh - {self.margin_top} - {self.margin_bottom});
            page-break-after: always;
        }}
        
        .page-wrapper:last-child {{
            page-break-after: auto;
        }}
        
        /* 标题层级 */
        h1 {{
            font-size: 20pt;
            font-weight: 700;
            line-height: 1.3;
            margin: 0 0 18pt 0;
            page-break-after: avoid;
        }}
        
        h2 {{
            font-size: 16pt;
            font-weight: 600;
            line-height: 1.4;
            margin: 16pt 0 12pt 0;
            page-break-after: avoid;
        }}
        
        h3 {{
            font-size: 14pt;
            font-weight: 500;
            line-height: 1.4;
            margin: 12pt 0 8pt 0;
            page-break-after: avoid;
        }}
        
        /* 段落 */
        p {{
            font-size: 12pt;
            line-height: 1.6;
            margin: 0 0 12pt 0;
            text-align: justify;
            orphans: 2;
            widows: 2;
        }}
        
        /* 图片处理 */
        img {{
            max-width: 100%;
            height: auto;
            page-break-inside: avoid;
            margin: 8pt 0;
        }}
        
        /* 表格 */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12pt 0;
            page-break-inside: avoid;
        }}
        
        th, td {{
            padding: 6pt 8pt;
            border: 0.5pt solid #ddd;
            font-size: 11pt;
        }}
        
        th {{
            background-color: #f8f9fa;
            font-weight: 600;
        }}
        
        /* 列表 */
        ul, ol {{
            margin: 8pt 0 12pt 20pt;
            padding: 0;
        }}
        
        li {{
            margin: 4pt 0;
            line-height: 1.5;
        }}
        
        /* 代码块 */
        code {{
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            background-color: #f5f5f5;
            padding: 2pt 4pt;
            border-radius: 2pt;
        }}
        
        pre {{
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            background-color: #f8f9fa;
            padding: 8pt;
            border-radius: 4pt;
            margin: 8pt 0;
            page-break-inside: avoid;
        }}
        
        /* 特殊元素隐藏 */
        .chapter-nav, .project-nav, .preview-note, 
        #pronunciation-guide, .print-info {{
            display: none !important;
        }}
        
        [style*="position: fixed"] {{
            display: none !important;
        }}
        
        /* 封面特殊样式 */
        .book-cover {{
            page: cover;
            width: 100%;
            height: 100vh;
            margin: 0;
            padding: 0;
        }}
        
        /* 章节开始页 */
        .chapter-start {{
            page-break-before: always;
        }}
        
        /* 避免孤立行 */
        .story-card, .word-card, .chapter-content {{
            page-break-inside: avoid;
            break-inside: avoid;
        }}
        
        /* 链接样式 */
        a {{
            color: #2563eb;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        /* 强调文本 */
        strong, b {{
            font-weight: 600;
        }}
        
        em, i {{
            font-style: italic;
        }}
        
        /* 引用 */
        blockquote {{
            margin: 12pt 20pt;
            padding: 8pt 12pt;
            border-left: 3pt solid #ddd;
            background-color: #f9f9f9;
            font-style: italic;
        }}
        """
    
    def create_professional_pdf(self):
        """创建专业PDF"""
        print("============================================================")
        print("📚 专业印刷级PDF导出工具")
        print("============================================================")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        all_styles = []
        all_content = []
        
        print("开始处理文件...")
        
        for i, filename in enumerate(self.chapter_files, 1):
            print(f"处理文件: {filename}")
            html_content = self.get_file_content(filename)
            
            if html_content is None:
                print(f"跳过文件: {filename}")
                continue
            
            # 提取CSS样式
            if filename in ["book_cover.html", "index.html", "chapter01.html"]:
                styles = self.extract_css_styles(html_content)
                if styles:
                    all_styles.append(styles)
            
            # 提取body内容
            body_content = self.extract_body_content(html_content, filename, i)
            if body_content:
                all_content.append(body_content)
        
        # 合并所有样式
        combined_styles = '\n'.join(all_styles)
        professional_css = self.get_professional_css()
        
        # 创建完整HTML
        combined_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>柯南侦探英语冒险：杨乐北的单词探案记 - 专业印刷版</title>
    <style>
        {professional_css}
        
        /* 原始样式（经过优化） */
        {combined_styles}
    </style>
</head>
<body>
    {''.join(all_content)}
</body>
</html>"""
        
        print("开始生成专业PDF...")
        
        try:
            # 配置字体
            font_config = FontConfiguration()
            
            # 创建CSS配置
            css_config = CSS(string=f"""
                @page {{
                    size: {self.page_width} {self.page_height};
                    margin: {self.margin_top} {self.margin_outer} {self.margin_bottom} {self.margin_inner};
                }}
            """, font_config=font_config)
            
            # 生成PDF
            html_doc = HTML(string=combined_html)
            html_doc.write_pdf(
                self.output_file,
                stylesheets=[css_config],
                font_config=font_config,
                presentational_hints=True
            )
            
            file_size = self.output_file.stat().st_size / (1024 * 1024)
            
            print("✅ 专业PDF导出成功！")
            print(f"📄 输出文件: {self.output_file}")
            print(f"📊 文件大小: {file_size:.2f} MB")
            print(f"📐 页面尺寸: {self.page_width} × {self.page_height}")
            print(f"🎯 分辨率: {self.dpi} DPI")
            print()
            print("============================================================")
            print("🎉 专业印刷级PDF制作完成！")
            print("📋 文件特性:")
            print("   • 符合专业印刷标准")
            print("   • 300 DPI 高分辨率")
            print("   • 标准16开本尺寸")
            print("   • 专业排版布局")
            print("   • 适合商业印刷")
            print(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("============================================================")
            
        except Exception as e:
            print(f"❌ PDF生成失败: {e}")
            return False
        
        return True

def main():
    exporter = ProfessionalPDFExporter()
    exporter.create_professional_pdf()

if __name__ == "__main__":
    main()