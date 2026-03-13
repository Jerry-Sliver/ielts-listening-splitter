# 📦 打包成 EXE 说明

## Windows 打包步骤

### 1. 安装依赖

```bash
pip install pyinstaller
pip install -r requirements.txt
```

### 2. 简单打包（推荐）

```bash
pyinstaller --onefile --name ielts_listening_splitter ielts_audio_splitter.py
```

### 3. 或者使用我提供的脚本

```bash
python build_exe.py
```

## ⚠️ 重要提示

### 问题：Whisper 模型下载

打包成 EXE 后，**第一次运行仍然需要联网下载 Whisper 模型**。

### 解决方案：预下载模型

在打包前，先运行一次 Python 脚本下载模型：

```python
import whisper
model = whisper.load_model("base")  # 会下载并缓存模型
```

模型会被缓存到：
- **Windows**: `C:\Users\你的用户名\.cache\whisper\`
- **Mac/Linux**: `~/.cache/whisper/`

### 完全离线使用（高级）

如果要制作完全离线的安装包：

1. 先在一台有网的电脑上下载好模型
2. 把模型文件一起打包
3. 修改代码，让 Whisper 从本地加载模型

## 📁 打包后的文件

打包成功后，在 `dist/` 目录下会有：

```
dist/
├── ielts_listening_splitter.exe    # 主程序
├── generate_html_player.py          # HTML播放器生成器
├── requirements.txt                 # 依赖说明
└── README.md                        # 使用说明
```

## 💡 推荐做法

**最简单的方式：**
1. 正常打包 EXE
2. 告诉用户第一次运行需要联网下载模型
3. 模型下载后就可以完全离线使用了

这样用户体验最好，也不需要复杂的打包配置！
