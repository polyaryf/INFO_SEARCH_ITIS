import os  # Модуль для работы с файловой системой
from bs4 import BeautifulSoup  # Библиотека для парсинга HTML
import nltk  # Библиотека для обработки естественного языка
from nltk.tokenize import word_tokenize  # Функция для разбиения текста на токены
from nltk.corpus import stopwords  # Стоп-слова для фильтрации ненужных слов
from nltk.stem import WordNetLemmatizer  # Лемматизатор для приведения слов к начальной форме

# Скачиваем необходимые ресурсы для nltk
nltk.download('punkt')  # Токенизатор
nltk.download('stopwords')  # Стоп-слова
nltk.download('wordnet')  # Лемматизатор

# Функция для токенизации и фильтрации текста
def tokenize_and_filter(text):
    tokens = word_tokenize(text)  # Разбиваем текст на токены (слова, знаки препинания)
    stop_words = set(stopwords.words("russian"))  # Загружаем список стоп-слов на русском языке
    
    # Оставляем только слова, исключаем числа и стоп-слова
    filtered_tokens = [token.lower() for token in tokens if token.isalpha() and token.lower() not in stop_words]
    return filtered_tokens

# Функция для лемматизации токенов
def lemmatize_tokens(tokens):
    lemmatizer = WordNetLemmatizer()  # Создаём объект лемматизатора
    return [lemmatizer.lemmatize(token) for token in tokens]  # Лемматизируем каждый токен

# Функция для обработки одного HTML-файла
def process_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()  # Читаем содержимое HTML-файла

    soup = BeautifulSoup(html_content, 'html.parser')  # Создаём объект BeautifulSoup для парсинга HTML
    text_content = soup.get_text()  # Извлекаем текст без разметки

    tokens = tokenize_and_filter(text_content)  # Токенизируем и фильтруем текст
    lemmatized_tokens = lemmatize_tokens(tokens)  # Лемматизируем токены

    return tokens, lemmatized_tokens  # Возвращаем токены и их лемматизированные формы

# Функция для обработки всех HTML-файлов в директории
def process_all_html_files(directory_path):
    all_tokens = []  # Список для хранения всех токенов
    all_lemmatized_tokens = []  # Список для хранения всех лемматизированных токенов

    print("DEBUG: ", directory_path)
    for filename in os.listdir(directory_path):  # Перебираем все файлы в папке
        file_path = os.path.join(directory_path, filename)  # Формируем полный путь к файлу
        if filename.endswith('.html'):  # Проверяем, является ли файл HTML
            print(f"Обрабатывается файл: {filename}")  # Выводим название файла
            tokens, lemmatized_tokens = process_html_file(file_path)  # Обрабатываем файл
            all_tokens.extend(tokens)  # Добавляем токены в общий список
            all_lemmatized_tokens.extend(lemmatized_tokens)  # Добавляем лемматизированные токены

    all_tokens = list(set(all_tokens))  # Убираем дубликаты из списка токенов

    # Группируем токены по леммам
    lemmatized_grouped = {}
    for token, lemmatized_token in zip(all_tokens, all_lemmatized_tokens):
        if lemmatized_token not in lemmatized_grouped:
            lemmatized_grouped[lemmatized_token] = []  # Создаём список, если леммы ещё нет в словаре
        lemmatized_grouped[lemmatized_token].append(token)  # Добавляем токен в соответствующую лемму

    return all_tokens, lemmatized_grouped  # Возвращаем списки токенов и сгруппированных лемм

# Функция для записи данных в файл
def write_to_file(filename, data, is_lemmatized=False):
    with open(filename, 'w', encoding='utf-8') as file:
        if is_lemmatized:  # Если записываем лемматизированные токены
            for lemma, tokens in data.items():
                file.write(f"{lemma} {' '.join(tokens)}\n")  # Формат: "лемма токен1 токен2 ..."
        else:
            for token in data:
                file.write(f"{token}\n")  # Просто записываем каждый токен на новой строке

# Основная функция
def main():
    directory_path = os.path.join(os.path.dirname(os.getcwd()), "downloaded_pages")  # Путь к папке с HTML-файлами
    
    all_tokens, lemmatized_grouped = process_all_html_files(directory_path)  # Обрабатываем все файлы

    write_to_file('tokens.txt', all_tokens)  # Записываем токены в файл
    write_to_file('lemmatized_tokens.txt', lemmatized_grouped, is_lemmatized=True)  # Записываем леммы

    print(f"Токенов: {len(all_tokens)}. Лемматизированных токенов: {len(lemmatized_grouped)}")  # Выводим результат

if __name__ == "__main__":
    main()  # Запускаем основную функцию