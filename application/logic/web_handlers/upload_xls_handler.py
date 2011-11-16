from google.appengine.ext.webapp import blobstore_handlers
from logic.models import ContactXlsFile

class UploadXlsHandler(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):

        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]

        file = ContactXlsFile(file_key=str(blob_info.key()))
        file.put()

        self.redirect('/parse_xls')
  