"""
collection of small functions use everywhere
"""
import logging
import re
import types
from afs.util.UtilError import UtilError

# log-level is set in AfsConfig
LOGGER = logging.getLogger("afs.util")

BASE1024_UNITS = ['', 'K', 'M', 'G', 'T', 'P']
PARTITION_RX = re.compile("/?(?:vicep)?([a-z][a-z]?)")
BASE1024_UNITS_RX = re.compile("(\d+)([KMGTP]?)")

def convert_to_base1024_unit_number(number) :
    """
    take a number and translate it to a string using base 1024 units 
    """
    best_unit = 0 
    for unit in range(len(BASE1024_UNITS)) :
        if float(number) / (1024 ** (unit + 1)) < 1 : 
            best_unit = unit 
            break
    return "%3.2f %s" % (float(number) / (1024 ** best_unit), \
         BASE1024_UNITS[best_unit])

def parse_number_with_base1024_unit(number_unit) :
    """
    return absolute Value of sth like 100M
    base 1024 used.
    """ 
    match_object = BASE1024_UNITS_RX.match(number_unit)
    if not match_object:
        raise UtilError("Cannot parse value %s. Should be an integer with " +
            "an optional unit of %s" % BASE1024_UNITS)  
    number, unit = match_object.groups()
    number = int(number)
    multiplicator = 1
    if len(unit) != 0 : 
        for _unit in range(len(BASE1024_UNITS)) :
            if unit == BASE1024_UNITS[_unit] :
                multiplicator = 1024**(_unit)
                break
    return multiplicator * number            

def canonicalize_partition(part) :
    """
    reduce given representation of a partition
    like /vicepa or vicepbb to the one-or-two-letter 
    representation "a" or "bb"
    """
    if type(part) == types.StringType :
        if part.isdigit() :
            part = int(part)
    if type(part) == types.IntType : 
        first_letter  = part / 26
        second_letter = part % 26
        partition = ""
        if first_letter != 0 :
            partition += chr(ord("a") + first_letter) 
        partition += chr(ord("a") + second_letter) 
    else :
        match_object = PARTITION_RX.match(part)
        if not match_object :
            raise UtilError("Cannot canonicalize \"%s\"" % part)
        partition = match_object.groups()[0] 
    return partition
 
 
def canonicalize_volume(volname):
    """
    remove well-known suffices .readonly and .backup
    from a volume-name, if presetn 
    """
    
    if volname.endswith(".readonly"):
        return volname[0:len(volname)-9]
    
    if volname.endswith(".backup"):
        return volname[0:len(volname)-6]

def is_name(ambiguous) :
    """
    checks if name_or_ip or name_or_id is acutally the name or an numerical ID
    """
    # first, convert to string 
    ambiguous = "%s" % ambiguous    
    ambiguous = ambiguous.strip()
    if len(ambiguous) == 0 :
        raise UtilError("isName called with empty string!")
    LOGGER.debug("isName: got '%s'" % ambiguous)
    if ambiguous[0].isdigit() : 
        return False
    else :
        return True
