# pulumi-extra

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/lasuillard-s/pulumi-extra/graph/badge.svg?token=uuckU93NAu)](https://codecov.io/gh/lasuillard-s/pulumi-extra)
[![PyPI - Version](https://img.shields.io/pypi/v/pulumi-extra)](https://pypi.org/project/pulumi-extra/)

Extra Pulumi utilities and resources for the Python runtime.

## ✨ Features

- Shortcuts for working with Pulumi resources, such as transforms, stack references, and template rendering
- Pulumi transforms to automatically tag (AWS) or label (GCP) resources
- Pulumi policies to require description (or label if unsupported) on resources (both AWS and GCP)

## 🚀 Quick start

The most common use case for `pulumi-extra` is auto-tagging AWS resources and auto-labeling GCP resources. For example, in your stack's `__main__.py` file:

```python
from pulumi_extra.contrib.aws import register_auto_tagging
from pulumi_extra.contrib.gcp import register_auto_labeling

register_auto_labeling()
register_auto_tagging()

... # Define your resources

```

To use policies, add the following to your policy module entrypoint (for example, `policy/__main__.py`):

```python
import pulumi_policy as policy
from pulumi_extra.contrib.aws import policies as aws_policies
from pulumi_extra.contrib.gcp import policies as gcp_policies

policy.PolicyPack(
    name="default",
    policies=[
        aws_policies.require_tags,
        aws_policies.require_description,
        gcp_policies.require_labels,
        gcp_policies.require_description,
    ],
)
```

Example `policy-config.json`:

```json
{
  "all": "advisory",
  "aws:require-description": {
    "exclude": [
      "aws:organizations/*"
    ]
  },
  "aws:require-tags": {
    "exclude": [
      "aws:organizations/*"
    ],
    "required-tags": [
      "Managed-By",
      "pulumi:Organization",
      "pulumi:Project",
      "pulumi:Stack"
    ]
  },
  "gcp:require-labels": {
    "required-labels": [
      "managed-by",
      "pulumi-organization",
      "pulumi-project",
      "pulumi-stack"
    ]
  }
}
```

You can pass the policy pack to `pulumi preview` like this:

```bash
$ pulumi preview \
  --policy-pack-config=<path_to_your_policy_config.json> \
  --policy-pack=<path_to_your_policy_module>
```

See the [documentation](https://lasuillard-s.github.io/pulumi-extra/) for the full list of supported utilities.

## 💖 Contributing

Please refer to [CONTRIBUTING.md](./CONTRIBUTING.md) for more information on how to contribute to this project.

## 📜 License

This project is licensed under the MIT License.
