from openai import OpenAI
from dotenv import load_dotenv
import os
from utils import (count_videos, count_videos_with_min_views, count_videos_with_new_views_on_date,
                   count_videos_by_creator_in_date_range, sum_growth_on_date)
from database import SessionLocal
import json
import dateparser
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

tools = [
    {
        "type": "function",
        "function":{
            "name": "count_videos",
            "description": "Возвращает количество видео",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_videos_by_creator_in_date_range",
            "description": "Возвращает количество видео у создателя за промежуток времени",
            "parameters": {
                "type": "object",
                "properties": {
                    "creator_id": {"type": "string"},
                    "start_date": {"type": "string"},
                    "end_date": {"type": "string"}
                },
                "required": ["creator_id", "start_date", "end_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_videos_with_min_views",
            "description": "Количество видео, у которых просмотров больше",
            "parameters": {
                "type": "object",
                "properties": {
                    "views": {"type": "integer"}
                },
                "required": ["views"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sum_growth_on_date",
            "description": "Суммарный рост просмотров всех видео за указанную дату",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"}
                },
                "required": ["date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_videos_with_new_views_on_date",
            "description": "Сколько разных видео получили новые просмотры в указанную дату",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"}
                },
                "required": ["date"]
            }
        },
    }
]

def parse_russian_date(text):
    dt = dateparser.parse(text, languages=["ru"])
    if dt:
        return dt.strftime("%Y-%m-%d")
    return None



def answer_llm(question):
    session = SessionLocal()

    sys_prompt = """
    Ты — ассистент, который отвечает на вопросы из базы данных с видео и их статистикой. 
    Твоя задача — понять вопрос, выбрать 
    нужную функцию (tool) и вызвать её с корректными аргументами.

    Твой ответ всегда должен быть числом. Никакого текста, комментариев или объяснений.

    Важно:
    - Ты не должен придумывать SQL — только вызывай доступные функции.
    - Если нужно несколько запросов — вызывай несколько функций подряд, пока не получишь все данные.
    - Даты могут быть в формате «28 ноября 2025», «с 1 по 5 ноября 2025», «1 ноября 2025».
    - Все даты нужно преобразовывать в формат YYYY-MM-DD.
    - Если в вопросе требуется диапазон дат — используй соответствующую функцию.
    - Если достать значение можно только через конкретный инструмент — используй его.

    Всегда выбирай наиболее подходящую функцию.
    Если вопрос касается "просмотров", "лайков", "роста", "новых просмотров", "всех видео", 
    "видео за период" — обязательно используй инструмент.

    Если запрос не соответствует функциям — отвечай числом 0.
    """

    response = client.chat.completions.create(
        model="mistralai/devstral-2512:free",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": question}
        ],
        tools=tools
    )
    resp = response.choices[0].message

    if not resp.tool_calls:
        return resp.content.strip()

    tool_call = resp.tool_calls[0]
    fn_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    if fn_name == "count_videos":
        result = count_videos(session)
    elif fn_name == "count_videos_by_creator_in_date_range":
        result = count_videos_by_creator_in_date_range(
            session, args["creator_id"], args["start_date"], args["end_date"]
        )
    elif fn_name == "count_videos_with_min_views":
        result = count_videos_with_min_views(session, args["views"])
    elif fn_name == "sum_growth_on_date":
        result = sum_growth_on_date(session, args["date"])
    elif fn_name == "count_videos_with_new_views_on_date":
        result = count_videos_with_new_views_on_date(session, args["date"])
    else:
        result = 0

    session.close()
    return str(result)










