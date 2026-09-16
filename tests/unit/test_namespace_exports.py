"""Public namespace exports must be importable at runtime, not just by type checkers."""

import importlib

import pytest


@pytest.mark.parametrize(
    "module_name",
    [
        "addepy",
        "addepy.resources",
        "addepy.resources.admin",
        "addepy.resources.portfolio",
        "addepy.resources.ownership",
    ],
)
def test_all_advertised_namespace_exports_can_be_imported(module_name):
    module = importlib.import_module(module_name)
    imported = {}
    exec(f"from {module_name} import *", imported)
    assert all(imported[name] is getattr(module, name) for name in module.__all__)


def test_ownership_exports_match_lazily_initialized_resource_types():
    from addepy.resources.ownership import (
        EntitiesResource,
        ExternalIdsResource,
        GroupsResource,
        OwnershipNamespace,
        PositionsResource,
    )

    namespace = OwnershipNamespace(object())
    for name, resource_class in (
        ("entities", EntitiesResource),
        ("external_ids", ExternalIdsResource),
        ("groups", GroupsResource),
        ("positions", PositionsResource),
    ):
        resource = getattr(namespace, name)
        assert isinstance(resource, resource_class)
        assert getattr(namespace, name) is resource
