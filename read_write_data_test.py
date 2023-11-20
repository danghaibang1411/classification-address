import json
from pathlib import Path

from unidecode import unidecode


def extract_text_from_json(json_file):
    # Đọc file JSON
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Tạo mảng để lưu trữ các giá trị của khóa "text"
    text_array = []

    # Lấy giá trị từ khóa "text" và thêm vào mảng
    for item in data:
        text_value = item.get("text")
        if text_value:
            text_array.append(text_value)

    return text_array


def get_text_input():
    current_directory = Path(__file__).resolve().parent
    json_file_path = current_directory / "data" / "public_new.json"

    # Gọi hàm để lấy mảng giá trị từ khóa "text"
    text_values = extract_text_from_json(json_file_path)

    # Chuyển đổi các chuỗi trong text_values thành chữ không dấu
    text_values_without_diacritics = [unidecode(text).lower() for text in text_values]

    return text_values_without_diacritics


def export_to_json(file_path, text, province, district, ward):
    # Sample values for the variables
    text_value = text
    province_value = province
    district_value = district
    ward_value = ward

    # Load existing data from output.json (if any)
    try:
        with open(file_path, "r", encoding="utf-8") as existing_file:
            existing_data = json.load(existing_file)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        existing_data = []

    # Create a dictionary with the specified format
    new_data = {
        "text": text_value,
        "result": {
            "province": province_value,
            "district": district_value,
            "ward": ward_value,
        },
    }
    # Add the new data to the existing list
    existing_data.append(new_data)

    # Write the updated data back to output.json
    with open("output.json", "w", encoding="utf-8") as output_file:
        json.dump(existing_data, output_file, ensure_ascii=False, indent=2)

    print("New data has been added to output.json")


def parser(text):
    values_after_comma = []
    for text in text:
        # Tìm vị trí của dấu phẩy cuối cùng trong chuỗi
        last_comma_index = text.rfind(",")

        if last_comma_index != -1:  # Nếu có dấu phẩy trong chuỗi
            # Lấy phần tử phía sau dấu phẩy và loại bỏ khoảng trắng ở đầu chuỗi kết quả
            value_after_comma = text[last_comma_index + 1 :].lstrip()
            values_after_comma.append(value_after_comma)
        else:
            values_after_comma.append(
                text
            )  # Nếu không có dấu phẩy, thêm chuỗi rỗng vào mảng kết quả

    return values_after_comma


if __name__ == "__main__":
    # text = "TT Tân Bình Huyện Yên Sơn, Tuyên Quang"
    # province = "Tuyên Quang"
    # district = "Yên Sơn"
    # ward = "Tân Bình"
    # file_path = "C:/Users/trong.le-van/Downloads/Slides/Project/test.json"
    # export_to_json(file_path, text, province, district, ward)
    get_text_input()
