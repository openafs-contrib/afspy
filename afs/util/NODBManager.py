# XXX: this should be generated while installing
from afs.exceptions.AfsError import AfsError

class NODBManager :
      def __init__(self) :
          pass
      def getFromCache(Class, mustBeunique=True,**where) :
          raise AfsError("No DBcache defined.")
      def getFromCacheByListElement(self,Class,Attr,Elem) :
          raise AfsError("No DBcache defined.")
      def getFromCacheByDictKey(self,Class,Attr,Elem) :
          raise AfsError("No DBcache defined.")
      def getFromCacheByDictValue(self,Class,Attr,Elem) :
          raise AfsError("No DBcache defined.")
      def getFromJoinwithFilter(self,ClassA,AttrA,ClassB,AttrB,**where) :
          raise AfsError("No DBcache defined.")
      def setIntoCache(self,Class,Obj,**unique) :
          raise AfsError("No DBcache defined.")
