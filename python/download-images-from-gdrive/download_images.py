from os import path, mkdir
from shutil import rmtree
from sys import exit, argv
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


class LoggerService:

    def __init__(self, logs_path, log_file_name):
        self.__message = ""
        self.__is_success = False
        self.__logs_path = logs_path
        self.__log_file_path = logs_path + "\\" + log_file_name + ".txt"

    def write_log(self, is_success, message):
        self.__message = message
        self.__is_success = is_success
        time = datetime.now().time().replace(microsecond=0)

        if self.__is_success:
            self.open_log_file().write(f"{time} (Info): {self.__message} \n")
        else:
            self.open_log_file().write(f"{time} (Error): {self.__message} \n")
            exit()

    def create_logs_path(self):
        if not path.exists(self.__logs_path):
            mkdir(self.__logs_path)
        else:
            pass

    def open_log_file(self):
        return open(self.__log_file_path, "a+")

    def clear_log_file(self):
        self.open_log_file().truncate(0)

    def close_log_file(self):
        self.open_log_file().close()


class GoogleService:

    def __init__(self, api_name, api_version, scopes, key_file_location):
        self.__api_name = api_name
        self.__api_version = api_version
        self.__scopes = scopes
        self.__key_file_location = key_file_location

    def create_service(self):
        credentials = service_account.Credentials.from_service_account_file(self.__key_file_location)
        scoped_credentials = credentials.with_scopes(self.__scopes)
        service = build(self.__api_name, self.__api_version, credentials=scoped_credentials, static_discovery=False)

        return service


class GoogleDriveFilesService:

    def __init__(self, service):
        self.__service = service

    def get_first_folder_id_by_name(self, folder_lookup_name, page_size):
        results = self.__service.files().list(
            q=f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_lookup_name}'",
            pageSize=f"{page_size}",
            fields="nextPageToken, files(id, name)"
        ).execute()
        return results.get("files")[0].get("id")

    def get_folder_files_by__id(self, folder_id, page_size):
        results = self.__service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=f"{page_size}",
            fields="nextPageToken, files(id, name)"
        ).execute()
        return results.get("files", [])

    def get_media_file_by_id(self, file_id):
        return self.__service.files().get_media(fileId=file_id)


class ImageService:

    def __init__(self, abs_output_path):
        self.__abs_output_path = abs_output_path

    def make_directory(self):
        if path.exists(self.__abs_output_path):
            rmtree(self.__abs_output_path)
        mkdir(self.__abs_output_path)

    def download(self, request, file_name):
        file = open(self.__abs_output_path + "\\" + file_name, "wb")
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()


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
