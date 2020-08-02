import os
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.web.static import File
from twisted.cred.portal import Portal # The point of integration of application and authentication.
from twisted.cred.checkers import FilePasswordDB # Basic credential checkers
from twisted.web.guard import HTTPAuthSessionWrapper, BasicCredentialFactory # Resource traversal integration with L{twisted.cred} to allow for authentication and authorization of HTTP requests.

from zope.interface import implements
from twisted.web.resource import IResource # A web resource.
from twisted.cred.portal import IRealm # The point of integration of application and authentication.

class PublicHTMLRealm(object):
    implements(IRealm) #The realm connects application-specific objects to the authentication system.
    def __init__(self, root):
        self.root = root
    
    def requestAvatar(self, avatarId, mind, *interfaces):
        if IResource in interfaces:
            return (IResource, self.root, lambda: None)
        raise NotImplementedError()


def build_sharing_resource():
    passwd_file = os.path.join(os.path.dirname(__file__), "httpd.password")
    root = build_shared_folder_resource()
    portal = Portal(PublicHTMLRealm(root), [FilePasswordDB(passwd_file)])

    credentialFactory = BasicCredentialFactory("Realm Description....")
    return HTTPAuthSessionWrapper(portal, [credentialFactory])


def build_shared_folder_resource():
    root = File(r"/folder/to/share")
    return root

if __name__ == "__main__":
    port = 8080
    root = build_sharing_resource()
    factory = Site(root)
    reactor.listenTCP(port, factory)
    print 'server is running on %i' % (port,)
    reactor.run()