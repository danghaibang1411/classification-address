import re

from read_write_data_test import get_text_input


def split_strings(input_strings):
    output = []
    for input_string in input_strings:
        # Sử dụng biểu thức chính quy để tách chuỗi theo các dấu , . - và dấu space
        split_list = re.split(r"[,.\-\s]", input_string)

        # Loại bỏ các phần tử rỗng trong list
        split_list = [item for item in split_list if item]

        # Thêm list đã tách vào mảng output
        output.append(split_list)

    return output


# Mảng các chuỗi đầu vào
input_strings = get_text_input()

output = split_strings(input_strings)
print(output)
