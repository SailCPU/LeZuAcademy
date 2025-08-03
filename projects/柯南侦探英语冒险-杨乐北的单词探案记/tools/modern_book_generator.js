#!/usr/bin/env node
/**
 * 现代书籍生成器 - Node.js版本
 * 使用现代Web技术栈实现专业书籍排版
 */

const fs = require('fs').promises;
const path = require('path');
const { JSDOM } = require('jsdom');

class ModernBookGenerator {
    constructor() {
        this.baseDir = path.join(__dirname, '..');
        this.outputDir = path.join(this.baseDir, 'output', 'modern');
        this.chaptersDir = path.join(this.baseDir, 'chapters');
        
        // 确保输出目录存在
        this.ensureDir(this.outputDir);
        
        // 设计系统配置
        this.designSystem = {
            colors: {
                primary: '#1a1a1a',
                secondary: '#4a5568',
                accent: '#3182ce',
                success: '#38a169',
                warning: '#d69e2e',
                error: '#e53e3e',
                background: '#ffffff',
                surface: '#f7fafc'
            },
            typography: {
                fonts: {
                    sans: '"Inter", "SF Pro Display", -apple-system, sans-serif',
                    serif: '"Merriweather", "Georgia", serif',
                    mono: '"JetBrains Mono", "SF Mono", monospace'
                },
                sizes: {
                    xs: '0.75rem',
                    sm: '0.875rem',
                    base: '1rem',
                    lg: '1.125rem',
                    xl: '1.25rem',
                    '2xl': '1.5rem',
                    '3xl': '1.875rem',
                    '4xl': '2.25rem'
                }
            },
            spacing: {
                px: '1px',
                0: '0',
                1: '0.25rem',
                2: '0.5rem',
                3: '0.75rem',
                4: '1rem',
                5: '1.25rem',
                6: '1.5rem',
                8: '2rem',
                10: '2.5rem',
                12: '3rem',
                16: '4rem',
                20: '5rem',
                24: '6rem'
            }
        };
    }
    
    async ensureDir(dir) {
        try {
            await fs.mkdir(dir, { recursive: true });
        } catch (error) {
            if (error.code !== 'EEXIST') throw error;
        }
    }
    
    /**
     * 生成CSS设计系统
     */
    generateDesignSystemCSS() {
        const { colors, typography, spacing } = this.designSystem;
        
        return `
        :root {
            /* 色彩系统 */
            ${Object.entries(colors).map(([key, value]) => 
                `--color-${key}: ${value};`
            ).join('\n            ')}
            
            /* 字体系统 */
            ${Object.entries(typography.fonts).map(([key, value]) => 
                `--font-${key}: ${value};`
            ).join('\n            ')}
            
            /* 字号系统 */
            ${Object.entries(typography.sizes).map(([key, value]) => 
                `--text-${key}: ${value};`
            ).join('\n            ')}
            
            /* 间距系统 */
            ${Object.entries(spacing).map(([key, value]) => 
                `--space-${key}: ${value};`
            ).join('\n            ')}
        }
        
        /* 响应式字体缩放 */
        @media print {
            :root {
                --text-xs: 10pt;
                --text-sm: 11pt;
                --text-base: 12pt;
                --text-lg: 14pt;
                --text-xl: 16pt;
                --text-2xl: 20pt;
                --text-3xl: 24pt;
                --text-4xl: 28pt;
            }
        }`;
    }
    
    /**
     * 生成专业排版CSS
     */
    generateTypographyCSS() {
        return `
        /* 专业排版系统 */
        
        /* 基础重置 */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        html {
            font-size: var(--text-base);
            line-height: 1.6;
            font-family: var(--font-sans);
            color: var(--color-primary);
            background: var(--color-background);
        }
        
        /* 标题层次 */
        h1, h2, h3, h4, h5, h6 {
            font-family: var(--font-serif);
            font-weight: 600;
            line-height: 1.2;
            margin-bottom: var(--space-4);
            page-break-after: avoid;
        }
        
        h1 { font-size: var(--text-4xl); margin-bottom: var(--space-8); }
        h2 { font-size: var(--text-3xl); margin-bottom: var(--space-6); }
        h3 { font-size: var(--text-2xl); margin-bottom: var(--space-5); }
        h4 { font-size: var(--text-xl); margin-bottom: var(--space-4); }
        h5 { font-size: var(--text-lg); margin-bottom: var(--space-3); }
        h6 { font-size: var(--text-base); margin-bottom: var(--space-2); }
        
        /* 段落系统 */
        p {
            margin-bottom: var(--space-4);
            text-align: justify;
            hyphens: auto;
            orphans: 2;
            widows: 2;
        }
        
        /* 首行缩进 */
        .paragraph-indent {
            text-indent: 2em;
        }
        
        /* 引言段落 */
        .lead {
            font-size: var(--text-lg);
            font-weight: 400;
            color: var(--color-secondary);
            margin-bottom: var(--space-6);
        }
        
        /* 列表系统 */
        ul, ol {
            margin: var(--space-4) 0;
            padding-left: var(--space-6);
        }
        
        li {
            margin-bottom: var(--space-2);
            line-height: 1.5;
        }
        
        /* 图片系统 */
        img {
            max-width: 100%;
            height: auto;
            page-break-inside: avoid;
        }
        
        figure {
            margin: var(--space-8) 0;
            text-align: center;
            page-break-inside: avoid;
        }
        
        figcaption {
            font-size: var(--text-sm);
            color: var(--color-secondary);
            margin-top: var(--space-2);
            font-style: italic;
        }
        
        /* 表格系统 */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: var(--space-6) 0;
            page-break-inside: avoid;
        }
        
        th, td {
            padding: var(--space-3);
            border: 1px solid var(--color-secondary);
            text-align: left;
        }
        
        th {
            background: var(--color-surface);
            font-weight: 600;
        }
        
        /* 代码系统 */
        code {
            font-family: var(--font-mono);
            font-size: 0.9em;
            background: var(--color-surface);
            padding: var(--space-1) var(--space-2);
            border-radius: 4px;
        }
        
        pre {
            font-family: var(--font-mono);
            background: var(--color-surface);
            padding: var(--space-4);
            border-radius: 8px;
            overflow-x: auto;
            margin: var(--space-6) 0;
            page-break-inside: avoid;
        }
        
        pre code {
            background: none;
            padding: 0;
        }`;
    }
    
    /**
     * 生成打印专用CSS
     */
    generatePrintCSS() {
        return `
        /* 专业打印样式 */
        @media print {
            @page {
                size: 185mm 260mm; /* 16开本 */
                margin: 20mm 15mm 25mm 25mm; /* 上右下左 */
                
                @top-left {
                    content: "柯南侦探英语冒险";
                    font-size: 9pt;
                    color: #666;
                }
                
                @bottom-right {
                    content: counter(page);
                    font-size: 10pt;
                }
            }
            
            @page :left {
                margin: 20mm 25mm 25mm 15mm;
            }
            
            @page :right {
                margin: 20mm 15mm 25mm 25mm;
            }
            
            @page cover {
                margin: 0;
                @top-left { content: none; }
                @bottom-right { content: none; }
            }
            
            /* 强制保持颜色 */
            * {
                -webkit-print-color-adjust: exact !important;
                color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            
            /* 页面控制 */
            .page-break { page-break-after: always; }
            .page-break-before { page-break-before: always; }
            .no-break { page-break-inside: avoid; }
            
            /* 隐藏非打印元素 */
            .no-print, nav, .sidebar {
                display: none !important;
            }
            
            /* 章节样式 */
            .chapter {
                page-break-before: always;
            }
            
            .chapter:first-child {
                page-break-before: auto;
            }
        }`;
    }
    
    /**
     * 读取HTML文件
     */
    async readHTMLFile(filename) {
        let filePath;
        
        if (['book_cover.html', 'book_back_cover.html', 'index.html'].includes(filename)) {
            filePath = path.join(this.baseDir, filename);
        } else {
            filePath = path.join(this.chaptersDir, filename);
        }
        
        try {
            return await fs.readFile(filePath, 'utf-8');
        } catch (error) {
            console.warn(`警告：无法读取文件 ${filename}`);
            return null;
        }
    }
    
    /**
     * 提取并清理内容
     */
    extractCleanContent(html) {
        if (!html) return '';
        
        const dom = new JSDOM(html);
        const document = dom.window.document;
        
        // 移除脚本和不需要的元素
        const unwantedSelectors = [
            'script',
            'noscript',
            '.no-print',
            '#pronunciation-guide',
            '.preview-note',
            '[style*="position: fixed"]'
        ];
        
        unwantedSelectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => el.remove());
        });
        
        // 获取body内容
        const body = document.querySelector('body');
        return body ? body.innerHTML : '';
    }
    
    /**
     * 生成现代化书籍HTML
     */
    async generateModernBook() {
        console.log('🚀 开始生成现代化书籍...');
        
        const chapters = [
            'book_cover.html',
            'index.html',
            'chapter01.html',
            'chapter02.html',
            'chapter03.html',
            'chapter04.html',
            'chapter05.html',
            'chapter06.html',
            'chapter07.html',
            'chapter08.html',
            'chapter09.html',
            'chapter10.html',
            'chapter11.html',
            'appendix.html',
            'book_back_cover.html'
        ];
        
        console.log('📖 处理章节内容...');
        const chapterContents = [];
        
        for (const [index, filename] of chapters.entries()) {
            console.log(`处理: ${filename}`);
            const html = await this.readHTMLFile(filename);
            const cleanContent = this.extractCleanContent(html);
            
            if (cleanContent) {
                const isLastChapter = index === chapters.length - 1;
                chapterContents.push(`
                    <div class="chapter" data-chapter="${filename}">
                        ${cleanContent}
                        ${!isLastChapter ? '<div class="page-break"></div>' : ''}
                    </div>
                `);
            }
        }
        
        console.log('🎨 生成设计系统...');
        const designSystemCSS = this.generateDesignSystemCSS();
        const typographyCSS = this.generateTypographyCSS();
        const printCSS = this.generatePrintCSS();
        
        const modernBookHTML = `
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>柯南侦探英语冒险：杨乐北的单词探案记 - 现代版</title>
            
            <!-- Google Fonts -->
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Merriweather:wght@300;400;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
            
            <style>
                /* 设计系统 */
                ${designSystemCSS}
                
                /* 排版系统 */
                ${typographyCSS}
                
                /* 打印样式 */
                ${printCSS}
                
                /* 自定义组件样式 */
                .word-card {
                    background: var(--color-surface);
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: var(--space-4);
                    margin: var(--space-3) 0;
                    page-break-inside: avoid;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                }
                
                .story-card {
                    background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
                    border-left: 4px solid var(--color-accent);
                    padding: var(--space-6);
                    margin: var(--space-8) 0;
                    border-radius: 0 8px 8px 0;
                    page-break-inside: avoid;
                }
                
                .chapter-intro {
                    background: var(--color-surface);
                    padding: var(--space-10);
                    margin: var(--space-12) 0;
                    border-radius: 12px;
                    text-align: center;
                    page-break-inside: avoid;
                    border: 2px solid #e2e8f0;
                }
                
                .vocabulary-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: var(--space-4);
                    margin: var(--space-8) 0;
                }
                
                .grammar-highlight {
                    border: 2px solid var(--color-accent);
                    border-radius: 8px;
                    padding: var(--space-6);
                    margin: var(--space-6) 0;
                    background: rgba(49, 130, 206, 0.05);
                    page-break-inside: avoid;
                }
                
                /* 屏幕预览样式 */
                @media screen {
                    body {
                        max-width: 800px;
                        margin: 0 auto;
                        padding: var(--space-8);
                        background: #f8f9fa;
                    }
                    
                    .chapter {
                        background: white;
                        padding: var(--space-8);
                        margin-bottom: var(--space-8);
                        border-radius: 12px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
                    }
                    
                    .page-break {
                        border-top: 2px dashed #cbd5e0;
                        margin: var(--space-8) 0;
                        padding-top: var(--space-4);
                        text-align: center;
                        color: #718096;
                        font-size: var(--text-sm);
                    }
                    
                    .page-break::after {
                        content: "— 页面分隔 —";
                    }
                }
                
                /* 打印优化 */
                @media print {
                    .chapter {
                        background: white;
                        padding: 0;
                        margin: 0;
                    }
                }
            </style>
        </head>
        <body>
            <div class="book-container">
                ${chapterContents.join('')}
            </div>
        </body>
        </html>`;
        
        const outputPath = path.join(this.outputDir, '柯南侦探英语冒险-现代版.html');
        await fs.writeFile(outputPath, modernBookHTML, 'utf-8');
        
        console.log('✅ 现代化书籍生成完成！');
        console.log(`📄 输出文件: ${outputPath}`);
        
        // 生成使用说明
        await this.generateUsageGuide();
        
        return outputPath;
    }
    
    /**
     * 生成使用说明
     */
    async generateUsageGuide() {
        const guide = `
# 现代Web技术书籍设计系统

## 🚀 特性

- **设计系统**: 基于Design Tokens的可维护设计系统
- **响应式排版**: 屏幕和打印双重优化
- **专业品质**: 符合印刷标准的排版规范
- **模块化**: 可复用的组件系统
- **现代技术**: CSS Grid、Flexbox、自定义属性

## 💻 技术栈

- **CSS Grid/Flexbox**: 现代布局技术
- **CSS Custom Properties**: 设计令牌系统
- **Print CSS**: 专业打印样式
- **Web Fonts**: 高质量字体渲染
- **JavaScript**: 动态内容生成

## 🎨 设计系统

### 色彩系统
- Primary: #1a1a1a (主色)
- Secondary: #4a5568 (辅助色)
- Accent: #3182ce (强调色)
- Surface: #f7fafc (表面色)

### 字体系统
- Sans: Inter (无衬线字体)
- Serif: Merriweather (衬线字体)
- Mono: JetBrains Mono (等宽字体)

### 间距系统
- 基于 0.25rem (4px) 的倍数系统
- 响应式缩放支持

## 📖 使用方法

1. **浏览器预览**: 直接打开HTML文件
2. **打印PDF**: Ctrl+P → 保存为PDF
3. **自定义**: 修改CSS变量调整样式

## 🔧 自定义配置

\`\`\`css
:root {
  --color-primary: #your-color;
  --font-sans: "Your Font", sans-serif;
  --space-base: 1rem;
}
\`\`\`

## 📋 最佳实践

1. 使用语义化HTML结构
2. 保持设计一致性
3. 优化打印性能
4. 测试多种设备
5. 遵循无障碍标准

---

*生成时间: ${new Date().toLocaleString('zh-CN')}*
        `;
        
        const guidePath = path.join(this.outputDir, 'README.md');
        await fs.writeFile(guidePath, guide, 'utf-8');
    }
}

// CLI执行
async function main() {
    try {
        const generator = new ModernBookGenerator();
        await generator.generateModernBook();
    } catch (error) {
        console.error('❌ 生成失败:', error);
        process.exit(1);
    }
}

// 如果直接运行此脚本
if (require.main === module) {
    main();
}

module.exports = ModernBookGenerator;