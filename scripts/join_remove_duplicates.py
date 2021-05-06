import zipfile

from utils.FileUtils import FileUtils

if __name__ == "__main__":
    # Get the zip files
    paths_zipcodes_downloaded = FileUtils.get_files_in_folder("data/download/", extensions=["zip"])
    # Read files in parallel
    phones_urls_df = FileUtils.read(paths_zipcodes_downloaded, concat=True)
    print(phones_urls_df.head())
    # # Delete duplicates
    # FileUtils.delete_duplicates(phones_urls_df, subset=["phone"])
    # Save results