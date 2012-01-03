class VolError(Exception):
    def __init__(self, message, Errors=[]):
        Exception.__init__(self, message)
        # Now for your custom code...
        self.Errors = Errors

  
    def __str__(self):
      #FIXME parse build a complete message with stack
      return repr(self.message)
