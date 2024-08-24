from django.conf import settings
from django.http import FileResponse
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import FileChunk, Secret
import base64
from rest_framework.decorators import parser_classes
from .parser import OctetStreamParser
import shutil


@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([OctetStreamParser])
def handleFileUpload(request):
    id = request.META.get("HTTP_ID")
    index = request.META.get("HTTP_INDEX")
    chunk = request.body

    print("id: ", id)
    print("index: ", index)
    # print("chunk: ", chunk)

    if id is None or chunk is None or index is None:
        return Response({"error": "Failed to upload chunk"}, status=400)
    else:
        fileDir = os.path.join(settings.STORAGE_ROOT, id)
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)
        chunkPath = os.path.join(fileDir, index)
        with open(chunkPath, "wb") as f:
            f.write(chunk)

        if str(index) == "meta":
            linkLifetime = int(request.META.get("HTTP_LINKLIFETIME"))
            totalChunks = int(request.META.get("HTTP_TOTALCHUNKS"))
            iv = request.META.get("HTTP_IV")
            FileChunk.objects.create(
                file_id=id, link_lifetime=linkLifetime, total_chunks=totalChunks, iv=iv
            )
            if not request.user.is_authenticated and totalChunks > 25:
                return Response({"error": "I'm a teapot"}, status=418)

        return Response({"status": "Chunk uploaded"}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def handleFileDownload(request, id, index):
    print("id: ", id)
    if id is None:
        return Response({"error": "Failed to download file"}, status=400)
    else:
        fileDir = os.path.join(settings.STORAGE_ROOT, id)
        chunkPath = os.path.join(fileDir, str(index))
        if not os.path.exists(chunkPath):
            return Response({"error": "File not found"}, status=404)
        else:
            response = FileResponse(
                open(chunkPath, "rb"), content_type="application/octet-stream"
            )
            if index == "meta":
                response["iv"] = FileChunk.objects.get(file_id=id).iv
                response["Access-Control-Expose-Headers"] = "iv"
                print("iv: ", response["iv"])
            return response


@api_view(["POST"])
@permission_classes([AllowAny])
def deleteFile(request, id):
    if id is None:
        return Response({"error": "Failed to delete file"}, status=400)
    else:
        fileDir = os.path.join(settings.STORAGE_ROOT, id)
        if os.path.exists(fileDir):
            shutil.rmtree(fileDir)
            # to keep or not to keep
            # FileChunk.objects.filter(file_id=id).delete()
            return Response({"status": "File deleted"}, status=200)
        else:
            return Response({"error": "File not found"}, status=404)


@api_view(["POST"])
@permission_classes([AllowAny])
def handleSecretUpload(request):
    secret = request.data.get("secret")
    secretId = request.data.get("id")
    iv = request.data.get("iv")
    linkLifetime = request.data.get("linkLifetime")

    if secret is None or secretId is None or iv is None or linkLifetime is None:
        return Response({"error": "Failed to create secret"}, status=400)
    if not request.user.is_authenticated and len(secret) > 250:
        return Response({"error": "I'm a teapot"}, status=418)
    elif len(secret) > 10000:
        return Response({"error": "I'm a teapot"}, status=418)
    Secret.objects.create(
        secret=secret, secret_id=secretId, iv=iv, link_lifetime=linkLifetime
    )

    return Response({"status": "Secret created"}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def handleSecretDownload(request, id):
    if id is None:
        return Response({"error": "Failed to download secret"}, status=400)
    else:
        secret = Secret.objects.get(secret_id=id)
        return Response({"secret": secret.secret, "iv": secret.iv}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def deleteSecret(request, id):
    if id is None:
        return Response({"error": "Failed to delete secret"}, status=400)
    else:
        Secret.objects.filter(secret_id=id).update(secret="deleted")
        return Response({"status": "Secret deleted"}, status=200)
