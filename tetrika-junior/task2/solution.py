import csv
import sys
from collections import defaultdict
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import logging
import time

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('animal_counter.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Константы
WIKI_ROOT = "https://ru.wikipedia.org"
ANIMAL_CATEGORY_PATH = "/wiki/Категория:Животные_по_алфавиту"
REQUEST_DELAY = 0.5  # Увеличим задержку для надежности


def fetch_page_content(url):
    """Загружает HTML-контент страницы."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Ошибка при загрузке {url}: {e}")
        raise


def extract_animal_data(html_content):
    """Извлекает имена животных из HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    animal_entries = soup.select('#mw-pages .mw-category-group li')
    return [entry.get_text(strip=True) for entry in animal_entries]


def find_next_page(soup):
    """Ищет ссылку на следующую страницу категории."""
    # Используем string вместо устаревшего text
    next_page_link = soup.find('a', string='Следующая страница')
    if next_page_link:
        return urljoin(WIKI_ROOT, next_page_link['href'])

    # Альтернативный поиск для совместимости
    for link in soup.select('#mw-pages a'):
        if 'pagefrom' in link.get('href', ''):
            return urljoin(WIKI_ROOT, link['href'])
    return None


def collect_animal_statistics():
    """Собирает статистику по животным."""
    statistics = defaultdict(int)
    current_url = urljoin(WIKI_ROOT, ANIMAL_CATEGORY_PATH)
    processed_pages = 0

    logging.info("Начало сбора статистики...")

    while current_url:
        try:
            logging.info(
                f"Обработка страницы {processed_pages + 1}: {current_url}")

            html_content = fetch_page_content(current_url)
            soup = BeautifulSoup(html_content, 'html.parser')

            for animal in extract_animal_data(html_content):
                first_char = animal[0].upper()
                if 'А' <= first_char <= 'Я':
                    statistics[first_char] += 1

            current_url = find_next_page(soup)
            processed_pages += 1
            time.sleep(REQUEST_DELAY)

        except Exception as e:
            logging.error(f"Ошибка при обработке страницы: {str(e)}")
            break

    logging.info(f"Сбор завершен. Обработано страниц: {processed_pages}")
    return statistics


def save_statistics(data, filename='beasts.csv'):
    """Сохраняет статистику в CSV файл."""
    try:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Буква', 'Количество животных'])
            for letter in sorted(data.keys()):
                writer.writerow([letter, data[letter]])
        logging.info(f"Данные сохранены в {filename}")
    except IOError as e:
        logging.error(f"Ошибка записи в файл: {str(e)}")
        raise


if __name__ == '__main__':
    try:
        animal_data = collect_animal_statistics()
        save_statistics(animal_data)
    except Exception as e:
        logging.critical(f"Критическая ошибка: {str(e)}")
        raise
