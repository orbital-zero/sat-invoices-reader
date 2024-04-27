#!/usr/bin/env python3

import abc

from classes.dto.Callback import Callback


class FileReaderInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'do_in_list') and callable(subclass.do_in_list))

    @abc.abstractmethod
    def do_in_list(self, path: str, _callback: Callback):
        """
            Execute a custom operation during file iteration in a defined path,
            the callback function is excuted on each file
        """
        raise NotImplementedError
