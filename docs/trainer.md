# Kubeflow Trainer Guide

The Kubeflow Trainer component in the SDK allows you to train and fine-tune your ML models in a distributed fashion.

## `TrainerClient`

The `TrainerClient` is the main entry point for interacting with the Kubeflow Trainer.

```python
from kubeflow.trainer import TrainerClient

client = TrainerClient()
```

## Running a Training Job

To run a training job, you first need to define a `Trainer`. The SDK provides a `CustomTrainer` that allows you to run any Python function as a training job.

```python
from kubeflow.trainer import CustomTrainer

def train_fn():
    """A simple training function."""
    print("Training...")

trainer = CustomTrainer(
    func=train_fn,
    num_nodes=1,
)

job = client.train(trainer)
```

## Distributed Training

The `CustomTrainer` also supports distributed training. To run a distributed training job, you can specify the number of nodes.

```python
from kubeflow.trainer import CustomTrainer

def distributed_train_fn():
    """A simple distributed training function."""
    import torch.distributed as dist

    dist.init_process_group(backend="gloo")
    print(f"World size: {dist.get_world_size()}")
    print(f"Rank: {dist.get_rank()}")

trainer = CustomTrainer(
    func=distributed_train_fn,
    num_nodes=2,
)

job = client.train(trainer)
```

## Monitoring Training Jobs

You can use the `wait_for_job_status` method to wait for a training job to complete.

```python
client.wait_for_job_status(job.name)
```

You can also get the logs of a training job.

```python
logs = client.get_job_logs(job.name)
print(logs)
```
