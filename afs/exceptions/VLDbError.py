

class VLDbError(Exception):
    def __init__(self, msg, stack=[]):
      self.msg   = msg
      self.stack = stack
  
    def __str__(self):
      #FIXME parse build a complete message with stack
      return repr(self.value)