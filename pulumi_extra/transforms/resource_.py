"""Pulumi resource transforms."""

from __future__ import annotations

from fnmatch import fnmatch
from itertools import chain
from typing import Any, Callable, cast

import pulumi
from braceexpand import braceexpand

_Props = dict[str, Any]


def override_resource(
    *resource_types: str,
    props: _Props | Callable[[_Props], _Props] | None = None,
    opts: pulumi.ResourceOptions | Callable[[pulumi.ResourceOptions], pulumi.ResourceOptions] | None = None,
) -> pulumi.ResourceTransform:
    """Pulumi transform factory that overrides the provider for resources of given types.

    Args:
        *resource_types: Resource types to match. Supports glob patterns and brace expand.
        props: Resource properties to override, or a callable that returns the new properties from given `args.props` input.
        opts: Resource options to override, or a callable that returns the new options given `args.opts` input.

    """  # noqa: E501

    def transform(args: pulumi.ResourceTransformArgs) -> pulumi.ResourceTransformResult | None:
        nonlocal props, opts

        for rt in chain.from_iterable(map(braceexpand, resource_types)):
            if not fnmatch(args.type_, rt):
                continue

            # Transform resource properties
            new_props = props(cast(dict, args.props)) if callable(props) else (props or {})

            # Transform resource options
            new_opts = opts(args.opts) if callable(opts) else (opts or pulumi.ResourceOptions())
            new_opts = pulumi.ResourceOptions.merge(args.opts, new_opts)

            return pulumi.ResourceTransformResult(props=new_props, opts=new_opts)

        return None

    return transform


def override_resource_defaults(
    *resource_types: str,
    defaults: dict[str, pulumi.Input[Any]],
) -> pulumi.ResourceTransform:
    """Pulumi transform factory that provides default properties to matching resource types.

    Args:
        *resource_types: Resource type to match.
        defaults: Default properties.

    """
    return override_resource(
        *resource_types,
        props=lambda props: defaults | props,
    )


def override_resource_options(*resource_types: str, **options: Any) -> pulumi.ResourceTransform:
    """Pulumi transform factory that overrides the resource options for resources of given types.

    Args:
        *resource_types: Resource types to match.
        options: Arguments of `pulumi.ResourceOptions`.

    """
    return override_resource(
        *resource_types,
        opts=pulumi.ResourceOptions(**options),
    )
