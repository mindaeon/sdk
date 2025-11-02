# Kubeflow Notebooks Guide

The Kubeflow Notebooks integration in the SDK allows you to manage the lifecycle of your interactive notebook servers.

## `NotebookClient`

The `NotebookClient` is the main entry point for interacting with Kubeflow Notebooks.

```python
from kubeflow.notebooks.api import NotebookClient

client = NotebookClient()
```

### Creating a Notebook

To create a notebook, you first need to define a `Notebook` object. You can use one of the default templates to create a notebook with a pre-configured environment.

```python
from kubeflow.notebooks.templates import JUPYTER_TEMPLATE
from kubeflow.notebooks.models import Notebook

notebook = Notebook(name="my-notebook", spec={"template": JUPYTER_TEMPLATE.template})

client.create(notebook)
```

### Getting a Notebook

You can get a notebook by name.

```python
notebook = client.get("my-notebook")
```

### Listing Notebooks

You can list all the notebooks in a namespace.

```python
notebooks = client.list()
```

### Deleting a Notebook

You can delete a notebook by name.

```python
client.delete("my-notebook")
```

## Template System

The SDK provides a template system that allows you to define and use templates for creating notebooks.

### `JUPYTER_TEMPLATE` and `VSCODE_TEMPLATE`

The SDK provides two default templates: `JUPYTER_TEMPLATE` and `VSCODE_TEMPLATE`.

```python
from kubeflow.notebooks.templates import JUPYTER_TEMPLATE

notebook = Notebook(name="my-notebook", spec={"template": JUPYTER_TEMPLATE.template})
```

## Local Simulator

The SDK provides a local simulator that allows you to test your notebook configurations without needing a full Kubeflow deployment.

### `NotebookSimulator`

The `NotebookSimulator` is used to create and manage simulated notebooks.

```python
from kubeflow.notebooks.simulator import NotebookSimulator
from kubeflow.notebooks.models import Notebook
from kubeflow.notebooks.templates import JUPYTER_TEMPLATE

simulator = NotebookSimulator()

# Create a simulated notebook
notebook = Notebook(name="my-notebook", spec={"template": JUPYTER_TEMPLATE.template})
container = simulator.create(notebook)

# Delete the simulated notebook
simulator.delete(container.name)
```
