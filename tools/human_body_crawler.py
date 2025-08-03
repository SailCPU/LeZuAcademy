#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人体器官与细胞图片爬虫
用于收集人体器官、细胞等医学相关图片，作为书籍创作素材
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
        logging.FileHandler('human_body_crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class HumanBodyCrawler:
    """人体器官与细胞图片爬虫类"""
    
    def __init__(self, base_dir="images"):
        self.base_dir = Path(base_dir)
        self.human_body_dir = self.base_dir / "人体器官与细胞"
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
        
        # 人体器官与细胞分类定义
        self.body_categories = {
            "心血管系统": [
                "心脏", "血管", "动脉", "静脉", "毛细血管", "心脏解剖", "心脏结构",
                "血液循环", "心肌", "心房", "心室", "主动脉", "肺动脉"
            ],
            "呼吸系统": [
                "肺", "气管", "支气管", "肺泡", "鼻腔", "咽喉", "喉咙", 
                "呼吸道", "肺部结构", "气体交换", "肺叶", "胸腔"
            ],
            "消化系统": [
                "胃", "肝脏", "肠道", "小肠", "大肠", "食道", "胰腺", "胆囊",
                "十二指肠", "结肠", "直肠", "消化道", "胃壁", "肠绒毛"
            ],
            "神经系统": [
                "大脑", "脊髓", "神经", "神经元", "大脑皮层", "小脑", "脑干",
                "神经细胞", "突触", "脑部结构", "中枢神经", "周围神经"
            ],
            "内分泌系统": [
                "甲状腺", "肾上腺", "胰岛", "垂体", "下丘脑", "性腺",
                "内分泌腺", "激素", "胰岛素", "甲状腺激素"
            ],
            "泌尿系统": [
                "肾脏", "膀胱", "输尿管", "尿道", "肾单位", "肾小球",
                "肾小管", "泌尿道", "肾脏结构", "排泄系统"
            ],
            "骨骼肌肉系统": [
                "骨骼", "肌肉", "关节", "骨头", "肌纤维", "骨骼结构",
                "肌肉组织", "骨细胞", "软骨", "韧带", "肌腱"
            ],
            "细胞类型": [
                "细胞", "红细胞", "白细胞", "血小板", "神经细胞", "肌细胞",
                "上皮细胞", "干细胞", "癌细胞", "细胞分裂", "细胞膜", "细胞核",
                "线粒体", "细胞器", "DNA", "染色体"
            ],
            "组织学": [
                "组织", "上皮组织", "结缔组织", "肌肉组织", "神经组织",
                "血液组织", "淋巴组织", "脂肪组织", "纤维组织"
            ],
            "医学影像": [
                "X光", "CT扫描", "MRI", "超声波", "医学影像", "解剖图",
                "人体结构图", "器官切片", "组织切片", "病理图片"
            ]
        }
        
        # 创建目录结构
        self.create_directories()
        
    def create_directories(self):
        """创建图片存储目录"""
        for category in self.body_categories.keys():
            directory = self.human_body_dir / category
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
    
    def categorize_body_part(self, title, keyword):
        """根据标题和关键词对人体器官图片进行分类"""
        title_lower = title.lower()
        keyword_lower = keyword.lower()
        
        # 检查各个人体系统分类
        for category, parts in self.body_categories.items():
            for part in parts:
                if part in title_lower or part in keyword_lower:
                    return category
        
        # 如果包含医学、解剖等通用词汇，归类到医学影像
        medical_terms = ['医学', '解剖', '生物', '生理', '病理', '临床']
        if any(term in title_lower or term in keyword_lower for term in medical_terms):
            return "医学影像"
        
        # 默认分类为医学影像
        return "医学影像"
    
    def get_search_keywords(self):
        """获取搜索关键词列表"""
        keywords = []
        
        # 为每个分类生成搜索关键词
        for category, parts in self.body_categories.items():
            for part in parts:
                # 基础关键词
                keywords.append(part)
                # 添加"解剖"、"结构"等修饰词
                keywords.append(f"{part} 解剖")
                keywords.append(f"{part} 结构")
                keywords.append(f"{part} 医学")
                
                # 为细胞相关添加显微镜关键词
                if "细胞" in part:
                    keywords.append(f"{part} 显微镜")
                    keywords.append(f"{part} 电镜")
        
        # 添加一些通用的医学关键词
        general_keywords = [
            "人体解剖", "人体结构", "医学图谱", "解剖学",
            "生理学", "组织学", "细胞生物学", "人体器官",
            "医学插图", "解剖图", "人体系统", "生物医学",
            "临床解剖", "病理解剖", "功能解剖"
        ]
        keywords.extend(general_keywords)
        
        return keywords
    
    def run(self, max_images_per_category=30):
        """运行爬虫"""
        logging.info("开始爬取人体器官与细胞图片...")
        
        keywords = self.get_search_keywords()
        random.shuffle(keywords)  # 随机打乱关键词顺序
        
        total_downloaded = 0
        category_counts = {category: 0 for category in self.body_categories.keys()}
        
        for keyword in keywords:
            logging.info(f"搜索关键词: {keyword}")
            images = self.search_baidu_images(keyword, max_pages=2)
            
            for i, img_info in enumerate(images):
                # 确定图片分类和保存目录
                category = self.categorize_body_part(img_info['title'], img_info['keyword'])
                
                # 检查该分类是否已达到上限
                if category_counts[category] >= max_images_per_category:
                    continue
                
                save_dir = self.human_body_dir / category
                
                # 生成文件名
                clean_keyword = keyword.replace(' ', '_').replace('解剖', '').replace('结构', '').replace('医学', '')
                filename = f"{clean_keyword}_{category_counts[category]+1:03d}"
                
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
                if total_downloaded >= 300:
                    logging.info("已下载300张图片，停止下载")
                    break
            
            if total_downloaded >= 300:
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
            "人体系统": list(self.body_categories.keys())
        }
        
        # 统计各分类的实际图片数量
        for category_dir in self.human_body_dir.iterdir():
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
        report_file = self.human_body_dir / "下载报告.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logging.info(f"下载报告已保存: {report_file}")
        print("\n" + "="*60)
        print("🧬 人体器官与细胞图片下载完成! 🧬")
        print(f"总共下载: {total_downloaded} 张图片")
        print("\n分类统计:")
        for category, stats in report["分类统计"].items():
            if stats["总数"] > 0:
                print(f"  📁 {category}: {stats['总数']} 张")
        print("="*60)

def main():
    """主函数"""
    print("🧬 人体器官与细胞图片爬虫 🧬")
    print("用于收集人体器官、细胞等医学图片作为书籍创作素材")
    print("-" * 50)
    
    # 询问用户配置
    print("\n配置选项:")
    print("1. 每个分类下载多少张图片? (默认: 30)")
    max_images = input("请输入数字 (直接回车使用默认值): ").strip()
    
    try:
        max_images_per_category = int(max_images) if max_images else 30
    except ValueError:
        max_images_per_category = 30
        print("输入无效，使用默认值: 30")
    
    print(f"\n将为每个人体系统分类下载最多 {max_images_per_category} 张图片")
    print("开始下载...\n")
    
    # 创建爬虫实例并运行
    crawler = HumanBodyCrawler()
    
    try:
        crawler.run(max_images_per_category=max_images_per_category)
    except KeyboardInterrupt:
        print("\n🛑 用户中断了程序")
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        logging.error(f"程序异常: {e}")

if __name__ == "__main__":
    main()