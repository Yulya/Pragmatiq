import urllib
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):

    def get(self, resource):

        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)
