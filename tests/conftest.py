from __future__ import annotations

from typing import TYPE_CHECKING, Any
from unittest import mock

import pulumi
import pytest

if TYPE_CHECKING:
    from collections.abc import Iterator


class ResourceMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs) -> Any:
        return [args.name + "_id", args.inputs]

    def call(self, args: pulumi.runtime.MockCallArgs) -> Any:  # noqa: ARG002
        return {}


@pytest.fixture(autouse=True)
def pulumi_mocks() -> None:
    """Set up Pulumi mocks."""
    pulumi.runtime.set_mocks(ResourceMocks(), preview=False)


@pytest.fixture(autouse=True)
def pulumi_organization() -> Iterator[None]:
    """Set up Pulumi organization (unless it is `None`)."""
    with mock.patch("pulumi.get_organization") as m:
        m.return_value = "organization"
        yield
