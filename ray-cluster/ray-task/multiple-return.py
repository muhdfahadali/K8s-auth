#Multiple returns
import ray

# Initialize Ray. This starts a Ray cluster with a head node and some workers.
# If running locally, you can use ray.init() without arguments.
ray.init(address="auto")  # Remove or adjust address if running locally

# By default, a Ray task only returns a single Object Ref.
@ray.remote
def return_single():
    return 0, 1, 2

# Retrieve and check the result of the single object ref function.
object_ref = return_single.remote()
assert ray.get(object_ref) == (0, 1, 2)
print("Single return results:", ray.get(object_ref))

# However, you can configure Ray tasks to return multiple Object Refs.
@ray.remote(num_returns=3)
def return_multiple():
    return 0, 1, 2

# Retrieve and check the results of the multiple object refs function.
object_ref0, object_ref1, object_ref2 = return_multiple.remote()
assert ray.get(object_ref0) == 0
assert ray.get(object_ref1) == 1
assert ray.get(object_ref2) == 2
print("Multiple return results:", ray.get([object_ref0, object_ref1, object_ref2]))

# Shutdown Ray. This cleans up the Ray cluster.
ray.shutdown()
