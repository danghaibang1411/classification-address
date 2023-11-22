import json
import re
import unicodedata
import time

from LCSubStr import LCSubStr

from read_write_data_test import export_to_json

abbreviation_mapping = {
    'thành phố': 'tp',
    'tỉnh': 't',
    'huyện': 'h',
    'quận': 'q',
    'phuong': 'p',
    'thị trấn': 'tt',
    'a1': 'huyen',
    'a2': 'thanhpho',
    'a3': 'quan',
    'a4': 'tinh',
    'a5': 'thitran',
    'a9': 'thi tran',
    'a6': 'thi',
    'a7': 'tran',
    'a8': 'ho',
    'a10': 'thanh pho',
    'a11': 'phuong',
    'a12': 'tx',
    'a13': 'thi xa',
    'empty': '',
    'a14': 'khupho',
    'a15': 'khu',
    'a16': 'xa',
}

with open('data/cities.json', 'r', errors="ignore", encoding="utf-8") as file:
    list_province = json.load(file)

with open('data/districts.json', 'r', errors="ignore", encoding="utf-8") as file:
    list_districts = json.load(file)

with open('data/wards.json', 'r', errors="ignore", encoding="utf-8") as file:
    list_wards = json.load(file)

with open('data/public_new.json', 'r', errors="ignore", encoding="utf-8") as file:
    list_data = json.load(file)

result_list_cities = []
result_list_districts = []
result_list_wards = []


def main():
    all_record = 0
    correct_record = 0
    # Record starting time
    start_time = time.time()
    name_cities = ""
    name_districts = ""
    name_wards = ""
    data = ""
    open('data/output_correct.json', 'w').close()
    data = []
    regex_text = []
    with open('data/output_correct.json', "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=2)
    open('data/output_incorrect.json', 'w').close()
    data = []
    regex_text = []
    with open('data/output_incorrect.json', "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=2)
    for line_data in list_data:
        start_time_line = time.time()
        all_record = all_record + 1
        try:
            name_cities = ""
            name_districts = ""
            name_wards = ""
            result_list_cities.clear()
            result_list_districts.clear()
            result_list_wards.clear()
            data = line_data.get("text")
            # data = "Ấp 17 Long Trung, Cai Lậy, Tiền Giang"
            result_array = [token.strip() for token in
                            re.split(r'^[a-z]+|[A-Z][^A-Z]*(?<=[a-z])(?=[A-Z])|[,\s.]+', data)]
            result_array = all_lower(result_array)
            final = []
            for ss in result_array:
                final.append(re.sub('<.*?>', '', remove_regex(ss).replace(".", "")))
                for word in final:
                    if word in [abbr.lower() for abbr in abbreviation_mapping.values()] or (
                            not word.isdigit() and len(word) == 1):
                        final.remove(word)
            regex_text = str(final)
            i = len(final) - 1
            is_possible_miss = i < 4

            # Code for cities
            if i < 0:
                continue
            is_use_second_word, result_for_cities = get_result_list_for_cities(final[i], final[i - 1], list_province)
            temp_for_cities = result_for_cities
            ret = len(result_for_cities)
            if is_use_second_word:
                text = final[i - 1] + final[i]
                i = i - 1
            else:
                text = final[i]
            result_for_cities_again = []
            if i > 0 and ret > 10:
                i = i - 1
                text = final[i] + text
                result_for_cities_again = get_result_list_for_again(text, list_province)
                ret = len(result_for_cities_again)
            if len(result_for_cities_again) > 0:
                result_for_cities = result_for_cities_again

            if not is_possible_miss or len(result_for_cities) > 0:
                i = i - 1
            if i < 0:
                continue

            if len(result_for_cities) > 0:
                while final[i] in [abbr.lower() for abbr in abbreviation_mapping.values()]:
                    i = i - 1
                    if i < 0:
                        continue
                while final[i - 1] + final[i] in [abbr.lower() for abbr in abbreviation_mapping.values()]:
                    i = i - 2
                    if i < 0:
                        continue
                name_cities = result_for_cities[0].get('name')
            for each_name_cities in result_for_cities:
                code = each_name_cities.get("code")
                for list_dis in list_districts:
                    if list_dis.get("parent_code") == code and len(list_dis.get("parent_code")) == len(code):
                        result_list_districts.append(list_dis)

            if len(result_list_districts) == 0 and not is_possible_miss and len(temp_for_cities) > 0:
                for each_name_cities in temp_for_cities:
                    code = each_name_cities.get("code")
                    for list_dis in list_districts:
                        if list_dis.get("parent_code") == code and len(list_dis.get("parent_code")) == len(code):
                            result_list_districts.append(list_dis)
            elif len(result_list_districts) == 0 and is_possible_miss and len(result_for_cities) == 0:
                for list_dis in list_districts:
                    result_list_districts.append(list_dis)

            # Code for districts
            is_use_second_word, result_for_districts = get_result_list_for_cities(final[i], final[i - 1],
                                                                                  result_list_districts)
            temp_for_districts = result_for_districts
            ret = len(result_for_districts)
            if is_use_second_word:
                text = final[i - 1] + final[i]
                i = i - 1
                if i < 0:
                    continue
            else:
                text = final[i]
            result_for_districts_again = []
            if i > 0 and ret > 5:
                i = i - 1
                if i < 0:
                    continue
                text = final[i] + text
                result_for_districts_again = get_result_list_for_again(text, result_list_districts)
                ret = len(result_for_districts_again)
            if not is_possible_miss or len(result_for_districts) > 0:
                i = i - 1

            if len(result_for_districts_again) > 0:
                result_for_districts = result_for_districts_again

            if len(result_for_districts) > 0:
                while final[i] in [abbr.lower() for abbr in abbreviation_mapping.values()]:
                    i = i - 1
                    if i < 0:
                        continue
                while final[i - 1] + final[i] in [abbr.lower() for abbr in abbreviation_mapping.values()]:
                    i = i - 2
                    if i < 0:
                        continue
                name_districts = result_for_districts[0].get('name')
            for each_name_district in result_for_districts:
                code = each_name_district.get("code")
                for list_ward in list_wards:
                    if list_ward.get("parent_code") == code and len(list_ward.get("parent_code")) == len(code):
                        result_list_wards.append(list_ward)

            if len(result_list_wards) == 0 and not is_possible_miss and len(temp_for_districts) > 0:
                for each_name_district in temp_for_districts:
                    code = each_name_district.get("code")
                    for list_ward in list_wards:
                        if list_ward.get("parent_code") == code and len(list_ward.get("parent_code")) == len(code):
                            result_list_wards.append(list_ward)
            elif len(result_list_wards) == 0 and is_possible_miss and len(result_for_districts) == 0:
                if len(result_for_cities) > 0:
                    for each_name_cities in result_for_cities:
                        code = each_name_cities.get("code")
                        for list_dis in list_districts:
                            if list_dis.get("parent_code") == code and len(list_dis.get("parent_code")) == len(code):
                                code_wards = list_dis.get('code')
                                for list_ward in list_wards:
                                    if list_ward.get("parent_code") == code_wards and len(
                                            list_ward.get("parent_code")) == len(code_wards):
                                        result_list_wards.append(list_ward)

            # Code for wards
            is_use_second_word, result_for_wards = get_result_list_for_wards(final[i], final[i - 1], result_list_wards)
            ret = len(result_for_wards)
            if is_use_second_word:
                text = final[i - 1] + final[i]
                i = i - 1
            else:
                text = final[i]
            result_for_wards_again = []
            while i > 0 and ret > 1:
                i = i - 1
                text = final[i] + text
                result_for_wards_again = get_result_list_for_again(text, result_list_wards)
                ret = len(result_for_wards_again)
            i = i - 1
            if len(result_for_wards_again) > 0:
                result_for_wards = result_for_wards_again

            is_worst = False
            if len(result_for_wards) > 1:
                is_bool, result_for_wards = get_result_list_for_cities(text, "", result_list_wards)
                is_worst = True

            if len(result_for_wards) == 1 and not is_worst:
                arr = result_for_wards[0].get('path').split(', ')
                name_cities = arr[2]
                name_districts = arr[1]
                name_wards = arr[0]
            elif len(result_for_wards) > 0:
                name_wards = result_for_wards[0].get('name')

        finally:
            end_time_line = time.time()
            execution_time_line = end_time_line - start_time_line
            expected_result = line_data.get('result')
            if ((name_cities == expected_result.get('province') or expected_result.get('province') == "")
                    and (name_districts == expected_result.get('district') or expected_result.get('district') == "")
                    and (name_wards == expected_result.get('ward') or expected_result.get('ward') == "")):
                correct_record = correct_record + 1
                export_to_json('data/output_correct.json', data, regex_text, execution_time_line, expected_result,
                               name_cities, name_districts, name_wards)
            else:
                export_to_json('data/output_incorrect.json', data, regex_text, execution_time_line,
                               expected_result, name_cities, name_districts, name_wards)
    print("Classification correct: ", correct_record, "/", all_record)
    print("Percent correct = ", (correct_record / all_record) * 100)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total Time execution: {execution_time} seconds")


def get_scale(x):
    if x < 3:
        return 0.65
    elif 3 <= x < 5:
        return 0.7
    elif 5 <= x < 7:
        return 0.75
    elif 7 <= x:
        return 0.85
    else:
        return 0.7


def get_result_list_for_cities(first_word, second_word, list_data_add):
    is_use_second_word = False
    result = []
    result_one_word = []
    result_two_word = []
    if len(first_word) < 1 or len(first_word + second_word) < 1:
        return is_use_second_word, result
    for ref in list_data_add:
        cities = ref.get("slug").replace("-", "")
        min_same = min(len(first_word), len(cities))
        same = LCSubStr(first_word, cities, len(first_word), len(cities))
        if ((same / min_same)*0.7 + 0.3*(same/len(cities))) >= get_scale(min_same):
            result_one_word.append({'data': ref, 'weight': (same / min_same)*0.7 + 0.3*(same/len(cities))})

    double_word = second_word + first_word
    for ref in list_data_add:
        cities = ref.get("slug").replace("-", "")
        min_same = min(len(double_word), len(cities))
        same = LCSubStr(double_word, cities, len(double_word), len(cities))
        if ((same / min_same)*0.7 + 0.3*(same/len(cities))) >= get_scale(min_same):
            result_two_word.append({'data': ref, 'weight': (same / min_same)*0.7 + 0.3*(same/len(cities))})

    if 0 < len(result_two_word) < len(result_one_word) or (len(result_two_word) > 0 and len(result_one_word) == 0) \
            or (len(result_two_word) == len(result_one_word) and len(first_word) < 7) and len(result_one_word) > 0:
        is_use_second_word = True
        result.append(max(result_two_word, key=lambda x: x['weight']).get('data'))
    elif len(result_two_word) == 0 and len(result_one_word) == 0:
        is_use_second_word = False
        result = []
    else:
        is_use_second_word = False
        result.append(max(result_one_word, key=lambda x: x['weight']).get('data'))
    return is_use_second_word, result


def get_result_list_for_wards(first_word, second_word, list_data_add):
    is_use_second_word = False
    result = []
    result_one_word = []
    result_two_word = []
    if len(first_word) < 1 or len(first_word + second_word) < 1:
        return is_use_second_word, result
    for ref in list_data_add:
        cities = ref.get("slug").replace("-", "")
        min_same = min(len(first_word), len(cities))
        same = LCSubStr(first_word, cities, len(first_word), len(cities))
        if ((same / min_same)*0.7 + 0.3*(same/len(cities))) >= get_scale(min_same):
            result_one_word.append(ref)

    double_word = second_word + first_word
    for ref in list_data_add:
        cities = ref.get("slug").replace("-", "")
        min_same = min(len(double_word), len(cities))
        same = LCSubStr(double_word, cities, len(double_word), len(cities))
        if ((same / min_same)*0.7 + 0.3*(same/len(cities))) >= get_scale(min_same):
            result_two_word.append(ref)

    if 0 < len(result_two_word) < len(result_one_word) or (len(result_two_word) > 0 and len(result_one_word) == 0) \
            or (len(result_two_word) == len(result_one_word) and len(first_word) < 7) and len(result_one_word) > 0:
        is_use_second_word = True
        result = result_two_word
    elif len(result_two_word) == 0 and len(result_one_word) == 0:
        is_use_second_word = False
        result = []
    else:
        is_use_second_word = False
        result = result_one_word
    return is_use_second_word, result


def get_result_list_for_again(text, list_data_add):
    result = []
    for ref in list_data_add:
        cities = ref.get("slug").replace("-", "")
        min_same = min(len(text), len(cities))
        same = LCSubStr(text, cities, len(text), len(cities))
        if ((same / min_same)*0.7 + 0.3*(same/len(cities))) >= get_scale(min_same):
            result.append(ref)
    return result


def all_lower(my_list):
    return [x.lower() for x in my_list]


BANG_XOA_DAU = str.maketrans(
    "ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨ"
    "ỤƯỨỪỬỮỰÝỲỶỸỴáàảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệíìỉĩịóòỏõọôốồổ"
    "ỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ",
    "A" * 17 + "D" + "E" * 11 + "I" * 5 + "O" * 17 + "U" * 11 + "Y"
    * 5 + "a" * 17 + "d" + "e" * 11 + "i" * 5 + "o" * 17 + "u" * 11 + "y" * 5
)


def remove_regex(txt: str) -> str:
    if not unicodedata.is_normalized("NFC", txt):
        txt = unicodedata.normalize("NFC", txt)
    return txt.translate(BANG_XOA_DAU)


# Check if this is the main program
if __name__ == "__main__":
    main()
