import ray
import sys

ray.init(namespace="ray-cluster")
detached_actor = ray.get_actor(sys.argv[1])
ray.kill(detached_actor)