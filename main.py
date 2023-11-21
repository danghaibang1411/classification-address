import json
import re
import unicodedata

from LCSubStr import LCSubStr

import time

from read_write_data_test import export_to_json

with open('data/cities.json', 'r') as file:
    list_province = json.load(file)

with open('data/districts.json', 'r') as file:
    list_districts = json.load(file)

with open('data/wards.json', 'r') as file:
    list_wards = json.load(file)

with open('data/public_new.json', 'r') as file:
    list_data = json.load(file)

result_list_cities = []
result_list_districts = []
result_list_wards = []


def main():
    # Ghi lại thời điểm bắt đầu
    start_time = time.time()
    name_cities = ""
    name_districts = ""
    name_wards = ""
    data = ""
    open('data/output.json', 'w').close()
    data = []
    with open('data/output.json', "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=2)
    for line_data in list_data:
        try:
            name_cities = ""
            name_districts = ""
            name_wards = ""
            result_list_cities.clear()
            result_list_districts.clear()
            result_list_wards.clear()
            data = line_data.get("text")
            result_array = [token.strip() for token in re.split(r'[,\s]+', data)]
            result_array = all_lower(result_array)
            final = []
            for ss in result_array:
                final.append(re.sub('<.*?>', '', xoa_dau(ss).replace(".","")))
            i = len(final) - 1
            a = get_result_list_for_all(final[i], list_province)
            ret = len(a)
            text = final[i]
            b = []
            is_second_loop = False
            while i>0 and ret > 1:
                i = i-1
                text = final[i] + text
                b = get_result_list_for_all(text, list_province)
                ret = len(b)
            i = i - 1
            if len(b) > 0:
                a = b

            if len(a) > 0:
                if is_type_existed(final[i], a[0].get("type")):
                    i = i - 1
            max_ele = 0
            if len(a) > 0:
                name_cities = a[0].get('name')
            for ele in a:
                code = ele.get("code")
                counter = 0
                for list_dis in list_districts:
                    if list_dis.get("parent_code") == code and len(list_dis.get("parent_code")) == len(code):
                        result_list_districts.append(list_dis)
                        counter = counter + 1
                if counter >= max_ele:
                    max_ele = counter
            a = get_result_list_for_all(final[i], result_list_districts)
            ret = len(a)
            text = final[i]
            b = []
            is_second_loop = False
            while i > 0 and ret > 1:
                i = i - 1
                text = final[i] + text
                b = get_result_list_for_all(text, result_list_districts)
                ret = len(b)
                is_second_loop = True
            i = i-1
            if len(b) > 0:
                a = b
            if len(a) > 0:
                if is_type_existed(final[i], a[0].get("type")):
                    i = i - 1
            if len(a) > 0:
                name_districts = a[0].get('name_with_type')
            max_ele = 0
            for ele in a:
                code = ele.get("code")
                counter = 0
                for list_ward in list_wards:
                    if list_ward.get("parent_code") == code and len(list_ward.get("parent_code")) == len(code):
                        result_list_wards.append(list_ward)
                        counter = counter + 1
                if counter >= max_ele:
                    max_ele = counter
            a = get_result_list_for_all(final[i], result_list_wards)
            ret = len(a)
            text = final[i]
            b = []
            is_second_loop = False
            while i > 0 and ret > 1:
                i = i - 1
                text = final[i] + text
                b = get_result_list_for_all(text, result_list_wards)
                ret = len(b)
            if len(b) > 0:
                a = b
            if len(a) > 0:
                name_wards = a[0].get('name_with_type')
        finally:
            export_to_json('data/output.json', data, name_cities,name_districts,name_wards)



    # Ghi lại thời điểm kết thúc
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Thời gian chạy: {execution_time} giây")


def is_type_existed(text, data_type):
    if len(text) < 1:
        return False
    result = False
    min_same = min(len(text), len(data_type))
    same = LCSubStr(text, data_type, len(text), len(data_type))
    if (same/min_same) > 0.8:
        result = True
    return result


def get_result_list_for_all(text, list_data_add):
    if len(text) < 1:
        return []
    result = []
    for ref in list_data_add:
        cities = ref.get("slug").replace("-", "")
        min_same = min(len(text), len(cities))
        same = LCSubStr(text, cities, len(text), len(cities))
        if (same/min_same) >= 0.7:
            result.append(ref)
    return result


def get_result_list_second(text, list_data_add):
    result = []
    max = 0
    for ref in list_data_add:
        cities = ref.get("slug").replace("-", "")
        min_same = min(len(text), len(cities))
        same = LCSubStr(text, cities, len(text), len(cities))
        if (same/min_same) >= 0.7:
            result.append(ref)
    return result


def all_lower(my_list):
    return [x.lower() for x in my_list]


BANG_XOA_DAU = str.maketrans(
    "ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴáàảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ",
    "A"*17 + "D" + "E"*11 + "I"*5 + "O"*17 + "U"*11 + "Y"*5 + "a"*17 + "d" + "e"*11 + "i"*5 + "o"*17 + "u"*11 + "y"*5
)


def xoa_dau(txt: str) -> str:
    if not unicodedata.is_normalized("NFC", txt):
        txt = unicodedata.normalize("NFC", txt)
    return txt.translate(BANG_XOA_DAU)


# Check if this is the main program
if __name__ == "__main__":
    main()
