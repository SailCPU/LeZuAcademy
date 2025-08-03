/**
 * 单词卡发音功能
 * Word Card Pronunciation Feature
 * 
 * 为所有单词卡添加点击发音功能
 * Add click-to-pronounce functionality for all word cards
 */

class WordPronunciation {
    constructor() {
        this.synthesis = window.speechSynthesis;
        this.isSupported = 'speechSynthesis' in window;
        this.currentUtterance = null;
        this.voices = [];
        this.preferredVoice = null;
        
        this.init();
    }
    
    init() {
        if (!this.isSupported) {
            console.warn('Speech Synthesis API is not supported in this browser');
            return;
        }
        
        // 等待语音加载完成
        this.loadVoices();
        
        // 为现有的单词卡添加功能
        this.addPronunciationToWordCards();
        
        // 添加全局样式
        this.addStyles();
        
        console.log('🔊 单词发音功能已加载 Word Pronunciation Feature Loaded');
    }
    
    loadVoices() {
        // 获取可用的语音
        const updateVoices = () => {
            this.voices = this.synthesis.getVoices();
            this.selectPreferredVoice();
        };
        
        updateVoices();
        
        // 某些浏览器需要异步加载语音
        if (this.synthesis.onvoiceschanged !== undefined) {
            this.synthesis.onvoiceschanged = updateVoices;
        }
    }
    
    selectPreferredVoice() {
        // 优先选择英语语音
        const englishVoices = this.voices.filter(voice => 
            voice.lang.startsWith('en-') || voice.lang === 'en'
        );
        
        // 按优先级选择语音
        const preferredPatterns = [
            /US/i,           // 美式英语
            /United States/i, // 美式英语
            /GB/i,           // 英式英语
            /UK/i,           // 英式英语
            /en/i            // 任何英语
        ];
        
        for (const pattern of preferredPatterns) {
            const voice = englishVoices.find(v => pattern.test(v.name) || pattern.test(v.lang));
            if (voice) {
                this.preferredVoice = voice;
                console.log(`🗣️ 选择语音: ${voice.name} (${voice.lang})`);
                break;
            }
        }
        
        // 如果没有找到英语语音，使用第一个可用语音
        if (!this.preferredVoice && this.voices.length > 0) {
            this.preferredVoice = this.voices[0];
        }
    }
    
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .word-card {
                cursor: pointer;
                transition: all 0.3s ease;
                position: relative;
            }
            
            .word-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                border-color: #007bff;
            }
            
            .word-card.pronouncing {
                animation: pulse-pronunciation 0.6s ease-in-out;
                border-color: #28a745;
                box-shadow: 0 0 20px rgba(40, 167, 69, 0.3);
            }
            
            .word-card::before {
                content: "🔊";
                position: absolute;
                top: 8px;
                right: 8px;
                opacity: 0;
                transition: opacity 0.3s ease;
                font-size: 0.8em;
            }
            
            .word-card:hover::before {
                opacity: 0.6;
            }
            
            .word-card.pronouncing::before {
                opacity: 1;
                animation: speaker-bounce 0.6s ease-in-out;
            }
            
            @keyframes pulse-pronunciation {
                0% { transform: scale(1); }
                50% { transform: scale(1.02); }
                100% { transform: scale(1); }
            }
            
            @keyframes speaker-bounce {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.2); }
            }
            
            .pronunciation-tooltip {
                position: absolute;
                bottom: -30px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.8em;
                white-space: nowrap;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.3s ease;
                z-index: 1000;
            }
            
            .word-card:hover .pronunciation-tooltip {
                opacity: 1;
            }
        `;
        document.head.appendChild(style);
    }
    
    addPronunciationToWordCards() {
        const wordCards = document.querySelectorAll('.word-card');
        
        wordCards.forEach((card, index) => {
            this.setupWordCard(card, index);
        });
        
        console.log(`✅ 已为 ${wordCards.length} 个单词卡添加发音功能`);
    }
    
    setupWordCard(card, index) {
        // 查找英文单词
        const englishElement = card.querySelector('.english');
        if (!englishElement) return;
        
        const englishText = englishElement.textContent.trim();
        
        // 添加提示工具
        const tooltip = document.createElement('div');
        tooltip.className = 'pronunciation-tooltip';
        tooltip.textContent = '点击发音 Click to pronounce';
        card.style.position = 'relative';
        card.appendChild(tooltip);
        
        // 添加点击事件
        card.addEventListener('click', (e) => {
            e.preventDefault();
            this.pronounceWord(englishText, card);
        });
        
        // 添加键盘支持
        card.setAttribute('tabindex', '0');
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.pronounceWord(englishText, card);
            }
        });
        
        // 添加辅助功能属性
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `Click to pronounce: ${englishText}`);
    }
    
    pronounceWord(text, cardElement = null) {
        if (!this.isSupported) {
            this.showFallbackMessage(text);
            return;
        }
        
        // 停止当前播放的语音
        if (this.currentUtterance) {
            this.synthesis.cancel();
        }
        
        // 清理文本（移除括号内容和标点符号）
        const cleanText = this.cleanTextForPronunciation(text);
        
        // 创建新的语音合成实例
        const utterance = new SpeechSynthesisUtterance(cleanText);
        
        // 设置语音参数
        if (this.preferredVoice) {
            utterance.voice = this.preferredVoice;
        }
        utterance.rate = 0.8;        // 语速稍慢一些
        utterance.pitch = 1.0;       // 正常音调
        utterance.volume = 0.8;      // 音量
        
        // 设置事件监听器
        utterance.onstart = () => {
            if (cardElement) {
                cardElement.classList.add('pronouncing');
            }
            console.log(`🔊 正在播放: ${cleanText}`);
        };
        
        utterance.onend = () => {
            if (cardElement) {
                cardElement.classList.remove('pronouncing');
            }
            this.currentUtterance = null;
        };
        
        utterance.onerror = (e) => {
            console.error('语音播放错误:', e);
            if (cardElement) {
                cardElement.classList.remove('pronouncing');
            }
            this.currentUtterance = null;
        };
        
        // 播放语音
        this.currentUtterance = utterance;
        this.synthesis.speak(utterance);
    }
    
    cleanTextForPronunciation(text) {
        return text
            .replace(/\([^)]*\)/g, '')     // 移除括号内容
            .replace(/\[[^\]]*\]/g, '')    // 移除方括号内容
            .replace(/[.,!?;:'"]/g, '')    // 移除标点符号
            .replace(/\s+/g, ' ')          // 规范化空格
            .trim();
    }
    
    showFallbackMessage(text) {
        // 浏览器不支持语音合成时的降级方案
        const message = `发音: ${text}\nPronunciation: ${text}`;
        
        // 创建临时提示框
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #f8d7da;
            color: #721c24;
            padding: 10px 15px;
            border-radius: 5px;
            border: 1px solid #f5c6cb;
            z-index: 10000;
            font-size: 14px;
            max-width: 300px;
        `;
        notification.textContent = `此浏览器不支持语音功能\n单词: ${text}`;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
    
    // 公共方法：手动发音
    speakText(text) {
        this.pronounceWord(text);
    }
    
    // 公共方法：停止发音
    stopSpeaking() {
        if (this.synthesis) {
            this.synthesis.cancel();
        }
    }
    
    // 公共方法：检查支持情况
    checkSupport() {
        return {
            isSupported: this.isSupported,
            voicesCount: this.voices.length,
            preferredVoice: this.preferredVoice ? this.preferredVoice.name : null
        };
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    // 创建全局实例
    window.wordPronunciation = new WordPronunciation();
});

// 如果页面已经加载完成，立即初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.wordPronunciation = new WordPronunciation();
    });
} else {
    window.wordPronunciation = new WordPronunciation();
}

// 导出供其他脚本使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WordPronunciation;
}