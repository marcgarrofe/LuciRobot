class VideoBaseModule():
    def __init__(self):
        self.on_finish = None
        self.on_start = None

        self.stopped = False
        self.called = False
    
    def start(self):
        if self.on_start is not None:
            self.on_start()
        return self

    def stop(self):
        self.stopped = True

        if self.on_finish is not None and not self.called:
            self.called = True
            self.on_finish()

        return self