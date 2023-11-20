from trie import TrieNode, insert_word, print_trie, search_word
from insert_database import *

from unidecode import unidecode
import time


def main():
    # Ghi lại thời điểm bắt đầu
    start_time = time.time()

    list_province, list_district, list_ward = readData()
    # Create a Trie and insert reversed words
    root_province = TrieNode()
    for word in list_province:
        insert_word(root_province, word)

    root_district = TrieNode()
    for word in list_district:
        insert_word(root_district, word)

    root_ward = TrieNode()
    for word in list_ward:
        insert_word(root_ward, word)

    search_word_result = search_word(root_province, "tien giang")
    print(f"Is a valid word? {search_word_result}")

    # Ghi lại thời điểm kết thúc
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Thời gian chạy: {execution_time} giây")


# Check if this is the main program
if __name__ == "__main__":
    main()
