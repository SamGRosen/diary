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
    """The most generic level of logging. No special behavior needed."""
    pass


@level
def warn(text, **kwargs):
    """A level of logging for info that may have side effects."""
    pass


@level
def error(text, **kwargs):
    """A level of information that may have caused an error"""
    if kwargs.get("raises", False):
        raise kwargs.get("e_type", Exception)(text)


@level
def debug(text, **kwargs):
    """A level of info pertinent to developers but not to users"""
    pass
