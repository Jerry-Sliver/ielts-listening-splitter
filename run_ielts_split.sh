#!/bin/bash
# 雅思听力音频切分一键脚本

echo "🎧 雅思听力单句切分工具"
echo "=========================="

# 检查参数
if [ $# -eq 0 ]; then
    echo "使用方法: $0 <音频文件> [输出目录]"
    echo "示例: $0 listening.mp3 ielts_test1"
    exit 1
fi

AUDIO_FILE="$1"
OUTPUT_DIR="${2:-output}"

# 检查文件是否存在
if [ ! -f "$AUDIO_FILE" ]; then
    echo "❌ 错误: 文件不存在 - $AUDIO_FILE"
    exit 1
fi

echo "📁 输入文件: $AUDIO_FILE"
echo "📂 输出目录: $OUTPUT_DIR"
echo ""

# 步骤1: 切分音频
echo "🚀 步骤 1/2: 切分音频..."
python ielts_audio_splitter.py "$AUDIO_FILE" -o "$OUTPUT_DIR" -m base

if [ $? -ne 0 ]; then
    echo "❌ 音频切分失败"
    exit 1
fi

# 步骤2: 生成HTML播放器
echo ""
echo "🎮 步骤 2/2: 生成HTML播放器..."
python generate_html_player.py "$OUTPUT_DIR/sentences.json"

if [ $? -ne 0 ]; then
    echo "❌ HTML播放器生成失败"
    exit 1
fi

echo ""
echo "🎉 全部完成！"
echo "=========================="
echo "📂 输出目录: $(realpath "$OUTPUT_DIR")"
echo "🎮 打开播放器: $(realpath "$OUTPUT_DIR/player.html")"
echo ""
echo "💡 提示: 用浏览器打开 player.html 开始精听练习！"
