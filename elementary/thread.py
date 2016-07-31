import threading


class ElemThread(threading.Thread):
    def __init__(self, name="Elementary Logger"):
        threading.Thread.__init__(name=name, daemon=True)
