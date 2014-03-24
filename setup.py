import sys, string, os, re
from distutils.core import setup
# we need to ask the user information about his cell

if len(sys.argv) == 2 :
    if sys.argv[1] == "install" :
        print "Configuration of afspy-module..."
        doModify=raw_input("Do you want to modify the config file afs/etc/afspy.cfg ? [y/N]")
        if doModify.lower() == "y" :
            configFilenname="afs/etc/afspy.cfg"
            templateFilename="{0}.template".format(configFilenname)
            # read in template file
            i_f=file(templateFilename)
            thisOption={"Comment" : []}
            o_f=file(configFilenname, "w+")
            while 1 :
                line=i_f.readline()
                if not line : break
                line =line.strip()
                if len(line) == 0  : continue
                if line[:2] == "##" :
                    tokens=line[2:].strip().split(":")
                    if not thisOption.has_key(tokens[0]) :
                            thisOption[tokens[0].strip().lower()] = tokens[1].strip().lower()
                elif line[0] == "#" :
                    if not thisOption.has_key("Comment") : continue
                    thisOption["Comment"].append(line)
                else :
                    try :
                        key, defaultValue=line.split("=")
                    except:
                        sys.stderr.write("parse error of {0} at line '{1}'\n".format(templateFilename, line))
                        sys.exit(1)
                    if defaultValue.strip() == "" :
                        if thisOption.has_key("default") :
                            defaultValue=thisOption["default"]
                    # post processing of lines
                    if thisOption.has_key("allowed") :
                        thisOption["allowedList"] = thisOption["allowed"].split(",")
                    print string.join(thisOption["Comment"], "\n")
                    print "# Type: {0}".format(thisOption["type"])
                    if thisOption.has_key("allowed") :
                        print "# Allowed values: '{0}'".format(thisOption["allowed"])
                    else :
                        print "# this is a free-form field"
                    if thisOption.has_key("mandatory") :
                        print "# this field is mandatory."
                    givenValue=raw_input("{0} [{1}] :".format(key,defaultValue))
                    print
                    if givenValue == "" :
                        realValue=defaultValue
                    else :
                        realValue = givenValue
                    # some testing
                    if realValue == ""  :
                        if  thisOption.get("mandatory", "false") == "true"  :
                            sys.stderr.write("No value for mandatory option '{0}' given.\n".format(key))
                            sys.exit(2)
                    if thisOption["type"] == "integer" :
                        try :
                            realValue=int(realValue)
                        except :
                            sys.stderr.write("Value '{0}' for key '{1}' is not an integer.\n".format(realValue, key))
                            sys.exit(1)
                    if thisOption.has_key("allowedList") :
                        if not realValue in thisOption["allowedList"] :
                            sys.stderr.write("Value '{0}' not allowed for key '{1}'\n".format(realValue, key))
                            sys.exit(1)
                    o_f.write("{0}={1}\n".format(key,realValue ))
                    thisOption={"Comment" : []}
            o_f.close()

        #
        # auto generate historic models for db :
        #
        model_object_rx = re.compile("class\s+(\S+)\(.*")
        h = file("afs/model/Historic.py", "w+")
        h.write("""# 
# autogenerated by setup.py
# DO NOT EDIT!
#
from datetime import datetime
from afs.model.BaseModel import BaseModel
from afs.magix import *

""")
        for model_object_file in os.listdir("afs/model") :
            if not model_object_file.endswith(".py") : continue
            if model_object_file in ["__init__.py", "BaseModel.py", "Historic.py"] : continue
            print "auto-generating historic class for %s" % model_object_file
            f = file("afs/model/%s" % model_object_file, "r")
            in_class = False
            while 1 :
                line = f.readline()
                if not line : break
                if line.startswith("class") :
                    model_object = model_object_rx.match(line).groups()[0]
                    h.write("""
#
# %s
#

""" % model_object)
                    h.write(line.replace(model_object,"historic_%s" % model_object))
                    in_class = True
                    continue
                if not in_class: continue
                if "BaseModel.__init__(self)" in line :
                    h.write(line)
                    h.write("        ## pointer to current table entry\n")
                    h.write("        self.real_db_id = -1\n")
                else :
                    h.write(line)
            f.close()
        h.close()        
        #
        # autogenerate historic mapping
        #     
        f = file("afs/orm/DBMapper.py", "r")
        h = file("afs/orm/Historic.py", "w+")
        h.write("""
# autogenerated by setup.py
# DO NOT EDIT!
#
import datetime
from afs.orm.DBMapper import safe_mapping, LOGGER
""")
        in_fct = False
        historic_tables=[]
        while 1 :
            line = f.readline()
            if not line : break            
            if line.startswith("def setup_db_mappings") :
                h.write(line)
                in_fct = True
                continue
            if not in_fct : continue
            if "Table" in line or "Key" in line :
                h.write(line.replace("tbl_","tbl_hist_"))
                if not "Table" in line : continue 
                if "tbl_" in line :
                    historic_tables.append(line.replace("tbl_","tbl_hist_").split()[0]) 
            elif ("import" in line) and (not "sqlalchemy" in line) :
                model_object = line.split()[-1:][0]
                h.write("    from afs.model.Historic import historic_%s\n" % model_object)
            elif "safe_mapping" in line :
                # import always comes before safe_mapping
                h.write(line.replace("tbl_","tbl_hist_").replace(model_object, "historic_%s" % model_object))
            elif "primary_key" in line :
                h.write(line)
                h.write("        Column('real_db_id', Integer),\n")
            else :
                h.write(line)
       
        f.close()
        
        h.write("\n# list of all historic tables\n")
        h.write("historic_tables = [")
        for line in historic_tables :
            h.write('"%s", ' % line)
        h.write("]\n") 
        h.close()

setup(
    name='afspy',
    version='0.2.0',
    author='Christof Hanke, Fabrizio Manfredi',
    author_email='hanke@rzg.mpg.de, fabrizio.manfredi@gmail.com',
    packages=['afs', 'afs.util', 'afs.model', 'afs.dao', 'afs.service', 'afs.tests', 'afs.orm'],
    package_data={'afs': ['etc/*.cfg', 'etc/pythonstartup']},
    url='http://pypi.python.org/pypi/afspy/',
    license='LICENSE.txt',
    description='high-level bindings to openAFS',
    long_description=open('README.txt').read(),
    requires=[
        "pymysql",
    ],
)
