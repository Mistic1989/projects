"""Testing coordinates conversion."""

import pytest
import unittest

from coordinates.src.coordinates_package.coordinates import coordinates_wgs_to_lest, coordinates_lest_to_wgs


class TestCoordinates(unittest.TestCase):
    """Test coordinates conversion."""

    def test_coordinates_lest_to_wsg(self):
        """Test conversion from L-Est97 to WGS84."""
        assert coordinates_lest_to_wgs("6584338.66", "537735.47") == (59.395312, 24.664182),\
            "Expected value is (59.395312, 24.664182)"

    def test_coordinates_wsg_to_lest(self):
        """Test conversion from WGS84 to L-Est97."""
        assert coordinates_wgs_to_lest("59.395312", "24.664182") == (6584338.66, 537735.47),\
            "Expected value is (6584338.66, 537735.47)"


if __name__ == '__main__':
    unittest.main()
