import os, pathlib, argparse, webbrowser, json
current_path = pathlib.Path(__name__).absolute().parent

def serverNow(host, port):
    webbrowser.open_new_tab('http://{}:{}'.format(host, port))
    os.system('php -S {}:{}'.format(host, port))
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host: Localhost')
    parser.add_argument('--port', help='Port: 8000')
    parser.add_argument('--admin', help='Open PhpMyAdmin HOST and PORT are irrespective to passed HOST and PORT. Change HOST and PORT in settings of this program for default. Cannot use --host and --port along with it')
    parser.add_argument('--set', help='Change settings. Cannot use --host and --port with it')
    arguments = parser.parse_args()
    host = ''
    port = ''
    
    if arguments.host == None:
        host = 'localhost'
    else:
        host = arguments.host
    if arguments.port == None:
        port = 8000
    else:
        port = int(arguments.port)
    if arguments.admin == None and arguments.set == None:
        serverNow(host, port)
        print('Working')
    else:
        filePath = os.path.join(current_path, 'settings.json')
        if arguments.admin != None:
            jsonFile = open(filePath, 'r')
            raw_json = json.load(jsonFile)
            json_host = raw_json['host']
            json_port = raw_json['port']
            url = "http://{}:{}/phpmyadmin/".format(json_host, json_port)
            webbrowser.open(url)
        if arguments.set != None:
            os.startfile(filePath)