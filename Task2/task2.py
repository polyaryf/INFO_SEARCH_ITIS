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

# Функция для Обработки всех HTML-файлов в директории
def process_all_html_files(directory_path):
    token_folder = "token_pages"
    lemmatized_folder = "lemmatized_tokens_pages"

    for filename in os.listdir(directory_path):
        if filename.endswith('.html'):
            file_path = os.path.join(directory_path, filename)
            print(f"Обрабатывается файл: {filename}")
            tokens, lemmatized_tokens = process_html_file(file_path)

            unique_tokens = list(set(tokens))
            
            lemmatized_grouped = {}
            for token, lemma in zip(tokens, lemmatized_tokens):
                if lemma not in lemmatized_grouped:
                    lemmatized_grouped[lemma] = []
                lemmatized_grouped[lemma].append(token)

            base_filename = os.path.splitext(filename)[0]

            # Запись в соответствующие папки
            write_to_file(token_folder, f'tokens_{base_filename}.txt', unique_tokens)
            write_to_file(lemmatized_folder, f'lemmatized_tokens_{base_filename}.txt', lemmatized_grouped, is_lemmatized=True)



# Функция для записи данных в файл
def write_to_file(folder, filename, data, is_lemmatized=False):
    os.makedirs(folder, exist_ok=True)  # Создаём папку, если её ещё нет
    file_path = os.path.join(folder, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        if is_lemmatized:
            for lemma, tokens in data.items():
                file.write(f"{lemma} {' '.join(tokens)}\n")
        else:
            for token in data:
                file.write(f"{token}\n")


# Основная функция
def main():
    directory_path = os.path.join(os.path.dirname(os.getcwd()), "downloaded_pages")  # Путь к папке с HTML-файлами
    process_all_html_files(directory_path)

if __name__ == "__main__":
    main()  # Запускаем основную функцию