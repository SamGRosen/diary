def level(logged):

    def level_wrapper(text, reporter, *args, **kwargs):

        reporter(logged, text)
        return logged(text, *args, **kwargs)

    return level_wrapper


@level
def info(text, **kwargs):
    pass


@level
def warn(text, **kwargs):
    pass


@level
def error(text, **kwargs):
    if kwargs.get("raises", False):
        raise kwargs.get("e_type", Exception)(text)


@level
def debug(text, **kwargs):
    pass
