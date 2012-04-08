from afs.model.Volume import Volume

class QueryVol(object):
    """
    Query the DB or live data
    """
    limit  = -1
    offset = -1
    field  = "name"
    value  = ""
    order  = ""
    dir    = ""
    
    
    def __init__(self):
        pass
    
    def getQuery(self):
        pass
    
    """
    Retrieve Volume List
    """
    def getVolList(self,volQuery,**kwargs):
        pass
    
    ###############################################
    # Volume Management Section
    ###############################################
   
    def loadVol(self, servername=None, **kwargs):
        
        # This function is good only with db
        if not self._CFG.DB_CACHE:
             return
         
        cellname = self._TOKEN._CELL_NAME
        
        if kwargs.get("cellname"):
            cellname = kwargs.get("cellname")
        
        servers = []
        
        #Create a Server List
        if servername:
            server = self._srvDAO.getServer( servername, cellname)  
            servers.append(server) 
        else:
            servers = self._srvDAO.getServerList(cellname)
        
        #Get DB Session
        session = self.DbSession()
           
            
        for server in servers:
            #List of partitions in the specific server
            parts = self._srvDAO.getPartList(server.name,cellname)
            
            for part in parts:
                volDbList = session.query(Volume).filter(Volume.serv == server.name).filter(Volume.part == part.name)
                #List of volume in the specific server and specific partition
                volSvrList = self._srvDAO.getVolIdList( part.name, server.name, cellname)
                for vol in volDbList: 
                    self._volDAO.getVolume(vol.vid, vol, cellname)
                    if volSvrList.has_key(vol.vid):  
                        volSvrList.pop(vol.vid)
                    else:
                        session.delete(vol)
                    
                session.flush()
                for vid in volSvrList:
                     vol = Volume()
                     self._volDAO.getVolume(vid, vol, cellname, self._TOKEN)
                session.flush()
            session.commit()      
 
