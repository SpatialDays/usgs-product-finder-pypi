import logging

# make a logger called "usgs_product_finder"
logger = logging.getLogger("usgs_product_finder")
# set its level to log all
logger.setLevel(logging.DEBUG)

import os
import pandas
import geopandas
import shapely


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
        pass

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

    def find_products_via_wkt(self, wkt: str, satellite: int):
        """
        Find products that intersect with a wkt string.
        :param wkt:
        :param satellite:
        :return:
        """
        pass

    def _download_file(self, url: str) -> str:
        """
        Download a file from a url into the path specified in the constructor.

        Skips the download if the file already exists and is newer than self.max_age_of_usgs_data.
        :param url: URL of a file to download
        :return:  Newly downloaded file's path
        """

    def _download_l4_l5_csv(self):
        """
        Download the csv's for Landsat 4 and 5.
        :return: New file location
        """
        pass

    def _download_l7_csv(self):
        """
        Download the csv for Landsat 7.
        :return: New file location
        """
        pass

    def _download_l8_l9_csv(self):
        """
        Download the csv's for Landsat 8 and 9.
        :return: New file location
        """
