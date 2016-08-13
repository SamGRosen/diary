"""
Levels are classifications of logs, typically based on their importance
levels take an event parameter and any number of keyword arguments
@level
def example_level(event):
    # do some behavior
"""

from functools import wraps
import traceback

def log_level(logged):
    """
    Decorator to automatically log an event based on level.
    Decorated functions handle appropriate behavior.
    """
    @wraps(logged)
    def level_wrapper(event, reporter, *args, **kwargs):
        try:
            logged(event, *args, **kwargs)
        except Exception as e:
            reporter(event)
            raise e
        else:
            reporter(event)


    return level_wrapper


@log_level
def info(event):
    """The most generic level of logging. No special behavior needed.

    :param event: event instance
    """
    pass


@log_level
def warn(event, log_trace=False):
    """A level of logging for info that may have side effects.

    :param event: event instance
    :param log_trace: boolean of whether or not to log current trace
    """
    if log_trace:
        event.info += ''.join(traceback.format_stack()[:-1])


@log_level
def error(event, raises=False, e_type=Exception, log_trace=True, limit=None):
    """A level of information that may have caused an error.

    :param event: error event instance
    :param raises: boolean of whether or not an error should be raised
    :param e_type: exception type to be raised
    :param log_trace: boolean of whether or not log traceback
    :param limit: integer of traceback limit
    """
    if raises:
        if hasattr(event, "info"):
            logged_exception = e_type(event.info)
        else:
            logged_exception = e_type(event)

        if log_trace:
            try:
                raise logged_exception
            except Exception as err:
                given_traceback = traceback.format_stack(limit=limit)[:-1]
                given_traceback.append(traceback.format_exc(limit=limit))
                event.info += '\n' + ''.join(given_traceback)
            finally:
                raise logged_exception
        else:
            raise logged_exception

    elif log_trace:
        event.info += ''.join(traceback.format_stack())


@log_level
def debug(event):
    """A level of info pertinent to developers but not to users.

    :param event: event instance
    """
    pass
