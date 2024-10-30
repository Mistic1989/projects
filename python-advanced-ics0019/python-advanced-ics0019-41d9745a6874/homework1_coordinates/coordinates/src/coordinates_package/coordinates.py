"""Convert coordinates L-Est97 and WGS84."""

from pyproj import Transformer


def coordinates_lest_to_wgs(x: str, y: str) -> tuple:
    """Calculate coordinates from L-Est97 to WGS84."""
    transformer = Transformer.from_crs("EPSG:3301", "EPSG:4326")
    transformed = transformer.transform(x, y)
    return round(transformed[0], 6), round(transformed[1], 6)


def coordinates_wgs_to_lest(latitude: str, longitude: str) -> tuple:
    """Calculate coordinates from WGS84 to L-Est97."""
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3301")
    transformed = transformer.transform(latitude, longitude)
    return round(transformed[0], 2), round(transformed[1], 2)


if __name__ == '__main__':
    print(coordinates_wgs_to_lest("59.395312", "24.664182"))
    print(coordinates_lest_to_wgs("6584338.66", "537735.47"))
