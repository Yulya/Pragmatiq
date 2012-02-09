from google.appengine.ext.blobstore import blobstore
from google.appengine.ext.db import Model
from logic.web_handlers.upload_handler import UploadHandler

class UploadFile(UploadHandler):

    blob_key = None

    def post(self):

        super(UploadFile, self).post()

        key = self.request.POST.get('key')
        form = Model.get(key)
        blob_info = blobstore.BlobInfo.get(self.blob_key)
        form.file_key = str(blob_info.key())
        form.file_name = blob_info.filename

        form.put()
