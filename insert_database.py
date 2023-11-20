from unidecode import unidecode
from pathlib import Path


def readData():
    current_directory = Path(__file__).resolve().parent
    # Read words from the file
    file_path_province = current_directory / "data" / "list_province_verification.txt"
    with open(file_path_province, "r", encoding="utf-8") as file:
        province = file.read().splitlines()

    # Chuyen thanh chu thuong, bo dau tieng Viet
    list_province = [unidecode(word).lower() for word in province]

    file_path_district = current_directory / "data" / "list_district_verification.txt"
    with open(file_path_district, "r", encoding="utf-8") as file:
        district = file.read().splitlines()

    # Chuyen thanh chu thuong, bo dau tieng Viet
    list_district = [unidecode(word).lower() for word in district]

    file_path_ward = current_directory / "data" / "list_ward_verification.txt"
    with open(file_path_ward, "r", encoding="utf-8") as file:
        ward = file.read().splitlines()

    # Chuyen thanh chu thuong, bo dau tieng Viet
    list_ward = [unidecode(word).lower() for word in ward]

    return list_province, list_district, list_ward
