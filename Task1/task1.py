import requests  # Импортируем библиотеку requests для выполнения HTTP-запросов
from bs4 import BeautifulSoup  # Импортируем BeautifulSoup для работы с HTML-разметкой
import os  # Импортируем os для работы с файловой системой
import time  # Импортируем time для создания задержек между запросами

# Папка для сохранения выкаченных страниц
OUTPUT_DIR = "downloaded_pages"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Создаём папку, если она не существует

#  Gредварительно  подготовленный список ссылок 
URLS = [
"https://vkusvill.ru/goods/ananas-rezanyy-140-g-47360.html",
"https://vkusvill.ru/goods/assorti-dayfukumoti-zam-4-sht-76462.html",
"https://vkusvill.ru/goods/assorti-mini-makaron-54433.html",
"https://vkusvill.ru/goods/assorti-iz-yablochnoy-pastily-fruktovo-yagodnoe-103335.html",
"https://vkusvill.ru/goods/assorti-iz-yablochnoy-pastily-200g-81455.html",
"https://vkusvill.ru/goods/assorti-makaron-vanil-fistashka-mango-marakuyya-36457.html",
"https://vkusvill.ru/goods/assorti-makaron-klubnichnyy-chizkeyk-chernika-fistashka-98224.html",
"https://vkusvill.ru/goods/assorti-makaron-mandarin-solyenaya-karamel-malina-42152.html",
"https://vkusvill.ru/goods/assorti-makaron-medovik-shokolad-shtrudel-103755.html",
"https://vkusvill.ru/goods/assorti-moti-sochnyy-miks-s-nachinkoy-zam-4-sht-94189.html",
"https://vkusvill.ru/goods/assorti-eklerov-vanil-fistashka-shokolad-53470.html",
"https://vkusvill.ru/goods/assorti-eklerov-syrnyy-s-maskarpone-i-plombir-5-sht-104212.html",
"https://vkusvill.ru/goods/assorti-eklerov-mango-syrnyy-lesnye-yagody-53640.html",
"https://vkusvill.ru/goods/assorti-eklerov-klassika-vkusov-3-sht-86796.html",
"https://vkusvill.ru/goods/banan-v-shokolade-27464.html",
"https://vkusvill.ru/goods/banan-v-shokolade-ves-59065.html",
"https://vkusvill.ru/goods/bananovyy-keks-s-orekhom-18744.html",
"https://vkusvill.ru/goods/batonchik-vozdushnaya-nuga-s-pechenem-v-shokolade-98346.html",
"https://vkusvill.ru/goods/batonchik-arakhis-vozdushnyy-ris-s-solyenoy-karamelyu-v-shok-79711.html",
"https://vkusvill.ru/goods/batonchik-arakhis-v-karamelnom-shokolade-vegan-36128.html",
"https://vkusvill.ru/goods/batonchik-grechishnyy-vegan-41980.html",
"https://vkusvill.ru/goods/batonchik-izyum-gretskiy-orekh-arakhis-s-pechenem-79378.html",
"https://vkusvill.ru/goods/batonchik-izyum-chernosliv-gretskiy-orekh-vegan-43934.html",
"https://vkusvill.ru/goods/batonchik-kakao-arakhis-vegan-77601.html",
"https://vkusvill.ru/goods/batonchik-karamelnoe-naslazhdenie-s-nugoy-i-pechenem-78563.html",
"https://vkusvill.ru/goods/batonchik-karamelnoe-naslazhdenie-s-nugoy-i-pechenem-ves-103043.html",
"https://vkusvill.ru/goods/batonchik-lesnoy-orekh-s-nugoy-i-karamelyu-83446.html",
"https://vkusvill.ru/goods/batonchik-kokos-v-karamelnom-shokolade-36130.html",
"https://vkusvill.ru/goods/batonchik-mindalnoe-praline-s-arakhisom-vegan-81782.html",
"https://vkusvill.ru/goods/batonchik-nuga-v-temnom-shokolade-s-fundukom-48166.html",
"https://vkusvill.ru/goods/batonchik-solenaya-karamel-v-shokolade-vegan-43938.html",
"https://vkusvill.ru/goods/batonchik-shokoladnyy-s-fundukom-vegan-76343.html",
"https://vkusvill.ru/goods/batonchik-shokoladnye-palochki-s-keshyu-vegan-76344.html",
"https://vkusvill.ru/goods/batonchik-khalva-v-molochnom-shokolade-105195.html",
"https://vkusvill.ru/goods/batonchik-arakhisovyy-s-sol-karamelyu-so-vkusom-irisa-70437.html",
"https://vkusvill.ru/goods/batonchik-glazir-martsipanovyy-klassicheskiy-34112.html",
"https://vkusvill.ru/goods/batonchik-zlakovyy-41786.html",
"https://vkusvill.ru/goods/batonchik-zlakovyy-s-klubnikoy-v-molochnom-shokolade-79953.html",
"https://vkusvill.ru/goods/batonchik-zlakovyy-so-sgushchennym-molokom-i-kakao-ves-105207.html",
"https://vkusvill.ru/goods/batonchik-iz-belevskoy-pastily-s-malinoy-83444.html",
"https://vkusvill.ru/goods/batonchik-iz-belevskoy-pastily-yagodnoe-assorti-83443.html",
"https://vkusvill.ru/goods/batonchik-zlakovyy-so-sgushchennym-molokom-i-yagodami-cherniki-ves-105209.html",
"https://vkusvill.ru/goods/batonchik-iz-belevskoy-yablochnoy-pastily-s-chernikoy-44736.html",
"https://vkusvill.ru/goods/batonchik-iz-belevskoy-yablochnoy-pastily-s-chernoy-smorodinoy-62231.html",
"https://vkusvill.ru/goods/batonchik-kokosovyy-s-limonom-71052.html",
"https://vkusvill.ru/goods/batonchik-orekhovyy-proteinovyy-mindal-pekan-40g-84729.html",
"https://vkusvill.ru/goods/batonchik-orekhovyy-yabloko-med-70992.html",
"https://vkusvill.ru/goods/batonchik-martsipanovyy-apelsinka-v-tem-shokolade-90766.html",
"https://vkusvill.ru/goods/batonchik-nizkouglevodnyy-s-kofe-vegan-97799.html",
"https://vkusvill.ru/goods/batonchik-orekhovyy-arakhis-keshyu-semena-tykvy-70997.html",
"https://vkusvill.ru/goods/batonchik-proteinovyy-solyenaya-karamel-v-moloch-shok-97796.html",
"https://vkusvill.ru/goods/batonchik-proteinovyy-glazirovannyy-arakhis-solenaya-karamel-77909.html",
"https://vkusvill.ru/goods/batonchik-proteinovyy-solenaya-karamel-s-fistashkami-89676.html",
"https://vkusvill.ru/goods/batonchik-proteinovyy-s-fistashkami-i-klyukvoy-vegan-63693.html",
"https://vkusvill.ru/goods/batonchik-proteinovyy-s-malinoy-i-keshyu-89675.html",
"https://vkusvill.ru/goods/batonchik-proteinovyy-mango-puding-86065.html",
"https://vkusvill.ru/goods/batonchik-shokoladnyy-martsipanovyy-vegan-91396.html",
"https://vkusvill.ru/goods/batonchik-myusli-s-bananom-72738.html",
"https://vkusvill.ru/goods/batonchik-myusli-s-klubnikoy-72732.html",
"https://vkusvill.ru/goods/batonchiki-shokoladnye-s-risovymi-sharikami-180-g-63634.html",
"https://vkusvill.ru/goods/batonchik-myusli-s-yablokom-v-karameli-i-koritsey-77069.html",
"https://vkusvill.ru/goods/batonchik-myusli-s-klyukvoy-72737.html",
"https://vkusvill.ru/goods/beze-klassicheskoe-31842.html",
"https://vkusvill.ru/goods/beze-assorti-s-kusochkami-yagod-48025.html",
"https://vkusvill.ru/goods/beze-kokosovoe-81269.html",
"https://vkusvill.ru/goods/vafelnaya-konfeta-s-kokosovoy-nachinkoy-v-belom-shokolade-ves-94214.html",
"https://vkusvill.ru/goods/brauni-proteinovoe-s-vishney-64469.html",
"https://vkusvill.ru/goods/brauni-proteinovoe-s-apelsinom-65336.html",
"https://vkusvill.ru/goods/brauni-proteinovoe-64471.html",
"https://vkusvill.ru/goods/brauni-iz-zelenoy-grechki-45038.html",
"https://vkusvill.ru/goods/vafli-gollandskie-s-limonnoy-nachinkoy-95760.html",
"https://vkusvill.ru/goods/vafli-arakhisovaya-pasta-v-shokoladnoy-glazuri-72769.html",
"https://vkusvill.ru/goods/vafli-gollandskie-s-molochnoy-karamelyu-48027.html",
"https://vkusvill.ru/goods/vafli-kokosovye-17573.html",
"https://vkusvill.ru/goods/vafli-kofeynye-150g-84196.html",
"https://vkusvill.ru/goods/vafli-klassicheskie-s-shokoladnym-listom-96394.html",
"https://vkusvill.ru/goods/vafli-limonnye-80g-39566.html",
"https://vkusvill.ru/goods/vafli-slivochnye-15250.html",
"https://vkusvill.ru/goods/vafli-slivochnye-350g-77590.html",
"https://vkusvill.ru/goods/vafli-ovsyanye-s-molokom-bez-dobavleniya-sakhara-83981.html",
"https://vkusvill.ru/goods/vafli-detskie-shokolad-bez-dob-sakhara-63205.html",
"https://vkusvill.ru/goods/vafli-grechishnye-s-belym-kokosovym-shokoladom-56673.html",
"https://vkusvill.ru/goods/vafli-s-kakao-15249.html",
"https://vkusvill.ru/goods/vafli-s-kakao-klassicheskie-74816.html",
"https://vkusvill.ru/goods/vafli-s-kakao-350-g-36744.html",
"https://vkusvill.ru/goods/vyalenye-banany-v-kakao-72969.html",
"https://vkusvill.ru/goods/vafli-s-fundukom-orekhovye-20964.html",
"https://vkusvill.ru/goods/vafli-s-kakao-90g-77596.html",
"https://vkusvill.ru/goods/gata-s-gretskim-orekhom-i-izyumom-104873.html",
"https://vkusvill.ru/goods/glazirovannye-konfety-s-orekhovoy-nachinkoy-ves-90489.html",
"https://vkusvill.ru/goods/galeta-s-vishney-160-g-89329.html",
"https://vkusvill.ru/goods/desert-brauni-vegan-44780.html",
"https://vkusvill.ru/goods/desert-verrin-karamelnyy-54999.html",
"https://vkusvill.ru/goods/desert-verrin-s-karamelyu-i-arakhisom-103072.html",
"https://vkusvill.ru/goods/desert-izumrudnaya-nezhnost-s-klubnikoy-103996.html",
"https://vkusvill.ru/goods/desert-dva-shokolada-vegan-77283.html",
"https://vkusvill.ru/goods/desert-verrin-s-karamelyu-i-arakhisom-zam-240-g-103803.html",
"https://vkusvill.ru/goods/desert-kartoshka-v-molochnom-belgiyskom-shokolade-78611.html",
"https://vkusvill.ru/goods/desert-kievskiy-100-g-68366.html",
"https://vkusvill.ru/goods/desert-klubnichnyy-s-syrno-slivochnym-kremom-98381.html",
"https://vkusvill.ru/goods/desert-morkovnyy-na-dvoikh-s-syrno-slivochnym-kremom-300-g-76248.html",
"https://vkusvill.ru/goods/desert-morkovnyy-na-dvoikh-s-syrno-slivochnym-kremom-96522.html",
"https://vkusvill.ru/goods/desert-medovyy-so-smetannym-kremom-140-g-96089.html",
"https://vkusvill.ru/goods/desert-panna-kotvill-vanil-97433.html",
"https://vkusvill.ru/goods/desert-napoleon-postnyy-80166.html",
"https://vkusvill.ru/goods/desert-romovaya-baba-s-vishney-i-krem-chiz-78659.html",
"https://vkusvill.ru/goods/desert-tiramisu-bezlaktoznyy-39512.html",
"https://vkusvill.ru/goods/desert-sufle-s-shokoladom-v-stakane-74947.html",
"https://vkusvill.ru/goods/desert-slivochno-shokoladnyy-s-vishney-71058.html",
"https://vkusvill.ru/goods/desert-tiramisu-bezlaktoznyy-bezglyutenovyy-53809.html",
"https://vkusvill.ru/goods/desert-tiramisu-zam-500-g-70663.html",
"https://vkusvill.ru/goods/desert-tiramisu-s-klubnikoy-zam-300-g-100880.html"
]

# Файл index.txt для хранения информации о выкачанных страницах
INDEX_FILE = "index.txt"

# Задержка между запросами (чтобы избежать блокировок)
REQUEST_DELAY = 2

def download_page(url, file_number):  # Функция для загрузки страницы и сохранения её в файл
    try:
        response = requests.get(url, timeout=10)  # Выполняем GET-запрос к странице
        response.raise_for_status()  # Проверяем успешность запроса
        
        # Формируем имя файла по номеру страницы
        filename = f"page_{file_number}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as file:
            file.write(response.text)  # Сохраняем содержимое страницы в файл

        return filename  # Возвращаем имя файла для записи в index.txt
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")  # Выводим ошибку, если не удалось скачать страницу
        return None  # Возвращаем None при ошибке

def main():  # Главная функция программы
    with open(INDEX_FILE, "w", encoding="utf-8") as index_file:  # Открываем index.txt для записи
        for i, url in enumerate(URLS, start=1):  # Перебираем список ссылок
            filename = download_page(url, i)  # Загружаем страницу
            if filename:  # Если страница успешно загружена
                index_file.write(f"{i} {url}\n")  # Добавляем запись в index.txt
                print(f"✅ Страница {i} загружена: {url}")  # Сообщаем об успешной загрузке
            time.sleep(REQUEST_DELAY)  # Делаем паузу между запросами, чтобы избежать блокировок

if __name__ == "__main__":
    main()  # Запускаем программу