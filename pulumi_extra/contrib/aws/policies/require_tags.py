# noqa: D100
from fnmatch import fnmatch

import pulumi_policy as policy

from pulumi_extra.contrib.aws import is_aws_resource, is_taggable


class RequireTags:
    """Policy validator to require specific tags on resources."""

    def __call__(  # noqa: D102
        self,
        args: policy.ResourceValidationArgs,
        report_violation: policy.ReportViolation,
    ) -> None:
        config = args.get_config()
        exclude = set(config.get("exclude", []))
        required_tags = set(config["required-tags"])
        if any(fnmatch(args.resource_type, pattern) for pattern in exclude):
            return

        if not required_tags:
            return

        if not is_aws_resource(args.resource_type):
            return

        if is_taggable(args.resource_type):
            tags = args.props.get("tags", {})
            for rt in required_tags:
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
