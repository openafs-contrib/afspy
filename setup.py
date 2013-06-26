import sys, string
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

setup(
    name='afspy',
    version='0.1.0',
    author='Christof Hanke, Fabrizio Manfredi',
    author_email='hanke@rzg.mpg.de, fabrizio.manfredi@gmail.com',
    packages=['afs', 'afs.util','afs.model','afs.dao','afs.service','afs.tests','afs.exceptions','afs.orm'],
    package_data={'afs': ['etc/*.cfg', 'etc/pythonstartup']},
    url='http://pypi.python.org/pypi/afspy/',
    license='LICENSE.txt',
    description='high- and low-level bindings to openAFS',
    long_description=open('README.txt').read(),
    requires=[
        "tornado",
        "pymysql",
    ],
)
