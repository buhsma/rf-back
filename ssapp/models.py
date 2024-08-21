from django.db import models

class FileChunk(models.Model):
    file_id = models.CharField(max_length=255)
    link_lifetime = models.IntegerField()
    total_chunks = models.IntegerField()
    iv = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chunks'

class Secret(models.Model):
    secret = models.CharField(max_length=10000)
    secret_id = models.CharField(max_length=255)
    link_lifetime = models.IntegerField()
    iv = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'secrets'