from os import path, mkdir
from shutil import rmtree
from sys import exit, argv
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# LoggerService class for logging information and errors
class LoggerService:

    def __init__(self, logs_path, log_file_name):
        self.__message = ""
        self.__is_success = False
        self.__logs_path = logs_path
        self.__log_file_path = logs_path + "\\" + log_file_name + ".txt"

    # Method to write logs
    def write_log(self, is_success, message):
        self.__message = message
        self.__is_success = is_success
        time = datetime.now().time().replace(microsecond=0)

        if self.__is_success:
            self.open_log_file().write(f"{time} (Info): {self.__message} \n")
        else:
            self.open_log_file().write(f"{time} (Error): {self.__message} \n")
            exit()

    # Method to create logs directory
    def create_logs_path(self):
        if not path.exists(self.__logs_path):
            mkdir(self.__logs_path)
        else:
            pass

    # Method to open log file
    def open_log_file(self):
        return open(self.__log_file_path, "a+")

    # Method to clear log file
    def clear_log_file(self):
        self.open_log_file().truncate(0)

    # Method to close log file
    def close_log_file(self):
        self.open_log_file().close()

# GoogleService class for creating Google API service
class GoogleService:

    def __init__(self, api_name, api_version, scopes, key_file_location):
        self.__api_name = api_name
        self.__api_version = api_version
        self.__scopes = scopes
        self.__key_file_location = key_file_location

    # Method to create Google API service
    def create_service(self):
        credentials = service_account.Credentials.from_service_account_file(self.__key_file_location)
        scoped_credentials = credentials.with_scopes(self.__scopes)
        service = build(self.__api_name, self.__api_version, credentials=scoped_credentials, static_discovery=False)

        return service

# GoogleDriveFilesService class for handling Google Drive files
class GoogleDriveFilesService:

    def __init__(self, service):
        self.__service = service

    # Method to get the first folder ID by name
    def get_first_folder_id_by_name(self, folder_lookup_name, page_size):
        results = self.__service.files().list(
            q=f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_lookup_name}'",
            pageSize=f"{page_size}",
            fields="nextPageToken, files(id, name)"
        ).execute()
        return results.get("files")[0].get("id")

    # Method to get files in a folder by folder ID
    def get_folder_files_by__id(self, folder_id, page_size):
        results = self.__service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=f"{page_size}",
            fields="nextPageToken, files(id, name)"
        ).execute()
        return results.get("files", [])

    # Method to get a media file by file ID
    def get_media_file_by_id(self, file_id):
        return self.__service.files().get_media(fileId=file_id)

# ImageService class for handling image files
class ImageService:

    def __init__(self, abs_output_path):
        self.__abs_output_path = abs_output_path

    # Method to create directory for images
    def make_directory(self):
        if path.exists(self.__abs_output_path):
            rmtree(self.__abs_output_path)
        mkdir(self.__abs_output_path)

    # Method to download image
    def download(self, request, file_name):
        file = open(self.__abs_output_path + "\\" + file_name, "wb")
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

# Main function
if __name__ == "__main__":

    API_NAME = "drive"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    LOGS_PATH = argv[1]
    JSON_CREDENTIALS_LOCATION = argv[2]
    ABS_OUTPUT_PATH = argv[3]
    FOLDER_NAME_LOOKUP = argv[4]

    logger_service = LoggerService(logs_path=LOGS_PATH, log_file_name=FOLDER_NAME_LOOKUP)
    logger_service.create_logs_path()
    logger_service.clear_log_file()
    logger_service.write_log(is_success=True, message="App started.")

    try:
        google_service = GoogleService(
            api_name=API_NAME,
            api_version=API_VERSION,
            scopes=SCOPES,
            key_file_location=JSON_CREDENTIALS_LOCATION
        ).create_service()

        google_drive_files_service = GoogleDriveFilesService(google_service)
        image_service = ImageService(ABS_OUTPUT_PATH)
        image_service.make_directory()

        logger_service.write_log(
            is_success=True,
            message=f"Connection successful, instances started, & output path: '{ABS_OUTPUT_PATH}' was created."
        )

        try:
            folder_id = google_drive_files_service.get_first_folder_id_by_name(FOLDER_NAME_LOOKUP, 5)

            files = google_drive_files_service.get_folder_files_by__id(folder_id, 50)

            if not files:
                logger_service.write_log(is_success=False, message="No files were found!")
            else:
                for index in range(0, len(files)):
                    file_id = files[index].get("id")
                    file_name = files[index].get("name")
                    file_request = google_drive_files_service.get_media_file_by_id(file_id)
                    image_service.download(request=file_request, file_name=file_name)
                    logger_service.write_log(is_success=True, message=f"Image: {file_name} was created.")
        except Exception as e:
            logger_service.write_log(is_success=False, message=f"{e}")

        logger_service.write_log(is_success=True, message="Download Complete.")
        logger_service.close_log_file()
    except HttpError as error:
        logger_service.write_log(False, error)