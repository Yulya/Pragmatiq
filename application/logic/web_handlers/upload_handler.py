import re
from google.appengine.api import files
from google.appengine.ext.webapp import blobstore_handlers

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):

    blob_key = None

    def post(self):

        upload_files = self.get_uploads('file')

        results = []
        blob_keys = []

        for name, fieldStorage in self.request.POST.items():
            if type(fieldStorage) is unicode:
                continue
            name = re.sub(r'^.*\\', '',
                fieldStorage.filename)
            t = fieldStorage.type

            blob = files.blobstore.create(
                mime_type=t,
                _blobinfo_uploaded_filename=name
            )
            with files.open(blob, 'a') as f:
                f.write(fieldStorage.value)
            files.finalize(blob)

            blob_key = files.blobstore.get_blob_key(blob)
            self.blob_key = blob_key


    