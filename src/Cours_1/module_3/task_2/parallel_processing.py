import json
import math
import random
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, Process, Queue, cpu_count


def generate_data(n):
    return [random.randint(1, 1000) for _ in range(n)]


def process_number(number):
    return math.factorial(number)


# Вариант А
def process_with_threads(data):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_number, data))
    return results


# Вариант Б
def process_with_pool(data):
    with Pool() as pool:
        results = pool.map(process_number, data)
    return results


# Вариант В
def worker(q1: Queue, q2: Queue):
    value = q1.get()
    if not value:
        return

    result = process_number(value)
    q2.put(result)


def process_with_processes(data):
    input_queue = Queue()
    output_queue = Queue()

    num_processes = cpu_count()
    processes = []

    for _ in range(num_processes):
        process = Process(target=worker, args=(input_queue, output_queue))
        processes.append(process)
        process.start()

    for number in data:
        input_queue.put(number)

    for i in range(num_processes):
        input_queue.put(None)

    for process in processes:
        process.join()

    ###### ЗДЕСЬ останавливается поток выполнения и зависает ######
    results = []
    while not output_queue.empty():
        results.append(output_queue.get())
    else:
        output_queue.close()

    return results


def measure_time(func, data):
    start_time = time.time()
    result = func(data)
    end_time = time.time()
    return end_time - start_time, result


def compare_methods(data):
    results = {}

    print("Параллельная обработка с потоками...")
    thread_time, _ = measure_time(process_with_threads, data)
    results["Thread pool"] = thread_time

    print("Параллельная обработка с пулами процессов...")
    pool_time, _ = measure_time(process_with_pool, data)
    results["Process pool"] = pool_time

    print("Параллельная обработка с отдельными процессами...")
    process_time, _ = measure_time(process_with_processes, data)
    results["Separate processes"] = process_time

    return results


def save_results_to_file(results, filename="results.json"):
    with open(filename, "w") as file:
        json.dump(results, file)


if __name__ == "__main__":
    n = 100000
    data = generate_data(n)

    comparison_results = compare_methods(data)

    print("\nВремя выполнения различных методов:")
    for method, time_taken in comparison_results.items():
        print(f"{method}: {time_taken:.4f} секунд")

    save_results_to_file(comparison_results)
