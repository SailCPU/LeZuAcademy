#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人体细胞图片爬虫
专门爬取各种人体细胞的高质量图片，使用英文关键词从国外网站获取
"""

import os
import requests
import time
import random
from urllib.parse import urljoin, urlparse, quote
from bs4 import BeautifulSoup
import json
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cell_crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class CellImageCrawler:
    """人体细胞图片爬虫类"""
    
    def __init__(self, base_dir="images"):
        self.base_dir = Path(base_dir)
        self.cells_dir = self.base_dir / "人体细胞"
        self.session = requests.Session()
        
        # 设置请求头，模拟浏览器
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        })
        
        # 人体细胞分类定义（英文关键词）
        self.cell_categories = {
            "血液细胞": [
                "red blood cells", "erythrocytes", "white blood cells", "leukocytes",
                "platelets", "thrombocytes", "neutrophils", "lymphocytes", "monocytes",
                "eosinophils", "basophils", "plasma cells", "macrophages"
            ],
            "神经细胞": [
                "neurons", "nerve cells", "glial cells", "astrocytes", "oligodendrocytes",
                "microglia", "schwann cells", "motor neurons", "sensory neurons",
                "interneurons", "pyramidal cells", "purkinje cells"
            ],
            "肌肉细胞": [
                "muscle cells", "myocytes", "skeletal muscle cells", "cardiac muscle cells",
                "smooth muscle cells", "muscle fibers", "myofibrils", "cardiomyocytes",
                "satellite cells"
            ],
            "上皮细胞": [
                "epithelial cells", "squamous epithelium", "cuboidal epithelium",
                "columnar epithelium", "ciliated epithelium", "keratinocytes",
                "melanocytes", "goblet cells"
            ],
            "结缔组织细胞": [
                "fibroblasts", "chondrocytes", "osteoblasts", "osteocytes", "osteoclasts",
                "adipocytes", "fat cells", "cartilage cells", "bone cells"
            ],
            "免疫细胞": [
                "T cells", "B cells", "NK cells", "dendritic cells", "helper T cells",
                "cytotoxic T cells", "regulatory T cells", "memory cells"
            ],
            "干细胞": [
                "stem cells", "embryonic stem cells", "adult stem cells", "mesenchymal stem cells",
                "hematopoietic stem cells", "neural stem cells", "induced pluripotent stem cells"
            ],
            "生殖细胞": [
                "sperm cells", "egg cells", "oocytes", "spermatozoa", "gametes",
                "follicle cells", "granulosa cells"
            ],
            "消化系统细胞": [
                "hepatocytes", "liver cells", "pancreatic cells", "gastric cells",
                "intestinal cells", "enterocytes", "parietal cells", "chief cells"
            ],
            "肾脏细胞": [
                "kidney cells", "nephron cells", "glomerular cells", "tubular cells",
                "podocytes", "mesangial cells"
            ],
            "癌细胞": [
                "cancer cells", "tumor cells", "malignant cells", "carcinoma cells",
                "adenocarcinoma", "sarcoma cells", "leukemia cells"
            ],
            "细胞结构": [
                "cell nucleus", "mitochondria", "ribosomes", "endoplasmic reticulum",
                "golgi apparatus", "lysosomes", "cell membrane", "cytoplasm",
                "chromosomes", "DNA", "cell organelles"
            ]
        }
        
        # 创建目录结构
        self.create_directories()
        
    def create_directories(self):
        """创建图片存储目录"""
        for category in self.cell_categories.keys():
            directory = self.cells_dir / category
            directory.mkdir(parents=True, exist_ok=True)
            logging.info(f"创建目录: {directory}")
    
    def download_image(self, url, filename, save_dir):
        """下载单张图片"""
        try:
            # 随机延迟，避免请求过快
            time.sleep(random.uniform(2, 4))
            
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
    
    def search_bing_images(self, keyword, max_pages=3):
        """Bing图片搜索"""
        images = []
        
        for page in range(max_pages):
            # Bing图片搜索URL
            params = {
                'q': keyword,
                'first': page * 20 + 1,
                'count': 20,
                'mkt': 'en-US'
            }
            
            search_url = f"https://www.bing.com/images/search?q={quote(keyword)}&first={page * 20 + 1}&count=20&mkt=en-US"
            
            try:
                response = self.session.get(search_url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找图片链接
                img_elements = soup.find_all('img', {'class': 'mimg'})
                
                for img in img_elements:
                    src = img.get('src')
                    if src and src.startswith('http'):
                        images.append({
                            'url': src,
                            'title': img.get('alt', ''),
                            'keyword': keyword
                        })
                
                logging.info(f"Bing搜索 '{keyword}' 第{page+1}页，获取{len(img_elements)}张图片")
                time.sleep(random.uniform(3, 5))
                
            except Exception as e:
                logging.error(f"Bing搜索失败 {keyword} 第{page+1}页: {e}")
                continue
        
        return images
    
    def search_duckduckgo_images(self, keyword, max_results=30):
        """DuckDuckGo图片搜索"""
        images = []
        
        try:
            # DuckDuckGo图片搜索API
            search_url = f"https://duckduckgo.com/"
            
            # 首先获取搜索token
            response = self.session.get(search_url)
            
            # 然后进行图片搜索
            search_params = {
                'q': keyword,
                'iax': 'images',
                'ia': 'images'
            }
            
            response = self.session.get(search_url, params=search_params)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 简化的图片提取（实际的DuckDuckGo API更复杂）
            img_elements = soup.find_all('img')[:max_results]
            
            for img in img_elements:
                src = img.get('src')
                if src and 'http' in src:
                    images.append({
                        'url': src,
                        'title': img.get('alt', ''),
                        'keyword': keyword
                    })
            
            logging.info(f"DuckDuckGo搜索 '{keyword}'，获取{len(images)}张图片")
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            logging.error(f"DuckDuckGo搜索失败 {keyword}: {e}")
        
        return images
    
    def search_unsplash_images(self, keyword, max_results=20):
        """Unsplash图片搜索（使用公开API）"""
        images = []
        
        try:
            # Unsplash公开搜索URL
            search_url = f"https://unsplash.com/napi/search/photos"
            params = {
                'query': keyword,
                'per_page': max_results
            }
            
            response = self.session.get(search_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                for item in data.get('results', []):
                    if 'urls' in item and 'regular' in item['urls']:
                        images.append({
                            'url': item['urls']['regular'],
                            'title': item.get('alt_description', ''),
                            'keyword': keyword
                        })
                
                logging.info(f"Unsplash搜索 '{keyword}'，获取{len(images)}张图片")
            
            time.sleep(random.uniform(2, 3))
            
        except Exception as e:
            logging.error(f"Unsplash搜索失败 {keyword}: {e}")
        
        return images
    
    def categorize_cell(self, title, keyword):
        """根据标题和关键词对细胞图片进行分类"""
        title_lower = title.lower()
        keyword_lower = keyword.lower()
        
        # 检查各个细胞分类
        for category, cell_types in self.cell_categories.items():
            for cell_type in cell_types:
                if cell_type.lower() in title_lower or cell_type.lower() in keyword_lower:
                    return category
        
        # 默认分类为细胞结构
        return "细胞结构"
    
    def get_search_keywords(self):
        """获取搜索关键词列表"""
        keywords = []
        
        # 为每个分类生成搜索关键词
        for category, cell_types in self.cell_categories.items():
            for cell_type in cell_types:
                # 基础关键词
                keywords.append(cell_type)
                # 添加"microscopy"、"histology"等修饰词
                keywords.append(f"{cell_type} microscopy")
                keywords.append(f"{cell_type} histology")
                keywords.append(f"{cell_type} anatomy")
                
                # 为特定细胞类型添加特殊关键词
                if "cells" in cell_type:
                    keywords.append(f"{cell_type} structure")
                    keywords.append(f"{cell_type} function")
        
        # 添加一些通用的细胞学关键词
        general_keywords = [
            "human cells", "cell biology", "cell structure", "cell types",
            "cellular anatomy", "histological sections", "cell microscopy",
            "human histology", "cell morphology", "cellular organelles"
        ]
        keywords.extend(general_keywords)
        
        return keywords
    
    def run(self, max_images_per_category=25):
        """运行爬虫"""
        logging.info("开始爬取人体细胞图片...")
        
        keywords = self.get_search_keywords()
        random.shuffle(keywords)  # 随机打乱关键词顺序
        
        total_downloaded = 0
        category_counts = {category: 0 for category in self.cell_categories.keys()}
        
        for keyword in keywords[:50]:  # 限制关键词数量，避免过多
            if total_downloaded >= 300:
                break
                
            logging.info(f"搜索关键词: {keyword}")
            
            # 使用多个搜索源
            all_images = []
            
            # Bing搜索
            try:
                bing_images = self.search_bing_images(keyword, max_pages=2)
                all_images.extend(bing_images)
            except Exception as e:
                logging.error(f"Bing搜索出错: {e}")
            
            # Unsplash搜索
            try:
                unsplash_images = self.search_unsplash_images(keyword, max_results=10)
                all_images.extend(unsplash_images)
            except Exception as e:
                logging.error(f"Unsplash搜索出错: {e}")
            
            # 处理搜索结果
            for i, img_info in enumerate(all_images[:15]):  # 每个关键词最多15张图
                # 确定图片分类和保存目录
                category = self.categorize_cell(img_info.get('title', ''), img_info['keyword'])
                
                # 检查该分类是否已达到上限
                if category_counts[category] >= max_images_per_category:
                    continue
                
                save_dir = self.cells_dir / category
                
                # 生成文件名
                clean_keyword = keyword.replace(' ', '_').replace('microscopy', '').replace('histology', '').replace('anatomy', '')
                filename = f"{clean_keyword}_{category_counts[category]+1:03d}"
                
                # 下载图片
                success = self.download_image(
                    img_info['url'], 
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
            "细胞类型": list(self.cell_categories.keys())
        }
        
        # 统计各分类的实际图片数量
        for category_dir in self.cells_dir.iterdir():
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
        report_file = self.cells_dir / "下载报告.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logging.info(f"下载报告已保存: {report_file}")
        print("\n" + "="*60)
        print("🔬 人体细胞图片下载完成! 🔬")
        print(f"总共下载: {total_downloaded} 张图片")
        print("\n分类统计:")
        for category, stats in report["分类统计"].items():
            if stats["总数"] > 0:
                print(f"  📁 {category}: {stats['总数']} 张")
        print("="*60)

def main():
    """主函数"""
    print("🔬 人体细胞图片爬虫 🔬")
    print("专门爬取各种人体细胞的高质量图片（使用英文关键词）")
    print("-" * 50)
    
    # 询问用户配置
    print("\n配置选项:")
    print("1. 每个细胞类型下载多少张图片? (默认: 25)")
    max_images = input("请输入数字 (直接回车使用默认值): ").strip()
    
    try:
        max_images_per_category = int(max_images) if max_images else 25
    except ValueError:
        max_images_per_category = 25
        print("输入无效，使用默认值: 25")
    
    print(f"\n将为每个细胞类型下载最多 {max_images_per_category} 张图片")
    print("搜索源: Bing、Unsplash等国外网站")
    print("开始下载...\n")
    
    # 创建爬虫实例并运行
    crawler = CellImageCrawler()
    
    try:
        crawler.run(max_images_per_category=max_images_per_category)
    except KeyboardInterrupt:
        print("\n🛑 用户中断了程序")
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        logging.error(f"程序异常: {e}")

if __name__ == "__main__":
    main()