## 项目亮点

1. **GPU 加速**：在支持 GPU（NVIDIA CUDA）的环境下，使用 GPU 加速 `faster-whisper` 模型的语音转录及 FFmpeg 的视频编码，显著提升处理效率。

2. **CPU 兼容性**：项目在无 GPU 的环境中仍可正常运行，自动切换为 CPU 进行计算，确保在各类硬件配置下的广泛适用性。

3. **字幕嵌入**：通过 FFmpeg 将生成的 SRT 字幕文件无缝嵌入到视频中，生成的字幕文件与各类视频播放器高度兼容，确保用户播放体验。

4. **支持多视频格式**：兼容多种视频格式，如 MP4、AVI、MOV 等。

5. **视频内容总结**：为视频生成概要性总结，自动提取视频的核心内容，生成清晰、简明的内容大纲和脑图。

6. **视频时间轴**：为视频生成带有时间节点的时间轴，每个节点都对应视频中相应片段的简要总结，便于快速浏览和跳转。

7. **ai问答助手**：集成智能问答助手，首先展示相关知识点，再根据用户问题提供详细解答，确保知识系统化、回答准确。

8. **脑图**：使用matplotlib和networkx生成视频大纲脑图，便于用户明确和复习视频内容

   

![项目大体](https://cdn.jsdelivr.net/gh/Big-Halo/Js-Image/img/202410111949265.png)



![视频脑图](https://cdn.jsdelivr.net/gh/Big-Halo/Js-Image/img/202410111949947.png)



## 项目运行

直接运行 run.py 文件

浏览器打开 http://127.0.0.1:5000

**项目需要自行提供 OpenAI api key ，网页输入框处也有提示** 



## 部署环境配置

### 1. 安装 Python 环境

如果还没有安装 Python，建议安装最新版 Python 3.x：

- 前往 [Python 官方网站](https://www.python.org/downloads/) 下载并安装适合你操作系统的 Python 3.x。

安装后，可以在终端/命令提示符中检查是否成功安装：

```shell
python --version
```

### 2. 安装 FFmpeg

FFmpeg 是用于处理音视频的开源工具。在不同的操作系统上安装步骤略有不同。

#### **Windows 安装 FFmpeg**

1. 前往 [FFmpeg 下载页面](https://ffmpeg.org/download.html)，下载适合 Windows 的版本。

2. 解压下载的压缩包，将其存储在指定的文件夹中（如 `C:\ffmpeg`）。

3. 将bin目录添加到系统路径中（Path）：

   - 右键点击“此电脑”或“我的电脑” → 属性 → 高级系统设置 → 环境变量。
   - 在系统变量中找到 `Path`，点击编辑，添加 `C:\ffmpeg\bin` 路径。

4. 在命令行中运行以下命令确认安装成功：

   ```shell
   ffmpeg -version
   ```



### 3.安装项目所需要的包

注：建议在虚拟环境中安装。

#### **创建虚拟环境**

在项目目录中创建虚拟环境并激活它：

```shell
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

**该命令安装项目所需要的包:**

```shell
pip install -r requirements.txt
```

**注**：解压`njx.zip`文件后，可以找到`requirements.txt`文件。

**除此之外，请手动安装 PyTorch：** 在运行 `pip install -r requirements.txt` 安装其他依赖之后，手动安装 PyTorch：

- 对于 CPU 版本：

  ```shell
  pip install torch --index-url https://download.pytorch.org/whl/cpu
  ```

- 对于 GPU 版本，请到 [PyTorch官网](https://pytorch.org) 获取相应的安装命令。

若有**GPU(NVIDIA)**加速需求，如：

1. 使用 GPU 加速的 `faster_whisper` 进行语音转录。
2. 使用 FFmpeg 并结合 GPU 加速的编码器将字幕嵌入视频。

还需额外配置。[安装教程-CSDN博客](https://blog.csdn.net/qlkaicx/article/details/134577555)

## 运行方式

运行 `run.py` 文件后，在终端中会显示访问地址，例如 `http://127.0.0.1:5000/`。按住 `CTRL` 并单击该地址，即可在浏览器中打开网页。在网页中上传需要处理的视频文件，稍等片刻，程序将自动完成处理。

---

### 下面是对安装的包简单介绍（可忽略）：

#### **安装 Fester-Whisper**

Faster-Whisper 是一个高效的 Whisper 变体，可用于生成高质量的语音转录，支持多种语言和音频格式。

```shell
pip install faster-whisper
```

#### 安装 ffmpeg-python

该库提供了 Python 接口，可以更轻松地与 FFmpeg 交互。

```shell
pip install ffmpeg-python
```

#### 安装 OpenCC

繁体中文到简体中文的转换的库，Whisper 默认识别生成的语言为中文

```shell
pip install opencc-python-reimplemented
```

#### 安装 Pysrt

Pysrt 是一个用于处理 SubRip (.srt) 字幕文件的库，方便读取和编辑字幕。

```shell
pip install pysrt
```

#### 安装 Langchain OpenAI

Langchain OpenAI 是 Langchain 库与 OpenAI 的集成插件，提供了与 OpenAI API 的无缝对接。

```shell
pip install langchain_openai
```

#### 安装 Langchain Core

Langchain Core 是 Langchain 库的核心组件，提供了构建语言模型应用所需的基本功能。

```shell
pip install langchain_core
```

#### 安装 Pydantic

Pydantic 是一个数据验证和设置管理的库，广泛用于数据模型的定义和验证。

```shell
pip install pydantic
```

#### 安装 Langchain

Langchain 是一个用于构建语言模型应用的框架，支持多种语言模型和工具的集成。

```shell
pip install langchain
```

#### 安装 Flask

Flask 是一个轻量级的 Web 应用框架，适用于构建简单且高效的 web 服务。

```shell
pip install Flask
```

#### 安装PyTorch

 PyTorch 是一个流行的开源机器学习库，广泛用于计算机视觉和自然语言处理等领域。它提供了强大的GPU加速的张量计算能力，并且支持动态计算图，使得模型的构建和调试更加灵活和高效。

```shell
pip install torch torchvision torchaudio
```

**安装 Pysrt**

pysrt库进行SRT文件的读取，获取文本和时间点

```
pip install pysrt
```

**安装 Tiktoken**

Tiktoken对要传入模型的文本进行分块，以便也能处理长视频（不受token限制）

```
pip install tiktoken
```

**安装 langchain_core**

调用langchain_core库，可以为大模型传入提示词模板，明确大模型的目标和任务

```
pip install langchain_core
```

**安装 pydantic**

pydantic可以制作输出解析器，明确大模型的输出格式

```
pip install pydantic
```

**安装 typing**

可以调用 List,Dict,Any 等数据结构

```
pip install typing
```

**安装 matplotlib**

matplotlib进行脑图绘制

```
pip install matplotlib
```

**安装 networkx**

networkx创作图片

```
pip install networkx
```

**安装 requests**

requests进行网络请求

```
pip install requests
```

**安装 lxml**

对网络请求的返回值进行xml解析

```
pip install lxml
```

