from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pulumi
import pytest
from pulumi import automation

from pulumi_extra import override_invoke, override_invoke_defaults

pytestmark = pytest.mark.integration


def pulumi_program() -> None:
    import pulumi_docker as docker

    # ? Invoke transforms cannot be applied to per-resource basis
    invoke_transforms = [
        # Will modify default
        override_invoke_defaults("*", defaults={"insecure_skip_verify": True}),
        # This will not have any effect (no match)
        override_invoke("_", args={"insecure_skip_verify": False}),
        # Will override argument
        override_invoke("*", args={"name": "busybox"}),
    ]
    for it in invoke_transforms:
        pulumi.runtime.register_invoke_transform(it)

    busybox = docker.get_registry_image(name="scratch")

    for attr in ("name", "insecure_skip_verify"):
        pulumi.export(attr, getattr(busybox, attr))


@pytest.fixture
def pulumi_stack(tmpdir: Path) -> Iterator[automation.Stack]:
    stack = automation.create_or_select_stack(
        stack_name="test",
        project_name="test",
        program=pulumi_program,
        opts=automation.LocalWorkspaceOptions(
            env_vars={
                "PULUMI_BACKEND_URL": f"file://{tmpdir}",
                "PULUMI_CONFIG_PASSPHRASE": "test",
            },
        ),
    )
    stack.up(on_output=print)
    yield stack
    stack.destroy(on_output=print, remove=True)


class Test__override_invoke:
    @pytest.mark.forked
    def test(self, pulumi_stack: automation.Stack) -> None:
        # Arrange
        # ...

        # Act
        outputs = pulumi_stack.outputs()

        # Assert
        def _resolve_output_values(outputs: automation.OutputMap) -> dict[str, Any]:
            return {k: v.value for k, v in outputs.items()}

        assert _resolve_output_values(outputs) == {
            "name": "busybox",
            "insecure_skip_verify": True,
        }
