from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # працюємо з окремим списком
    jobs = print_jobs.copy()
    groups = list() # фільнальний список груп черги

    while len(jobs): # поки є задачі в списку
        is_group_full = False
        group = list()
        # поки є задачі, група набрала кількість, чи наступна пріорітетна задача не поміститься
        while len(jobs) and len(group) < constraints['max_items'] and not is_group_full:
            # шукаємо задачі з найменшим пріорітетом
            min_priority = min(job["priority"] for job in jobs)
            priority_jobs = [job for job in jobs if job["priority"] == min_priority]

            # якщо декілька з самим малим пріорітетом - фільтруємо з найменшим з часом виконання
            if len(priority_jobs) > 1:
                final_job = min(priority_jobs, key=lambda job: job["print_time"])
            else:
                final_job = priority_jobs[0]
            
            current_group_sum = sum(job["volume"] for job in group)
            # спочатку перевіряємо, чи поміщається в групу
            if current_group_sum + final_job['volume'] <= constraints['max_volume']:
                # закидуємо в групу
                group.append(final_job)
                jobs.remove(final_job)
            else:
                # більше не поміститься, група повна
                is_group_full = True

        groups.append(group)

    total_time = 0
    print_order = list()
    for group in groups:
        # рахуємо максимальне виконання задач в групі
        group_time = max(job["print_time"] for job in group)
        total_time += group_time

        # формуємо список пріоритетів
        for job in group:
            print_order.append(job['id'])

    return {
        "print_order": print_order,
        "total_time": total_time
    }



# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()
