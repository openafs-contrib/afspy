class UtilError(Exception):
    """
    custom exception for utility functions
    """
    def __init__(self, message, Errors = None):
        Exception.__init__(self, message)
        # Now for your custom code...
        self.errors = Errors

