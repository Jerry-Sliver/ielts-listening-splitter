#!/usr/bin/env python3
"""
生成HTML精听播放器
"""

import json
import os
from pathlib import Path


def generate_html_player(sentences_json_path, output_html_path=None):
    """
    生成HTML精听播放器
    
    Args:
        sentences_json_path: sentences.json 文件路径
        output_html_path: 输出HTML文件路径（可选）
    """
    # 读取句子数据
    with open(sentences_json_path, 'r', encoding='utf-8') as f:
        sentences = json.load(f)
    
    if output_html_path is None:
        output_html_path = Path(sentences_json_path).parent / "player.html"
    
    # 生成HTML
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>雅思听力精听练习</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 15px 30px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        
        .sentence-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .sentence-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        
        .sentence-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .sentence-number {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.1em;
        }}
        
        .sentence-time {{
            color: #999;
            font-size: 0.9em;
        }}
        
        .sentence-text {{
            font-size: 1.3em;
            line-height: 1.8;
            color: #333;
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        
        .audio-player {{
            width: 100%;
            margin-bottom: 15px;
        }}
        
        .controls {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.95em;
            font-weight: 500;
            transition: all 0.2s;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .btn-primary:hover {{
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}
        
        .btn-secondary {{
            background: #e9ecef;
            color: #495057;
        }}
        
        .btn-secondary:hover {{
            background: #dee2e6;
        }}
        
        .progress {{
            margin-top: 30px;
            text-align: center;
            color: white;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 30px;
            background: rgba(255,255,255,0.2);
            border-radius: 15px;
            overflow: hidden;
            margin-top: 10px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        
        .hidden {{
            display: none;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎧 雅思听力精听练习</h1>
            <p>逐句精听，稳步提升！</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(sentences)}</div>
                <div class="stat-label">总句子数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="completed-count">0</div>
                <div class="stat-label">已完成</div>
            </div>
        </div>
        
        <div id="sentences-container">
"""
    
    # 为每个句子生成卡片
    for i, sent in enumerate(sentences):
        html_content += f"""
            <div class="sentence-card" id="sentence-{i+1}">
                <div class="sentence-header">
                    <div class="sentence-number">{i+1}</div>
                    <div class="sentence-time">⏱ {sent['start_time']}s - {sent['end_time']}s ({sent['duration']}s)</div>
                </div>
                <div class="sentence-text" id="text-{i+1}">{sent['text']}</div>
                <audio class="audio-player" controls>
                    <source src="{sent['audio_file']}" type="audio/mpeg">
                    您的浏览器不支持音频播放
                </audio>
                <div class="controls">
                    <button class="btn btn-primary" onclick="document.getElementById('sentence-{i+1}').querySelector('audio').play()">▶️ 播放</button>
                    <button class="btn btn-secondary" onclick="toggleText({i+1})">👁 显示/隐藏文本</button>
                    <button class="btn btn-secondary" onclick="markComplete({i+1})">✅ 已掌握</button>
                </div>
            </div>
"""
    
    html_content += f"""
        </div>
        
        <div class="progress">
            <div>学习进度</div>
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill" style="width: 0%">0%</div>
            </div>
        </div>
        
        <div class="footer">
            <p>💡 精听建议：每句听3-5遍，跟读模仿，然后听写检查</p>
        </div>
    </div>
    
    <script>
        let completed = new Set();
        
        function toggleText(id) {{
            const textEl = document.getElementById('text-' + id);
            textEl.classList.toggle('hidden');
        }}
        
        function markComplete(id) {{
            const card = document.getElementById('sentence-' + id);
            if (completed.has(id)) {{
                completed.delete(id);
                card.style.opacity = '1';
                card.style.background = 'white';
            }} else {{
                completed.add(id);
                card.style.opacity = '0.7';
                card.style.background = '#d4edda';
            }}
            updateProgress();
        }}
        
        function updateProgress() {{
            const total = {len(sentences)};
            const count = completed.size;
            const percent = Math.round((count / total) * 100);
            
            document.getElementById('completed-count').textContent = count;
            document.getElementById('progress-fill').style.width = percent + '%';
            document.getElementById('progress-fill').textContent = percent + '%';
        }}
        
        // 从localStorage恢复进度
        const saved = localStorage.getItem('ielts_progress');
        if (saved) {{
            const savedSet = new Set(JSON.parse(saved));
            savedSet.forEach(id => markComplete(id));
        }}
        
        // 保存进度
        setInterval(() => {{
            localStorage.setItem('ielts_progress', JSON.stringify([...completed]));
        }}, 5000);
    </script>
</body>
</html>"""
    
    # 写入HTML文件
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"🎮 HTML播放器已生成: {output_html_path}")
    print(f"   用浏览器打开这个文件开始精听练习！")
    
    return output_html_path


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='生成HTML精听播放器')
    parser.add_argument('sentences_json', help='sentences.json 文件路径')
    parser.add_argument('-o', '--output', help='输出HTML文件路径（可选）')
    
    args = parser.parse_args()
    
    generate_html_player(args.sentences_json, args.output)


if __name__ == '__main__':
    main()
