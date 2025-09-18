import os
import subprocess
import sys

SHORT_COMMIT_HASH_LENGTH = 7

if len(sys.argv) != 5:
    print("Использование: python bisect.py <путь_к_репозиторию> <хороший_коммит> <плохой_коммит> <команда_теста>")
    sys.exit(1)

repo_path = sys.argv[1]
good_commit = sys.argv[2]
bad_commit = sys.argv[3]
test_command = sys.argv[4]

get_commits_command = f"git rev-list --reverse {good_commit}..{bad_commit}"

result = subprocess.run(
    get_commits_command,
    cwd=repo_path,
    shell=True,
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print("Не удалось получить список коммитов.")
    print(result.stderr)
    sys.exit(1)

commits_text = result.stdout.strip()
commits = commits_text.splitlines()

if not commits_text:
    print("Нет коммитов для проверки.")
    sys.exit(0)

print(f"Начинаем бинарный поиск. Коммитов для проверки: {len(commits)}")

low = 0
high = len(commits) - 1
first_bad_commit_index = -1

while low <= high:
    mid = (low + high) // 2
    current_commit = commits[mid]

    print(f"Проверяем коммит: {current_commit[:SHORT_COMMIT_HASH_LENGTH]}")

    subprocess.run(
        f"git checkout -q {current_commit}",
        cwd=repo_path,
        shell=True,
        capture_output=True
    )

    test_result = subprocess.run(
        test_command,
        cwd=repo_path,
        shell=True,
        capture_output=True
    )

    if test_result.returncode == 0:
        print(" -> Коммит хороший")
        low = mid + 1
    else:
        print(f"    [Ошибка от теста]: {test_result.stderr.strip()}")
        print(" -> Коммит плохой")
        first_bad_commit_index = mid
        high = mid - 1

print("-" * 40)
if first_bad_commit_index != -1:
    found_commit = commits[first_bad_commit_index]
    print("Первый плохой коммит найден:")

    subprocess.run(
        f"git log -1 --oneline {found_commit}",
        cwd=repo_path,
        shell=True,
        text=True
    )
else:
    print(f"Все промежуточные коммиты хорошие. Проблема, скорее всего, в коммите {bad_commit[:SHORT_COMMIT_HASH_LENGTH]}")



