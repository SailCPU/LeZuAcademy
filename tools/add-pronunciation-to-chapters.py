#!/usr/bin/env python3
"""
为所有章节添加单词发音功能
Add pronunciation feature to all chapters
"""

import os
import re
from pathlib import Path

def add_pronunciation_feature(file_path):
    """为单个章节文件添加发音功能"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经添加了发音功能
        if 'word-pronunciation.js' in content:
            print(f"✅ {file_path.name} 已经包含发音功能")
            return True
        
        # 更新CSS样式
        old_css = r'\.word-card\s*\{[^}]*\}'
        new_css = """        .word-card {
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            user-select: none;
        }
        
        .word-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border-color: #007bff;
        }"""
        
        content = re.sub(old_css, new_css, content)
        
        # 在</body>之前添加JavaScript和提示
        js_and_guide = """    
    <!-- 单词发音功能 Word Pronunciation Feature -->
    <script src="../js/word-pronunciation.js"></script>
    
    <!-- 发音功能使用说明提示 -->
    <div id="pronunciation-guide" style="position: fixed; bottom: 20px; right: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); max-width: 300px; font-size: 0.9em; z-index: 1000; opacity: 0; transition: opacity 0.5s ease;">
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 1.2em; margin-right: 8px;">🔊</span>
            <strong>单词发音功能已启用！</strong>
        </div>
        <p style="margin: 5px 0; font-size: 0.85em;">点击任意单词卡即可听到标准英语发音</p>
        <p style="margin: 5px 0; font-size: 0.85em;">Click any word card to hear pronunciation</p>
        <button onclick="this.parentElement.style.opacity='0'" style="position: absolute; top: 5px; right: 8px; background: none; border: none; color: white; cursor: pointer; font-size: 1.1em;">×</button>
    </div>
    
    <script>
        // 显示发音功能提示
        setTimeout(() => {
            const guide = document.getElementById('pronunciation-guide');
            if (guide) {
                guide.style.opacity = '1';
                // 5秒后自动隐藏
                setTimeout(() => {
                    guide.style.opacity = '0';
                }, 5000);
            }
        }, 2000);
    </script>
</body>"""
        
        # 替换</body>
        content = content.replace('</body>', js_and_guide)
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已为 {file_path.name} 添加发音功能")
        return True
        
    except Exception as e:
        print(f"❌ 处理 {file_path.name} 时出错: {e}")
        return False

def main():
    """主函数"""
    chapters_dir = Path("柯南侦探英语冒险-杨乐北的单词探案记/chapters")
    
    if not chapters_dir.exists():
        print("❌ 章节目录不存在")
        return
    
    # 获取所有章节文件
    chapter_files = list(chapters_dir.glob("chapter*.html"))
    
    if not chapter_files:
        print("❌ 没有找到章节文件")
        return
    
    print(f"🔍 找到 {len(chapter_files)} 个章节文件")
    print("📝 开始添加发音功能...\n")
    
    success_count = 0
    
    for chapter_file in sorted(chapter_files):
        if add_pronunciation_feature(chapter_file):
            success_count += 1
    
    print(f"\n🎉 完成！成功为 {success_count}/{len(chapter_files)} 个章节添加了发音功能")
    
    # 检查JavaScript文件是否存在
    js_file = Path("柯南侦探英语冒险-杨乐北的单词探案记/js/word-pronunciation.js")
    if js_file.exists():
        print("✅ JavaScript发音文件存在")
    else:
        print("❌ JavaScript发音文件不存在，请检查路径")

if __name__ == "__main__":
    main()