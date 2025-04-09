# Импортируем необходимые библиотеки
import os  # Для работы с файловой системой, например, чтобы получать список файлов в директории
import math  # Для математических вычислений, например, логарифм
from collections import Counter  # Для удобного подсчёта элементов в списке
import nltk  # Библиотека для обработки естественного языка
from nltk.tokenize import word_tokenize  # Для разбиения текста на токены (слова)
from nltk.stem import WordNetLemmatizer  # Для лемматизации слов (приведения к нормальной форме)

# Загружаем необходимые ресурсы для NLTK
nltk.download('punkt')  # Скачиваем токенизатор
nltk.download('wordnet')  # Скачиваем словарь WordNet для лемматизации

# Функция для чтения всех текстовых файлов из папки
def read_documents(folder_path):
    documents = []  # Создаём пустой список для хранения текстов документов
    filenames = []  # Список для хранения имён файлов
    for filename in os.listdir(folder_path):  # Проходимся по каждому файлу в указанной папке
        if filename.endswith(".html"):  # Проверяем, что файл имеет расширение .txt
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:  # Открываем файл с указанием кодировки
                documents.append(file.read())  # Читаем содержимое файла и добавляем в список документов
                filenames.append(filename)  # Добавляем имя файла в список имён
    return documents, filenames  # Возвращаем список документов и список имён файлов

# Функция для предварительной обработки текста: токенизация и лемматизация
def preprocess(text):
    tokens = word_tokenize(text.lower())  # Приводим текст к нижнему регистру и разбиваем на токены
    lemmatizer = WordNetLemmatizer()  # Создаём объект лемматизатора
    lemmas = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha()]  # Лемматизируем токены, оставляя только алфавитные
    return tokens, lemmas  # Возвращаем исходные токены и леммы

# Функция для вычисления TF (Term Frequency) для списка токенов
def compute_tf(tokens):
    token_count = Counter(tokens)  # Считаем количество вхождений каждого токена
    total_tokens = len(tokens)  # Получаем общее количество токенов в документе
    tf = {token: count / total_tokens for token, count in token_count.items()}  # Вычисляем TF для каждого токена
    return tf  # Возвращаем словарь TF

# Функция для вычисления IDF (Inverse Document Frequency) для всех документов
def compute_idf(documents_tokens):
    N = len(documents_tokens)  # Общее количество документов
    df = Counter()  # Счётчик для подсчёта количества документов, содержащих термин

    # Проходим по токенам каждого документа
    for tokens in documents_tokens:
        unique_tokens = set(tokens)  # Получаем уникальные токены документа
        for token in unique_tokens:  # Проходим по каждому уникальному токену
            df[token] += 1  # Увеличиваем счётчик документов для токена

    # Вычисляем IDF для каждого токена
    idf = {token: math.log(N / df_count) for token, df_count in df.items()}  # log(N / df)
    return idf  # Возвращаем словарь IDF

# Функция для записи результатов в файл
def save_results(folder, filename, tf, idf):
    os.makedirs(folder, exist_ok=True)  # Создаём папку, если её ещё нет
    file_path = os.path.join(folder, filename)
    with open(file_path, 'w', encoding='utf-8') as f:  # Открываем файл для записи
        f.write("Term\tTF\tIDF\n")  # Пишем заголовок таблицы
        for term in tf:  # Проходим по каждому термину в TF
            f.write(f"{term}\t{tf[term]:.6f}\t{idf.get(term, 0):.6f}\n")  # Записываем термин, его TF и IDF

# Основная функция, объединяющая все шаги
def main():
    folder_path = os.path.join("..", "Task1", "downloaded_pages")
    documents, filenames = read_documents(folder_path)  # Читаем документы и имена файлов
 
    all_tokens = []  # Список для хранения токенов всех документов
    all_lemmas = []  # Список для хранения лемм всех документов

    documents_tokens = []  # Список для хранения токенов документов
    documents_lemmas = []  # Список для хранения лемм документов
    # Предобрабатываем каждый документ
    for doc in documents:
        tokens, lemmas = preprocess(doc)  # Токенизируем и лемматизируем документ
        documents_tokens.append(tokens)  # Добавляем токены документа в общий список
        documents_lemmas.append(lemmas)  # Добавляем леммы документа в общий список
        all_tokens.extend(tokens)  # Добавляем токены в общий список всех токенов
        all_lemmas.extend(lemmas)  # Добавляем леммы в общий список всех лемм

    # Вычисляем IDF для токенов и лемм
    idf_tokens = compute_idf(documents_tokens)  # IDF по токенам
    idf_lemmas = compute_idf(documents_lemmas)  # IDF по леммам

    # Вычисляем и сохраняем TF и IDF для каждого документа
    for i, filename in enumerate(filenames):
        tf_tokens = compute_tf(documents_tokens[i])  # TF по токенам для текущего документа
        tf_lemmas = compute_tf(documents_lemmas[i])  # TF по леммам для текущего документа

        save_results("idf_tokens", f"{filename}_tf_idf_tokens.txt", tf_tokens, idf_tokens)  # Сохраняем результаты по токенам
        save_results("idf_lemmas", f"{filename}_tf_idf_lemmas.txt", tf_lemmas, idf_lemmas)  # Сохраняем результаты по леммам

# Точка входа в программу
if __name__ == "__main__":
    main()  # Запускаем основную функцию