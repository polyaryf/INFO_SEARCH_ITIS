import os  # Работа с файловой системой
from collections import Counter  # Удобно считать частоты слов
import numpy as np  # Для векторных операций
from sklearn.metrics.pairwise import cosine_similarity  # Косинусное сходство
from nltk.tokenize import word_tokenize  # Токенизация запроса
from nltk.stem import WordNetLemmatizer  # Лемматизация запроса
import nltk

# Скачиваем необходимые ресурсы NLTK
nltk.download('punkt')
nltk.download('wordnet')


# ✅ Функция: загрузка TF-IDF весов из файлов
def load_tf_idf_vectors(folder_path):
    vectors = {}        # Словарь: имя документа -> {термин: вес}
    all_terms = set()   # Множество всех терминов во всём корпусе

    for filename in os.listdir(folder_path):  # Перебираем все файлы в папке
        if filename.endswith("_tf_idf_lemmas.txt"):
            doc_id = filename.replace("_tf_idf_lemmas.txt", "")  # Получаем имя документа без суффикса
            vector = {}  # Временный вектор документа

            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                next(f)  # Пропускаем заголовок строки: Term\tTF\tIDF
                for line in f:
                    parts = line.strip().split('\t')  # Разбиваем по табуляции
                    if len(parts) == 3:
                        term, tf, idf = parts
                        weight = float(tf) * float(idf)  # TF-IDF вес термина
                        vector[term] = weight
                        all_terms.add(term)  # Добавляем в общий список терминов

            vectors[doc_id] = vector  # Сохраняем вектор документа

    return vectors, sorted(all_terms)  # Возвращаем: {документ: вектор}, список всех терминов


# ✅ Функция: выполнить векторный поиск по запросу
def vector_search_from_files(query, vectors, all_terms):
    # Лемматизируем и токенизируем запрос
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(query.lower())
    lemmas = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha()]

    # Считаем TF для лемм запроса
    query_counts = Counter(lemmas)
    total = len(lemmas)
    query_vector = {lemma: (query_counts[lemma] / total) for lemma in query_counts}

    # Вспомогательная функция: словарь -> вектор по all_terms
    def to_vector(vec_dict):
        return np.array([vec_dict.get(term, 0) for term in all_terms])

    query_vec = to_vector(query_vector).reshape(1, -1)  # Преобразуем в 2D-вектор для cosine_similarity

    document_scores = []  # Массив пар (имя документа, сходство)

    for doc_id, doc_vector in vectors.items():
        doc_vec = to_vector(doc_vector).reshape(1, -1)
        sim = cosine_similarity(query_vec, doc_vec)[0][0]  # Вычисляем косинусное сходство
        document_scores.append((doc_id, sim))

    # Сортируем документы по убыванию сходства
    ranked = sorted(document_scores, key=lambda x: x[1], reverse=True)

    print("\n🔍 Результаты поиска по запросу:", query)
    for doc_id, score in ranked:
        if score > 0:
            print(f"{doc_id}: relevance = {score:.4f}")


# ✅ Основная функция
def main():
    folder_path = os.path.join("..", "Task4", "idf_lemmas")  # Путь к папке с tf-idf файлами

    # Загружаем векторы документов и общий словарь терминов
    vectors, all_terms = load_tf_idf_vectors(folder_path)
     # Цикл: запрашиваем у пользователя строку и ищем
    while True:
        query = input("\nВведите поисковый запрос (или 'выход'): ")
        if query.lower() in ["выход", "exit"]:
            print("✅ Завершение работы.")
            break
        vector_search_from_files(query, vectors, all_terms)


# Точка входа в программу
if __name__ == "__main__":
    main()
