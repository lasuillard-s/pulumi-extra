from __future__ import annotations

import pytest

from pulumi_extra import get_resource_cls, resource_has_attribute
from pulumi_extra.errors import UnknownResourceTypeError


@pytest.fixture(autouse=True)
def reset_cache() -> None:
    """Reset cache for each test."""
    resource_has_attribute.cache_clear()
    get_resource_cls.cache_clear()


class Test__resource_has_attribute:
    @pytest.mark.xdist_group("registry-initialized")
    def test(self) -> None:
        # Arrange
        import pulumi_aws  # noqa: F401

        # Act & Assert
        assert resource_has_attribute("aws:s3/bucket:Bucket", "bucket") is True
        assert resource_has_attribute("aws:s3/bucket:Bucket", "acl") is True
        assert resource_has_attribute("aws:s3/bucket:Bucket", "my-attribute") is False

    def test_unknown_resource_type(self) -> None:
        # Arrange
        # ...

        # Act & Assert
        with pytest.raises(
            UnknownResourceTypeError,
            match="Unable to resolve resource type 'aws:unknown/unknown:Unknown'",
        ):
            resource_has_attribute("aws:unknown/unknown:Unknown", "whatever")


class Test__get_resource_cls:
    @pytest.mark.xdist_group("registry-initialized")
    def test(self) -> None:
        # Arrange
        import pulumi_aws  # noqa: F401

        # Act
        cls = get_resource_cls("aws:accessanalyzer/analyzer:Analyzer")

        # Assert
        assert cls is not None
        assert f"{cls.__module__}.{cls.__name__}" == "pulumi_aws.accessanalyzer.analyzer.Analyzer"

    @pytest.mark.xdist_group("fresh-env")
    def test_registry_not_initialized(self) -> None:
        """If registry not initialized, it will return `None`."""
        # Arrange
        # ...

        # Act & Assert
        assert get_resource_cls("aws:accessanalyzer/analyzer:Analyzer") is None

    def test_unknown_resource_type(self) -> None:
        # Arrange
        # ...

        # Act & Assert
        assert get_resource_cls("aws:unknown/unknown:Unknown") is None
