#!/usr/bin/env python3

import typing


class Callback:

    def __init__(self) -> None:
        self._errors = []
        self._result = []

    @property
    def function(self) -> typing.Any:
        return self._function

    def set_function(self, _function):
        self._function = _function

    def get_function(self) -> typing.Any:
        return lambda: self._function

    @property
    def result(self) -> list:
        return self._result

    def set_result(self, _res):
        self._result = _res

    @property
    def errors(self) -> list:
        return self._errors
