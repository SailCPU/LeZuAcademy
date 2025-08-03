#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建用于浏览器打印的完整书籍HTML文件
"""

import os
from pathlib import Path
import re
from bs4 import BeautifulSoup

class PrintVersionCreator:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.chapters_dir = self.base_dir / "chapters"
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.output_file = self.output_dir / "柯南侦探英语冒险-完整打印版.html"
        
        # 完整书籍文件顺序
        self.chapter_files = [
            "book_cover.html",      # 封面
            "index.html",           # 目录页
            "chapter01.html",       # 第一章开始
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
        # 处理根目录下的文件
        if filename in ["book_cover.html", "book_back_cover.html", "index.html"]:
            file_path = self.base_dir / filename
        else:
            # 其他文件在chapters目录
            file_path = self.chapters_dir / filename
        
        if not file_path.exists():
            print(f"警告：文件 {filename} 不存在，路径: {file_path}")
            return None
        
        return self.read_html_file(file_path)
    
    def extract_css_styles(self, html_content):
        """提取CSS样式"""
        soup = BeautifulSoup(html_content, 'html.parser')
        styles = []
        
        # 提取所有<style>标签内容
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                styles.append(style_tag.string)
        
        return '\n'.join(styles)
    
    def extract_body_content(self, html_content, filename=""):
        """提取body内容"""
        soup = BeautifulSoup(html_content, 'html.parser')
        body = soup.find('body')
        
        if not body:
            return ""
        
        # 移除脚本标签
        for script in body.find_all('script'):
            script.decompose()
        
        # 为每个页面添加分页标记
        if filename != "book_back_cover.html":  # 最后一页不需要分页
            page_break = soup.new_tag('div', **{'class': 'page-break'})
            body.append(page_break)
        
        # 只返回body标签内的内容，不包含body标签本身
        return ''.join(str(child) for child in body.children)
    
    def fix_image_paths(self, html_content):
        """修复图片路径"""
        # 将相对路径转换为绝对路径
        image_pattern = r'src="([^"]*)"'
        
        def replace_path(match):
            path = match.group(1)
            if not path.startswith('http') and not path.startswith('data:'):
                # 转换相对路径为相对于输出文件的路径
                if path.startswith('./'):
                    path = path[2:]
                elif path.startswith('../'):
                    path = path[3:]
                return f'src="{path}"'
            return match.group(0)
        
        return re.sub(image_pattern, replace_path, html_content)
    
    def create_print_version(self):
        """创建打印版本"""
        print("============================================================")
        print("📚 创建浏览器打印版本")
        print("============================================================")
        
        all_styles = []
        all_content = []
        
        print("开始处理文件...")
        
        for i, filename in enumerate(self.chapter_files):
            print(f"处理文件: {filename}")
            html_content = self.get_file_content(filename)
            
            if html_content is None:
                print(f"跳过文件: {filename}")
                continue
            
            # 提取CSS样式（从主要文件提取）
            if filename in ["book_cover.html", "index.html", "chapter01.html"]:
                styles = self.extract_css_styles(html_content)
                if styles:
                    all_styles.append(styles)
            
            # 提取body内容
            body_content = self.extract_body_content(html_content, filename)
            if body_content:
                all_content.append(body_content)
        
        # 修复图片路径
        combined_content = '\n'.join(all_content)
        combined_content = self.fix_image_paths(combined_content)
        
        # 创建完整的HTML文档
        combined_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>柯南侦探英语冒险：杨乐北的单词探案记 - 打印版</title>
    <style>
        {chr(10).join(all_styles)}
        
        /* 打印专用样式 */
        @media print {{
            .page-break {{
                page-break-after: always;
            }}
            
            /* 隐藏不需要打印的元素 */
            .chapter-nav, .project-nav, .preview-note, #pronunciation-guide {{
                display: none !important;
            }}
            
            /* 隐藏所有固定定位元素 */
            [style*="position: fixed"] {{
                display: none !important;
            }}
            
            /* 强制保持所有颜色和效果 */
            * {{
                -webkit-print-color-adjust: exact !important;
                color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}
            
            /* 页面设置 */
            @page {{
                size: A4;
                margin: 15mm;
            }}
            
            /* 避免页面内容被截断 */
            body {{
                margin: 0;
                padding: 0;
            }}
            
            /* 确保图片不超出页面 */
            img {{
                max-width: 100% !important;
                height: auto !important;
                page-break-inside: avoid;
            }}
            
            /* 避免内容被分割 */
            .story-card, .word-card, .chapter-content {{
                page-break-inside: avoid;
                break-inside: avoid;
            }}
        }}
        
        /* 屏幕显示样式 */
        @media screen {{
            body {{
                max-width: 210mm;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }}
            
            .page-break {{
                border-top: 2px dashed #ccc;
                margin: 20px 0;
                padding: 10px 0;
                text-align: center;
                color: #666;
            }}
            
            .page-break::after {{
                content: "— 分页符 —";
                font-size: 12px;
            }}
            
            /* 隐藏不需要的元素 */
            .chapter-nav, .project-nav, .preview-note, #pronunciation-guide {{
                display: none !important;
            }}
            
            [style*="position: fixed"] {{
                display: none !important;
            }}
        }}
        
        /* 通用样式优化 */
        body {{
            font-family: "Microsoft YaHei", "PingFang SC", "Hiragino Sans GB", sans-serif;
            line-height: 1.6;
        }}
        
        .print-info {{
            position: fixed;
            top: 10px;
            right: 10px;
            background: #2196F3;
            color: white;
            padding: 10px;
            border-radius: 5px;
            z-index: 9999;
            font-size: 12px;
        }}
        
        @media print {{
            .print-info {{
                display: none !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="print-info">
        📖 打印版本已准备就绪<br>
        按 Ctrl+P 开始打印
    </div>
    
    {combined_content}
</body>
</html>"""
        
        # 保存文件
        print(f"保存文件到: {self.output_file}")
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(combined_html)
        
        print("✅ 打印版本创建成功！")
        print(f"📄 输出文件: {self.output_file}")
        print("\n📋 使用说明:")
        print("1. 在浏览器中打开生成的HTML文件")
        print("2. 按 Ctrl+P (或 Cmd+P) 打开打印对话框")
        print("3. 选择'保存为PDF'或直接打印")
        print("4. 建议设置：A4纸张，打印背景图形")

def main():
    creator = PrintVersionCreator()
    creator.create_print_version()

if __name__ == "__main__":
    main()