def ai_analyse(srt_path):
    import pysrt
    import os
    #data=pysrt.open(os.path.join("output_subtitles.srt"))
    data=pysrt.open(os.path.join("../../show.srt"))
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

    from langchain_openai import ChatOpenAI
    model=ChatOpenAI(
        openai_api_key = "sk-15CZvhrQHk7f6AMEQffpvZKdvJ0ZB267pkEltUUSVhIZM45U",
        openai_api_base = "https://api.chatanywhere.tech/v1",
        model_name = "gpt-3.5-turbo",
        #openai_default_headers = {"x-foo": "true"},
        temperature=0.8,
    )
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
    res=chain.invoke({
        "parser_instructions":output_parser.get_format_instructions(),
        "data":ana_text_with_time
    })

    res_text=res.title
    print(res_text)
    res_contents=res.contents
    print(res_contents)
    print(res_contents[0])
    return res


# path=add_subtitles_to_video("videos/video_02.mp4")[0]
# ai_analyse(path)