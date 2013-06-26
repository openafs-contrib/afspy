"""
Collection classes providing valid values for certain objects
"""

class BNodeType(object):
  """
  Provides static information on BNode Type values  
  BNodes are the children of the bosserver
  """ 

  fs = "FILESERVER"
  simple  = "SIMPLE"
  cron = "CRON"
  dafs = "DemandAttachFileserver"

class ServerType(object):
  """
  Provides static information on Server Type values  
  """ 

  FS = "FILESERVER"
  DB  = "DATABASE"
  
class VolStatus(object):
  """
  Provides static information on  Volumes Type values  
  """ 

  OFF_LINE = "OFF_LINE"
  ON_LINE  = "ON_LINE"
  OK       = "OK"
  
class VolType():
    """
    Provides static information on  Volumes Status values 
    """
    RW = "RW"
    RO = "RO"
    BK = "BK"
   
