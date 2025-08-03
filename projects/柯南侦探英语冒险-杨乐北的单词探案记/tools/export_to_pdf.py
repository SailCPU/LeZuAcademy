#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF导出脚本 - 柯南侦探英语冒险：杨乐北的单词探案记
从各个章节HTML文件直接生成完整的PDF文档
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import datetime

try:
    import weasyprint
except ImportError:
    print("请先安装weasyprint库：pip install weasyprint")
    exit(1)

class BookPDFExporter:
    def __init__(self, base_dir=None):
        if base_dir is None:
            self.base_dir = Path(__file__).parent.parent
        else:
            self.base_dir = Path(base_dir)
        
        self.chapters_dir = self.base_dir / "chapters"
        # 输出到根目录的缓存区
        self.output_dir = self.base_dir.parent.parent / "output" / "pdf"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.output_file = self.output_dir / "柯南侦探英语冒险：杨乐北的单词探案记.pdf"
        
        # 完整书籍文件顺序（包含封面和后封面）
        self.chapter_files = [
            "book_cover.html",      # 封面（第1页，右页）
            "blank_page_1",         # 空白页（第2页，左页） 
            "index.html",           # 目录页（第3页，右页）
            "blank_page_2",         # 空白页（第4页，左页，如果需要）
            "chapter01.html",       # 第一章开始（右页）
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
            "book_back_cover.html"  # 后封面（最后一页，左页）
        ]
    
    def read_html_file(self, file_path):
        """读取HTML文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
            return None
    
    def get_file_content(self, filename):
        """获取文件内容，处理特殊文件（如空白页、封面等）"""
        # 处理空白页
        if filename.startswith("blank_page"):
            return self.create_blank_page()
        
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
    
    def create_blank_page(self):
        """创建空白页HTML内容"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            background: white;
        }
        .blank-page {
            width: 100%;
            height: 100vh;
            page-break-after: always;
        }
    </style>
</head>
<body>
    <div class="blank-page"></div>
</body>
</html>"""
    
    def extract_body_content(self, html_content, is_first=False, is_cover=False, filename=""):
        """提取HTML文件的body内容"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取body内容
        body = soup.find('body')
        if not body:
            return ""
        
        # 封面和后封面保持原样，不做任何修改
        if is_cover or filename in ["book_cover.html", "book_back_cover.html"]:
            # 为封面添加特殊的CSS类
            if filename == "book_cover.html":
                body['class'] = body.get('class', []) + ['pdf-front-cover']
            elif filename == "book_back_cover.html":
                body['class'] = body.get('class', []) + ['pdf-back-cover']
            return str(body)
        
        # 移除导航元素（普通章节页面）
        if not is_first and not is_cover:
            nav_elements = body.find_all(['nav', 'div'], class_=['chapter-nav', 'navigation', 'project-nav'])
            for nav in nav_elements:
                nav.decompose()
            
            # 移除预览说明
            preview_elements = body.find_all(['div'], class_=['preview-note'])
            for preview in preview_elements:
                preview.decompose()
        
        # 添加分页符（除了第一个文件和封面）
        if not is_first and not is_cover:
            page_break_div = soup.new_tag('div', **{'class': 'page-break'})
            body.insert(0, page_break_div)
        
        return str(body)
    
    def extract_css_styles(self, html_content):
        """提取HTML文件中的CSS样式"""
        soup = BeautifulSoup(html_content, 'html.parser')
        styles = []
        
        # 提取内联样式
        style_tags = soup.find_all('style')
        for style in style_tags:
            if style.string:
                styles.append(style.string)
        
        return '\n'.join(styles)
    
    def create_combined_html(self):
        """创建合并的HTML文档"""
        print("开始创建合并的HTML文档...")
        
        # 收集所有CSS样式和内容
        all_styles = []
        all_content = []
        
        for i, filename in enumerate(self.chapter_files):
            print(f"处理文件: {filename}")
            
            # 使用新的方法获取文件内容
            html_content = self.get_file_content(filename)
            
            if html_content is None:
                print(f"跳过文件: {filename}")
                continue
            
            # 判断是否为封面页
            is_cover = filename in ["book_cover.html", "book_back_cover.html"]
            is_first = (i == 0)
            
            # 提取CSS样式（从封面、目录页和第一章提取）
            if filename in ["book_cover.html", "index.html", "chapter01.html"]:
                styles = self.extract_css_styles(html_content)
                if styles:
                    all_styles.append(styles)
            
            # 提取body内容
            body_content = self.extract_body_content(
                html_content, 
                is_first=is_first, 
                is_cover=is_cover, 
                filename=filename
            )
            all_content.append(body_content)
        
        # 创建完整的HTML文档
        combined_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>柯南侦探英语冒险：杨乐北的单词探案记</title>
    <style>
        {chr(10).join(all_styles)}
        
        /* PDF专用样式 - 强制保持色彩 */
        .page-break {{
            page-break-before: always;
        }}
        
        .blank-page {{
            page-break-after: always;
            height: 100vh;
        }}
        
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
        
        /* 双面打印页面设置 */
        @page {{
            size: A4;
            margin: 15mm;
        }}
        
        /* 右页（奇数页）- 封面、章节开始页 */
        @page :right {{
            margin-left: 20mm;
            margin-right: 15mm;
        }}
        
        /* 左页（偶数页）- 后封面、章节内容页 */
        @page :left {{
            margin-left: 15mm;
            margin-right: 20mm;
        }}
        
        /* 封面页面样式 */
        .pdf-front-cover {{
            page: cover-front;
            margin: 0 !important;
            padding: 0 !important;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .pdf-back-cover {{
            page: cover-back;
            margin: 0 !important;
            padding: 0 !important;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            page-break-before: always;
        }}
        
        @page cover-front {{
            margin: 0;
        }}
        
        @page cover-back {{
            margin: 0;
        }}
        
        /* 封面内容尺寸调整 */
        .pdf-front-cover .book-cover,
        .pdf-back-cover .book-back-cover {{
            width: 185mm !important;
            height: 260mm !important;
            max-width: none !important;
            max-height: none !important;
            margin: 0 !important;
            border-radius: 0 !important;
        }}
        
        /* 优化打印样式 - 保持原有效果 */
        @media print {{
            body {{
                margin: 0 !important;
                padding: 0 !important;
                background: white;
            }}
            
            .container {{
                max-width: 100% !important;
                margin: 0 !important;
                padding: 15mm !important;
                box-shadow: none !important;
            }}
            
            /* 确保封面全屏显示 */
            .pdf-front-cover,
            .pdf-back-cover {{
                width: 100vw !important;
                height: 100vh !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
        }}
        
        /* 优化字体显示 */
        body {{
            font-family: 'Microsoft YaHei', 'SimSun', serif;
            color: #333;
            background: white;
        }}
        
        /* 确保图片在PDF中正确显示 */
        img {{
            max-width: 100%;
            height: auto;
            page-break-inside: avoid;
        }}
        
        /* 避免在不合适的地方分页 */
        .word-item, .case-analysis, .exercise, .magic-box, .story-box, .word-box, .game-box, .adventure-box {{
            page-break-inside: avoid;
            break-inside: avoid;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            page-break-after: avoid;
            break-after: avoid;
        }}
        
        /* 章节标题确保在新页开始 */
        .chapter-title {{
            page-break-before: always;
            break-before: always;
        }}
        
        /* 确保重要内容不被分割 */
        .character-area, .feature-grid, .chapter-list, .info-section {{
            page-break-inside: avoid;
            break-inside: avoid;
        }}
        
        /* 隐藏不需要打印的元素 */
        .export-pdf-button, .pdf-export-instructions {{
            display: none !important;
        }}
    </style>
</head>
<body>
{chr(10).join(all_content)}
</body>
</html>"""
        
        return combined_html
    
    def export_to_pdf(self):
        """导出为PDF文件"""
        print(f"开始导出PDF文件到: {self.output_file}")
        
        try:
            # 创建合并的HTML内容
            html_content = self.create_combined_html()
            
            # 确保图片路径正确
            html_content = self.fix_image_paths(html_content)
            
            # 使用weasyprint转换为PDF，启用色彩优化
            print("正在转换为PDF...")
            html_doc = weasyprint.HTML(
                string=html_content,
                base_url=str(self.base_dir)
            )
            
            # 配置PDF生成选项，优化色彩显示
            html_doc.write_pdf(
                str(self.output_file),
                presentational_hints=True,  # 保持演示样式
                optimize_images=True        # 优化图片质量
            )
            
            print(f"✅ PDF导出成功！")
            print(f"📄 输出文件: {self.output_file}")
            print(f"📊 文件大小: {self.output_file.stat().st_size / 1024 / 1024:.2f} MB")
            
            return True
            
        except Exception as e:
            print(f"❌ 导出PDF时出错: {e}")
            return False
    
    def fix_image_paths(self, html_content):
        """修复HTML中的图片路径"""
        # 将相对路径转换为绝对路径
        image_pattern = r'src="(?!http)([^"]+)"'
        
        def replace_path(match):
            old_path = match.group(1)
            # 如果是相对路径，转换为绝对路径
            if not old_path.startswith('/'):
                if old_path.startswith('../'):
                    # 处理 ../images/ 这种路径
                    new_path = str(self.base_dir / old_path.replace('../', ''))
                else:
                    # 处理 images/ 这种路径
                    new_path = str(self.chapters_dir / old_path)
                return f'src="file://{new_path}"'
            return match.group(0)
        
        return re.sub(image_pattern, replace_path, html_content)
    
    def check_dependencies(self):
        """检查依赖项"""
        print("检查依赖项...")
        
        # 检查文件
        missing_files = []
        for filename in self.chapter_files:
            # 跳过虚拟的空白页
            if filename.startswith("blank_page"):
                continue
                
            # 检查根目录下的文件
            if filename in ["book_cover.html", "book_back_cover.html", "index.html"]:
                file_path = self.base_dir / filename
            else:
                # 其他文件在chapters目录
                file_path = self.chapters_dir / filename
                
            if not file_path.exists():
                missing_files.append(f"{filename} (路径: {file_path})")
        
        if missing_files:
            print(f"⚠️  以下文件缺失:")
            for missing_file in missing_files:
                print(f"   - {missing_file}")
            return False
        
        print("✅ 所有依赖项检查完成")
        print(f"📋 将处理以下文件:")
        for filename in self.chapter_files:
            if filename.startswith("blank_page"):
                print(f"   - {filename} (虚拟空白页)")
            else:
                print(f"   - {filename}")
        return True

def main():
    """主函数"""
    print("=" * 60)
    print("📚 柯南侦探英语冒险：杨乐北的单词探案记 - PDF导出工具")
    print("=" * 60)
    print(f"⏰ 开始时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 创建导出器
    exporter = BookPDFExporter()
    
    # 检查依赖项
    if not exporter.check_dependencies():
        print("❌ 依赖项检查失败，请确保所有章节文件存在")
        return
    
    # 导出PDF
    success = exporter.export_to_pdf()
    
    print()
    print("=" * 60)
    if success:
        print("🎉 导出完成！您可以查看生成的PDF文件了。")
    else:
        print("😞 导出失败，请检查错误信息。")
    print(f"⏰ 结束时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    main()