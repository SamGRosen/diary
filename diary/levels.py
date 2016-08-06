"""
Levels are classifications of logs, typically based on their importance
levels take an event parameter and any number of keyword arguments
@level
def example_level(event):
    # do some behavior
"""

from functools import wraps


def level(logged):
    """
    Decorator to automatically log an event based on level.
    Decorated functions handle appropriate behavior.
    """
    @wraps(logged)
    def level_wrapper(event, reporter, *args, **kwargs):
        reporter(event)
        return logged(event, *args, **kwargs)

    return level_wrapper


@level
def info(event):
    """The most generic level of logging. No special behavior needed.

    :param event: event instance
    """
    pass


@level
def warn(event):
    """A level of logging for info that may have side effects.

    :param event: event instance
    """
    pass


@level
def error(event, raises=False, e_type=Exception):
    """A level of information that may have caused an error.

    :param event: error event instance
    :param raises: boolean of whether or not an error should be raised
    :param e_type: exception type to be raised
    """
    if raises:
        raise e_type(event)


@level
def debug(event):
    """A level of info pertinent to developers but not to users.

    :param event: event instance
    """
    pass
