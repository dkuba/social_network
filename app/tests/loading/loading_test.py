"""
Скрипт запускает нагрузочный тест для API на ручку поиска пользователей.
"""
import requests
import time
import threading

from requests.adapters import HTTPAdapter
from urllib3 import Retry

url = 'http://localhost:8000/v1/users/search/?first_name=di'

# Define the retry strategy
retry_strategy = Retry(
    total=4,
)
# Create an HTTP adapter with the retry strategy and mount it to session
adapter = HTTPAdapter(max_retries=retry_strategy)

# Create a new session object
session = requests.Session()
session.mount('http://', adapter)
session.mount('https://', adapter)

overload_counter = 0
NUM_CONNECTIONS = (1, 10, 100, 1000)


def make_request(latency_results, throughput_results):
    start_time = time.time()

    def _make_request():
        try:
            session.get(url, timeout=1000)
        except Exception:
            global overload_counter
            overload_counter += 1
            if overload_counter % 100:
                print(f'overload happened {overload_counter} times')

            _make_request()

    _make_request()
    end_time = time.time()
    latency = end_time - start_time
    latency_results.append(latency)

    throughput = len(latency_results) / (latency)
    throughput_results.append(throughput)


def main():

    threads = []

    for num_connections in NUM_CONNECTIONS:

        latency_results = []
        throughput_results = []

        for i in range(num_connections):
            thread = threading.Thread(target=make_request, args=(latency_results, throughput_results))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        average_throughput = sum(throughput_results) / len(throughput_results)
        avarage_latency = sum(latency_results) / len(latency_results)

        print(f'Total connection: {num_connections}, '
              f'avarage latency: {avarage_latency}, '
              f'avarage throughput: {average_throughput} ')


if __name__ == '__main__':
    main()
