# noqa: D100
from __future__ import annotations

from fnmatch import fnmatch
from typing import TYPE_CHECKING, Any, TypedDict

import pulumi_policy as policy

from pulumi_extra.contrib.gcp import is_gcp_resource, is_labelable

if TYPE_CHECKING:
    from collections.abc import Mapping


class RequireLabelsConfig(TypedDict):
    """Configuration schema for RequireLabels policy."""

    exclude: set[str]
    """Resource types to exclude from this policy. Supports glob patterns."""

    required_labels: set[str]
    """The set of required labels."""


class RequireLabels:
    """Policy validator to require specific labels on resources."""

    def _load_config(self, config: Mapping[str, Any]) -> RequireLabelsConfig:
        exclude = set(config.get("exclude", []))
        required_labels = set(config.get("required-labels", []))
        return RequireLabelsConfig(exclude=exclude, required_labels=required_labels)

    def __call__(  # noqa: D102
        self,
        args: policy.ResourceValidationArgs,
        report_violation: policy.ReportViolation,
    ) -> None:
        config = self._load_config(args.get_config())
        if any(fnmatch(args.resource_type, pattern) for pattern in config["exclude"]):
            return

        if not config["required_labels"]:
            return

        if not is_gcp_resource(args.resource_type):
            return

        if is_labelable(args.resource_type):
            labels = args.props.get("labels", {})
            for rl in config["required_labels"]:
                if not labels or rl not in labels:
                    report_violation(
                        f"Resource '{args.urn}' is missing required label '{rl}'",
                        None,
                    )


require_labels = policy.ResourceValidationPolicy(
    name="gcp:require-labels",
    description="Require specific labels on resources",
    config_schema=policy.PolicyConfigSchema(
        properties={
            "exclude": {
                "type": "array",
                "items": {"type": "string"},
            },
            "required-labels": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
    ),
    validate=RequireLabels(),
)
