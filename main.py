from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import orgo
from urllib.parse import unquote

hostName = "0.0.0.0"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		
		if self.path.startswith("/ozone"):
			inchi = self.path.split("inchi=")[1]
			inchi = unquote(inchi)
			try:
				output = '\n'.join(orgo.ozonolyse(inchi))
				self.wfile.write(bytes(output, "utf-8"))
			except AttributeError:
				self.wfile.write(bytes("bad"), "utf-8")
		elif self.path.startswith("/hydrogen"):
			inchi = self.path.split("inchi=")[1]
			inchi = unquote(inchi)
			try:
				output = '\n'.join(orgo.hydrogenate(inchi))
				self.wfile.write(bytes(output, "utf-8"))
			except AttributeError:
				self.wfile.write(bytes("bad"), "utf-8")
		else:
			self.wfile.write(bytes("bad"), "utf-8")
		
		

if __name__ == "__main__":
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	print("Server stopped.")
