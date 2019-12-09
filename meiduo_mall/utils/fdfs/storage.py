from django.core.files.storage import Storage
from django.conf import settings
from django.utils import timezone
from fdfs_client.client import Fdfs_client
from rest_framework import serializers

class FdfsStorage(Storage):
    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content, max_length=None):
       pass

    def url(self, name):
        return settings.FDFS_URL + name
