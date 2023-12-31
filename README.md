# usgs-product-finder-pypi

Simple utility to find USGS Landsat products by AOI provided as WKT or shapely object.

## Installation

```bash
pip3 install usgs-product-finder
```

## Usage

```python
from usgs_product_finder import UsgsProductFinder

# Initialize finder
usgs_product_finder = UsgsProductFinder()
# You can also specify a path where to download the products and
# maximum age of the files in days

# usgs_product_finder = UsgsProductFinder(
#                       path_for_usgs_data="/home/user/usgs-product-finder", 
#                       max_age_of_usgs_data=7)


# define aoi in wkt
aoi_wkt = """MULTIPOLYGON (((-175 -12,-179.99999 -12,-179.99999 -20,-175 -20,-175 -12)), ((175 -12,179.99999
    -12,179.99999 -20,175 -20,175 -12))) """
    
# find products
pandas_obj = usgs_product_finder.find_products_via_wkt(aoi_wkt, 8, minimal_output=False)
list_of_dicts = usgs_product_finder.find_products_via_wkt(aoi_wkt, 8, minimal_output=True)


```
