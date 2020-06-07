from code.classes import district


if __name__ == "__main__":

    # Code testing for class Disctrict
    data_folder = "district-1"

    district = district.District(data_folder)
    for house in district.houses:
        print("pos:", house.position, "  maxout:", house.maxoutput)
    for battery in district.batteries:
        print("pos:", battery.position, "  capacity:", battery.capacity)