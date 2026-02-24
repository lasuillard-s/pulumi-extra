# noqa: D100
from fnmatch import fnmatch

import pulumi_policy as policy

from pulumi_extra.contrib.gcp import is_gcp_resource, is_labelable


class RequireLabels:
    """Policy validator to require specific labels on resources."""

    def __call__(  # noqa: D102
        self,
        args: policy.ResourceValidationArgs,
        report_violation: policy.ReportViolation,
    ) -> None:
        config = args.get_config()
        exclude = set(config.get("exclude", []))
        required_labels = set(config["required-labels"])
        if any(fnmatch(args.resource_type, pattern) for pattern in exclude):
            return

        if not required_labels:
            return

        if not is_gcp_resource(args.resource_type):
            return

        if is_labelable(args.resource_type):
            labels = args.props.get("labels", {})
            for rl in required_labels:
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
