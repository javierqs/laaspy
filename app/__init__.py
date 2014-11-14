import cherrypy
import subprocess
import os
from time import time
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('views'))

class MainController(object):

    def index(self):
        tmpl = env.get_template("/home/index.html")
        return tmpl.render()

class ModelsController(object):

    def index(self):
        return "Model#index"

    def show(self, name):
        tmpl = env.get_template("/models/show.html")
        return tmpl.render(new_name = name)

    def process(self, **kwargs):
        p = kwargs
        hs = "MODEL:\nTITLE:{0}\nSETS:\n{1}\nENDSETS\nDATA:\n{2}\nENDDATA\nCALC:\n{3}\nENDCALC\n{4}\nEND".format(p["model_title"],p["model_sets"],p["model_data"],p["model_calc"],p["model_obj"])
        test_file = open("test.ltf","w")
        test_file.write(hs)
        test_file.close
        cherrypy.log(hs)
        cherrypy.log(','.join(kwargs.values()))
        raise cherrypy.HTTPRedirect("/")

class Laaspy(object):
    def index(self):
        return file("views/models/index.html")
    index.exposed = True

    @cherrypy.expose
    def models(self, name):
        return "MMM"        

    def lingo_process(self):
        # Set time of arriving
        current_time = int(time()*1000) 
        lingo_file_name = "test_one_1"
        '''
        # Lingo script file name
        lingo_file_name = "lingo_{0}".format(current_time) 

        # Lingo script file
        lingo_file = open("{0}.ltf".format(lingo_file_name), 'w')
 
        # Writing from html-form input
        # TODO: check dictionaries
        lingo_file.write(model[script]) 
        
        # Adding lingo commands that outputs results and saving them in a txt file
        # Text file that contains the output have a related name
        # TODO: check python string interpolation
        lingo_file.write("\nSET TERSEO 3\nGO\n\DIVERT output_{0}.txt\nSOLUTION\nRVRT\nQUIT".format(lingo_file_name))

        # After filling the txt file with proper content, it has to be closed
        lingo_file.close()
        '''
        # And the magic(tm) begins...
        #   Setting wine prefix in order to use 32bits architecture
        wine_prfx = "WINEARCH=win32 WINEPREFIX=~/win32 "

        #   Here is the command used:
        #   wine [RunLingo.exe path] [Path of file with Lingo commands]
        wine_cmd  = "wine 'C:\LINGO14\RunLingo.exe' /home/j/python/laaspy/{0}.ltf".format(lingo_file_name)

        #   While Lingo could be used as a linear programming solver, in this case (as an example)
        #   I'm adding the ability of using a db (via ODBC drivers and other stuff)
        # TODO: 
        #   - check if _script_ needs/uses @ODBC method in order to avoid creating this string and then executing 
        #   - replace Driver name value according to what I would use
        #   - replace DSN name
        #   - replace db name
        odbc_dsn  = "wine odbcconf configdsn \"Microsoft Access Driver (*.mdb, *.accdb)\" \"DSN=Transportation|DBQ=c:\\LINGO14\\Samples\\TRANDB.mdb\""

        # And now, we start the processes
        #       n           Process var    Description
        #   Process 1          p1          Executes the command that creates the data source value in ODBC windows administrator
        #   Process 2          p2          Executes command that runs Lingo script
        # value "shell=True" passed to Popen method needs to be checked (Just in order to understand what its happening
        # It also has to wait for the process to finish by using method ".wait()" because one can run faster than the other
        # but I need that the DSN gets created first
        p1 = subprocess.Popen([wine_prfx + odbc_dsn], shell=True)
        p1.wait()

        p2 = subprocess.Popen([wine_prfx + wine_cmd], shell=True, stdout = subprocess.PIPE)
        p2.wait()

        # Here comes the tricky part. I have to solve these issues
        # - Wrong script
        # - missing statements
        # - bad script order
        # The first time I handled these by reading the output of the process that execute the lingo script in real time
        # but now I just waited for it to finish (if it actually finishes) and then doing what I need to do with the result
        # TODO: check if it _actually_ works with bad input
        html_content = open("output_{0}.txt".format(lingo_file_name)).read()

        # Now we proceed to delete script file and output file
        os.remove("{0}.ltf".format(lingo_file_name))
        os.remove("output_{0}.txt".format(lingo_file_name))

        # And now we proceed to remove the DSN's (because we don't want that ODBC admin gets full of sh*t)
        # TODO: Set string interpolation for whatever values come in
        wine_rmv_odbc_dsn = "wine reg delete \"HKEY_CURRENT_USER\\SOFTWARE\\ODBC\\ODBC.INI\\Transportation\" /f"
        wine_rmv_odbc_adm = "wine reg delete \"HKEY_CURRENT_USER\\SOFTWARE\\ODBC\\ODBC.INI\\ODBC Data Sources\" /v Transportation /f"

        # Damn ... more process???
        # Process below are just to avoid ODBC admin gets full
        # TODO: why do I still use shell = True? I guess nobody knows
        del_dsn_p = subprocess.Popen([wine_prfx + wine_rmv_odbc_dsn], shell = True)
        del_dsn_p.wait()
   
        del_adm_p = subprocess.Popen([wine_prfx + wine_rmv_odbc_adm], shell = True)
        del_dsn_p.wait()

        return html_content
    lingo_process.exposed = True
