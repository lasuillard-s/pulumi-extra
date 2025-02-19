# noqa: D100
from __future__ import annotations

import pulumi

from .transform import override_invoke_provider, override_resource_provider


def set_default_provider(
    *resource_types: str,
    provider: pulumi.ProviderResource,
) -> None:
    """Set the default provider for resources of given types.

    Args:
        *resource_types: Resource types to match. Supports glob patterns.
        provider: Provider to set.

    """
    pulumi.runtime.register_resource_transform(
        override_resource_provider(*resource_types, provider=provider),
    )
    pulumi.runtime.register_invoke_transform(
        override_invoke_provider(*resource_types, provider=provider),
    )
