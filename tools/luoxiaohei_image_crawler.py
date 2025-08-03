#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
罗小黑战记图片爬虫
用于收集书籍创作素材
"""

import os
import requests
import time
import random
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import json
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class LuoXiaoHeiCrawler:
    """罗小黑战记图片爬虫类"""
    
    def __init__(self, base_dir="images"):
        self.base_dir = Path(base_dir)
        self.luoxiaohei_dir = self.base_dir / "罗小黑战记"
        self.session = requests.Session()
        
        # 设置请求头，模拟浏览器
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # 创建目录结构
        self.create_directories()
        
    def create_directories(self):
        """创建图片存储目录"""
        directories = [
            self.luoxiaohei_dir / "角色",
            self.luoxiaohei_dir / "场景",
            self.luoxiaohei_dir / "剧照",
            self.luoxiaohei_dir / "壁纸",
            self.luoxiaohei_dir / "其他"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logging.info(f"创建目录: {directory}")
    
    def download_image(self, url, filename, save_dir):
        """下载单张图片"""
        try:
            # 随机延迟，避免请求过快
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # 检查是否为图片
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type.lower():
                logging.warning(f"URL不是图片: {url}")
                return False
                
            # 确定文件扩展名
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                ext = self.get_image_extension(url, content_type)
                filename = f"{filename}{ext}"
            
            filepath = save_dir / filename
            
            # 检查文件是否已存在
            if filepath.exists():
                logging.info(f"文件已存在，跳过: {filename}")
                return True
                
            # 保存图片
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            logging.info(f"下载成功: {filename} -> {save_dir}")
            return True
            
        except Exception as e:
            logging.error(f"下载失败 {url}: {e}")
            return False
    
    def get_image_extension(self, url, content_type):
        """根据URL和content-type确定图片扩展名"""
        # 先尝试从URL获取扩展名
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        if path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            return os.path.splitext(path)[1]
        
        # 根据content-type确定扩展名
        if 'jpeg' in content_type:
            return '.jpg'
        elif 'png' in content_type:
            return '.png'
        elif 'gif' in content_type:
            return '.gif'
        elif 'webp' in content_type:
            return '.webp'
        else:
            return '.jpg'  # 默认使用jpg
    
    def search_baidu_images(self, keyword, max_pages=3):
        """百度图片搜索"""
        images = []
        base_url = "https://image.baidu.com/search/acjson"
        
        for page in range(max_pages):
            params = {
                'tn': 'resultjson_com',
                'word': keyword,
                'pn': page * 30,
                'rn': 30,
                'ct': 1,
                'ic': 0,
                'lm': -1,
                'nc': 1,
                'ie': 'utf-8',
                'oe': 'utf-8',
                'face': 0,
            }
            
            try:
                response = self.session.get(base_url, params=params, timeout=30)
                data = response.json()
                
                if 'data' in data:
                    for item in data['data']:
                        if 'thumbURL' in item and 'middleURL' in item:
                            images.append({
                                'thumb_url': item['thumbURL'],
                                'middle_url': item['middleURL'],
                                'title': item.get('fromPageTitle', ''),
                                'keyword': keyword
                            })
                
                logging.info(f"百度搜索 '{keyword}' 第{page+1}页，获取{len(data.get('data', []))}张图片")
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                logging.error(f"百度搜索失败 {keyword} 第{page+1}页: {e}")
                continue
        
        return images
    
    def categorize_image(self, title, keyword):
        """根据标题和关键词对图片进行分类"""
        title_lower = title.lower()
        keyword_lower = keyword.lower()
        
        # 角色相关关键词
        character_keywords = ['罗小黑', '小黑', '小白', '嘿咻', '周末', '老君', '无限', '谛听', '风息']
        if any(char in title_lower or char in keyword_lower for char in character_keywords):
            return "角色"
        
        # 场景相关关键词
        scene_keywords = ['背景', '场景', '森林', '城市', '建筑', '风景']
        if any(scene in title_lower or scene in keyword_lower for scene in scene_keywords):
            return "场景"
        
        # 剧照相关关键词
        still_keywords = ['剧照', '截图', '电影', '动画']
        if any(still in title_lower or still in keyword_lower for still in still_keywords):
            return "剧照"
        
        # 壁纸相关关键词
        wallpaper_keywords = ['壁纸', '桌面', 'wallpaper']
        if any(wallpaper in title_lower or wallpaper in keyword_lower for wallpaper in wallpaper_keywords):
            return "壁纸"
        
        return "其他"
    
    def run(self):
        """运行爬虫"""
        logging.info("开始爬取罗小黑战记图片...")
        
        # 搜索关键词列表
        keywords = [
            "罗小黑战记",
            "罗小黑战记 角色",
            "罗小黑战记 壁纸",
            "罗小黑战记 剧照",
            "罗小黑 小白",
            "罗小黑战记 动画",
        ]
        
        total_downloaded = 0
        
        for keyword in keywords:
            logging.info(f"搜索关键词: {keyword}")
            images = self.search_baidu_images(keyword, max_pages=2)
            
            for i, img_info in enumerate(images):
                # 确定图片分类和保存目录
                category = self.categorize_image(img_info['title'], img_info['keyword'])
                save_dir = self.luoxiaohei_dir / category
                
                # 生成文件名
                filename = f"{keyword}_{i+1:03d}"
                
                # 下载图片（优先下载中等尺寸图片）
                success = self.download_image(
                    img_info['middle_url'], 
                    filename, 
                    save_dir
                )
                
                if success:
                    total_downloaded += 1
                
                # 控制下载数量，避免过多
                if total_downloaded >= 100:
                    logging.info("已下载100张图片，停止下载")
                    break
            
            if total_downloaded >= 100:
                break
        
        logging.info(f"爬虫完成！总共下载了 {total_downloaded} 张图片")
        
        # 生成下载报告
        self.generate_report(total_downloaded)
    
    def generate_report(self, total_downloaded):
        """生成下载报告"""
        report = {
            "总下载数量": total_downloaded,
            "下载时间": time.strftime("%Y-%m-%d %H:%M:%S"),
            "分类统计": {}
        }
        
        # 统计各分类的图片数量
        for category_dir in self.luoxiaohei_dir.iterdir():
            if category_dir.is_dir():
                count = len(list(category_dir.glob("*")))
                report["分类统计"][category_dir.name] = count
        
        # 保存报告
        report_file = self.luoxiaohei_dir / "下载报告.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logging.info(f"下载报告已保存: {report_file}")
        print("\n" + "="*50)
        print("下载完成!")
        print(f"总共下载: {total_downloaded} 张图片")
        print("分类统计:")
        for category, count in report["分类统计"].items():
            print(f"  {category}: {count} 张")
        print("="*50)

def main():
    """主函数"""
    print("罗小黑战记图片爬虫")
    print("用于收集书籍创作素材")
    print("-" * 30)
    
    # 创建爬虫实例并运行
    crawler = LuoXiaoHeiCrawler()
    
    try:
        crawler.run()
    except KeyboardInterrupt:
        print("\n用户中断了程序")
    except Exception as e:
        print(f"程序运行出错: {e}")
        logging.error(f"程序异常: {e}")

if __name__ == "__main__":
    main()