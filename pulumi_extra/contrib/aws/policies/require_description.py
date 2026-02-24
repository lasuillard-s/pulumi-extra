# noqa: D100
from __future__ import annotations

from fnmatch import fnmatch
from typing import TYPE_CHECKING, Any, TypedDict

import pulumi_policy as policy

from pulumi_extra import resource_has_attribute
from pulumi_extra.contrib.aws import is_aws_resource, is_taggable

if TYPE_CHECKING:
    from collections.abc import Mapping


class RequireDescriptionConfig(TypedDict):
    """Configuration schema for RequireDescription policy."""

    exclude: set[str]
    """Resource types to exclude from this policy. Supports glob patterns."""

    require_tag_if_description_unsupported: bool
    """Whether to require a tag if description is unsupported."""

    description_tag_key: str
    """The tag key to use for description if description is unsupported."""


class RequireDescription:
    """Policy validator to require description (or tag if unsupported) on resources."""

    def _load_config(self, config: Mapping[str, Any]) -> RequireDescriptionConfig:
        exclude = set(config.get("exclude", []))
        require_tag_if_description_unsupported = config.get("require-tag-if-description-unsupported", False)
        description_tag_key = config.get("description-tag-key", "Description")
        return RequireDescriptionConfig(
            exclude=exclude,
            require_tag_if_description_unsupported=require_tag_if_description_unsupported,
            description_tag_key=description_tag_key,
        )

    def __call__(  # noqa: D102
        self,
        args: policy.ResourceValidationArgs,
        report_violation: policy.ReportViolation,
    ) -> None:
        config = self._load_config(args.get_config())
        if any(fnmatch(args.resource_type, pattern) for pattern in config["exclude"]):
            return

        if not is_aws_resource(args.resource_type):
            return

        if resource_has_attribute(args.resource_type, "description") and args.props.get("description") is None:
            report_violation(
                f"Resource '{args.urn}' is missing required description",
                None,
            )

        if config["require_tag_if_description_unsupported"]:  # noqa: SIM102
            if is_taggable(args.resource_type):
                tags = args.props.get("tags", {})
                if config["description_tag_key"] not in tags:
                    report_violation(
                        f"Resource '{args.urn}' is missing required tag '{config['description_tag_key']}'",
                        None,
                    )


require_description = policy.ResourceValidationPolicy(
    name="aws:require-description",
    description="Require description (or tag if unsupported) on resources",
    config_schema=policy.PolicyConfigSchema(
        properties={
            "exclude": {
                "type": "array",
                "items": {"type": "string"},
            },
            "require-tag-if-description-unsupported": {
                "type": "boolean",
            },
            "description-tag-key": {
                "type": "string",
            },
        },
    ),
    validate=RequireDescription(),
)
