#!/usr/bin/env python3
"""
雅思听力音频切分工具
将完整的雅思听力MP3切分成单句，方便精听练习
"""

import os
import json
import whisper
from pydub import AudioSegment
from pathlib import Path


class IELTSAudioSplitter:
    def __init__(self, model_size="base"):
        """
        初始化切分器
        model_size: tiny, base, small, medium, large
        """
        print(f"正在加载Whisper模型: {model_size}...")
        self.model = whisper.load_model(model_size)
        print("模型加载完成！")
    
    def transcribe_audio(self, audio_path):
        """
        转录音频，获取带时间戳的文本
        """
        print(f"正在转录音频: {audio_path}...")
        result = self.model.transcribe(
            audio_path, 
            word_timestamps=True,
            language="en"  # 雅思是英语
        )
        return result
    
    def split_audio(self, audio_path, output_dir, min_sentence_duration=1.0, max_sentence_duration=10.0):
        """
        切分音频为单句
        
        Args:
            audio_path: 输入音频路径
            output_dir: 输出目录
            min_sentence_duration: 最小句子时长（秒）
            max_sentence_duration: 最大句子时长（秒）
        """
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 转录音频
        result = self.transcribe_audio(audio_path)
        
        # 加载音频
        print("正在加载音频文件...")
        audio = AudioSegment.from_file(audio_path)
        
        # 保存完整转录结果
        transcript_file = output_path / "full_transcript.json"
        with open(transcript_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"完整转录已保存到: {transcript_file}")
        
        # 切分句子
        sentences = []
        for i, segment in enumerate(result['segments']):
            start_time = segment['start']
            end_time = segment['end']
            text = segment['text'].strip()
            
            # 过滤太短或太长的片段
            duration = end_time - start_time
            if duration < min_sentence_duration or duration > max_sentence_duration:
                continue
            
            if not text:
                continue
            
            # 切分音频
            start_ms = int(start_time * 1000)
            end_ms = int(end_time * 1000)
            segment_audio = audio[start_ms:end_ms]
            
            # 保存音频片段
            audio_filename = f"sentence_{i+1:03d}.mp3"
            audio_filepath = output_path / audio_filename
            segment_audio.export(audio_filepath, format="mp3")
            
            # 保存句子信息
            sentence_info = {
                'id': i + 1,
                'audio_file': audio_filename,
                'text': text,
                'start_time': round(start_time, 2),
                'end_time': round(end_time, 2),
                'duration': round(duration, 2)
            }
            sentences.append(sentence_info)
            
            print(f"已切分: {audio_filename} - {text[:50]}...")
        
        # 生成句子列表文件
        sentences_file = output_path / "sentences.json"
        with open(sentences_file, 'w', encoding='utf-8') as f:
            json.dump(sentences, f, ensure_ascii=False, indent=2)
        
        # 生成方便阅读的文本文件
        text_file = output_path / "sentences.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            for sent in sentences:
                f.write(f"[{sent['id']}] {sent['text']}\n")
                f.write(f"    音频: {sent['audio_file']}\n")
                f.write(f"    时间: {sent['start_time']}s - {sent['end_time']}s\n\n")
        
        print(f"\n🎉 切分完成！")
        print(f"共切分 {len(sentences)} 个句子")
        print(f"输出目录: {output_path.absolute()}")
        
        return sentences


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='雅思听力音频切分工具')
    parser.add_argument('audio_file', help='输入音频文件路径')
    parser.add_argument('-o', '--output', default='output', help='输出目录 (默认: output)')
    parser.add_argument('-m', '--model', default='base', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper模型大小 (默认: base)')
    parser.add_argument('--min-duration', type=float, default=1.0, 
                       help='最小句子时长(秒) (默认: 1.0)')
    parser.add_argument('--max-duration', type=float, default=15.0, 
                       help='最大句子时长(秒) (默认: 15.0)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.audio_file):
        print(f"错误: 文件不存在 - {args.audio_file}")
        return
    
    splitter = IELTSAudioSplitter(model_size=args.model)
    splitter.split_audio(
        args.audio_file, 
        args.output,
        min_sentence_duration=args.min_duration,
        max_sentence_duration=args.max_duration
    )


if __name__ == '__main__':
    main()
