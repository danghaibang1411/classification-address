from unidecode import unidecode


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


def insert_word(root, word):
    current_node = root
    for char in word:
        if char not in current_node.children:
            current_node.children[char] = TrieNode()
        current_node = current_node.children[char]
    current_node.is_end_of_word = True


def print_trie(root, prefix=""):
    if root.is_end_of_word:
        print(prefix)

    for char, child_node in root.children.items():
        print_trie(child_node, prefix + char)


def search_word(root, word):
    current_node = root

    for char in word:
        if char not in current_node.children:
            return False

        current_node = current_node.children[char]

    # Check if the last node is marked as end_of_word
    return current_node.is_end_of_word
