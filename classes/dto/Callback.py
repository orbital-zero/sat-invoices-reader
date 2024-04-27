#!/usr/bin/env python3

import typing


class Callback:

    def __init__(self) -> None:
        self._errors = []
        self._result = []

    @property
    def function(self) -> typing.Callable:
        return self._function

    def set_function(self, _function):
        self._function = _function

    @property
    def result(self) -> list:
        return self._result
    
    def set_result(self, _result):
        self._result = _result

    @property
    def errors(self) -> list:
        return self._errors
