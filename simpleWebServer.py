import sys

from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from twisted.python import log

class Counter(resource.Resource):
    isLeaf = True
    numberRequests = 0

    def render_GET(self, request):
        self.numberRequests += 1
        request.setHeader(b"content-type", b"text/plain")
        content = u"I am request #{}\n".format(self.numberRequests)
        return content.encode("ascii")

log.startLogging(sys.stdout) # log to console
endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(Counter()))
reactor.run()