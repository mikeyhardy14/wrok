import http.server
import socketserver
import csv
import json
import os
import urllib.parse

PORT = 8080

Handler = http.server.SimpleHTTPRequestHandler

# Change the directory to the folder containing your CSV file
# For example, if your file is located at 'C:/users/data/results.csv', change to 'C:/users/data/'
DIRECTORY = 'C:/users/data/'

class CustomHandler(Handler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if parsed_url.path == '/convert' and 'csv' in query_params:
            csv_file = query_params['csv'][0]
            json_file = csv_file[:-4] + '.json'
            csv_path = os.path.join(DIRECTORY, csv_file)
            json_path = os.path.join(DIRECTORY, json_file)
            if os.path.isfile(csv_path):
                self.convert_csv_to_json(csv_path, json_path)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                with open(json_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'File not found')
        else:
            super().do_GET()

    def convert_csv_to_json(self, csv_file, json_file):
        csv_data = []
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                csv_data.append(row)
        with open(json_file, 'w') as file:
            json.dump(csv_data, file)

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()