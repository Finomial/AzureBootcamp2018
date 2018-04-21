import os
import sys
import glob
from shutil import copyfile
from azure.storage.blob import BlockBlobService
from azure.storage.blob.models import ContentSettings
import moviepy.editor 
#from moviepy.video.VideoClip import VideoClip, ImageClip, TextClip

storage_account_name = os.getenv('STORAGE_ACCOUNT_NAME', 'kolaz')
storage_account_key = os.getenv('STORAGE_ACCOUNT_KEY', 'DNbZRtB4422yE/y1gYf+z0NnazfeJVGaicFecL7CKYawW6zgGjRNVDCoL6omTG/wObLhG4ZJeiMsTYlsKs4dIw==')
container_name = os.getenv('CONTAINER_NAME', 'green')
source_video_name = os.getenv('SOURCE_VIDEO_NAME', 'source.mp4')
source_audio_name = os.getenv('SOURCE_AUDIO_NAME', 'source.mp3')
smashed_name = os.getenv('SMASHED_NAME', 'smashed.mp4')
smashed_content_type = os.getenv('SMASHED_CONTENT_TYPE', 'video/mp4')

print('%s = %s' % ('storage_account_name', storage_account_name))
print('%s = %s' % ('storage_account_key', storage_account_key))
print('%s = %s' % ('container_name', container_name))
print('%s = %s' % ('source_video_name', source_video_name))
print('%s = %s' % ('source_audio_name', source_audio_name))
print('%s = %s' % ('smashed_name', smashed_name))
print('%s = %s' % ('smashed_content_type', smashed_content_type))

def smash_video_audio(video_path, audio_path, smash_path):
    try:
        video = moviepy.editor.VideoFileClip(video_path)
        audio = moviepy.editor.AudioFileClip(audio_path)
        video.audio = audio
        video.write_videofile(smash_path, fps=4)

        print('successfully wrote %s' % smash_path)
    except Exception as e:
        print('failed in writing %s with error %s' % (smash_path, str(e)))
    

# derived from snippets here: https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
blob_service = BlockBlobService(account_name=storage_account_name, account_key=storage_account_key) 

generator = blob_service.list_blobs(container_name)
for blob in generator:
    print('%s/%s' % (container_name, blob.name))

print('Downloading cloud %s/%s to local %s' % (container_name, source_audio_name, source_audio_name))
blob_service.get_blob_to_path(container_name, source_audio_name, source_audio_name)
print('Downloading cloud %s/%s to local %s' % (container_name, source_video_name, source_video_name))
blob_service.get_blob_to_path(container_name, source_video_name, source_video_name)

print('smash away here - just copying video file for now')
copyfile(source_video_name, smashed_name)
blob_service.create_blob_from_path(container_name, smashed_name, smashed_name, content_settings=ContentSettings(content_type=smashed_content_type))
print('URL for public download is https://%s.blob.core.windows.net/%s/%s' % (storage_account_name, container_name, smashed_name))

print('Uploading local %s to cloud %s/%s' % (smashed_name, container_name, smashed_name))
smash_video_audio(source_video_name, source_audio_name, smashed_name)
blob_service.create_blob_from_path(container_name, smashed_name, smashed_name, content_settings=ContentSettings(content_type=smashed_content_type))
print('URL for public download is https://%s.blob.core.windows.net/%s/%s' % (storage_account_name, container_name, smashed_name))
