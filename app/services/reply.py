# def interact_with_model(question):
#     #与大模型交互的逻辑
#     return "这是模型的回答。"  #回答

from langchain_openai import ChatOpenAI

def interact_with_model(question):
    model=ChatOpenAI(
        openai_api_key="sk-15CZvhrQHk7f6AMEQffpvZKdvJ0ZB267pkEltUUSVhIZM45U",
        # openai_api_key="sk-cQhLrvpFYCTQfiNHC65c0f63438c40A1Bd6bA72f379464Fe",
        openai_api_base="https://api.chatanywhere.tech/v1",
        model_name="gpt-3.5-turbo",
        # openai_default_headers = {"x-foo": "true"},
        temperature=0.8,
    )

    # 提示词模板
    from app.templates.reply_template import ask_template_text,user_template_text
    from langchain_core.prompts import ChatPromptTemplate
    prompt = ChatPromptTemplate([
        ("system", ask_template_text),
        ("user", user_template_text),  # not :
    ])

    # 解析器
    from pydantic import BaseModel, Field
    #from typing import List, Dict, Any
    class Outline(BaseModel):
        acknowledge: str = Field(description="问题所需要的知识点")
        # contents: List[str]=Field(description="视频概要的分段主题")
        # contents: List[Dict[str, Any]] = Field(
        #     description="视频概要的分段主题及其结束时间",
        #     default_factory=list
        # )
        reply: str=Field(description="问题的答案是")

    from langchain.output_parsers import PydanticOutputParser
    output_parser = PydanticOutputParser(pydantic_object=Outline)

    chain = prompt | model | output_parser
    res = chain.invoke({
        "parser_instructions": output_parser.get_format_instructions(),
        "data": question
    })

    from app.services.baidu import baidu_search
    url = baidu_search(res.acknowledge)

    return res,url


if __name__ == '__main__':
    ask=True
    while(ask):
        question = input()
        if question=="exit":
            ask=False
        else:
            res=interact_with_model(question)
            print(res)
