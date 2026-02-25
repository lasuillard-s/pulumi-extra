# noqa: D100
from __future__ import annotations

from fnmatch import fnmatch
from typing import TYPE_CHECKING, Any, TypedDict

import pulumi_policy as policy

from pulumi_extra.contrib.aws import is_aws_resource, is_taggable

if TYPE_CHECKING:
    from collections.abc import Mapping


class RequireTagsConfig(TypedDict):
    """Configuration schema for RequireTags policy."""

    exclude: set[str]
    """Resource types to exclude from this policy. Supports glob patterns."""

    required_tags: set[str]
    """The set of required tags."""


class RequireTags:
    """Policy validator to require specific tags on resources."""

    def _load_config(self, config: Mapping[str, Any]) -> RequireTagsConfig:
        exclude = set(config.get("exclude", []))
        required_tags = set(config.get("required-tags", []))
        return RequireTagsConfig(exclude=exclude, required_tags=required_tags)

    def __call__(  # noqa: D102
        self,
        args: policy.ResourceValidationArgs,
        report_violation: policy.ReportViolation,
    ) -> None:
        config = self._load_config(args.get_config())

        if any(fnmatch(args.resource_type, pattern) for pattern in config["exclude"]):
            return

        if not config["required_tags"]:
            return

        if not is_aws_resource(args.resource_type):
            return

        if is_taggable(args.resource_type):
            tags = args.props.get("tags", {})
            for rt in config["required_tags"]:
                if not tags or rt not in tags:
                    report_violation(
                        f"Resource '{args.urn}' is missing required tag '{rt}'",
                        None,
                    )


require_tags = policy.ResourceValidationPolicy(
    name="aws:require-tags",
    description="Require specific tags on resources",
    config_schema=policy.PolicyConfigSchema(
        properties={
            "exclude": {
                "type": "array",
                "items": {"type": "string"},
            },
            "required-tags": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
    ),
    validate=RequireTags(),
)
