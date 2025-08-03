#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动物图片爬虫
用于收集各种动物图片和动图，作为书籍创作素材
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
        logging.FileHandler('animal_crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class AnimalImageCrawler:
    """动物图片爬虫类"""
    
    def __init__(self, base_dir="images"):
        self.base_dir = Path(base_dir)
        self.animals_dir = self.base_dir / "动物"
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
        
        # 动物分类定义
        self.animal_categories = {
            "猫科动物": ["猫", "老虎", "狮子", "豹子", "猎豹", "美洲豹", "山猫", "猞猁"],
            "犬科动物": ["狗", "狼", "狐狸", "郊狼", "小狗", "金毛", "哈士奇", "柴犬"],
            "鸟类": ["鸟", "老鹰", "鹦鹉", "企鹅", "孔雀", "猫头鹰", "燕子", "鸽子"],
            "海洋动物": ["鲸鱼", "海豚", "鲨鱼", "海龟", "章鱼", "水母", "海马", "螃蟹"],
            "农场动物": ["牛", "马", "羊", "猪", "鸡", "鸭", "鹅", "兔子"],
            "野生动物": ["大象", "长颈鹿", "河马", "犀牛", "斑马", "袋鼠", "熊猫", "考拉"],
            "小动物": ["松鼠", "刺猬", "仓鼠", "兔子", "小鸟", "小猫", "小狗", "小鸭"],
            "动图专区": ["动物动图", "可爱动物gif", "搞笑动物", "动物表情包"]
        }
        
        # 创建目录结构
        self.create_directories()
        
    def create_directories(self):
        """创建图片存储目录"""
        for category in self.animal_categories.keys():
            directory = self.animals_dir / category
            directory.mkdir(parents=True, exist_ok=True)
            logging.info(f"创建目录: {directory}")
    
    def download_image(self, url, filename, save_dir):
        """下载单张图片或动图"""
        try:
            # 随机延迟，避免请求过快
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # 检查是否为图片或动图
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
                
            # 记录文件大小信息
            file_size = len(response.content)
            file_size_mb = file_size / (1024 * 1024)
            logging.info(f"下载成功: {filename} ({file_size_mb:.2f}MB) -> {save_dir}")
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
    
    def search_baidu_images(self, keyword, max_pages=3, include_gif=False):
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
            
            # 如果搜索动图，添加gif参数
            if include_gif or 'gif' in keyword.lower() or '动图' in keyword:
                params['f'] = 'gif'
            
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
                                'keyword': keyword,
                                'is_gif': include_gif or 'gif' in keyword.lower()
                            })
                
                logging.info(f"百度搜索 '{keyword}' 第{page+1}页，获取{len(data.get('data', []))}张图片")
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                logging.error(f"百度搜索失败 {keyword} 第{page+1}页: {e}")
                continue
        
        return images
    
    def categorize_animal(self, title, keyword):
        """根据标题和关键词对动物图片进行分类"""
        title_lower = title.lower()
        keyword_lower = keyword.lower()
        
        # 检查是否为动图
        if any(gif_word in title_lower or gif_word in keyword_lower 
               for gif_word in ['gif', '动图', '表情包', '搞笑']):
            return "动图专区"
        
        # 检查各个动物分类
        for category, animals in self.animal_categories.items():
            if category == "动图专区":
                continue
            for animal in animals:
                if animal in title_lower or animal in keyword_lower:
                    return category
        
        # 默认分类为野生动物
        return "野生动物"
    
    def get_search_keywords(self):
        """获取搜索关键词列表"""
        keywords = []
        
        # 为每个分类生成搜索关键词
        for category, animals in self.animal_categories.items():
            for animal in animals:
                # 基础关键词
                keywords.append(animal)
                # 添加"高清"、"可爱"等修饰词
                keywords.append(f"{animal} 高清")
                keywords.append(f"可爱{animal}")
                
                # 为动图专区添加gif关键词
                if category == "动图专区" or animal in ["动物动图", "可爱动物gif"]:
                    keywords.append(f"{animal} gif")
                    keywords.append(f"{animal} 动图")
        
        # 添加一些通用的动物关键词
        general_keywords = [
            "野生动物", "动物世界", "可爱动物", "动物摄影",
            "萌宠", "动物园", "野生动物园", "动物高清壁纸",
            "动物gif", "搞笑动物", "动物表情包"
        ]
        keywords.extend(general_keywords)
        
        return keywords
    
    def run(self, max_images_per_category=50):
        """运行爬虫"""
        logging.info("开始爬取动物图片...")
        
        keywords = self.get_search_keywords()
        random.shuffle(keywords)  # 随机打乱关键词顺序
        
        total_downloaded = 0
        category_counts = {category: 0 for category in self.animal_categories.keys()}
        
        for keyword in keywords:
            # 检查是否需要搜索动图
            include_gif = 'gif' in keyword.lower() or '动图' in keyword
            
            logging.info(f"搜索关键词: {keyword}")
            images = self.search_baidu_images(keyword, max_pages=2, include_gif=include_gif)
            
            for i, img_info in enumerate(images):
                # 确定图片分类和保存目录
                category = self.categorize_animal(img_info['title'], img_info['keyword'])
                
                # 检查该分类是否已达到上限
                if category_counts[category] >= max_images_per_category:
                    continue
                
                save_dir = self.animals_dir / category
                
                # 生成文件名
                animal_name = keyword.replace(' ', '_').replace('可爱', '').replace('高清', '')
                filename = f"{animal_name}_{category_counts[category]+1:03d}"
                
                # 下载图片
                success = self.download_image(
                    img_info['middle_url'], 
                    filename, 
                    save_dir
                )
                
                if success:
                    total_downloaded += 1
                    category_counts[category] += 1
                
                # 控制总下载数量
                if total_downloaded >= 500:
                    logging.info("已下载500张图片，停止下载")
                    break
            
            if total_downloaded >= 500:
                break
            
            # 检查是否所有分类都已达到上限
            if all(count >= max_images_per_category for count in category_counts.values()):
                logging.info("所有分类都已达到下载上限")
                break
        
        logging.info(f"爬虫完成！总共下载了 {total_downloaded} 张图片")
        
        # 生成下载报告
        self.generate_report(total_downloaded, category_counts)
    
    def generate_report(self, total_downloaded, category_counts):
        """生成下载报告"""
        report = {
            "总下载数量": total_downloaded,
            "下载时间": time.strftime("%Y-%m-%d %H:%M:%S"),
            "分类统计": {},
            "动物类别": list(self.animal_categories.keys())
        }
        
        # 统计各分类的实际图片数量
        for category_dir in self.animals_dir.iterdir():
            if category_dir.is_dir():
                # 统计各种类型的文件
                jpg_count = len(list(category_dir.glob("*.jpg")))
                png_count = len(list(category_dir.glob("*.png")))
                gif_count = len(list(category_dir.glob("*.gif")))
                webp_count = len(list(category_dir.glob("*.webp")))
                total_count = jpg_count + png_count + gif_count + webp_count
                
                report["分类统计"][category_dir.name] = {
                    "总数": total_count,
                    "JPG": jpg_count,
                    "PNG": png_count,
                    "GIF": gif_count,
                    "WEBP": webp_count
                }
        
        # 保存报告
        report_file = self.animals_dir / "下载报告.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logging.info(f"下载报告已保存: {report_file}")
        print("\n" + "="*60)
        print("🐾 动物图片下载完成! 🐾")
        print(f"总共下载: {total_downloaded} 张图片")
        print("\n分类统计:")
        for category, stats in report["分类统计"].items():
            if stats["总数"] > 0:
                print(f"  📁 {category}: {stats['总数']} 张")
                if stats["GIF"] > 0:
                    print(f"     └─ 包含 {stats['GIF']} 张动图")
        print("="*60)

def main():
    """主函数"""
    print("🐾 动物图片爬虫 🐾")
    print("用于收集各种动物图片和动图作为书籍创作素材")
    print("-" * 50)
    
    # 询问用户配置
    print("\n配置选项:")
    print("1. 每个分类下载多少张图片? (默认: 50)")
    max_images = input("请输入数字 (直接回车使用默认值): ").strip()
    
    try:
        max_images_per_category = int(max_images) if max_images else 50
    except ValueError:
        max_images_per_category = 50
        print("输入无效，使用默认值: 50")
    
    print(f"\n将为每个动物分类下载最多 {max_images_per_category} 张图片")
    print("开始下载...\n")
    
    # 创建爬虫实例并运行
    crawler = AnimalImageCrawler()
    
    try:
        crawler.run(max_images_per_category=max_images_per_category)
    except KeyboardInterrupt:
        print("\n🛑 用户中断了程序")
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        logging.error(f"程序异常: {e}")

if __name__ == "__main__":
    main()