"""
Telegram Cleaner Monitor
=========================
Разработчик: CANICK
Репозиторий: https://github.com/CANICK/Telegram-Cleaner-Monitor

Описание:
Этот скрипт проверяет, запущен ли процесс Telegram. Если процесс не активен, скрипт автоматически очищает указанную пользователем папку.
Параметры (путь к папке и интервал проверки) сохраняются для удобного использования.

Дисклеймер:
Этот скрипт предназначен только для образовательных целей. Автор не несет ответственности за любые
последствия использования программы. Используйте на свой страх и риск.
"""

import os
import time
import psutil
import shutil
import json
from colorama import Fore, Style, init

init(autoreset=True)

SETTINGS_FILE = "settings.txt"

def is_telegram_running(process_name="Telegram.exe"):
    """
    Проверяет, запущен ли процесс с указанным именем.
    """
    for process in psutil.process_iter(attrs=["name"]):
        if process.info["name"] == process_name:
            return True
    return False

def clear_tdata(folder_path):
    """
    Удаляет содержимое указанной папки, но не саму папку.
    """
    if os.path.exists(folder_path):
        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)  # Удаление файла или символической ссылки
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Удаление вложенной папки
            print(Fore.GREEN + f"[INFO] Содержимое папки {folder_path} успешно очищено.")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Ошибка при очистке содержимого папки {folder_path}: {e}")
    else:
        print(Fore.YELLOW + f"[INFO] Папка {folder_path} не существует.")


def load_settings():
    """
    Загружает настройки из файла.
    """
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"folder_path": "", "timer": 300}

def save_settings(settings):
    """
    Сохраняет настройки в файл.
    """
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def main():
    settings = load_settings()
    folder_path = settings["folder_path"]
    timer = settings["timer"]
    is_running = False

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        # Вывод заголовка с автором
        print(Fore.CYAN + Style.BRIGHT + "Telegram Cleaner Monitor")
        print(Fore.YELLOW + "=========================")
        print(Fore.CYAN + "Разработчик: CANICK")
        print(Fore.CYAN + "Репозиторий: https://github.com/CANICK/Telegram-Cleaner-Monitor\n")
        print(Fore.YELLOW + "Описание:")
        print(Fore.WHITE + "Скрипт проверяет, запущен ли Telegram. Если Telegram не активен, очищается выбранная папка.\n")

        # Меню
        print(Fore.MAGENTA + "=== Главное меню ===")
        print(Fore.GREEN + "[1]" + Fore.WHITE + " Включить скрипт")
        print(Fore.GREEN + "[2]" + Fore.WHITE + " Выключить скрипт")
        print(Fore.GREEN + "[3]" + Fore.WHITE + " Указать папку для очистки")
        print(Fore.GREEN + "[4]" + Fore.WHITE + " Изменить интервал проверки (в секундах)")
        print(Fore.RED + "[5]" + Fore.WHITE + " Выход")
        print(Fore.YELLOW + "====================")
        print(Fore.WHITE + f"Статус работы: {Fore.GREEN + 'ВКЛЮЧЕН' if is_running else Fore.RED + 'ВЫКЛЮЧЕН'}")
        print(Fore.WHITE + f"Выбранная папка: {Fore.BLUE + folder_path if folder_path else Fore.RED + 'Не указана'}")
        print(Fore.WHITE + f"Таймер проверки: {Fore.BLUE + str(timer)} секунд")
        print()

        choice = input(Fore.WHITE + "Выберите действие: ")

        if choice == "1":
            if is_running:
                print(Fore.YELLOW + "[INFO] Скрипт уже включен!")
            elif not folder_path:
                print(Fore.RED + "[ERROR] Папка для очистки не указана. Выберите пункт [3].")
            else:
                print(Fore.GREEN + "[INFO] Включаем скрипт...")
                is_running = True
        elif choice == "2":
            if not is_running:
                print(Fore.YELLOW + "[INFO] Скрипт уже выключен!")
            else:
                print(Fore.RED + "[INFO] Выключаем скрипт...")
                is_running = False
        elif choice == "3":
            folder_path = input(Fore.WHITE + "Введите полный путь к папке для очистки: ").strip()
            if os.path.exists(folder_path):
                print(Fore.GREEN + f"[INFO] Папка {folder_path} успешно выбрана.")
                settings["folder_path"] = folder_path
                save_settings(settings)
            else:
                print(Fore.RED + f"[ERROR] Папка {folder_path} не существует. Попробуйте снова.")
        elif choice == "4":
            try:
                timer = int(input(Fore.WHITE + "Введите новый интервал проверки (в секундах): ").strip())
                if timer > 0:
                    settings["timer"] = timer
                    save_settings(settings)
                    print(Fore.GREEN + f"[INFO] Таймер успешно изменен на {timer} секунд.")
                else:
                    print(Fore.RED + "[ERROR] Интервал должен быть больше 0.")
            except ValueError:
                print(Fore.RED + "[ERROR] Некорректный ввод. Укажите целое число.")
        elif choice == "5":
            print(Fore.YELLOW + "[INFO] Завершение программы...")
            break
        else:
            print(Fore.RED + "[ERROR] Некорректный выбор. Попробуйте снова.")
            time.sleep(2)
            continue

        while is_running:
            if is_telegram_running():
                print(Fore.GREEN + "[INFO] Telegram.exe запущен. Ничего не делаем.")
            else:
                print(Fore.YELLOW + f"[INFO] Telegram.exe не запущен. Очищаем папку {folder_path}.")
                clear_tdata(folder_path)

            # Проверка статуса каждые N секунд
            print(Fore.CYAN + f"[INFO] Проверка снова через {timer} секунд...")
            time.sleep(timer)

if __name__ == "__main__":
    main()
