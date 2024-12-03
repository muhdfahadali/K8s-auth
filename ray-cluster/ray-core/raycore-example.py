import ray
ray.init()
import time

database = [
    "Learning", "Ray", "Flexible", "Distributed", "Python", "for", "Machine", "Learning"
]


def retrieve(item):
    time.sleep(item / 10.)
    return item, database[item]

def print_runtime(input_data, start_time):
    print(f'Runtime: {time.time() - start_time:.2f} seconds, data:')
    print(*input_data, sep="\n")


start = time.time()
data = [retrieve(item) for item in range(8)]
print_runtime(data, start)