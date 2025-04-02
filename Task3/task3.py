import re  # Импортируем модуль регулярных выражений для разбора текста

# Словарь документов: ключ — ID, значение — текст документа
documents = {
    0: "Леонардо ДиКаприо и Мартин Скорсезе сняли новый фильм",
    1: "Марго Робби сыграла главную роль в Барби",
    2: "Квентин Тарантино известен своими нестандартными фильмами",
    3: "Брэд Питт и Джордж Клуни снова снимаются вместе",
    4: "Оскар получил фильм Кристофера Нолана"
}

# Функция создания инвертированного индекса: слово → множество ID документов
def build_inverted_index(docs):
    index = {}
    for doc_id, text in docs.items():
        # Приводим к нижнему регистру и находим все слова
        words = re.findall(r'\w+', text.lower())
        for word in set(words):  # set() — убираем повторы слов
            index.setdefault(word, set()).add(doc_id)  # Добавляем ID документа в множество
    return index

# Булева операция AND: пересечение множеств
def boolean_and(set1, set2):
    return set1 & set2

# Булева операция OR: объединение множеств
def boolean_or(set1, set2):
    return set1 | set2

# Булева операция NOT: множество всех документов минус те, что в set1
def boolean_not(set1, all_docs):
    return all_docs - set1

# Главная функция, обрабатывающая логический запрос
def evaluate_query(query, index, all_doc_ids):
    query = query.lower()  # Приводим запрос к нижнему регистру
    # Разбиваем запрос на токены: слова, операторы, скобки
    tokens = re.findall(r'\w+|AND|OR|NOT|\(|\)', query)
    
    # Функция: токен → множество документов
    def token_to_set(token):
        if token in index:
            return index[token]         # Если слово есть в индексе
        elif re.match(r'\w+', token):   # Если это слово, но его нет в индексe
            return set()                # Пустое множество
        return token                    # Если это оператор или скобка — вернуть как есть

    output = []  # Стек для операндов (множеств документов)
    ops = []     # Стек для операторов (AND, OR, NOT, скобки)

    # Приоритет операторов: NOT > AND > OR
    precedence = {'NOT': 3, 'AND': 2, 'OR': 1}

    # Функция, применяющая оператор к элементам из стека
    def apply_op(op):
        if op == 'NOT':
            operand = output.pop()
            output.append(boolean_not(operand, all_doc_ids))
        else:
            right = output.pop()
            left = output.pop()
            if op == 'AND':
                output.append(boolean_and(left, right))
            elif op == 'OR':
                output.append(boolean_or(left, right))

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '(':  # Если открывающая скобка — просто кладём на стек
            ops.append(token)
        elif token == ')':  # Закрывающая скобка — применяем операторы до '('
            while ops and ops[-1] != '(':
                apply_op(ops.pop())
            ops.pop()  # Убираем '('
        elif token.upper() in ('AND', 'OR', 'NOT'):  # Если это логический оператор
            while ops and ops[-1] != '(' and precedence.get(ops[-1], 0) >= precedence[token.upper()]:
                apply_op(ops.pop())  # Применяем оператор с более высоким приоритетом
            ops.append(token.upper())
        else:
            # Это слово: преобразуем в множество документов и кладём в стек
            output.append(token_to_set(token))
        i += 1

    # Обрабатываем оставшиеся операторы
    while ops:
        apply_op(ops.pop())

    return output[0]  # Результат запроса — верхний элемент стека

# Главная функция, запускающая поиск
def run_search_engine():
    # Строим индекс и множество всех ID документов
    index = build_inverted_index(documents)
    all_doc_ids = set(documents.keys())

    # Приветственное сообщение
    print("Введите логический запрос (используйте AND, OR, NOT, скобки).")
    print("Пример: (ДиКаприо AND Барби) OR Тарантино\n")

    while True:
        # Ввод запроса пользователем
        user_query = input("🔍 Ваш запрос (или 'выход'): ")
        if user_query.strip().lower() in ["выход", "quit", "exit"]:
            break  # Завершаем работу по команде

        try:
            # Выполняем поиск
            result = evaluate_query(user_query, index, all_doc_ids)
            if result:
                print("🔎 Найдены документы:")
                for doc_id in sorted(result):
                    print(f"[{doc_id}] {documents[doc_id]}")
            else:
                print("⚠️ Ничего не найдено.")
        except Exception as e:
            print("❌ Ошибка в запросе:", e)
        print()

# Точка входа в программу
if __name__ == "__main__":
    run_search_engine()
