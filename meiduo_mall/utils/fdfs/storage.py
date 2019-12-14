from django.core.files.storage import Storage
from django.conf import settings
from django.utils import timezone
from fdfs_client.client import Fdfs_client
from rest_framework import serializers
from meiduo_mall.utils.fdfs.custom_upload_handler import custom_upload_by_buffer
class FdfsStorage(Storage):
    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content, max_length=None):
        file_bytes = content.read()  # 文件的字节数据
        file_id = custom_upload_by_buffer(file_bytes)
        return file_id

    def url(self, name):
        return settings.FDFS_URL + name
    def exists(self, name):
        return False
