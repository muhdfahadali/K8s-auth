#Passing object refs to Ray tasks
import ray
import time

# Initialize Ray. This starts a Ray cluster with a head node and some workers.

ray.init(address="auto")  

# A regular Python function.
def normal_function():
    return 1

# By adding the `@ray.remote` decorator, a regular Python function becomes a Ray remote function.
@ray.remote
def my_function():
    return 1

# Another Ray remote function that takes an argument.
@ray.remote
def function_with_an_argument(value):
    return value + 1

# To invoke this remote function, use the `remote` method.
obj_ref1 = my_function.remote()

# The result of the remote function can be retrieved with `ray.get`.
assert ray.get(obj_ref1) == 1

# You can pass an object ref as an argument to another Ray task.
obj_ref2 = function_with_an_argument.remote(obj_ref1)
assert ray.get(obj_ref2) == 2

# Corrected: Provide a valid argument when calling the remote function.
result_ref = function_with_an_argument.remote(5)
print("Results : ", ray.get(result_ref)) 

# Shutdown Ray. This cleans up the Ray cluster.
ray.shutdown()
