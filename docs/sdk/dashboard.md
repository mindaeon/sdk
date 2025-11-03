# Kubeflow Dashboard SDK

The Kubeflow Dashboard SDK provides a client for interacting with the Kubeflow Central Dashboard.
This component is responsible for managing multi-user isolation, which is based on `Profile`
custom resources.

## `DashboardClient`

The `DashboardClient` provides a Pythonic interface for managing `Profile` resources in your
Kubernetes cluster.

### Create a Profile

Here's an example of how to use the `DashboardClient` to create a new `Profile`:

```python
from kubeflow.dashboard import DashboardClient
from kubeflow.dashboard.types import Profile, ResourceQuota

# Initialize the client
client = DashboardClient()

# Define the profile
profile = Profile(
    metadata={"name": "my-new-profile"},
    spec={
        "owner": {"kind": "User", "name": "user@example.com"},
        "resourceQuotaSpec": ResourceQuota(
            hard={
                "cpu": "1",
                "memory": "1Gi",
                "requests.storage": "1Gi",
                "persistentvolumeclaims": "1",
            }
        ),
    },
)

# Create the profile
client.create_profile(profile)

print("Profile 'my-new-profile' created successfully.")
```

### Get a Profile

```python
profile = client.get_profile(name="my-new-profile")
print(profile)
```

### Delete a Profile

```python
client.delete_profile(name="my-new-profile")
print("Profile 'my-new-profile' deleted successfully.")
```
