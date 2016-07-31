"""
Levels are classifications of logs, typically based on their importance
levels take a text parameter and any number of keyword arguments
@level
def example_level(text, **kwargs):
    # do some behavior
"""


def level(logged):
    """
    Decorator to automatically log an event based on level.
    Decorated functions handle appropriate behavior.
    """
    def level_wrapper(text, reporter, *args, **kwargs):

        reporter(logged, text)
        return logged(text, *args, **kwargs)

    return level_wrapper


@level
def info(text):
    """The most generic level of logging. No special behavior needed.

    :param text: str of log message
    """
    pass


@level
def warn(text):
    """A level of logging for info that may have side effects.

    :param text: str of log message
    """
    pass


@level
def error(text, raises=False, e_type=Exception):
    """A level of information that may have caused an error.

    :param text: str of error message and log
    :param raises: boolean of whether or not an error should be raised
    :param e_type: exception type to be raised
    """
    if raises:
        raise e_type(text)


@level
def debug(text):
    """A level of info pertinent to developers but not to users.

    :param text: str of log message
    """
    pass
