#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理未使用的图片文件
自动识别并删除项目中未被引用的图片
"""

import os
import sys
import shutil
from pathlib import Path
import re
from datetime import datetime

class ImageCleaner:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.images_dir = self.base_dir / "assets" / "images"
        self.chapters_dir = self.base_dir / "chapters"
        self.cache_dir = self.base_dir / "cache" / "unused_images_backup"
        
        # 创建备份目录
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 已知被使用的图片（从搜索结果中获得）
        self.used_images = {
            "magic_ball.jpg",
            "erythrocytes__020.jpg",
            "罗小黑战记/角色/罗小黑战记 角色_001.webp",
            "罗小黑战记/角色/罗小黑战记 角色_003.webp", 
            "罗小黑战记/角色/罗小黑战记 角色_005.webp",
            "罗小黑战记/角色/罗小黑战记 角色_007.webp"
        }
        
        # 支持的图片格式
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg'}
        
    def scan_html_files(self):
        """扫描所有HTML文件，查找图片引用"""
        print("🔍 扫描HTML文件中的图片引用...")
        
        found_images = set()
        
        # 扫描所有HTML文件
        html_files = list(self.base_dir.glob("**/*.html"))
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 查找图片引用
                # 匹配 src="..." 和 src='...' 格式
                img_pattern = r'src=["\'](.*?)["\']'
                matches = re.findall(img_pattern, content, re.IGNORECASE)
                
                for match in matches:
                    # 只处理指向images目录的引用
                    if 'images/' in match:
                        # 提取相对于images目录的路径
                        img_path = match.split('images/')[-1]
                        found_images.add(img_path)
                        
            except Exception as e:
                print(f"   ⚠️ 读取文件失败 {html_file}: {e}")
        
        print(f"   ✅ 发现 {len(found_images)} 个被引用的图片")
        return found_images
    
    def find_all_images(self):
        """查找所有图片文件"""
        print("📂 扫描images目录中的所有图片...")
        
        all_images = []
        
        for root, dirs, files in os.walk(self.images_dir):
            for file in files:
                if Path(file).suffix.lower() in self.image_extensions:
                    # 计算相对于images目录的路径
                    rel_path = os.path.relpath(
                        os.path.join(root, file), 
                        self.images_dir
                    )
                    all_images.append(rel_path)
        
        print(f"   ✅ 发现 {len(all_images)} 个图片文件")
        return all_images
    
    def get_file_size(self, file_path):
        """获取文件大小（人类可读格式）"""
        try:
            size = file_path.stat().st_size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"
        except:
            return "未知"
    
    def analyze_unused_images(self):
        """分析未使用的图片"""
        print("=" * 60)
        print("🎯 分析未使用的图片...")
        
        # 获取HTML中引用的图片
        used_in_html = self.scan_html_files()
        
        # 合并已知使用的图片
        all_used = self.used_images.union(used_in_html)
        
        # 获取所有图片文件
        all_images = self.find_all_images()
        
        # 找出未使用的图片
        unused_images = []
        for img in all_images:
            if img not in all_used:
                unused_images.append(img)
        
        print("=" * 60)
        print("📊 分析结果:")
        print(f"   总图片数量: {len(all_images)}")
        print(f"   正在使用: {len(all_used)}")
        print(f"   未使用: {len(unused_images)}")
        
        if unused_images:
            print("\n🗑️ 未使用的图片列表:")
            total_size = 0
            
            for img in unused_images:
                img_path = self.images_dir / img
                size_str = self.get_file_size(img_path)
                print(f"   📄 {img} ({size_str})")
                
                try:
                    total_size += img_path.stat().st_size
                except:
                    pass
            
            # 显示总大小
            total_size_str = ""
            for unit in ['B', 'KB', 'MB', 'GB']:
                if total_size < 1024:
                    total_size_str = f"{total_size:.1f} {unit}"
                    break
                total_size /= 1024
            
            print(f"\n💾 可清理空间: {total_size_str}")
        
        return unused_images
    
    def backup_and_clean(self, unused_images, backup_only=False):
        """备份并清理未使用的图片"""
        if not unused_images:
            print("✅ 没有发现未使用的图片，无需清理")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.cache_dir / f"backup_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📦 备份目录: {backup_dir}")
        
        success_count = 0
        error_count = 0
        
        for img in unused_images:
            try:
                src_path = self.images_dir / img
                dst_path = backup_dir / img
                
                # 创建目标目录
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 复制文件到备份目录
                shutil.copy2(src_path, dst_path)
                
                if not backup_only:
                    # 删除原文件
                    if src_path.is_file():
                        src_path.unlink()
                    elif src_path.is_dir() and not any(src_path.iterdir()):
                        # 删除空目录
                        src_path.rmdir()
                
                success_count += 1
                
            except Exception as e:
                print(f"   ❌ 处理失败 {img}: {e}")
                error_count += 1
        
        print(f"\n✅ 处理完成:")
        print(f"   成功: {success_count} 个文件")
        if error_count > 0:
            print(f"   失败: {error_count} 个文件")
        
        if not backup_only:
            print(f"   🗑️ 原文件已删除")
        print(f"   📦 备份保存在: {backup_dir}")
        
        # 清理空目录
        self.clean_empty_dirs()
    
    def clean_empty_dirs(self):
        """清理空目录"""
        try:
            for root, dirs, files in os.walk(self.images_dir, topdown=False):
                for dir_name in dirs:
                    dir_path = Path(root) / dir_name
                    try:
                        if dir_path.is_dir() and not any(dir_path.iterdir()):
                            dir_path.rmdir()
                            print(f"   🗂️ 删除空目录: {dir_path.relative_to(self.images_dir)}")
                    except:
                        pass
        except:
            pass

def main():
    """主函数"""
    print("🧹 图片清理工具 - 柯南侦探英语冒险")
    print("=" * 60)
    
    cleaner = ImageCleaner()
    
    # 分析未使用的图片
    unused_images = cleaner.analyze_unused_images()
    
    if not unused_images:
        print("\n🎉 恭喜！没有发现未使用的图片")
        return
    
    print("\n" + "=" * 60)
    print("🤔 清理选项:")
    print("1. 仅备份（不删除原文件）")
    print("2. 备份并删除原文件")
    print("3. 取消操作")
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("\n请选择操作 (1/2/3): ").strip()
    
    if choice == "1":
        print("\n📦 开始备份未使用的图片...")
        cleaner.backup_and_clean(unused_images, backup_only=True)
        print("\n💡 原文件保持不变，已创建备份")
        
    elif choice == "2":
        print(f"\n⚠️ 即将删除 {len(unused_images)} 个未使用的图片文件")
        
        if len(sys.argv) <= 1:  # 交互模式
            confirm = input("确认删除吗？(yes/no): ").strip().lower()
            if confirm not in ['yes', 'y', '是', '确定']:
                print("❌ 操作已取消")
                return
        
        print("\n🗑️ 开始备份并删除未使用的图片...")
        cleaner.backup_and_clean(unused_images, backup_only=False)
        print("\n✅ 清理完成！空间已释放")
        
    else:
        print("❌ 操作已取消")

if __name__ == "__main__":
    main()