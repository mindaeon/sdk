# Kubeflow Katib SDK

The Kubeflow Katib SDK provides a Pythonic interface for managing Katib resources, including Experiments, Suggestions, and Trials.

## KatibClient

The `KatibClient` is the main entry point for the Katib SDK. It provides access to sub-clients for managing Experiments, Suggestions, and Trials.

```python
from kubeflow.katib import KatibClient

client = KatibClient()

# Get the Experiment client
experiment_client = client.experiments()

# Get the Suggestion client
suggestion_client = client.suggestions()

# Get the Trial client
trial_client = client.trials()
```

## ExperimentClient

The `ExperimentClient` provides methods for managing Katib Experiments.

### Create an Experiment

```python
from kubeflow.katib.types import Optimizer, SearchSpace

search_space = SearchSpace(
    [
        {
            "name": "learning_rate",
            "type": "double",
            "space": {"min": "0.1", "max": "0.5", "step": "0.1"},
        },
        {
            "name": "num_layers",
            "type": "int",
            "space": {"min": "2", "max": "10", "step": "1"},
        },
    ]
)

optimizer = Optimizer(
    name="my-experiment",
    search_space=search_space,
    objective={
        "type": "maximize",
        "goal": 0.99,
    },
    algorithm={"name": "random", "settings": {"random_state": "10"}},
)

experiment_client.create(optimizer=optimizer, namespace="my-namespace")
```

### Get an Experiment

```python
experiment = experiment_client.get(name="my-experiment", namespace="my-namespace")
```

### List Experiments

```python
experiments = experiment_client.list(namespace="my-namespace")
```

### Pause and Resume an Experiment

```python
experiment_client.pause(name="my-experiment", namespace="my-namespace")
experiment_client.resume(name="my-experiment", namespace="my-namespace")
```

### Get the Optimal Trial

```python
optimal_trial = experiment_client.get_optimal_trial(name="my-experiment", namespace="my-namespace")
```

### Delete an Experiment

```python
experiment_client.delete(name="my-experiment", namespace="my-namespace")
```

## SuggestionClient

The `SuggestionClient` provides methods for managing Katib Suggestions.

### Get a Suggestion

```python
suggestion = suggestion_client.get(name="my-suggestion", namespace="my-namespace")
```

### List Suggestions

```python
suggestions = suggestion_client.list(namespace="my-namespace")
```

## TrialClient

The `TrialClient` provides methods for managing Katib Trials.

### Get a Trial

```python
trial = trial_client.get(name="my-trial", namespace="my-namespace")
```

### List Trials

```python
trials = trial_client.list(namespace="my-namespace")
```
