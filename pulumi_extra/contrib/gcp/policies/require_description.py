# noqa: D100
from __future__ import annotations

from fnmatch import fnmatch
from typing import TYPE_CHECKING, Any, TypedDict

import pulumi_policy as policy

from pulumi_extra import resource_has_attribute
from pulumi_extra.contrib.gcp import is_gcp_resource, is_labelable

if TYPE_CHECKING:
    from collections.abc import Mapping


class RequireDescriptionConfig(TypedDict):
    """Configuration schema for RequireDescription policy."""

    exclude: set[str]
    """Resource types to exclude from this policy. Supports glob patterns."""

    require_label_if_description_unsupported: bool
    """Whether to require a label if description is unsupported."""

    description_label_key: str
    """The label key to use for description if description is unsupported."""


class RequireDescription:
    """Policy validator to require description (or label if unsupported) on resources."""

    def _load_config(self, config: Mapping[str, Any]) -> RequireDescriptionConfig:
        exclude = set(config.get("exclude", []))
        require_label_if_description_unsupported = config.get("require-label-if-description-unsupported", False)
        description_label_key = config.get("description-label-key", "description")
        return RequireDescriptionConfig(
            exclude=exclude,
            require_label_if_description_unsupported=require_label_if_description_unsupported,
            description_label_key=description_label_key,
        )

    def __call__(  # noqa: D102
        self,
        args: policy.ResourceValidationArgs,
        report_violation: policy.ReportViolation,
    ) -> None:
        config = self._load_config(args.get_config())
        if any(fnmatch(args.resource_type, pattern) for pattern in config["exclude"]):
            return

        if not is_gcp_resource(args.resource_type):
            return

        if resource_has_attribute(args.resource_type, "description") and args.props.get("description") is None:
            report_violation(
                f"Resource '{args.urn}' is missing required description",
                None,
            )

        if config["require_label_if_description_unsupported"]:  # noqa: SIM102
            if is_labelable(args.resource_type):
                labels = args.props.get("labels", {})
                if config["description_label_key"] not in labels:
                    report_violation(
                        f"Resource '{args.urn}' is missing required label '{config['description_label_key']}'",
                        None,
                    )


require_description = policy.ResourceValidationPolicy(
    name="gcp:require-description",
    description="Require description (or label if unsupported) on resources",
    config_schema=policy.PolicyConfigSchema(
        properties={
            "exclude": {
                "type": "array",
                "items": {"type": "string"},
            },
            "require-label-if-description-unsupported": {
                "type": "boolean",
            },
            "description-label-key": {
                "type": "string",
            },
        },
    ),
    validate=RequireDescription(),
)
