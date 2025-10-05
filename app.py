import os
import streamlit as st
from langchain_gigachat import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage

PRE_PROMPT = "Ты выступаешь в роли ИИ ассистента. Подробно отвечай на вопросы, чтобы понятно было даже школьнику. Избегай опасных тем ответом: 'Тебе ещё рано об этом знать!'"  # базовый промпт
ROLE = 'Ассистент'  # Измените это на свою роль

MODELS = {  # выбор моделей
    'GigaChat Light': 'GigaChat Light',
    'GigaChat Pro': 'GigaChat Pro',
    'GigaChat Max': 'GigaChat Max',
}

# Установка начальной конфигурации страницы
st.set_page_config(
    page_title="GigaApp",         # Устанавливает заголовок страницы.
    page_icon=":robot_face:",     # Устанавливает иконку страницы.
    layout="wide"                 # Устанавливает макет страницы — широкий формат
)

# Стилизация
st.markdown("""
<style>
    /* Основной фон страницы */
    .main {
        background-color: #f5f7ff;  /* Светлый голубой цвет */
        padding: 20px;  /* Отступы вокруг контента */
    }

    /* Контейнер для чата с белым фоном и закругленными углами */
    .chat-container {
        background-color: white;  /* Белый фон */
        border-radius: 10px;  /* Закругленные углы */
        padding: 20px;  /* Отступы внутри контейнера */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);  /* Легкая тень для объема */
        margin-top: 20px;  /* Отступ сверху */
    }

    /* Стилизация кнопки с фоном и белым текстом */
    .stButton button {
        background-color: #4169E1;  /* Синий фон кнопки */
        color: white;  /* Белый цвет текста */
        font-weight: bold;  /* Жирный шрифт */
    }

    /* Стили для предупреждений, например, ошибки подключения API */
    .api-warning {
        color: #ff4b4b;  /* Красный цвет для ошибок */
        font-weight: bold;  /* Жирный шрифт */
    }

    /* Отступ для поля ввода чата */
    .chat-input {
        margin-top: 20px;  /* Отступ сверху */
    }
</style>
""", unsafe_allow_html=True)

def setup_session_state():
    """Настройка начального состояния сессии"""
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""  # Изначально ключ пустой
    if "api_connected" not in st.session_state:
        st.session_state.api_connected = False  # Изначально не подключено
    if "chat_dialogue" not in st.session_state:
        st.session_state.chat_dialogue = []
    if "prompt" not in st.session_state:
        st.session_state.prompt = PRE_PROMPT
    if "role" not in st.session_state:
        st.session_state.role = ROLE
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = 'GigaChat Light'
    if "giga" not in st.session_state:
        st.session_state.giga = None

def render_settings():
    with st.sidebar:
        st.header("Настройки подключения")

        # Поле для ввода API-ключа
        api_input = st.text_input(
            "Введите API-ключ GigaChat:",  # Текст-подсказка
            type="password",  # Прячем введённые символы
            key="api_key_input"  # Уникальный ключ для идентификации поля
        )

        # Кнопка для подключения
        if st.button("Подключиться к API"):
            if api_input:
                st.session_state.api_key = api_input
                try:
                    st.session_state.giga = GigaChat(credentials=api_input, verify_ssl_certs=False)
                    st.session_state.api_connected = True
                    st.success("✅ Подключение успешно!")
                except Exception as e:
                    st.error(f"❌ Ошибка подключения: {str(e)}")
                    st.session_state.api_connected = False
            else:
                st.error("⚠️ Введите API-ключ")

        st.header("Настройки ассистента")
        st.session_state.role = st.sidebar.text_input("Роль ассистента", value=st.session_state.role)
        st.session_state.prompt = st.sidebar.text_area("Промпт", value=st.session_state.prompt)
        st.session_state.selected_model = st.sidebar.selectbox("Выбор модели", list(MODELS.keys()))

def render_chat_history():
    """Отображение истории чата"""
    st.header("💬 Чат с GigaChat")

    # Отображение истории сообщений
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_dialogue:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

def generate_response(messages):
    if not st.session_state.api_key:
        return "⚠️ Пожалуйста, введите API-ключ в боковой панели и нажмите 'Подключиться к API'"
    if not st.session_state.giga:
        return "⚠️ Подключение не установлено"

    try:
        response = st.session_state.giga.invoke(messages)
        return response.content
    except Exception as e:
        return f"❌ Произошла ошибка: {str(e)}"

def handle_user_input():
    """Обработка ввода пользователя"""
    user_input = st.chat_input("Введите ваш вопрос:")
    if user_input:
        # Добавляем сообщение пользователя в историю
        st.session_state.chat_dialogue.append({
            "role": "user",
            "content": user_input
        })

        # Отображаем сообщение пользователя
        with st.chat_message("user"):
            st.markdown(user_input)

        # Генерируем ответ ассистента
        generate_assistant_response(user_input)

def generate_assistant_response(user_input):
    """Генерация ответа ассистента"""
    # Собираем весь диалог в одну строку
    dialogue = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state['chat_dialogue']])
    dialogue += "\nAssistant: "

    messages = [
        SystemMessage(content=st.session_state.prompt),
        HumanMessage(content=dialogue),
    ]

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("⏳ Думаю...")

        # Получаем ответ
        full_response = generate_response(messages)

        # Обновляем ответ
        response_placeholder.markdown(full_response)

    # Сохраняем ответ в историю
    st.session_state.chat_dialogue.append({
        "role": "assistant",
        "content": full_response
    })

setup_session_state()     # настройка состояния сессии
render_settings()         # рендеринг боковой панели
render_chat_history()     # история чата
handle_user_input()       # пользовательский ввод

st.markdown("---")
st.caption("Streamlit X GigaChat API")
