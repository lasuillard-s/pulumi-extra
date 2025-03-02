from __future__ import annotations

from typing import Any
from unittest import mock

import pulumi
import pytest

from pulumi_extra import get_stack_reference
from pulumi_extra.stack_reference import get_stack_outputs


class Test__get_stack_reference:
    @pytest.fixture(autouse=True)
    def reset_cache(self) -> None:
        """Reset cache for each test."""
        get_stack_reference.cache_clear()

    @pytest.mark.parametrize(
        ("ref", "expect"),
        [
            ("dev", "organization/project/dev"),
            ("network/dev", "organization/network/dev"),
            ("organization/management/default", "organization/management/default"),
        ],
    )
    @pulumi.runtime.test
    def test_ref(self, *, ref: str, expect: str) -> Any:
        # Arrange
        # ...

        # Act
        sr = get_stack_reference(ref)

        # Assert
        def check(args: list[Any]) -> None:
            sr_name = args[0]
            assert sr_name == expect

        return pulumi.Output.all(sr.name).apply(check)

    def test_invalid_ref(self) -> Any:
        # Arrange
        # ...

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid stack reference: 'organization/project/dev/extra'"):
            get_stack_reference("organization/project/dev/extra")


class Test__get_stack_outputs:
    @pytest.mark.parametrize(
        ("ref", "expect"),
        [
            ("dev:ami-id", "ami-id"),
            ("dev:{ec2-instance-id,elastic-ip}", ["ec2-instance-id", "elastic-ip"]),
        ],
    )
    @pulumi.runtime.test
    def test_ref(self, *, ref: str, expect: Any) -> Any:
        # Arrange
        # ...

        # Act
        with mock.patch("pulumi.StackReference") as m:
            m.return_value.require_output.side_effect = lambda v: pulumi.Output.from_input(v)
            outputs = get_stack_outputs(ref)

        # Assert
        def check(args: list[Any]) -> None:
            assert args[0] == expect

        return pulumi.Output.all(outputs).apply(check)

    def test_invalid_ref(self) -> Any:
        # Arrange
        # ...

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid output reference: ':output'"):
            get_stack_outputs(":output")
