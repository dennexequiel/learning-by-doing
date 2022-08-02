## DOWNLOAD IMAGES FROM GOOGLE DRIVE

This simple application lets you download images from a Google Drive folder 
using a service.

## ARGS

This app requires four arguments:
1. Absolute path where logs will be created.
2. Path where credential.json will be located.
3. Absolute path where images will be downloaded.
4. Google Drive folder name that was shared to the service.

Sample run once build using pyinstaller:
.\download_images.exe "D:\logs" "D:\google-service.json" "D:\images" "test-lookup-folder"
