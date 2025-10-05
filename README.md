# Improved Streamlit GigaChat App

Интерактивное веб-приложение на базе **Streamlit** для общения с **GigaChat API** от Сбера. Поддерживает настройку роли, системного промпта и выбор модели.

## Возможности

- Подключение к GigaChat API по API-ключу
- Выбор модели: Light / Pro / Max
- Настройка роли и системной инструкции (prompt)
- Сохранение истории диалога
- Простой интерфейс на базе Streamlit

## Используемые технологии

- [`GigaChat API`](https://developers.sber.ru/docs/ru/gigachat/quickstart/main) — работа с языковой моделью от Сбера
- [Streamlit](https://streamlit.io/) — быстрый прототипинг веб-интерфейса
- [LangChain](https://www.langchain.com/) — фреймворк для создания LLM-приложений, позволяет строить цепочки обработки, подключать внешние источники данных, инструменты и агенты.
- [langchain-gigachat](https://pypi.org/project/langchain-gigachat/)
- `ngrok` — инструмент для проброса локального сервера в интернет. Используется для доступа к приложению извне (например, при запуске в Google Colab).

## Демонстрация

[![image.png](https://i.postimg.cc/vmnjTKTY/image.png)](https://postimg.cc/jWsvkZym)

## Результат

Создано полноценное приложение на Streamlit с интеграцией GigaChat API. В этом приложении реализован функционал чата, где пользователи могут вводить свои запросы и получать ответы от модели GigaChat.

Настроено подключение через API-ключ, обработку ошибок, а также хранение истории сообщений в сессии.

## Как запустить

1. **Установите зависимости:**

```bash
pip install streamlit langchain langchain-gigachat
```

2. **Запустите приложение:**

```bash
streamlit run app.py
```

3. **Введите API-ключ от GigaChat** в боковой панели и нажмите “Подключиться к API”.

## Связанные проекты

- [Gigachat Streamlit Demo App](https://github.com/QSquirreld/Gigachat-Streamlit-Demo-App) — демо GigaChat Streamlit.
