import pysrt
import os
from flask import Flask, render_template
def ai_anaylase(srt_path,api_key):

    #data=pysrt.open(os.path.join("output_subtitles.srt"))
    data=pysrt.open(os.path.join(srt_path))
    # 要分析的文本（不带时间）
    #data=data.text
    start_time=[]
    end_time=[]
    text=[]
    for sub in data:
        start_time.append(sub.start)
        end_time.append(sub.end)
        text.append(sub.text)
        #print(f"{start_time}~{end_time}\n{text}")

    #subtitle_text = "\n".join([sub.text for sub in data])
    ana_text=''.join(text)
    ana_text_with_time = ''.join([f"{sub.text} (结束时间: {sub.end})\n" for sub in data])

    # 开始接入大模型
    import openai


    from langchain_openai import ChatOpenAI
    model=ChatOpenAI(
        openai_api_key = api_key,
        openai_api_base = "https://api.chatanywhere.tech/v1",
        model_name = "gpt-3.5-turbo",
        #openai_default_headers = {"x-foo": "true"},
        temperature=0.8,
    )

    # divide chunks
    import tiktoken

    # 加载 tokenizer
    # tokenizer = AutoTokenizer.from_pretrained("gpt-3.5-turbo")
    # tokenizer=tiktoken.get_encoding("gpt-3.5-turbo")

    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def text_to_chunk(text, chunk_size=3500, overlap=100):
        token_ids = tokenizer.encode(text)
        num_tokens = len(token_ids)
        chunks = []

        for i in range(0, num_tokens, chunk_size - overlap):
            chunk = token_ids[i:i + chunk_size]
            if len(chunk) <= chunk_size:  # 检查块长度
                chunks.append(tokenizer.decode(chunk))  # 解码为文本
        return chunks

    ana_data=text_to_chunk(ana_text_with_time)


    # 模板，历史对话，cvs解析器，

    from app.templates.prompt_template import theme_template_text,user_template_text
    from langchain_core.prompts import ChatPromptTemplate
    prompt=ChatPromptTemplate([
        ("system",theme_template_text),
        ("user",user_template_text), # not :
    ])

    # 解析器
    from pydantic import BaseModel,Field
    from typing import List,Dict,Any
    class Outline(BaseModel):
        title: str=Field(description="视频概要的标题")
        #contents: List[str]=Field(description="视频概要的分段主题")
        contents: List[Dict[str, Any]] = Field(
            description="视频概要的分段主题及其结束时间",
            default_factory=list
        )

    from langchain.output_parsers import PydanticOutputParser
    output_parser=PydanticOutputParser(pydantic_object=Outline)

    chain=prompt|model|output_parser

    ana_chunks=[]

    for chunk in ana_data:
        res=chain.invoke({
            "parser_instructions":output_parser.get_format_instructions(),
            "data":chunk
        })
        ana_chunks.append(res)

    # 整体分析
    # combined_data = "\n".join(chunk['contents'] for chunk in ana_chunks)
    # overall_summary = "\n".join(
    #     f"标题: {chunk.title}, 主题: {', '.join(f'{item['topic']} (结束时间: {item['end_time']})' for item in chunk.contents)}"
    #     for chunk in ana_chunks
    # )
    combined_data=[]
    for chunk in ana_chunks:
        combined_data.append(f"标题是{chunk.title}，")
        for item in chunk.contents:
            combined_data.append(f"主题是{item['topic']}，其结束时间是{item['end_time']}")
        combined_data.append('\n')
    #print(combined_data)

    combined_data=''.join(combined_data)

    #print('----------------------')

    overall_summary=chain.invoke({
            "parser_instructions":output_parser.get_format_instructions(),
            "data":combined_data
        })

    #print(overall_summary)

    return ana_chunks,overall_summary


def picture_mind(overall_summary,save_path="analyse_chart.png"):
    # 处理文本
    chunk_topics = []
    chunk_titles = []
    sum_title = overall_summary.title
    sum_topics = []

    # for chunk in ana_chunks:
    #     chunk_titles.append(chunk.title)
    #     for item in chunk.contents:
    #         chunk_topics.append(item['topic'])

    for topic in overall_summary.contents:
        sum_topics.append(topic['topic'])

    import matplotlib.pyplot as plt
    import networkx as nx
    from matplotlib import rcParams

    # 设置中文字体
    rcParams['font.sans-serif'] = ['SimHei']  # 黑体
    rcParams['axes.unicode_minus'] = False  # 用于显示负号

    # 创建有向图
    G = nx.DiGraph()

    # 添加节点
    G.add_node(sum_title)

    # 第一层
    for sum in sum_topics:
        G.add_node(sum)
        G.add_edge(sum_title, sum)

    # 定义节点位置，使用 spring_layout 增加美观度
    pos = nx.spring_layout(G, k=0.5)  # k 值控制节点之间的距离，数值越小，距离越大

    # 绘制节点和边
    nx.draw(G, pos, with_labels=True, arrows=True, node_size=4000, node_color='lightblue', font_size=10,
            font_weight='bold', width=2, arrowstyle='->', arrowsize=20)

    # 添加标题
    plt.title("视频脑图", fontsize=15)

    # 保存为 PNG 文件
    plt.savefig(save_path, format="png", bbox_inches="tight")
    plt.close()  # 关闭图形以释放内存

    return save_path


# ana_chunks,overall_summary=ai_anaylase("show.srt")
# print('-------------------')
# picture_mind(ana_chunks,overall_summary)
#
# # short_res=ai_anaylase('short_show.srt')
# # print(short_res)
