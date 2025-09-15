# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Support a 'release-artifacts' key which automatically sets up the artifacts
under 'public/build' and adds the corresponding attribute needed by downstream
release tasks.
"""
import os

from taskgraph.transforms.base import TransformSequence
from taskgraph.util.schema import Schema
from taskgraph.util.workertypes import worker_type_implementation

transforms = TransformSequence()


class ReleaseArtifactsSchema(Schema, kw_only=True, forbid_unknown_fields=False):
    """Schema for tasks with release artifacts configuration."""

    label: str | None = None
    description: str | None = None
    worker_type: str
    release_artifacts: list[str] | None = None


transforms.add_validate(ReleaseArtifactsSchema)


@transforms.add
def add_release_artifacts(config, tasks):
    for task in tasks:
        if "release-artifacts" not in task:
            yield task
            continue

        release_artifacts = task.setdefault("attributes", {}).setdefault(
            "release-artifacts", []
        )

        impl, _ = worker_type_implementation(config.graph_config, task["worker-type"])
        if impl == "generic-worker":
            path_tmpl = "artifacts/{}"
        else:
            path_tmpl = "/builds/worker/artifacts/{}"

        for path in task.pop("release-artifacts"):
            if os.path.isabs(path):
                raise Exception("Cannot have absolute path artifacts")

            release_artifacts.append(
                {
                    "type": "file",
                    "name": f"public/build/{path}",
                    "path": path_tmpl.format(path),
                }
            )

        artifacts = task.setdefault("worker", {}).setdefault("artifacts", [])
        artifacts.extend(release_artifacts)
        yield task
