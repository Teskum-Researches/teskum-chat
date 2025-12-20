#! /usr/bin/env python3
import sqlite3
import os
from config import db_name

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, db_name)

class ChatDB:
    def __init__(self):
        # Устанавливаем соединение с базой данных
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''') # Создаём таблицу если её ещё нет

    def get_messages(self):
        # Выбираем все сообщения
        self.cursor.execute('SELECT author, content FROM messages')
        output = self.cursor.fetchall()
        messages = []
        for row in output:
            messages.append({"user": row[0], "content": row[1]})
        return messages

    def add_message(self, user: str, text: str) -> None:
        self.cursor.execute(
            "INSERT INTO messages (author, content) VALUES (?, ?)",
            (user, text)
        )
        self.connection.commit()

    def close(self):
        # Закрываем соединение
        self.connection.close()
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()