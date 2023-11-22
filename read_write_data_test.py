import json
import re
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


def export_to_json(file_path, text,regex_text, exec_time, expected_result, province, district, ward):
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
        "raw_text": text_value,
        "reg_text": regex_text,
        "exec_time": exec_time,
        "expected_result": expected_result,
        "actual_result": {
            "province": province_value,
            "district": district_value,
            "ward": ward_value,
        },
    }
    # Add the new data to the existing list
    existing_data.append(new_data)

    # Write the updated data back
    with open(file_path, "w", encoding="utf-8") as output_file:
        json.dump(existing_data, output_file, ensure_ascii=False, indent=2)


def parser(text):
    result_array = [token.strip() for token in re.split(r'[,\s]+', text)]
    return result_array
