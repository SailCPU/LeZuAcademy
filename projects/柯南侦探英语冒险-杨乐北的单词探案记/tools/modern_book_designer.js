/**
 * 现代Web技术书籍设计工具
 * 使用最新的Web标准实现专业级书籍排版
 */

class ModernBookDesigner {
    constructor(options = {}) {
        this.config = {
            // 书籍规格配置
            format: options.format || '16K', // 16K, A4, A5
            orientation: options.orientation || 'portrait',
            
            // 印刷规格
            dpi: options.dpi || 300,
            colorMode: options.colorMode || 'CMYK',
            bleed: options.bleed || '3mm',
            
            // 页面布局
            margins: {
                top: '20mm',
                bottom: '25mm',
                inner: '25mm',  // 装订侧
                outer: '20mm'
            },
            
            // 字体系统
            fonts: {
                primary: '"Noto Sans SC", "PingFang SC", sans-serif',
                heading: '"Noto Serif SC", "Georgia", serif',
                code: '"JetBrains Mono", "Consolas", monospace'
            },
            
            // 设计令牌 (Design Tokens)
            tokens: {
                colors: {
                    primary: '#1a1a1a',
                    secondary: '#666666',
                    accent: '#2563eb',
                    background: '#ffffff',
                    surface: '#f8f9fa'
                },
                typography: {
                    scale: {
                        xs: '10pt',
                        sm: '11pt',
                        base: '12pt',
                        lg: '14pt',
                        xl: '16pt',
                        '2xl': '20pt',
                        '3xl': '24pt'
                    },
                    lineHeight: {
                        tight: 1.2,
                        normal: 1.6,
                        relaxed: 1.8
                    }
                },
                spacing: {
                    xs: '4pt',
                    sm: '8pt',
                    md: '12pt',
                    lg: '16pt',
                    xl: '24pt',
                    '2xl': '32pt'
                }
            }
        };
        
        this.init();
    }
    
    init() {
        this.createDesignSystem();
        this.setupPrintStyles();
        this.initializeComponents();
    }
    
    /**
     * 创建设计系统CSS
     */
    createDesignSystem() {
        const tokens = this.config.tokens;
        
        // CSS自定义属性 (CSS Variables)
        const cssVariables = `
        :root {
            /* 颜色系统 */
            --color-primary: ${tokens.colors.primary};
            --color-secondary: ${tokens.colors.secondary};
            --color-accent: ${tokens.colors.accent};
            --color-background: ${tokens.colors.background};
            --color-surface: ${tokens.colors.surface};
            
            /* 字体系统 */
            --font-primary: ${this.config.fonts.primary};
            --font-heading: ${this.config.fonts.heading};
            --font-code: ${this.config.fonts.code};
            
            /* 字号系统 */
            --text-xs: ${tokens.typography.scale.xs};
            --text-sm: ${tokens.typography.scale.sm};
            --text-base: ${tokens.typography.scale.base};
            --text-lg: ${tokens.typography.scale.lg};
            --text-xl: ${tokens.typography.scale.xl};
            --text-2xl: ${tokens.typography.scale['2xl']};
            --text-3xl: ${tokens.typography.scale['3xl']};
            
            /* 行高系统 */
            --leading-tight: ${tokens.typography.lineHeight.tight};
            --leading-normal: ${tokens.typography.lineHeight.normal};
            --leading-relaxed: ${tokens.typography.lineHeight.relaxed};
            
            /* 间距系统 */
            --space-xs: ${tokens.spacing.xs};
            --space-sm: ${tokens.spacing.sm};
            --space-md: ${tokens.spacing.md};
            --space-lg: ${tokens.spacing.lg};
            --space-xl: ${tokens.spacing.xl};
            --space-2xl: ${tokens.spacing['2xl']};
            
            /* 页面配置 */
            --page-width: ${this.getPageWidth()};
            --page-height: ${this.getPageHeight()};
            --margin-top: ${this.config.margins.top};
            --margin-bottom: ${this.config.margins.bottom};
            --margin-inner: ${this.config.margins.inner};
            --margin-outer: ${this.config.margins.outer};
            --bleed: ${this.config.bleed};
        }`;
        
        this.injectCSS(cssVariables);
    }
    
    /**
     * 设置专业打印样式
     */
    setupPrintStyles() {
        const printCSS = `
        /* 专业打印媒体查询 */
        @media print {
            /* 页面配置 */
            @page {
                size: var(--page-width) var(--page-height);
                margin: var(--margin-top) var(--margin-outer) var(--margin-bottom) var(--margin-inner);
                
                /* 页眉 */
                @top-left {
                    content: "柯南侦探英语冒险";
                    font: var(--text-xs) var(--font-primary);
                    color: var(--color-secondary);
                }
                
                /* 页码 */
                @bottom-right {
                    content: counter(page);
                    font: var(--text-sm) var(--font-primary);
                    color: var(--color-primary);
                }
            }
            
            /* 左右页差异化 */
            @page :left {
                margin: var(--margin-top) var(--margin-inner) var(--margin-bottom) var(--margin-outer);
            }
            
            @page :right {
                margin: var(--margin-top) var(--margin-outer) var(--margin-bottom) var(--margin-inner);
            }
            
            /* 特殊页面 */
            @page cover {
                margin: 0;
                @top-left { content: none; }
                @bottom-right { content: none; }
            }
            
            @page blank {
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
            .page-break-avoid { page-break-inside: avoid; }
            .page-break-auto { page-break-after: auto; }
            
            /* 孤立行和寡妇行控制 */
            p, .text-block {
                orphans: 2;
                widows: 2;
            }
            
            /* 隐藏交互元素 */
            .no-print, .interactive, [aria-hidden="true"] {
                display: none !important;
            }
        }`;
        
        this.injectCSS(printCSS);
    }
    
    /**
     * 初始化组件库
     */
    initializeComponents() {
        // 标题组件
        this.defineComponent('heading', (level, content, options = {}) => {
            const classes = [
                'heading',
                `heading-${level}`,
                options.center ? 'text-center' : '',
                options.pageBreak ? 'page-break-before' : '',
                'page-break-avoid'
            ].filter(Boolean).join(' ');
            
            return `<h${level} class="${classes}">${content}</h${level}>`;
        });
        
        // 段落组件
        this.defineComponent('paragraph', (content, options = {}) => {
            const classes = [
                'paragraph',
                options.indent ? 'indent' : '',
                options.justify ? 'text-justify' : '',
                'page-break-avoid'
            ].filter(Boolean).join(' ');
            
            return `<p class="${classes}">${content}</p>`;
        });
        
        // 图片组件
        this.defineComponent('image', (src, alt, options = {}) => {
            const figureClasses = [
                'figure',
                options.fullWidth ? 'full-width' : '',
                options.center ? 'text-center' : '',
                'page-break-avoid'
            ].filter(Boolean).join(' ');
            
            const imgClasses = [
                'image',
                options.responsive ? 'responsive' : ''
            ].filter(Boolean).join(' ');
            
            return `
            <figure class="${figureClasses}">
                <img src="${src}" alt="${alt}" class="${imgClasses}" loading="lazy">
                ${options.caption ? `<figcaption class="caption">${options.caption}</figcaption>` : ''}
            </figure>`;
        });
        
        // 代码块组件
        this.defineComponent('codeBlock', (code, language = '', options = {}) => {
            return `
            <div class="code-block page-break-avoid">
                ${options.title ? `<div class="code-title">${options.title}</div>` : ''}
                <pre class="code"><code class="language-${language}">${this.escapeHtml(code)}</code></pre>
            </div>`;
        });
        
        // 表格组件
        this.defineComponent('table', (data, options = {}) => {
            const headers = data[0];
            const rows = data.slice(1);
            
            return `
            <div class="table-container page-break-avoid">
                ${options.title ? `<div class="table-title">${options.title}</div>` : ''}
                <table class="table">
                    <thead>
                        <tr>
                            ${headers.map(header => `<th>${header}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${rows.map(row => `
                            <tr>
                                ${row.map(cell => `<td>${cell}</td>`).join('')}
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>`;
        });
    }
    
    /**
     * 定义可复用组件
     */
    defineComponent(name, generator) {
        if (!this.components) this.components = {};
        this.components[name] = generator;
    }
    
    /**
     * 生成组件
     */
    component(name, ...args) {
        if (!this.components || !this.components[name]) {
            throw new Error(`组件 "${name}" 未定义`);
        }
        return this.components[name](...args);
    }
    
    /**
     * 创建完整书籍HTML
     */
    createBook(chapters) {
        const baseCSS = this.getBaseCSS();
        const componentsCSS = this.getComponentsCSS();
        
        const html = `
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>柯南侦探英语冒险：杨乐北的单词探案记</title>
            <style>
                ${baseCSS}
                ${componentsCSS}
            </style>
        </head>
        <body>
            ${chapters.map(chapter => this.renderChapter(chapter)).join('')}
        </body>
        </html>`;
        
        return html;
    }
    
    /**
     * 渲染章节
     */
    renderChapter(chapter) {
        return `
        <div class="chapter ${chapter.type || ''}" data-chapter="${chapter.id}">
            ${chapter.pageBreak !== false ? '<div class="page-break-before"></div>' : ''}
            ${chapter.content}
            ${chapter.id !== 'back-cover' ? '<div class="page-break"></div>' : ''}
        </div>`;
    }
    
    /**
     * 获取基础CSS
     */
    getBaseCSS() {
        return `
        /* 重置样式 */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        /* 基础样式 */
        html {
            font-size: var(--text-base);
            line-height: var(--leading-normal);
            font-family: var(--font-primary);
            color: var(--color-primary);
            background: var(--color-background);
        }
        
        body {
            margin: 0;
            padding: var(--space-lg);
            max-width: calc(var(--page-width) + var(--space-xl));
            margin: 0 auto;
        }
        
        /* 标题样式 */
        .heading {
            font-family: var(--font-heading);
            font-weight: 600;
            line-height: var(--leading-tight);
            margin-bottom: var(--space-md);
        }
        
        .heading-1 { font-size: var(--text-3xl); margin-bottom: var(--space-xl); }
        .heading-2 { font-size: var(--text-2xl); margin-bottom: var(--space-lg); }
        .heading-3 { font-size: var(--text-xl); margin-bottom: var(--space-md); }
        .heading-4 { font-size: var(--text-lg); margin-bottom: var(--space-sm); }
        
        /* 段落样式 */
        .paragraph {
            margin-bottom: var(--space-md);
            text-align: justify;
            line-height: var(--leading-normal);
        }
        
        .paragraph.indent {
            text-indent: 2em;
        }
        
        /* 图片样式 */
        .figure {
            margin: var(--space-lg) 0;
        }
        
        .image {
            max-width: 100%;
            height: auto;
            display: block;
        }
        
        .image.responsive {
            width: 100%;
        }
        
        .caption {
            font-size: var(--text-sm);
            color: var(--color-secondary);
            margin-top: var(--space-xs);
            text-align: center;
            font-style: italic;
        }
        
        /* 代码样式 */
        .code-block {
            margin: var(--space-lg) 0;
            background: var(--color-surface);
            border-radius: 4pt;
            overflow: hidden;
        }
        
        .code-title {
            background: var(--color-secondary);
            color: var(--color-background);
            padding: var(--space-sm) var(--space-md);
            font-size: var(--text-sm);
            font-weight: 500;
        }
        
        .code {
            font-family: var(--font-code);
            font-size: var(--text-sm);
            padding: var(--space-md);
            margin: 0;
            background: none;
            border: none;
            overflow-x: auto;
        }
        
        /* 表格样式 */
        .table-container {
            margin: var(--space-lg) 0;
        }
        
        .table-title {
            font-weight: 600;
            margin-bottom: var(--space-sm);
            color: var(--color-primary);
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
            border: 1pt solid var(--color-secondary);
        }
        
        .table th,
        .table td {
            padding: var(--space-sm);
            border: 0.5pt solid var(--color-secondary);
            text-align: left;
        }
        
        .table th {
            background: var(--color-surface);
            font-weight: 600;
            color: var(--color-primary);
        }
        
        /* 布局工具类 */
        .text-center { text-align: center; }
        .text-justify { text-align: justify; }
        .text-left { text-align: left; }
        .text-right { text-align: right; }
        
        .full-width { width: 100%; }
        
        /* 章节样式 */
        .chapter {
            min-height: calc(var(--page-height) - var(--margin-top) - var(--margin-bottom));
        }
        
        .chapter.cover {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }`;
    }
    
    /**
     * 获取组件CSS
     */
    getComponentsCSS() {
        return `
        /* 专用组件样式 */
        .word-card {
            background: var(--color-surface);
            border: 1pt solid var(--color-secondary);
            border-radius: 6pt;
            padding: var(--space-md);
            margin: var(--space-sm) 0;
            page-break-inside: avoid;
        }
        
        .story-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-left: 4pt solid var(--color-accent);
            padding: var(--space-lg);
            margin: var(--space-lg) 0;
            border-radius: 0 6pt 6pt 0;
            page-break-inside: avoid;
        }
        
        .chapter-intro {
            background: var(--color-surface);
            padding: var(--space-xl);
            margin: var(--space-xl) 0;
            border-radius: 8pt;
            text-align: center;
            page-break-inside: avoid;
        }
        
        .vocabulary-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250pt, 1fr));
            gap: var(--space-md);
            margin: var(--space-lg) 0;
        }
        
        .grammar-box {
            border: 2pt solid var(--color-accent);
            border-radius: 8pt;
            padding: var(--space-lg);
            margin: var(--space-lg) 0;
            background: rgba(37, 99, 235, 0.05);
            page-break-inside: avoid;
        }`;
    }
    
    /**
     * 获取页面尺寸
     */
    getPageWidth() {
        const formats = {
            '16K': '185mm',
            'A4': '210mm',
            'A5': '148mm'
        };
        return formats[this.config.format] || formats['16K'];
    }
    
    getPageHeight() {
        const formats = {
            '16K': '260mm',
            'A4': '297mm',
            'A5': '210mm'
        };
        return formats[this.config.format] || formats['16K'];
    }
    
    /**
     * 注入CSS到页面
     */
    injectCSS(css) {
        if (typeof document !== 'undefined') {
            const style = document.createElement('style');
            style.textContent = css;
            document.head.appendChild(style);
        }
    }
    
    /**
     * HTML转义
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    /**
     * 高级PDF生成 (使用Puppeteer)
     */
    async generateProfessionalPDF(html, outputPath) {
        // 这里可以集成Puppeteer进行高质量PDF生成
        // 支持更高级的渲染选项
        const options = {
            format: 'A4',
            printBackground: true,
            margin: {
                top: this.config.margins.top,
                bottom: this.config.margins.bottom,
                left: this.config.margins.inner,
                right: this.config.margins.outer
            },
            preferCSSPageSize: true,
            displayHeaderFooter: true
        };
        
        // 实际实现需要Puppeteer环境
        console.log('Professional PDF generation with options:', options);
        return outputPath;
    }
}

// 使用示例
function createModernBook() {
    const designer = new ModernBookDesigner({
        format: '16K',
        dpi: 300
    });
    
    // 示例章节数据
    const chapters = [
        {
            id: 'cover',
            type: 'cover',
            pageBreak: false,
            content: `
                <div class="book-cover">
                    ${designer.component('heading', 1, '柯南侦探英语冒险', { center: true })}
                    ${designer.component('heading', 2, '杨乐北的单词探案记', { center: true })}
                </div>
            `
        },
        {
            id: 'chapter1',
            content: `
                ${designer.component('heading', 1, '第一章：神秘的单词宝盒')}
                ${designer.component('paragraph', '在一个阳光明媚的下午，杨乐北正在整理他的书桌...')}
                ${designer.component('image', 'assets/images/chapter1.jpg', '神秘的宝盒', { 
                    caption: '图1-1: 杨乐北发现的神秘宝盒',
                    center: true 
                })}
            `
        }
    ];
    
    return designer.createBook(chapters);
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ModernBookDesigner, createModernBook };
}

// 浏览器环境
if (typeof window !== 'undefined') {
    window.ModernBookDesigner = ModernBookDesigner;
    window.createModernBook = createModernBook;
}