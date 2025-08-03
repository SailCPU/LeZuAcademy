# PDF导出功能使用说明

本工具可以将各个章节的HTML文件直接合并导出为一个完整的PDF文档，无需手动复制粘贴。

## 安装依赖

### 方法一：使用pip安装（推荐）

```bash
pip install -r requirements_pdf.txt
```

### 方法二：单独安装

```bash
pip install weasyprint beautifulsoup4 lxml
```

### 系统依赖（Linux/Ubuntu）

如果在Linux系统上安装weasyprint遇到问题，可能需要安装系统依赖：

```bash
sudo apt-get install python3-dev python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

### 系统依赖（macOS）

```bash
brew install cairo pango gdk-pixbuf libffi
```

### 系统依赖（Windows）

Windows用户建议使用预编译的wheel包：

```bash
pip install --upgrade pip
pip install weasyprint
```

## 使用方法

### 基本使用

在项目根目录执行：

```bash
cd 柯南侦探英语冒险-杨乐北的单词探案记
python export_to_pdf.py
```

### 脚本功能

1. **自动读取章节**: 按顺序读取所有章节文件（chapter01.html 到 chapter11.html）
2. **包含目录和附录**: 自动包含index.html（目录）和appendix.html（附录）
3. **样式保持**: 保持原有的CSS样式和格式
4. **图片处理**: 自动处理图片路径，确保在PDF中正确显示
5. **分页优化**: 自动在章节间添加分页符
6. **打印优化**: 针对PDF打印进行样式优化

### 输出文件

导出的PDF文件将保存为：`柯南侦探英语冒险：杨乐北的单词探案记.pdf`

## 文件结构要求

确保以下文件存在：

```
柯南侦探英语冒险-杨乐北的单词探案记/
├── chapters/
│   ├── index.html          # 目录页
│   ├── chapter01.html      # 第1章
│   ├── chapter02.html      # 第2章
│   ├── ...                 # 其他章节
│   ├── chapter11.html      # 第11章
│   └── appendix.html       # 附录
├── images/                 # 图片文件夹
├── style.css              # 样式文件
└── export_to_pdf.py       # 导出脚本
```

## 特性说明

### 1. 智能内容合并
- 自动提取每个HTML文件的内容部分
- 去除重复的导航元素
- 合并所有CSS样式

### 2. 分页控制
- 每个章节自动分页
- 避免在不合适的位置分页
- 优化标题和内容的分页处理

### 3. 样式优化
- 针对PDF打印优化CSS样式
- 确保字体和颜色在PDF中正确显示
- 自动处理背景和阴影效果

### 4. 图片处理
- 自动修复相对路径
- 确保图片在PDF中正确显示
- 防止图片被分页截断

## 常见问题解决

### 1. 安装weasyprint失败

如果遇到安装问题，可以尝试：

```bash
# 升级pip
pip install --upgrade pip

# 使用conda安装（如果有conda环境）
conda install -c conda-forge weasyprint

# 或者使用系统包管理器安装依赖后再用pip
```

### 2. 字体显示问题

如果PDF中字体显示不正确，可以：
- 确保系统已安装"微软雅黑"字体
- 或修改脚本中的字体设置

### 3. 图片不显示

如果PDF中图片不显示：
- 检查images文件夹是否存在
- 确保图片文件路径正确
- 检查图片文件权限

### 4. 内存不足

如果处理大文件时内存不足：
- 尝试关闭其他程序
- 或分批处理章节

## 自定义选项

可以修改脚本中的以下设置：

```python
# 修改章节文件列表
self.chapter_files = [
    "index.html",
    "chapter01.html",
    # ... 添加或删除章节
]

# 修改输出文件名
self.output_file = self.base_dir / "自定义文件名.pdf"
```

## 注意事项

1. **文件编码**: 确保所有HTML文件使用UTF-8编码
2. **路径问题**: 确保在正确的目录下运行脚本
3. **权限问题**: 确保有写入权限生成PDF文件
4. **文件大小**: 生成的PDF文件可能较大，请确保有足够的磁盘空间

## 技术说明

- **HTML解析**: 使用BeautifulSoup4解析HTML
- **PDF生成**: 使用WeasyPrint将HTML转换为PDF
- **样式处理**: 保持原有CSS样式并优化PDF显示效果
- **编码处理**: 全程使用UTF-8编码确保中文正确显示

## 更新日志

### v1.0 (2024)
- 初始版本
- 支持自动读取所有章节
- 支持图片和样式处理
- 支持分页优化

如有问题，请检查依赖安装和文件路径是否正确。