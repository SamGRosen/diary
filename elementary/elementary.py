class Elementary(object):
    """
        Elementary is meant to be a low-dependency and easy to use logger
    """
    def __init__(self, path, async=False):
        """
            Initialization takes a file path meant to make startup simple
            :param path: str of a path pointing to -
                * An empty directory where Elementary will initiate
                * A txt file where Elementary will write
                * A database file where Elementary will read and write
                * A directory with a database and txt file
                * A nonexistent path for assumed writing
            :param async: boolean if logging should occur in own thread
        """
        self.path = path
        self.async = async
        if async:
            from .thread import ElemThread

if __name__ == '__main__':
    # from elementary import Elementary as el
    el = Elementary
    example_el = el("")
