import logging
import re
from google.appengine.api import files
from google.appengine.ext.webapp import blobstore_handlers
from logic.web_handlers.upload_handler import UploadHandler

class UploadXml(UploadHandler):

    blob_key = None

    def post(self):

        super(UploadXml, self).post()

        key = self.request.POST.get('key')
        logging.debug(key)
        role = self.request.POST.get('role')

        self.redirect('/parse_xml/%s/%s/%s' %(role, key, self.blob_key))


