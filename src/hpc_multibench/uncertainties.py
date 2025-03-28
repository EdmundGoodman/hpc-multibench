#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mypy: disable-error-code="no-any-unimported"
"""Export a set of functions for representing values with uncertainties."""

from uncertainties.core import Variable


class UFloat(Variable):  # type: ignore[misc]
    """A wrapper class for floating point numbers with uncertainties.

    Args:
        nominal_value: The nominal value of the random variable. It is
            more meaningful to use a value close to the central value or to the
            mean. This value is propagated by mathematical operations as if it
            was a float.
        std_dev: The standard deviation of the random
            variable. The standard deviation must be convertible to a positive
            float, or be NaN. Defaults to None.
        tag: An optional string tag for the variable.
            Variables don't have to have distinct tags. Tags are useful for
            tracing what values (and errors) enter in a given result (through
            the `error_components()` method). Defaults to None.
    """

    nominal_value: float
    std_dev: float | None
    tag: str | None

    def __str__(self) -> str:
        """Modify the default implementation of stringify-ing the class."""
        return super().__str__().replace("+/-", " ± ")  # type: ignore[no-any-return]
