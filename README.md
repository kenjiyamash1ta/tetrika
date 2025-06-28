# tetrika-junior

## Описание

Репозиторий содержит решения трёх задач на Python для тестового задания:

- **Задача 1:** Декоратор строгой проверки типов (`@strict`)
- **Задача 2:** Сбор статистики по животным с Википедии и запись в CSV
- **Задача 3:** Подсчёт общего времени одновременного присутствия ученика и преподавателя на уроке

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/yourusername/tetrika-junior.git
    ```
2. Создание виртуального окружения
    ```sh
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate  # Windows
    ```
2. Установите зависимости:
    ```sh
    pip install -r requarement.txt
    ```

## Тестирование

Для запуска всех тестов:
```sh
pytest
```

## Проверка покрытия тестами

Для запуска тестов с анализом покрытия:
```sh
pytest --cov=task1 --cov=task2 --cov=task3 --cov-report=term-missing tests/
```

---
