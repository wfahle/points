import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = 'algorithmsr.us' # my IP address 
host_port = 80

class MyServer(BaseHTTPRequestHandler):
    """ A web page of points
    """
    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command
        'curl -I http://server-ip-address:port'
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()
    def do_GET(self):
        """ do_GET() can be tested using curl command
            'curl http://server-ip-address:port'
        """
        html = '''
            <html>
            <body style="width:960px; margin: 20px auto;">
            <h1>Welcome to Fahle test page</h1>
            <form action="/" method="POST">
                <label style="50px;width:200px;font-size:large" for="payer">Payer:</label>
                <input style="height:50px;width:200px;font-size:large" type="string" id="payer" name="payer">
                <label style="50px;width:200px;font-size:large" for="points">Points:</label>
                <input style="height:50px;width:200px;font-size:large" type="number" id="points" name="points">
                <label style="50px;width:200px;font-size:large" for="timestamp">Timestamp:</label>
                <input style="height:50px;width:200px;font-size:large" type="date" id="timestamp" name="timestamp">
                <input style="height:50px;width:200px;font-size:large" type="submit" name="submit" value="Ok">
                <input style="height:50px;width:200px;font-size:large" type="submit" name="submit" value="Clear">
            </form>
            </body>
            </html>
        '''
        self.do_HEAD()
        self.wfile.write(html.encode("utf-8"))
    def do_POST(self):
        """ do_POST() can be tested using curl command
            'curl -d "submit=Ok" http://server-ip-address:port'
        """
        content_length = int(self.headers['Content-Length']) # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8") # Get the data
        print(post_data)
        submit_data = post_data.split("submit=")[1] # Only keep the value
        if submit_data == 'Ok':
            payer_data = post_data.split("&")[0] #only keep the payer
            payer_data = payer_data.split("=")[1] #only keep the value
            print("Payer {}".format(payer_data)) #put out the payer so we know
            points_data = post_data.split("&")[1] #only keep the points
            points_data = points_data.split("=")[1] #only keep the value
            print("Points {}".format(points_data)) #put out the points so we know
            timestamp_data = post_data.split("&")[2] #only keep the timestamp
            timestamp_data = timestamp_data.split("=")[1] #only keep the value
            print("Timestamp {}".format(timestamp_data)) #put out the timestamp so we know
            print("Button is {}".format(submit_data))
#            subprocess.call(['sh', './replay.sh', hours_data])
        else:
            print("Button is {}".format(submit_data))
#            subprocess.call(['sh', './lightsoff.sh'])
        self._redirect('/') # Redirect back to the root url
    
if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
