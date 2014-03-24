class ExecutionError(BaseException) :
    """custom exception for executing shell commands."""

    def __init__(self, message, stack = None):
        BaseException.__init__(self, message)
        self.message   = message
        if stack != None :
            self.stack = stack
        else :
            self.stack = []

    def __str__(self):
        return repr(self.message)
       

