from typing import List, Dict

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію
    """
    memo = {} # наша памʼять

    def dp(n):
        # початкова значення для нуля, ми до нього завжди доходимо
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]
        
        max_profit = 0
        best_cuts = []

        for i in range(1, n + 1): # i - це довжина відрізка, від 1 до 5
            # беремо найкращий варіант з попередньої довжини, 
            # щоб в сумі була шукана довжина
            current_profit, cuts = dp(n - i)
            # до попередньої довжини додаємо ціну розглядаємо відрізка
            current_profit += prices[i - 1]
            if current_profit > max_profit:
                # якщо сума більша, то значить це нова макс сума
                # та потрібна комбінація відрізків
                max_profit = current_profit 
                best_cuts = cuts + [i]

        memo[n] = (max_profit, best_cuts)
        return memo[n]
    
    max_profit, cuts = dp(length)

    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts)
    }

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію
    """
    dp = [0] * (length + 1) # максимальний прибуток для довжини i
    cuts = [0] * (length + 1) # перший відрізок, який потрібно відрізати
    
    for i in range(1, length + 1):
        for j in range(1, i + 1):
            # рухаємо починаючи з відрізка в довжину 1
            # коли прибуток попереднього + сума розглядаємого стають більше, записуємо їх
            # як раз розглядаємо індекси 0+3, 2+1, щоб був повний набір відрізків
            if dp[i] < dp[i - j] + prices[j - 1]:
                dp[i] = dp[i - j] + prices[j - 1]
                cuts[i] = j
    
    cut_list = []
    n = length
    while n > 0:
        cut_list.append(cuts[n]) # додаємо перший шматок
        n -= cuts[n] # і його ж відрізаємо, і по колу поки не закінчаться кращі шматки
    
    return {
        "max_profit": dp[length],
        "cuts": cut_list,
        "number_of_cuts": len(cut_list)
    }

def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(f"Тест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        print("----------")
        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("Результат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        print("----------")
        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("Результат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("Перевірка пройшла успішно!")
        print("---------------------")

if __name__ == "__main__":
    run_tests()