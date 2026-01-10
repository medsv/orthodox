import streamlit as st
from footer import show_footer
#from dotenv import load_dotenv
import os

#load_dotenv()  # загружает переменные из .env
#api_key = os.getenv("API_KEY")
#folder_id = os.getenv("FOLDER_ID")

# Получаем API-ключи
api_key = st.secrets.get("API_KEY")
folder_id = st.secrets.get("FOLDER_ID")

from openai import OpenAI
#model = f"gpt://{folder_id}/gemma-3-27b-it"
#model = f"gpt://{folder_id}/yandexgpt-lite"
#model = f"gpt://{folder_id}/gpt-oss-20b/latest"
#model = f"gpt://{folder_id}/yandexgpt"
model = f"gpt://{folder_id}/qwen3-235b-a22b-fp8/latest"

from datetime import date  # Для определения текущей даты
from assistant import Assistant

client = OpenAI(
    base_url="https://rest-assistant.api.cloud.yandex.net/v1",
    api_key=api_key,
#    project=folder_id
)

       
# Инициализация истории чата и ассистента в session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "today" not in st.session_state:
    st.session_state.today = f"Сегодня {date.today()}. "

    #st.write(st.session_state.today)

#if "user" not in st.session_state:
#    st.session_state.user = "Вы

if "assistant" not in st.session_state:
    # ЗАМЕНИТЕ `instructions` и `model` на реальные значения
    instructions = st.session_state.today + """Ты - знаток русского православия. Общайся как православный священнослужитель.
Отвечай на вопросы о:
1. Русских православных праздниках.
2. Классификации праздников (двунадесятые, подвижные, ...)
2. Событиях, личностях и местах, связанных с русским православием. 
3. Видах постов, их различиях, какую пищу можно употреблять во время постов.
Ответ формулируй на основании данных, полученных в интернете с помощью инструмента web_search. 
Ответы должны быть понятны людям, которые не являются верующими. 
Если вопрос не касется русского православия, то отвечай "Отвечаю только на вопросы о русском православии". 
Если не смог найти запрошенные данные, то отвечай "Не могу ответить на данный вопрос.", НИЧЕГО НЕ ПРИДУМЫВАЙ!"""
    #model = "your-model-name"  # Например, "meta-llama/Llama-3.2-11B-Vision-Instruct"
    st.session_state.assistant = Assistant(instructions=instructions, model=model, client=client)

st.set_page_config(
    page_icon = "☦️",
    page_title = "Чат-бот о русском православии"
)

#with st.sidebar:
#    st.write("Настройки")

# Заголовок приложения
st.title("💬 Чат-бот о русском православии")

# Отображение истории сообщений
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле ввода для нового сообщения
if prompt := st.chat_input("Задайте вопрос..."):
    # Добавляем сообщение пользователя в историю для отображения
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Отображаем сообщение пользователя
    with st.chat_message("user"):
        st.markdown(prompt)

    # Вызываем ассистента; контекст управляется внутри него
    response = st.session_state.assistant(input=prompt, session_id='default')

    # Добавляем ответ нейросети в историю для отображения
    st.session_state.messages.append({"role": "assistant", "content": response})
    # Отображаем ответ нейросети
    with st.chat_message("assistant"):
        st.markdown(response)
     
# --- Кнопка скачивания чата ---
if st.session_state.messages: # Показываем кнопку, только если есть сообщения
    # Генерируем текст чата
    chat_history_text = ""
    for message in st.session_state.messages:
        role = message["role"].capitalize()
        content = message["content"]
        chat_history_text += f"[{role}]: {content}\n\n"

    # Добавляем кнопку загрузки
    st.download_button(
        label="📥 Скачать чат в формате Markdown(.md)",
        data=chat_history_text.encode('utf-8'), # Кодируем в UTF-8
        file_name=f"chat_history_{date.today()}.txt",
        mime="text/plain"
    )
else:
    #st.info("Пока нет сообщений для скачивания.")
    pass

show_footer() # Показываем подвал
