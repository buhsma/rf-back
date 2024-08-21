from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.parsers import BaseParser

class OctetStreamParser(BaseParser):
    media_type = 'application/octet-stream'

    def parse(self, stream, media_type=None, parser_context=None):
        return SimpleUploadedFile(name="chunk", content=stream.read())