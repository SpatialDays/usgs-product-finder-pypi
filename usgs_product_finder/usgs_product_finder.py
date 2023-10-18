import logging

# make a logger called "usgs_product_finder"
logger = logging.getLogger("usgs_product_finder")
logger.setLevel(logging.DEBUG)

import os
import pandas
import geopandas
import shapely
import requests


class UsgsProductFinder:

    def __init__(self, path_for_usgs_data: str = None, max_age_of_usgs_data: int = 1):
        """
        Initialize the UsgsProductFinder class.

        If the path_for_usgs_data parameter is filled, the library will download csv's and auxiliary files to that path.
        If the files already exist, they will not be downloaded again unless they are older than one day or the
        max_age_of_usgs_data parameter specified.

        :param path_for_usgs_data:
        :param max_age_of_usgs_data:
        """
        logger.debug("Initializing UsgsProductFinder")
        self.max_age_of_usgs_data = max_age_of_usgs_data
        if path_for_usgs_data is not None:
            if not os.path.exists(path_for_usgs_data):
                os.makedirs(path_for_usgs_data)
            self.path_for_usgs_data = path_for_usgs_data
        else:
            self.path_for_usgs_data = os.path.join(os.path.dirname(__file__), "data")
        self._load_in_wrs2()

    def _find_products_via_filtered_geodataframe(self, filtered_geodataframe: geopandas.GeoDataFrame, satellite: int):
        """
        Find products that intersect with a geodataframe.
        :param filtered_geodataframe: AOI-Filtered geodataframe
        :param satellite: Number for the satellite
        :return:
        """

        satellite_csv_path = ""
        if satellite in [4, 5]:
            satellite_csv_path = self._download_l4_l5_csv()
        elif satellite == 7:
            satellite_csv_path = self._download_l7_csv()
        elif satellite in [8, 9]:
            satellite_csv_path = self._download_l8_l9_csv()
        else:
            raise ValueError("Satellite must be 4, 5, 7, 8 or 9, other satellites from landsat \
                mission are not supported")

        logger.debug(f"As the satellite is {satellite}, the CSV file {satellite_csv_path} will be used")

    def find_products_via_wrs_row_and_path(self, wrs_row: int, wrs_path: int, satellite: int):
        """
        Find products that intersect with a WRS row and path.
        :param wrs_row:
        :param wrs_path:
        :param satellite:
        :return:
        """
        pass

    def find_products_via_shapely_object(self, shapely_multipolygon_object: shapely.geometry.multipolygon.MultiPolygon,
                                         satellite: int):
        """
        Find products that intersect with a shapely object.
        :param shapely_multipolygon_object:
        :param satellite:
        :return:
        """
        filtered_geodataframe: geopandas.GeoDataFrame = self.geodataframe_wrs2[
            self.geodataframe_wrs2.intersects(shapely_multipolygon_object)]
        return self._find_products_via_filtered_geodataframe(filtered_geodataframe, satellite)

    def find_products_via_wkt(self, wkt: str, satellite: int):
        """
        Find products that intersect with a wkt string.
        :param wkt:
        :param satellite:
        :return:
        """
        shapely_multipolygon_object = shapely.wkt.loads(wkt)
        return self.find_products_via_shapely_object(shapely_multipolygon_object, satellite)

    def _download_file(self, url: str) -> str:
        """
        Download a file from specified url into the path specified in the constructor.

        Skips the download if the file already exists and is newer than self.max_age_of_usgs_data.
        :param url: URL of a file to download
        :return:  Newly downloaded file's path
        """
        local_filepath = os.path.join(self.path_for_usgs_data, os.path.basename(url))
        logger.debug(f"Checking if {local_filepath} exists and is less than {self.max_age_of_usgs_data} days old")
        if not os.path.exists(local_filepath) or (
                (
                        os.path.exists(local_filepath)
                        and (
                                os.path.getmtime(local_filepath)
                                < (pandas.Timestamp.now() - pandas.Timedelta(
                            days=self.max_age_of_usgs_data)).timestamp()
                        )
                )
        ):
            logger.debug(f"Downloading CSV file from {url} into {local_filepath}")
            r = requests.get(url, stream=True)
            with open(local_filepath, "wb") as f:
                f.write(r.content)
            logger.debug("Download complete")
        else:
            logger.debug(
                "CSV file already exists and is less than 7 days old, not downloading again"
            )
        logger.debug(f"Returning {local_filepath}")
        return local_filepath

    def _download_l4_l5_csv(self) -> str:
        """
        Download the csv's for Landsat 4 and 5.
        :return: New file location
        """
        l4_l5_csv_url = "https://landsat.usgs.gov/landsat/metadata_service/bulk_metadata_files/LANDSAT_TM_C2_L2.csv.gz"
        return self._download_file(l4_l5_csv_url)

    def _download_l7_csv(self):
        """
        Download the csv for Landsat 7.
        :return: New file location
        """
        l7_url = "https://landsat.usgs.gov/landsat/metadata_service/bulk_metadata_files/LANDSAT_ETM_C2_L2.csv.gz"
        return self._download_file(l7_url)

    def _download_l8_l9_csv(self):
        """
        Download the csv's for Landsat 8 and 9.
        :return: New file location
        """
        l8_l9_url = "https://landsat.usgs.gov/landsat/metadata_service/bulk_metadata_files/LANDSAT_OT_C2_L2.csv.gz"
        return self._download_file(l8_l9_url)

    def _load_in_wrs2(self):
        """
        Load in the WRS2 shapefile
        :return:
        """
        wrs2_filepath = os.path.join(os.path.dirname(__file__), "files", "WRS2_descending.geojson")
        logger.debug(f"Loading in WRS2 shapefile from {wrs2_filepath}")
        self.geodataframe_wrs2 = geopandas.read_file(wrs2_filepath)
        logger.debug("WRS2 shapefile loaded in")
