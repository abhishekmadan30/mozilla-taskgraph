from taskgraph import config as tg
from taskgraph.util.schema import Schema


class ShipitConfig(Schema, kw_only=True):
    """Configuration for Ship It integration."""

    product: str | None = None
    release_format: str | None = None
    scope_prefix: str | None = None


class MozillaGraphConfig(tg.GraphConfigSchema):
    """Mozilla-specific extensions to the graph configuration."""

    shipit: ShipitConfig | None = None
    version_parser: str | None = None
    """
    Python path of the form ``<module>:<obj>`` pointing to a
    function that takes a set of parameters as input and returns
    the version string to use for release tasks.

    Defaults to ``mozilla_taskgraph.version:default_parser``.
    """


# Replace the taskgraph's GraphConfigSchema with our extended version
tg.GraphConfigSchema = MozillaGraphConfig
