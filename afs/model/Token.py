class Token(object):
    """
    Model object of a Token... t
    """
    _CELL_NAME = ""
    _AFS_ID = -1


    def __init__(self,afsid,cellname):
        """
        initialize an empty object
        """
        #Check the cell
        self._CELL_NAME = cellname
        self._AFS_ID = afsid
