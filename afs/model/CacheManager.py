"""
Declares Model object of a CacheManager
This will never be cached to DB. 
"""
class CacheManager(object) :
    """
    empty Model for a CacheManager
    """
    def __init__(self):
        """
        Initializes empty shell
        """
        
        ## Cellname
        self.ws_cell = ""
        ## Aliases
        self.cell_aliases={}
