#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缓存区管理工具 - BeiTianDa项目
用于管理output缓存目录中的文件
"""

import os
import shutil
import datetime
from pathlib import Path
import argparse

class CacheManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / "output"
        self.pdf_dir = self.output_dir / "pdf"
        self.temp_dir = self.output_dir / "temp"
        self.logs_dir = self.output_dir / "logs"
        
        # 确保目录存在
        for dir_path in [self.pdf_dir, self.temp_dir, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def list_files(self, file_type=None):
        """列出缓存区文件"""
        print(f"📦 缓存区内容 ({self.output_dir})")
        print("=" * 50)
        
        if file_type is None or file_type == "pdf":
            print("\n📄 PDF文件:")
            pdf_files = list(self.pdf_dir.glob("*.pdf"))
            if pdf_files:
                for pdf_file in sorted(pdf_files):
                    size = self._format_size(pdf_file.stat().st_size)
                    mtime = datetime.datetime.fromtimestamp(pdf_file.stat().st_mtime)
                    print(f"  ✅ {pdf_file.name} ({size}) - {mtime.strftime('%Y-%m-%d %H:%M')}")
            else:
                print("  (暂无PDF文件)")
        
        if file_type is None or file_type == "temp":
            print("\n🗂️ 临时文件:")
            temp_files = list(self.temp_dir.rglob("*"))
            temp_files = [f for f in temp_files if f.is_file()]
            if temp_files:
                for temp_file in sorted(temp_files):
                    size = self._format_size(temp_file.stat().st_size)
                    rel_path = temp_file.relative_to(self.temp_dir)
                    print(f"  📄 {rel_path} ({size})")
            else:
                print("  (暂无临时文件)")
        
        if file_type is None or file_type == "logs":
            print("\n📊 日志文件:")
            log_files = list(self.logs_dir.glob("*.log"))
            if log_files:
                for log_file in sorted(log_files):
                    size = self._format_size(log_file.stat().st_size)
                    mtime = datetime.datetime.fromtimestamp(log_file.stat().st_mtime)
                    print(f"  📋 {log_file.name} ({size}) - {mtime.strftime('%Y-%m-%d %H:%M')}")
            else:
                print("  (暂无日志文件)")
    
    def clean_temp_files(self, days=7):
        """清理临时文件"""
        cutoff_time = datetime.datetime.now() - datetime.timedelta(days=days)
        cutoff_timestamp = cutoff_time.timestamp()
        
        cleaned_count = 0
        for temp_file in self.temp_dir.rglob("*"):
            if temp_file.is_file() and temp_file.stat().st_mtime < cutoff_timestamp:
                temp_file.unlink()
                cleaned_count += 1
                print(f"🗑️ 已删除临时文件: {temp_file.name}")
        
        if cleaned_count == 0:
            print("✅ 没有需要清理的临时文件")
        else:
            print(f"✅ 已清理 {cleaned_count} 个临时文件")
    
    def clean_logs(self, days=30):
        """清理日志文件"""
        cutoff_time = datetime.datetime.now() - datetime.timedelta(days=days)
        cutoff_timestamp = cutoff_time.timestamp()
        
        cleaned_count = 0
        for log_file in self.logs_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_timestamp:
                log_file.unlink()
                cleaned_count += 1
                print(f"🗑️ 已删除日志文件: {log_file.name}")
        
        if cleaned_count == 0:
            print("✅ 没有需要清理的日志文件")
        else:
            print(f"✅ 已清理 {cleaned_count} 个日志文件")
    
    def backup_pdfs(self, backup_dir=None):
        """备份PDF文件"""
        if backup_dir is None:
            backup_dir = Path.home() / "Documents" / "BeiTianDa_PDF_Backup"
        else:
            backup_dir = Path(backup_dir)
        
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建时间戳文件夹
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamped_backup = backup_dir / f"backup_{timestamp}"
        timestamped_backup.mkdir(exist_ok=True)
        
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        if not pdf_files:
            print("❌ 没有PDF文件需要备份")
            return
        
        copied_count = 0
        for pdf_file in pdf_files:
            backup_file = timestamped_backup / pdf_file.name
            shutil.copy2(pdf_file, backup_file)
            copied_count += 1
            print(f"📋 已备份: {pdf_file.name}")
        
        print(f"✅ 已备份 {copied_count} 个PDF文件到: {timestamped_backup}")
    
    def get_cache_size(self):
        """获取缓存区总大小"""
        total_size = 0
        for file_path in self.output_dir.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        
        return self._format_size(total_size)
    
    def _format_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes < 1024:
            return f"{size_bytes}B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f}KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f}MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f}GB"

def main():
    parser = argparse.ArgumentParser(description="BeiTianDa缓存区管理工具")
    parser.add_argument("command", choices=["list", "clean", "backup", "size"], 
                       help="操作命令")
    parser.add_argument("--type", choices=["pdf", "temp", "logs"], 
                       help="文件类型 (仅适用于list命令)")
    parser.add_argument("--days", type=int, default=7, 
                       help="清理天数 (默认7天，日志文件默认30天)")
    parser.add_argument("--backup-dir", 
                       help="备份目录路径")
    
    args = parser.parse_args()
    
    manager = CacheManager()
    
    if args.command == "list":
        manager.list_files(args.type)
    elif args.command == "clean":
        print("🧹 开始清理缓存...")
        manager.clean_temp_files(args.days)
        manager.clean_logs(30)  # 日志文件保留30天
    elif args.command == "backup":
        print("📦 开始备份PDF文件...")
        manager.backup_pdfs(args.backup_dir)
    elif args.command == "size":
        size = manager.get_cache_size()
        print(f"📊 缓存区总大小: {size}")

if __name__ == "__main__":
    main()