"""
Hierarchical key / value store with keys written using dot notation e.g. ``some.id.attribute``. Basic getting and setting of values is simple: ::

    config.set("some.id.attribute", "value")
    config.get("some.id.attribute")  # => "value"

Keys can also contain one or more ``*`` placeholders, each of which match one or more parts. This makes it possible to define "defaults" that apply to more specific keys e.g. ::

    config.set("some.*.attribute", "value")
    config.get("some.id.attribute")  # => "value"
    config.get("some.other.attribute")  # => "value"
    config.get("some.other.deeper.attribute")  # => "value"
"""

import re


class Config:
    def __init__(self):
        self.__backend = {}
        self.__cache = {}

    def get(self, path, default=None):
        # find all patterns that match the path
        matches = [
            pattern
            for pattern in self.__backend
            if self.__match(
                pattern,
                path,
            )
        ]

        if not matches and default is not None:
            return default

        if not matches:
            raise KeyError(f"No config defined for '{path}'")

        # sort patterns - highest priority first
        matches = sorted(
            matches,
            key=self.__priority,
            reverse=True,
        )

        return self.__backend[matches[0]]

    def __match(self, pattern, path):
        if (pattern, path) not in self.__cache:
            regex = pattern

            # match actual period characters
            regex = regex.replace(".", r"\.")
            # a "*" can match multiple parts
            regex = regex.replace("*", r"\w+(.\w+)*")
            # pattern matches the entire path
            matcher = re.compile(f"^{regex}$")

            match = matcher.match(path)
            self.__cache[(pattern, path)] = match

        return self.__cache[(pattern, path)]

    def __priority(self, pattern):
        parts = pattern.split(".")

        # first sort by pattern length
        score = len(parts)

        # then score by specificity
        ids = [part for part in parts if part != "*"]
        score += len(ids) * 0.1

        return score

    def set(self, path, value):
        self.__backend[path] = value

    def reset(self):
        self.__backend = {}
