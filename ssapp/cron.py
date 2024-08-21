from rest_framework_simplejwt.token_blacklist.management.commands import flushexpiredtokens
from ssapp.models import FileChunk, Secret
from django.db.models import F
from django.utils import timezone
def flushBlacklist():
    flushexpiredtokens.Command().handle()

def deleteExpiredData():
    
    now = timezone.now()

    FileChunk.objects.filter(created_at__lt=now - timezone.timedelta(hours=F('link_lifetime'))).delete()
    Secret.objects.filter(created_at__lt=now - timezone.timedelta(hours=F('link_lifetime'))).delete()