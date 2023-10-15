class SocketClosedError(BaseException):
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return f'Socket closed'