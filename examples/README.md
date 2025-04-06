# 视频生成流程使用指南

本指南将帮助您使用视频生成流程系统，从文本脚本生成完整的视频。

## 系统概述

视频生成流程包括以下几个主要步骤：

1. **文案转语音（TTS）**：将文本脚本转换为语音文件
2. **脚本关键词提取与媒资检索**：从脚本中提取关键词，并在媒资库中检索相关视频素材
3. **视频素材拼接**：将检索到的视频素材拼接成一个连续的视频
4. **语音与视频合成**：将生成的语音与拼接好的视频合成，生成最终视频

## 安装依赖

在使用视频生成流程系统前，请确保已安装以下依赖：

```bash
pip install ffmpeg-python edge-tts jieba
```

此外，您还需要安装FFmpeg软件：
- Windows: 下载FFmpeg并将其添加到系统PATH
- Linux: `sudo apt-get install ffmpeg`
- macOS: `brew install ffmpeg`

## 准备媒资库

1. 在`media_library`目录下按类别组织视频素材
2. 视频文件名和目录名将作为关键词用于检索
3. 支持的视频格式：MP4、AVI、MOV、MKV

例如：
```
media_library/
├── 自然/
│   ├── 山脉/
│   │   └── 雪山.mp4
│   ├── 湖泊/
│   │   └── 平静湖面.mp4
│   └── 森林/
│       └── 茂密森林.mp4
├── 城市/
│   ├── 摩天大楼.mp4
│   ├── 繁华街道.mp4
│   └── 城市夜景.mp4
└── default/
    └── 默认视频.mp4
```

## 索引媒资库

在使用视频生成系统前，需要先索引媒资库：

```bash
python examples/index_media_library_example.py
```

或者使用脚本：

```bash
python scripts/index_media_library.py
```

## 使用示例

### 1. 基本用法

使用现有脚本生成视频：

```bash
python examples/city_video_generation.py
```

### 2. 完整工作流程

使用完整工作流程脚本，可以指定不同的参数：

```bash
python examples/complete_video_generation_workflow.py --script examples/scripts/city_script.txt --output_dir output --index_media
```

参数说明：
- `--script`：指定脚本文件路径
- `--narration`：指定自定义旁白文件路径（可选）
- `--output_dir`：指定输出目录
- `--output_file`：指定输出文件名
- `--index_media`：是否在生成视频前索引媒资库

### 3. 自定义脚本

您可以创建自己的脚本文件，格式参考`examples/scripts/city_script.txt`或`examples/scripts/nature_script.txt`。

## 常见问题

1. **未找到匹配的视频素材**：请确保媒资库中有相关视频素材，并且已经运行索引脚本更新媒资库索引。

2. **FFmpeg错误**：请确保已正确安装FFmpeg并添加到系统PATH。

3. **视频生成失败**：检查日志文件了解详细错误信息，通常位于`data/logs/`目录下。

## 进一步优化

1. 添加更多视频素材到媒资库
2. 优化关键词提取算法
3. 添加视频转场效果
4. 支持更多语音角色和情感表达

## 示例文件说明

- `city_video_generation.py`：使用城市脚本生成视频的示例
- `index_media_library_example.py`：索引媒资库的示例
- `complete_video_generation_workflow.py`：完整视频生成工作流程示例
- `video_generation_example.py`：使用自然脚本生成视频的示例