from google.appengine.ext.webapp import blobstore_handlers
from logic.models import User

class UploadXml(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):

        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]

        key = self.request.get('key')
        
        self.redirect('/parse_xml/%s/%s' %(key, blob_info.key()))

  