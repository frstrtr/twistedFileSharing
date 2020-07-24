import os
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.web.static import File
from twisted.cred.portal import Portal
from twisted.cred.checkers import FilePasswordDB
from twisted.web.guard import HTTPAuthSessionWrapper, BasicCredentialFactory

from zope.interface import implements
from twisted.web.resource import IResource
from twisted.cred.portal import IRealm

class PublicHTMLRealm(object):
    implements(IRealm)
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