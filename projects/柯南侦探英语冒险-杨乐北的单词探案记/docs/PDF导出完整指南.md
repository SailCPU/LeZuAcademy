# 📄 PDF导出完整指南

## 🎯 导出方式对比

我们提供两种PDF导出方式，您可以根据需要选择：

### 🌟 方式一：浏览器一键导出（推荐）

**适用场景**：快速导出、简单使用

1. 打开项目首页 `index.html`
2. 找到"📄 PDF导出"部分  
3. 点击"📄 导出完整书籍为PDF"按钮
4. **系统自动完成**：
   - 🚀 自动打开完整版本
   - 📄 自动开始生成PDF
   - 💾 自动下载到您的下载文件夹

**特点**：
- ✅ 无需安装额外软件
- ✅ 一键操作，完全自动化
- ✅ 支持所有现代浏览器
- ✅ 生成速度快

### 🔧 方式二：Python脚本导出（高级）

**适用场景**：批量处理、高质量输出、自定义设置

#### 🛠️ 准备工作

1. **安装Python环境**（Python 3.7+）
2. **安装依赖包**：
   ```bash
   cd tools
   pip install -r requirements_pdf.txt
   ```

#### 🚀 使用方法

**Windows用户**：
```bash
cd tools
export_pdf.bat
```

**Mac/Linux用户**：
```bash
cd tools
chmod +x export_pdf.sh
./export_pdf.sh
```

**手动运行**：
```bash
cd tools
python export_to_pdf.py
```

**特点**：
- ✅ 高质量PDF输出
- ✅ 支持自定义样式
- ✅ 适合批量处理
- ✅ 可编程化控制

## 🔧 系统依赖安装

### Linux/Ubuntu
```bash
sudo apt-get install python3-dev python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

### macOS
```bash
brew install cairo pango gdk-pixbuf libffi
```

### Windows
```bash
pip install --upgrade pip
pip install weasyprint
```

## 📁 输出文件

两种方式都会生成：`柯南侦探英语冒险：杨乐北的单词探案记.pdf`

**内容包含**：
- ✅ 精美的封面页
- ✅ 完整的目录
- ✅ 全部11个章节内容  
- ✅ 附录：魔法词典和参考答案
- ✅ 保持原有样式和格式
- ✅ 适合A4纸张打印

## 🛠️ 常见问题解决

### 1. 浏览器导出问题
- 确保使用最新版本的Chrome、Firefox或Edge
- 如果自动下载失败，可使用浏览器打印功能手动保存

### 2. Python脚本问题
- 检查Python版本：`python --version`
- 重新安装依赖：`pip install -r requirements_pdf.txt`
- 检查文件路径是否正确

### 3. 字体显示问题
- 确保系统已安装"微软雅黑"字体
- Linux用户可能需要安装中文字体包

### 4. 权限问题
- 确保有文件写入权限
- Windows用户可能需要以管理员身份运行

## 📋 技术说明

### 浏览器方式
- 使用现代浏览器的原生PDF生成功能
- 基于CSS打印样式优化
- 支持JavaScript交互元素

### Python方式  
- HTML解析：BeautifulSoup4
- PDF生成：WeasyPrint
- 样式处理：CSS + 打印优化
- 编码：UTF-8中文支持

## 🎯 推荐使用场景

| 使用场景 | 推荐方式 | 原因 |
|---------|---------|------|
| 快速查看 | 浏览器导出 | 简单快速 |
| 教学使用 | 浏览器导出 | 易于操作 |
| 批量制作 | Python脚本 | 可自动化 |
| 高质量印刷 | Python脚本 | 输出质量高 |
| 自定义样式 | Python脚本 | 可编程控制 |

---

**制作理念**：为不同技术水平的用户提供适合的PDF导出方案，让优质内容能够方便地转换为纸质材料！