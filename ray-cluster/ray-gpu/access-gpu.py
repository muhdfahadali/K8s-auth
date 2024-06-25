import ray

ray.init()

@ray.remote(num_gpus=1)
class GPUActor:
    def say_hello(self):
        gpu_ids = ray.get_gpu_ids()
        print(f"Actor {self}: GPUs used by this actor: {gpu_ids}")

# Request actor placement.
gpu_actor = GPUActor.remote()

# block Ray pod with GPU access is scaled
ray.get(gpu_actor.say_hello.remote())
