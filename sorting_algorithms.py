import timeit
import random
from typing import List

def merge_sort(arr):
    """Сортування злиттям - O(n log n)"""
    arr_copy = arr.copy()
    
    def merge(left, right):
        """Злиття двох відсортованих масивів"""
        result = []
        i, j = 0, 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def merge_sort_recursive(arr):
        """Рекурсивна частина сортування злиттям"""
        if len(arr) <= 1:
            return arr
            
        mid = len(arr) // 2
        left = merge_sort_recursive(arr[:mid])
        right = merge_sort_recursive(arr[mid:])
        
        return merge(left, right)
    
    return merge_sort_recursive(arr_copy)

def insertion_sort(arr):
    """Сортування вставками - O(n²)"""
    arr_copy = arr.copy()
    
    for i in range(1, len(arr_copy)):
        key = arr_copy[i]
        j = i - 1
        while j >= 0 and arr_copy[j] > key:
            arr_copy[j + 1] = arr_copy[j]
            j -= 1
        arr_copy[j + 1] = key
    
    return arr_copy

def timsort_wrapper(arr):
    """Обгортка для вбудованого сортування Python (Timsort) - O(n log n)"""
    arr_copy = arr.copy()
    arr_copy.sort()
    return arr_copy

def measure_time_with_timeit(sort_func, arr, number=10):
    """Вимірює час виконання алгоритму сортування за допомогою timeit"""
    # Створюємо функцію для timeit
    def test_function():
        return sort_func(arr.copy())
    
    # Вимірюємо час виконання
    exec_time = timeit.timeit(test_function, number=number) / number
    
    # Отримуємо відсортований масив для перевірки
    sorted_arr = sort_func(arr)
    
    return exec_time, sorted_arr

def compare_sorting_algorithms():
    """Порівнює ефективність трьох алгоритмів сортування"""
    
    # Різні розміри масивів для тестування
    sizes = [100, 500, 1000, 2000]
    algorithms = [
        ("Merge Sort", merge_sort),
        ("Insertion Sort", insertion_sort),
        ("Timsort (Python)", timsort_wrapper)
    ]
    
    print("=== ПОРІВНЯННЯ АЛГОРИТМІВ СОРТУВАННЯ ===\n")
    
    for size in sizes:
        print(f"Розмір масиву: {size} елементів")
        print("-" * 50)
        
        # Генеруємо випадковий масив
        test_array = [random.randint(1, 1000) for _ in range(size)]
        
        results = []
        for name, algorithm in algorithms:
            exec_time, sorted_arr = measure_time_with_timeit(algorithm, test_array, number=5)
            results.append((name, exec_time))
            print(f"{name:20} | Час: {exec_time:.6f} сек (середній з 5 запусків)")
        
        # Знаходимо найшвидший алгоритм
        fastest = min(results, key=lambda x: x[1])
        print(f"Найшвидший: {fastest[0]} ({fastest[1]:.6f} сек)")
        print()

def merge_k_lists(lists: List[List[int]]) -> List[int]:
    """
    Злиття k відсортованих списків в один відсортований список
    
    Args:
        lists: Список відсортованих списків цілих чисел
    
    Returns:
        Відсортований список з усіх елементів
    """
    # Метод 1: Простий підхід - об'єднати всі списки та відсортувати
    merged_list = []
    for lst in lists:
        merged_list.extend(lst)
    
    merged_list.sort()  # Використовуємо Timsort
    return merged_list

def merge_k_lists_optimized(lists: List[List[int]]) -> List[int]:
    """
    Оптимізована версія злиття k відсортованих списків
    Використовує підхід "розділяй і володарюй"
    """
    if not lists:
        return []
    
    def merge_two_lists(list1, list2):
        """Злиття двох відсортованих списків"""
        merged = []
        i, j = 0, 0
        
        while i < len(list1) and j < len(list2):
            if list1[i] <= list2[j]:
                merged.append(list1[i])
                i += 1
            else:
                merged.append(list2[j])
                j += 1
        
        # Додаємо залишки
        merged.extend(list1[i:])
        merged.extend(list2[j:])
        
        return merged
    
    # Послідовно зливаємо списки попарно
    while len(lists) > 1:
        merged_lists = []
        for i in range(0, len(lists), 2):
            list1 = lists[i]
            list2 = lists[i + 1] if i + 1 < len(lists) else []
            merged_lists.append(merge_two_lists(list1, list2))
        lists = merged_lists
    
    return lists[0] if lists else []

# Демонстрація роботи
if __name__ == "__main__":
    # Порівняння алгоритмів сортування
    compare_sorting_algorithms()
    
    print("\n=== ТЕСТУВАННЯ ФУНКЦІЇ MERGE_K_LISTS ===\n")
    
    # Приклад з завдання
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    merged_list = merge_k_lists(lists)
    print(f"Вхідні списки: {lists}")
    print(f"Відсортований список: {merged_list}")
    
    # Додаткові тести
    test_cases = [
        [[], [1, 2, 3], [4, 5]],  # Порожній список
        [[1], [2], [3], [4]],     # Одноелементні списки
        [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]],  # Більше списків
    ]
    
    print("\nДодаткові тести:")
    for i, test_lists in enumerate(test_cases, 1):
        result = merge_k_lists(test_lists)
        print(f"Тест {i}: {test_lists} -> {result}")
    
    # Порівняння швидкості двох підходів з timeit
    print("\n=== ПОРІВНЯННЯ ШВИДКОСТІ MERGE_K_LISTS З TIMEIT ===")
    
    # Створюємо великі тестові дані
    large_lists = []
    for i in range(10):
        sorted_list = sorted([random.randint(1, 1000) for _ in range(100)])
        large_lists.append(sorted_list)
    
    # Тестуємо простий підхід з timeit
    def test_simple():
        return merge_k_lists(large_lists)
    
    def test_optimized():  
        return merge_k_lists_optimized(large_lists)
    
    time1 = timeit.timeit(test_simple, number=100) / 100
    time2 = timeit.timeit(test_optimized, number=100) / 100
    
    print(f"Простий підхід: {time1:.6f} сек (середній з 100 запусків)")
    print(f"Оптимізований підхід: {time2:.6f} сек (середній з 100 запусків)")
    
    # Перевіряємо правильність
    result1 = merge_k_lists(large_lists)
    result2 = merge_k_lists_optimized(large_lists)
    print(f"Результати однакові: {result1 == result2}")
    
    print("\n=== ТЕОРЕТИЧНИЙ АНАЛІЗ ===")
    print("Складність алгоритмів сортування:")
    print("• Merge Sort: O(n log n) - стабільний, гарантована складність")
    print("• Insertion Sort: O(n²) - ефективний для малих або майже відсортованих масивів")
    print("• Timsort: O(n log n) - гібридний алгоритм, адаптивний")
    print("\nЯк Timsort використовує переваги обох алгоритмів:")
    print("• Виявляє природні послідовності (runs) у даних")
    print("• Для коротких runs використовує Insertion Sort (ефективний на малих масивах)")
    print("• Для об'єднання runs використовує модифікований Merge Sort")
    print("• Адаптується до структури даних (майже відсортовані масиви сортуються швидше)")
    print("\nРекомендації:")
    print("• Для малих масивів (< 50): Insertion Sort")
    print("• Для великих масивів з гарантованою складністю: Merge Sort")
    print("• Для загального використання: Timsort (вбудований sort())")
    print("• Timsort об'єднує переваги обох: швидкість Insertion Sort на малих")
    print("  фрагментах та надійність Merge Sort для великих об'ємів даних")
