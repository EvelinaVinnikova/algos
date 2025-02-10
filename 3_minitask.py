import sys
import subprocess
import os

def run_command(command):
    """Запускает команду в shell и возвращает код завершения"""
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode

def main(repo_path, good_commit, bad_commit, check_command):
    """Бинарный поиск первого плохого коммита"""
    
    # Переход в репозиторий
    if not os.path.exists(repo_path):
        print(f"Ошибка: Путь '{repo_path}' не найден")
        sys.exit(1)
    
    os.chdir(repo_path)

    # Запуск git bisect
    subprocess.run("git bisect start", shell=True, check=True)
    subprocess.run(f"git bisect good {good_commit}", shell=True, check=True)
    subprocess.run(f"git bisect bad {bad_commit}", shell=True, check=True)

    # Автоматический бинарный поиск
    exit_code = subprocess.run(f"git bisect run bash -c '{check_command}'", shell=True).returncode

    # Очистка bisect
    subprocess.run("git bisect reset", shell=True, check=True)

    # Вывод результата
    if exit_code == 0:
        print("Поиск завершен успешно!")
    else:
        print("Ошибка во время выполнения поиска!")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Использование: python script.py <repo_path> <good_commit> <bad_commit> <check_command>")
        sys.exit(1)

    repo_path = sys.argv[1]
    good_commit = sys.argv[2]
    bad_commit = sys.argv[3]
    check_command = sys.argv[4]

    main(repo_path, good_commit, bad_commit, check_command)
