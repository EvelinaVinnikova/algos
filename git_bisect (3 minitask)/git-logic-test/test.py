import subprocess
import sys

# Ожидаемый правильный результат
EXPECTED_SUM = 5

# Запускаем калькулятор и получаем его вывод
result = subprocess.run(
    [sys.executable, 'calculator.py'], 
    capture_output=True, 
    text=True
)

try:
    # Пытаемся превратить вывод в число
    actual_result = int(result.stdout.strip())
    
    # Сравниваем с тем, что ожидали
    if actual_result == EXPECTED_SUM:
        print(f"Тест пройден: результат {actual_result}")
        sys.exit(0) # Код 0 = успех
    else:
        print(f"Тест провален: результат {actual_result}, а ожидалось {EXPECTED_SUM}")
        sys.exit(1) # Код 1 = ошибка

except (ValueError, IndexError):
    print("Тест провален: программа не вывела число")
    sys.exit(1) # Код 1 = ошибка
