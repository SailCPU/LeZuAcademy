#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门导出书籍封面的工具
快速生成封面和后封面的PDF文件
"""

import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError:
    print("❌ 请先安装依赖: pip install weasyprint")
    print("   运行: cd tools && pip install -r requirements_pdf.txt")
    sys.exit(1)

class CoverExporter:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 16开本原始尺寸
        self.book_width = "185mm"
        self.book_height = "260mm"
        
        # A4纸张尺寸 (210mm × 297mm)
        self.a4_width = "210mm"
        self.a4_height = "297mm"
        
        self.dpi = 300
        
    def create_cover_css(self, print_mode="professional"):
        """创建封面专用CSS样式
        
        Args:
            print_mode: "professional" (16开本专业印刷) 或 "a4" (A4家庭打印)
        """
        if print_mode == "a4":
            # A4打印模式：16开本内容居中显示在A4纸上
            return CSS(string=f"""
            @page {{
                size: {self.a4_width} {self.a4_height};
                margin: 12.5mm 12.5mm;
                background: white;
            }}
            
            html, body {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                display: flex;
                justify-content: center;
                align-items: center;
                background: white;
            }}
            
            .book-cover {{
                width: {self.book_width};
                height: {self.book_height};
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                transform: scale(1);
            }}
            
            /* 确保16开本内容完整显示 */
            * {{
                box-sizing: border-box;
            }}
            
            /* 打印时隐藏动画 */
            @keyframes fadeInUp,
            @keyframes glowing,
            @keyframes rotate,
            @keyframes pulse,
            @keyframes float {{
                from, to {{ transform: none; opacity: 1; }}
            }}
            """)
        else:
            # 专业印刷模式：原始16开本尺寸
            return CSS(string=f"""
            @page {{
                size: {self.book_width} {self.book_height};
                margin: 0;
                padding: 0;
                background: white;
            }}
            
            html, body {{
                margin: 0;
                padding: 0;
                width: {self.book_width};
                height: {self.book_height};
                overflow: hidden;
            }}
            
            .book-cover {{
                width: {self.book_width};
                height: {self.book_height};
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            /* 确保所有元素都显示正确 */
            * {{
                box-sizing: border-box;
            }}
            
            /* 打印时隐藏动画 */
            @keyframes fadeInUp,
            @keyframes glowing,
            @keyframes rotate,
            @keyframes pulse,
            @keyframes float {{
                from, to {{ transform: none; opacity: 1; }}
            }}
            """)
    
    def export_front_cover(self, print_mode="professional"):
        """导出封面
        
        Args:
            print_mode: "professional" (16开本专业印刷) 或 "a4" (A4家庭打印)
        """
        cover_file = self.base_dir / "book_cover.html"
        
        if print_mode == "a4":
            output_file = self.output_dir / "封面-A4打印版.pdf"
            print("📖 正在导出封面 (A4打印版)...")
        else:
            output_file = self.output_dir / "封面-专业印刷版.pdf"
            print("📖 正在导出封面 (专业印刷版)...")
        
        if not cover_file.exists():
            print(f"❌ 封面文件不存在: {cover_file}")
            return False
            
        try:
            # 读取HTML文件
            with open(cover_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 创建HTML对象
            html_doc = HTML(string=html_content, base_url=str(self.base_dir))
            
            # 导出PDF
            html_doc.write_pdf(
                str(output_file),
                stylesheets=[self.create_cover_css(print_mode)],
                resolution=self.dpi,
                optimize_images=True
            )
            
            print(f"✅ 封面导出成功: {output_file}")
            print(f"   文件大小: {output_file.stat().st_size / 1024:.0f} KB")
            
            if print_mode == "a4":
                print("   💡 此版本适合家庭A4打印机")
            else:
                print("   💡 此版本适合专业印刷厂")
            
            return True
            
        except Exception as e:
            print(f"❌ 封面导出失败: {e}")
            return False
    
    def export_back_cover(self, print_mode="professional"):
        """导出后封面
        
        Args:
            print_mode: "professional" (16开本专业印刷) 或 "a4" (A4家庭打印)
        """
        back_cover_file = self.base_dir / "book_back_cover.html"
        
        if print_mode == "a4":
            output_file = self.output_dir / "后封面-A4打印版.pdf"
            print("📖 正在导出后封面 (A4打印版)...")
        else:
            output_file = self.output_dir / "后封面-专业印刷版.pdf"
            print("📖 正在导出后封面 (专业印刷版)...")
        
        if not back_cover_file.exists():
            print(f"❌ 后封面文件不存在: {back_cover_file}")
            return False
            
        try:
            # 读取HTML文件
            with open(back_cover_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 创建HTML对象
            html_doc = HTML(string=html_content, base_url=str(self.base_dir))
            
            # 导出PDF
            html_doc.write_pdf(
                str(output_file),
                stylesheets=[self.create_cover_css(print_mode)],
                resolution=self.dpi,
                optimize_images=True
            )
            
            print(f"✅ 后封面导出成功: {output_file}")
            print(f"   文件大小: {output_file.stat().st_size / 1024:.0f} KB")
            
            if print_mode == "a4":
                print("   💡 此版本适合家庭A4打印机")
            else:
                print("   💡 此版本适合专业印刷厂")
            
            return True
            
        except Exception as e:
            print(f"❌ 后封面导出失败: {e}")
            return False
    
    def export_both_covers(self, print_mode="both"):
        """同时导出封面和后封面
        
        Args:
            print_mode: "professional", "a4", 或 "both" (两种版本都导出)
        """
        print("🎨 开始导出书籍封面...")
        print(f"📏 16开本设计尺寸: {self.book_width} × {self.book_height}")
        print(f"🎯 分辨率: {self.dpi} DPI")
        
        if print_mode == "both":
            print("📦 导出模式: 专业印刷版 + A4打印版")
        elif print_mode == "a4":
            print("📦 导出模式: A4家庭打印版")
        else:
            print("📦 导出模式: 专业印刷版")
            
        print("=" * 50)
        
        success_count = 0
        total_count = 0
        
        if print_mode in ["professional", "both"]:
            front_success = self.export_front_cover("professional")
            back_success = self.export_back_cover("professional")
            total_count += 2
            if front_success: success_count += 1
            if back_success: success_count += 1
        
        if print_mode in ["a4", "both"]:
            front_success_a4 = self.export_front_cover("a4")
            back_success_a4 = self.export_back_cover("a4")
            total_count += 2
            if front_success_a4: success_count += 1
            if back_success_a4: success_count += 1
        
        print("=" * 50)
        
        if success_count == total_count:
            print("🎉 封面导出完成！")
            print("\n📁 导出文件位置:")
            
            if print_mode in ["professional", "both"]:
                print("   🏢 专业印刷版:")
                print(f"      封面: {self.output_dir}/封面-专业印刷版.pdf")
                print(f"      后封面: {self.output_dir}/后封面-专业印刷版.pdf")
                
            if print_mode in ["a4", "both"]:
                print("   🖨️  A4打印版:")
                print(f"      封面: {self.output_dir}/封面-A4打印版.pdf")
                print(f"      后封面: {self.output_dir}/后封面-A4打印版.pdf")
            
            print("\n📋 打印说明:")
            if print_mode in ["a4", "both"]:
                print("   🖨️ A4打印版使用说明:")
                print("      1. 直接使用A4纸打印，无需缩放")
                print("      2. 16开本内容会居中显示在A4纸上")
                print("      3. 打印后可以裁剪到16开本尺寸")
                print("      4. 建议使用厚一点的纸张（如卡纸）")
                
            if print_mode in ["professional", "both"]:
                print("   🏢 专业印刷版使用说明:")
                print("      1. 发送给专业印刷厂制作")
                print("      2. 要求16开本尺寸 (185mm × 260mm)")
                print("      3. 建议使用250g铜版纸")
                print("      4. 可要求覆膜等后处理工艺")
            
            return True
        else:
            print(f"❌ 部分封面导出失败 ({success_count}/{total_count})，请检查文件")
            return False

def main():
    """主函数"""
    print("📚 柯南侦探英语冒险 - 封面PDF导出工具")
    print("=" * 50)
    
    exporter = CoverExporter()
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        # 解析打印模式参数
        print_mode = "professional"  # 默认专业印刷版
        if len(sys.argv) > 2:
            mode_arg = sys.argv[2].lower()
            if mode_arg in ["a4", "家庭", "打印"]:
                print_mode = "a4"
            elif mode_arg in ["both", "all", "全部"]:
                print_mode = "both"
        
        if arg in ["front", "封面"]:
            exporter.export_front_cover(print_mode)
        elif arg in ["back", "后封面"]:
            exporter.export_back_cover(print_mode)
        elif arg in ["a4", "家庭", "打印"]:
            exporter.export_both_covers("a4")
        elif arg in ["professional", "专业", "印刷"]:
            exporter.export_both_covers("professional")
        elif arg in ["both", "all", "全部"]:
            exporter.export_both_covers("both")
        elif arg in ["help", "-h", "--help", "帮助"]:
            print_help()
        else:
            print(f"❌ 未知参数: {arg}")
            print_help()
    else:
        # 默认导出A4打印版（更适合大多数用户）
        exporter.export_both_covers("a4")

def print_help():
    """显示帮助信息"""
    print("📋 使用说明:")
    print("   python export_cover.py [命令] [模式]")
    print("")
    print("🎯 命令选项:")
    print("   front/封面     - 仅导出封面")
    print("   back/后封面    - 仅导出后封面")
    print("   a4/家庭/打印   - 导出A4打印版封面")
    print("   professional/专业/印刷 - 导出专业印刷版封面")
    print("   both/all/全部  - 导出所有版本")
    print("   help/帮助      - 显示此帮助")
    print("")
    print("🎨 模式选项（配合front/back使用）:")
    print("   a4            - A4打印版")
    print("   professional  - 专业印刷版")
    print("   both          - 两种版本都导出")
    print("")
    print("💡 使用示例:")
    print("   python export_cover.py              # 导出A4打印版（推荐）")
    print("   python export_cover.py a4           # 导出A4打印版")
    print("   python export_cover.py both         # 导出所有版本")
    print("   python export_cover.py front a4     # 仅导出封面A4版")
    print("   python export_cover.py professional # 导出专业印刷版")

if __name__ == "__main__":
    main()