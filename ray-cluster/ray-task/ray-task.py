import ray
import time

# Initialize Ray. This starts a Ray cluster with a head node and some workers.
ray.init(address="auto")

# A regular Python function.
def normal_function():
    return 1

# By adding the `@ray.remote` decorator, a regular Python function
@ray.remote
def my_function():
    return 1

# To invoke this remote function, use the `remote` method.
obj_ref = my_function.remote()

# The result of the remote function can be retrieved with `ray.get`.
assert ray.get(obj_ref) == 1

# This function sleeps for 10 seconds to simulate a long-running task.
@ray.remote
def slow_function():
    time.sleep(10)
    return 1

# We can execute multiple instances of the remote function in parallel.
slow_function_refs = []
my_function_refs = []
for i in range(4):
    # Submitting tasks to be executed in parallel. This doesn't block the main program.
    print(f"Submitting slow_function task {i+1}")
    slow_function_refs.append(slow_function.remote())
    #my_function_refs.append(my_function.remote())


print("Waiting for slow_function tasks to complete...")
results1 = ray.get(slow_function_refs)
print("Results:", results1)  

# Shutdown Ray. This cleans up the Ray cluster.
ray.shutdown()
