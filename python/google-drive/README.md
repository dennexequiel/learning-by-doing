## Download Images from Google Drive

This Python script automates the download of images from a specified Google Drive folder using the Google Drive API. The script includes logging for tracking progress and errors.

### Features

* **Automated Download:**  Easily download all images from a designated Google Drive folder.
* **Customizable:**  Specify the folder name, log location, and credentials file.
* **Error Handling:**  Includes try-except blocks to catch potential errors during the download process.
* **Logging:**  Logs success and error messages for troubleshooting and monitoring.

### Requirements

* **Python:** Make sure you have Python installed on your system.
* **Google Drive API:** Enable the Google Drive API and obtain your credentials file (google-service.json).
* **Google API Client Library:** Install the Google API Client Library for Python:

   ```bash
   pip install google-api-python-client
   ```

### How to Use

1. **Place Credentials File:** Place your `google-service.json` credentials file in the location specified by the second argument when running the script.
2. **Share Folder with Service Account:** Share the desired Google Drive folder with the email address associated with your service account in the credentials file.
3. **Run the Script:** Execute the script from your terminal, providing the following arguments:

   ```bash
   python image_downloader.py <logs_path> <credentials_path> <output_path> <folder_name>
   ```

   * `<logs_path>`: Absolute path where log files will be created.
   * `<credentials_path>`: Absolute path to your credentials file.
   * `<output_path>`: Absolute path where images will be downloaded.
   * `<folder_name>`: Name of the Google Drive folder to download from.

### Additional Notes

* The script currently downloads the first 50 files within the specified folder. You can adjust the `page_size` parameters in the code to download more files.
* Review the log files in the specified `logs_path` for details on successful downloads and any errors encountered.
