import os
import json

# ✅ Указываем путь к папке с лемматизированными токенами из Task2
lemmatized_folder = os.path.join("..", "Task2", "lemmatized_tokens_pages")

# Функция для построения инвертированного индекса
def build_inverted_index_from_files(folder):
    index = {}
    # Список файлов в папке
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder, filename)
            # Получаем ID документа по имени файла
            doc_id = os.path.splitext(filename)[0].replace('lemmatized_tokens_', '')

            # Если doc_id содержит цифры, извлекаем их
            try:
                doc_id = int(''.join(filter(str.isdigit, doc_id)))
            except ValueError:
                pass  # если не число, оставляем как строку

            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # Каждая строка: лемма и её формы (но нам важна только лемма)
                    parts = line.strip().split()
                    if parts:
                        lemma = parts[0]
                        # Добавляем в индекс
                        index.setdefault(lemma, set()).add(doc_id)

    return index

# Основная функция
def main():
    # Строим инвертированный индекс
    inverted_index = build_inverted_index_from_files(lemmatized_folder)

    # Проверяем, не пустой ли индекс
    if not inverted_index:
        print("⚠️ Внимание: индекс пуст. Проверьте папку 'lemmatized_tokens_pages' и её содержимое!")
    else:
        # Сохраняем в JSON-файл
        with open("index.json", "w", encoding="utf-8") as f:
            json.dump({word: list(doc_ids) for word, doc_ids in inverted_index.items()}, f, ensure_ascii=False, indent=4)

        print("✅ Инвертированный индекс сохранён в 'index.json'")

# Точка входа
if __name__ == "__main__":
    main()
