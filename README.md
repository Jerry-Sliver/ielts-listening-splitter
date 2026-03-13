# 🎧 雅思听力单句切分工具

将完整的雅思听力MP3切分成单句，配合文本进行精听练习！

## ✨ 功能特点

- 🎯 **AI智能切分**：使用OpenAI Whisper精准识别句子边界
- 📝 **自动转录**：生成每个句子的英文文本
- 🎮 **交互式播放器**：精美的HTML界面，支持显示/隐藏文本
- 📊 **学习进度追踪**：自动保存学习进度到浏览器
- 🎨 **现代化界面**：渐变紫色主题，视觉舒适

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

还需要安装 ffmpeg：
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# MacOS
brew install ffmpeg

# Windows
# 从 https://ffmpeg.org/download.html 下载
```

### 2. 使用方法

#### 一键使用（推荐）
```bash
./run_ielts_split.sh your_audio.mp3 output_dir
```

#### 手动使用
```bash
# 切分音频
python ielts_audio_splitter.py your_audio.mp3 -o output_dir

# 生成HTML播放器
python generate_html_player.py output_dir/sentences.json
```

## 📁 输出文件

切分后会在输出目录生成：

```
output_dir/
├── sentence_001.mp3      # 第1句音频
├── sentence_002.mp3      # 第2句音频
├── ...
├── sentences.json         # 所有句子的JSON数据
├── sentences.txt          # 方便阅读的文本列表
├── player.html            # 交互式精听播放器
└── full_transcript.json   # 完整转录数据
```

## 🎯 雅思精听练习流程

1. **🔇 盲听**：不看文本，听句子3-5遍
2. **👁 对照**：看文本，找出没听懂的地方
3. **🗣 跟读**：跟着录音朗读，模仿发音和语调
4. **✍ 听写**：尝试听写句子，检查错误

## 💡 模型选择建议

| 模型 | 速度 | 准确率 | 推荐场景 |
|------|------|--------|----------|
| tiny | ⚡️ 最快 | ⭐️ | 快速测试 |
| base | ⚡️ 快 | ⭐️⭐️ | 日常使用（推荐） |
| small | 🐢 中等 | ⭐️⭐️⭐️ | 需要更高准确率 |
| medium | 🐢🐢 慢 | ⭐️⭐️⭐️⭐️ | 追求最佳效果 |
| large | 🐢🐢🐢 最慢 | ⭐️⭐️⭐️⭐️⭐️ | 专业级 |

## 📝 项目结构

```
ielts-listening-splitter/
├── ielts_audio_splitter.py    # 主程序：音频切分
├── generate_html_player.py     # HTML播放器生成器
├── run_ielts_split.sh          # 一键使用脚本
├── requirements.txt             # Python依赖
├── .gitignore                  # Git忽略文件
└── README.md                   # 说明文档
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

---

🎉 开始你的雅思精听之旅吧！
