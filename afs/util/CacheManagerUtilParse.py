"""
Parser of CacheMangerUtil
"""

def flush_all(ret, output, outerr, parse_param_list, logger) :
    """
    parses result from method of same name in VolumeLLA
    """
    obj = parse_param_list["args"][0]
    if ret :
        raise CMError("error: %s" % outerr)
    return

def flush_volume(ret, output, outerr, parse_param_list, logger) :
    """
    parses result from method of same name in VolumeLLA
    """
    obj = parse_param_list["args"][0]
    if ret :
        raise CMError("error: %s" % outerr)
    return

def flush_mount(ret, output, outerr, parse_param_list, logger) :
    """
    parses result from method of same name in VolumeLLA
    """
    obj = parse_param_list["args"][0]
    if ret :
        raise CMError("error: %s" % outerr)
    return

def flush(ret, output, outerr, parse_param_list, logger) :
    """
    parses result from method of same name in VolumeLLA
    """
    obj = parse_param_list["args"][0]
    if ret :
        raise CMError("error: %s" % outerr)
    return

def new_cell_alias(ret, output, outerr, parse_param_list, logger) :
    """
    parses result from method of same name in lo.CacheManager
    """
    obj = parse_param_list["args"][0]
    if ret :
        raise CacheManagerError("error: %s" % outerr)
    return

def pull_ws_cell(ret, output, outerr, parse_param_list, logger) :
    """
    parses result from method of same name in lo.CacheManager
    """
    obj = parse_param_list["args"][0]
    if ret :
        raise CacheManagerError("error: %s" % outerr)

    # parse "This workstation belongs to cell 'beolink.org'"
    # remove ' 
    obj.ws_cell = output[0].split()[5].replace("'","")
    return obj

def pull_cell_aliases(ret, output, outerr, parse_param_list, logger) :
    """
    parses result from method of same name in lo.CacheManager
    """
    obj = parse_param_list["args"][0]
    rx=re.compile('Alias (\S+) for cell (.*)')
    obj.cell_aliases = {}
    if ret :
        raise CacheManagerError("error: %s" % outerr)
    for line in output :
        match_obj = rx.match(line) 
        if match_obj :
            obj.cell_aliases[match_obj.groups()[0]] = match_obj.groups()[1]
    return obj
