import os
import subprocess
import sys

# Проверяем, что передали правильное количество аргументов
if len(sys.argv) != 5:
    print("Использование: python bisect.py <путь_к_репозиторию> <хороший_коммит> <плохой_коммит> <команда_теста>")
    # Выходим из программы, если аргументов не хватает
    sys.exit(1)

# Получаем аргументы из командной строки
repo_path = sys.argv[1]
good_commit = sys.argv[2]
bad_commit = sys.argv[3]
test_command = sys.argv[4]

# --- Шаг 1: Получаем список коммитов между "хорошим" и "плохим" ---

# Собираем команду для git
get_commits_command = f"git rev-list --reverse {good_commit}..{bad_commit}"

# Запускаем команду в терминале
result = subprocess.run(
    get_commits_command,
    cwd=repo_path,  # Указываем, в какой папке выполнять
    shell=True,  # Позволяет выполнять команду как строку
    capture_output=True,  # Захватываем вывод команды
    text=True  # Чтобы вывод был текстом, а не байтами
)

# Если команда выполнилась с ошибкой, сообщаем и выходим
if result.returncode != 0:
    print("Не удалось получить список коммитов.")
    print(result.stderr)
    sys.exit(1)

# Превращаем строку с коммитами в список
commits_text = result.stdout.strip()
commits = commits_text.split('\n')

# Если список пустой, значит проверять нечего
if not commits_text:
    print("Нет коммитов для проверки.")
    sys.exit(0)

print(f"Начинаем бинарный поиск. Коммитов для проверки: {len(commits)}")

# --- Шаг 2: Бинарный поиск первого "плохого" коммита ---

low = 0
high = len(commits) - 1
first_bad_commit_index = -1

# Цикл работает, пока левая граница не станет больше правой
while low <= high:
    # Находим середину
    mid = (low + high) // 2
    current_commit = commits[mid]

    print(f"Проверяем коммит: {current_commit[:7]}")

    # Переключаемся на этот коммит
    subprocess.run(
        f"git checkout -q {current_commit}",  # -q чтобы git не писал лишнего
        cwd=repo_path,
        shell=True,
        capture_output=True  # Скрываем вывод
    )

    # Запускаем тестовую команду
    test_result = subprocess.run(
        test_command,
        cwd=repo_path,
        shell=True,
        capture_output=True  # Скрываем вывод теста
    )

    # Смотрим на код возврата. 0 - хорошо, не 0 - плохо.
    if test_result.returncode == 0:
        # Коммит хороший. Значит, ошибка где-то справа от него.
        print(" -> Коммит хороший")
        low = mid + 1
    else:
        # Коммит плохой. Возможно, это он и есть.
        # Запоминаем его и ищем дальше в левой половине.
        print(f"    [Ошибка от теста]: {test_result.stderr.strip()}")
        print(" -> Коммит плохой")
        first_bad_commit_index = mid
        high = mid - 1

# --- Шаг 3: Показываем результат ---
print("-" * 40)
if first_bad_commit_index != -1:
    found_commit = commits[first_bad_commit_index]
    print("Первый плохой коммит найден:")

    # Показываем только краткую информацию о коммите
    subprocess.run(
        f"git log -1 --oneline {found_commit}",
        cwd=repo_path,
        shell=True,
        text=True
    )
else:
    print(f"Все промежуточные коммиты хорошие. Проблема, скорее всего, в коммите {bad_commit[:7]}")