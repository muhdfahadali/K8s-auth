import ray
import time

ray.init(address="auto")  # Remove or adjust address if running locally

# A regular Python function.
def normal_function():
    return 1

# By adding the `@ray.remote` decorator, a regular Python function becomes a Ray remote function.
@ray.remote
def my_function():
    return 1

# Another Ray remote function that simulates a long-running task.
@ray.remote
def slow_function():
    time.sleep(10)
    return 1

# To invoke a remote function, use the `remote` method.
obj_ref = my_function.remote()

# The result of the remote function can be retrieved with `ray.get`.
assert ray.get(obj_ref) == 1

# Submit a few more slow_function tasks.
object_refs = [slow_function.remote() for _ in range(2)]

# Return as soon as one of the tasks finished execution.
ready_refs, remaining_refs = ray.wait(object_refs, num_returns=1, timeout=None)

# ready_refs contains references to the tasks that have completed.
# remaining_refs contains references to the tasks that are still running.
print("Ready refs:", ready_refs)
print("Remaining refs:", remaining_refs)

# Retrieve the results of the completed tasks.
completed_results = ray.get(ready_refs)
print("Ready results:", completed_results)

# Now wait for all remaining tasks to complete and retrieve their results.
if remaining_refs:
    more_results = ray.get(remaining_refs)
    print("More results:", more_results)
    completed_results.extend(more_results)

print("All completed results:", completed_results)

# Shutdown Ray. This cleans up the Ray cluster.
ray.shutdown()
