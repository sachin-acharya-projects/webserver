import os, webbrowser, json, sys, colorama
from py_setenv import setenv
current_path = os.path.dirname(os.path.abspath(__file__))

colorama.init(autoreset=True)

help_text = """
usage: server [-h] [--host HOST] [--port PORT] [--admin] [--admin-port ADMIN_PORT] [--set] [--add-path] [-D] [--reset]

Launches Localhost server from PHP development Environment
    php -s host:port

options:
    -h, --help            show this help message and exit
    --host HOST           Host: Localhost
    --port PORT           Port: 8000
    --admin               Run server and open phpmyadmin on the same port
    --admin-port ADMIN_PORT
                        If you have running MySql on different port use this option
    --set                 Update settings with the provided/available port
    --add-path            Add the directory of main file to SYSTEM EVIRONMENT PATH VARIABLE to make this globally accessible. (If you installed this
                        module using pip, no need to use this option)
    -D                    Run server with default parameters irrespective to the settings changed (is incompatible with --host or --port)
    --reset               Reset settings to default. Use this option incase of errors
"""

def serverNow(host, port, isAdminReq, adminPort):
    if isAdminReq:
        webbrowser.open_new_tab('http://{}:{}/phpmyadmin'.format(host, adminPort))
    else:
        webbrowser.open_new_tab('http://{}:{}'.format(host, adminPort))
    os.system('php -S {}:{}'.format(host, port))

def doesExist(path: str):
    userprofile = os.environ['USERPROFILE']
    path_2 = ''
    if userprofile in path:
        path_2 = path.replace(userprofile, "%USERPROFILE%")
    elif "%USERPROFILE%" in path:
        path_2 = path.replace("%USERPROFILE%", userprofile)
    pathlist = setenv("path", user=True, suppress_echo=True).split(";")
    if path in pathlist or path_2 in pathlist:
        return True
    return False

def maniJson(params="read", write=False, data=''):
    with open(os.path.join(current_path, 'settings.json'), 'r+') as file:
        filedata = json.load(file)
        if write and params != 'read':
            if not data is filedata[params]:
                filedata[params] = data
            else:
                return False
            file.seek(0)
            file.truncate()
            json.dump(filedata, file, indent=4)
            return True
        else:
            if params == 'read':
                return filedata
            else:
                return filedata[params]

class Namespace:
    def __init__(self, **kargs):
        self.__dict__.update(kargs)

class ArgumentParser_:
    def __init__(self, args: list, argument_req: list):
        self.result_dict = {
            
        }
        
        for argument, action in argument_req:
            argument_name = str(argument).removeprefix('-').removeprefix('-').replace('-', '_')
            if action:
                self.result_dict[argument_name] = True if argument in args else False
            else:
                try:
                    self.result_dict[argument_name] = args[args.index(argument) + 1] if argument in args else None
                except:
                    print(f"{colorama.Fore.RED}Positional argument {argument} cannot accept empty value. Please use --help to find out more")
                    sys.exit()
    @property
    def parse_args_all(self):
        return Namespace(**self.result_dict)
def argumentParser():
    # Useless function - left for future
    import argparse
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--host', help='Host: Localhost')
    parser.add_argument('--port', help='Port: 8000')
    
    parser.add_argument('--admin', help='Run server and open phpmyadmin on the same port', action="store_true")
    
    parser.add_argument('--admin-port', help='If you have running MySql on different port use this option')
    parser.add_argument('--set', help='Update settings with the provided/available port', action="store_true")
    
    parser.add_argument("--add-path", help="Add the directory of main file to SYSTEM EVIRONMENT PATH VARIABLE to make this globally accessible. (If you installed this module using pip, no need to use this option)", action='store_true')
    
    parser.add_argument('-D', help="Run server with default parameters irrespective to the settings changed (is incompatible with --host or --port)", action='store_true')
    parser.add_argument("--reset", help="Reset settings to default. Use this option incase of errors", action='store_true')
    
    return parser
def main():
    arguments = sys.argv
    parser = ArgumentParser_(arguments, [
        ('--host', False),
        ('--port', False),
        ('--admin', True),
        
        ('--admin-port', False),
        ('--set', True),
        
        ('--add-path', True),
        ('-D', True),
        ('--reset', True),
        ('--help', True),
        ('-h', True)
    ])

    arguments = parser.parse_args_all
    if arguments.help or arguments.h:
        print(f"{colorama.Fore.CYAN}{help_text}")
        sys.exit()
    host = ''
    port = ''

    if arguments.reset:
        maniJson("host", write=True, data="localhost")
        maniJson("port", write=True, data="8000")
        print(f"{colorama.Fore.CYAN}Settings are restored to previous one. Please re-run the command")
        exit()
    # Getting Host
    if arguments.host == None:
        if arguments.D:
            host = maniJson()['default_host']
        else:
            host = maniJson()['host']
    else:
        host = arguments.host
        
    # Getting Port
    if arguments.port == None:
        if arguments.D:
            port = int(maniJson()['default_port'])
        else:
            port = int(maniJson()['port'])
    else:
        port = int(arguments.port)
    
    # Updating Settings
    if arguments.set:
        maniJson("host", write=True, data=host)
        maniJson("port", write=True, data=str(port))
    
    # Adding to SystemPath if asked
    if arguments.add_path:
        if not doesExist(current_path):
            setenv("path", value=current_path, append=True, user=True, suppress_echo=True)
            print(f"{colorama.Fore.CYAN}Location {current_path} has been [APPENED] to [PATH]")

    # Checking if admin is asked
    if arguments.admin_port:
        adminPort = arguments.admin_port
    else:
        adminPort = port
    
    serverNow(host, port, arguments.admin, adminPort)
if __name__ == '__main__':
    main()