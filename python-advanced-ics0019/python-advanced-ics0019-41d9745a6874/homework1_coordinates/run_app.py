"""User interface for converting coordinates from L-Est97 to WGS84 and vice versa."""

from coordinates_package import coordinates

while True:
    print("CONVERT COORDINATES FROM L-Est97 TO WGS84 OR WGS84 TO L-Est97\n"
          "-------------------------------------------------------------")
    user_input = input("If you would like to convert coordinates from L-Est97 to WGS84, enter 1\n"
                       "If you would like to convert coordinates from WGS84 to L-Est97, enter 2\n"
                       "If you would like to exit program, type exit\n")

    result = tuple()
    if user_input == "1":
        print("Please enter the X and Y axis:\n")
        latitude = input("X: ")
        longitude = input("Y: ")
        print("Coordinates converted from L-Est97 to WGS84 are:\n")
        result = coordinates.coordinates_lest_to_wgs(latitude, longitude)
    if user_input == "2":
        print("Please enter the coordinates (latitude/longitude):\n")
        latitude = input("Latitude: ")
        longitude = input("Longitude: ")
        print("Coordinates converted from WGS84 to L-Est97 are:\n")
        result = coordinates.coordinates_wgs_to_lest(latitude, longitude)
    if user_input == "exit":
        print("Program terminated")
        break
    if user_input not in ["1", "2", "exit"]:
        print("Please enter the correct input!\n")
        continue

    latitude = result[0]
    longitude = result[1]
    if type(result[0]) == float('inf'):
        latitude = "Out of bounds"
    if type(result[1]) == float('inf'):
        longitude = "Out of bounds"
    print(f"{latitude} | {longitude}\n"
          "Conversion completed!\n\n"
          "-------------------------------------------------------------")
