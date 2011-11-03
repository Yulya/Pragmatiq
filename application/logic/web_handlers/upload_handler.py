from google.appengine.ext.db import Model
from google.appengine.ext.webapp import blobstore_handlers

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):

        upload_files = self.get_uploads('file')
        key = self.request.get('key')
        blob_info = upload_files[0]
        form = Model.get(key)
        form.file_key = str(blob_info.key())
        form.file_name = blob_info.filename

        form.put()
        self.redirect('/')