from __future__ import annotations

import fnmatch
from typing import TYPE_CHECKING

import pulumi

if TYPE_CHECKING:
    from typing import Any


def apply_defaults(
    resource_type: str,
    *,
    defaults: dict[str, pulumi.Input[Any]],
) -> pulumi.ResourceTransform:
    """Pulumi transform factory that applies default properties to resources of a given type.

    Args:
        resource_type: Resource type to match.
        defaults: Default properties to apply.

    """

    def transform(
        args: pulumi.ResourceTransformArgs,
    ) -> pulumi.ResourceTransformResult | None:
        # NOTE: Workaround for type error
        if TYPE_CHECKING:
            assert isinstance(args.props, dict)

        if args.type_ == resource_type:
            args.props = defaults | args.props
            return pulumi.ResourceTransformResult(args.props, args.opts)

        return None

    return transform


def override_resource_provider(
    *resource_types: str,
    provider: pulumi.ProviderResource,
) -> pulumi.ResourceTransform:
    """Pulumi transform factory that overrides the provider for resources of given types.

    Args:
        *resource_types: Resource types to match. Supports glob patterns.
        provider: Provider to set.

    """

    def transform(
        args: pulumi.ResourceTransformArgs,
    ) -> pulumi.ResourceTransformResult | None:
        for rt in resource_types:
            if not fnmatch.fnmatch(args.type_, rt):
                continue

            return pulumi.ResourceTransformResult(
                props=args.props,
                opts=pulumi.ResourceOptions.merge(
                    args.opts,
                    pulumi.ResourceOptions(provider=provider),
                ),
            )
        return None

    return transform


def override_invoke_provider(
    *invoke_tokens: str,
    provider: pulumi.ProviderResource,
) -> pulumi.InvokeTransform:
    """Pulumi transform factory that overrides the provider for resources of given types.

    Args:
        *invoke_tokens: Resource types to match. Supports glob patterns.
        provider: Provider to set.

    """

    def transform(
        args: pulumi.InvokeTransformArgs,
    ) -> pulumi.InvokeTransformResult | None:
        for it in invoke_tokens:
            if not fnmatch.fnmatch(args.token, it):
                continue

            return pulumi.InvokeTransformResult(
                args=args.args,
                opts=pulumi.InvokeOptions.merge(
                    args.opts,
                    pulumi.InvokeOptions(provider=provider),
                ),
            )
        return None

    return transform
