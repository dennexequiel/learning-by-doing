## Markdown Generator (from CSV)

This Python script automates the creation of Markdown files for static websites using data from a CSV file. The script is designed to be flexible and adaptable to your specific content needs.

### Purpose

Simplify the process of generating multiple Markdown files with front matter, using the column headers in your CSV as the front matter keys. This streamlines content creation for static site generators like Hugo, Jekyll, or others that use Markdown with front matter.

### How to Use

1. **Prepare your CSV file:**
   * Organize your content data in a CSV file.
   * Ensure one column contains the desired file names for the Markdown files (e.g., "file_name").
   * The remaining column headers will become the front matter keys.

2. **Update the Constants (in the script):**
   * `CSV_FILE_PATH`: Set the path to your CSV file.
   * `OUTPUT_PATH`: Set the directory where the Markdown files should be created.
   * `FILE_NAME_COL_NAME`: Set the name of the column in your CSV that contains the file names.
   * `FRONT_MATTER_TYPE`: Choose either "toml" or "yaml" for your preferred front matter format.

3. **Run the Script:**
   * Make sure you have Python and the `pandas` library installed (`pip install pandas`).
   * Execute the script from your terminal:

     ```bash
     python markdown_generator.py 
     ```

### How It Works

1. **Reads CSV Data:**  The script reads your CSV file into a Pandas DataFrame.
2. **Creates Output Directory:** It creates the specified output directory if it doesn't exist.
3. **Generates Markdown Files:**
   * For each row in the CSV:
      * A new Markdown file is created with the name from the `FILE_NAME_COL_NAME` column.
      * The front matter is written in the chosen format (toml or yaml).
      * Each column header (except the file name column) becomes a key in the front matter.
      * The corresponding row values are written as the values for the front matter keys.
4. **Output:** The script informs you when the task is completed.

### Example CSV Structure

```
file_name,title,author,date,category
post1,My First Post,John Doe,2024-05-22,blog
post2,Another Exciting Article,Jane Smith,2024-05-21,news
```

### Additional Notes

* The script handles boolean values (True/False) and converts them to lowercase (true/false) for compatibility with some static site generators.
* Ensure the data in your CSV is properly formatted and escaped.
* If you encounter issues, double-check the CSV file path and column names.