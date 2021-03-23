from utils.FileUtils import FileUtils
from scripts.get_location_from_zipcode import get_location


if __name__ == "__main__":
    zipcodes_df = FileUtils.read_single_file("yellowpages_zip_codes.xlsx")
    cities = []
    print(len(zipcodes_df["zipcodes"]))
    FileUtils.delete_duplicates(zipcodes_df)
    print(len(zipcodes_df["zipcodes"]))
    # for zipcode in zipcodes_df["zipcodes"]:
    #     city = get_location(zipcode).get("city", "")
    #     cities.append(city)

    # zipcodes_df["city"] = cities
    # zipcodes_df.to_csv("zips_with_cities.csv")
