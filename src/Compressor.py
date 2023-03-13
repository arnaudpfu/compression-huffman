import os
from Node import Node
from utils import read_file


class Compressor:
    """
    Enable to compress a file using the Huffman algorithm.
    """

    def __init__(self, path: str):
        self.path: str = path
        self.alphabet_frequency: dict = {}
        self.encoding_table: dict = {}

    def __create_alphabet_frequency(self) -> dict:
        """
        Create a dictionary with the frequency of each character in the file.

        Returns:
            dict: The alphabet_frequency dictionary.
        """
        alphabet_frequency = {}

        # Open the file for reading
        with open(self.path, "r") as f:
            while True:
                char = f.read(1)
                if not char:
                    break
                alphabet_frequency[char] = alphabet_frequency.get(char, 0) + 1

        # sort the alphabet_frequency by character
        alphabet_frequency = dict(
            sorted(alphabet_frequency.items(), key=lambda item: item[0], reverse=False))

        # sort the alphabet_frequency by bigger frequency
        alphabet_frequency = dict(
            sorted(alphabet_frequency.items(), key=lambda item: item[1], reverse=False))
        return alphabet_frequency

    def __get_two_smallest_nodes(self, nodes: list) -> tuple:
        """
        Returns the two nodes with the lowest frequencies in a list of nodes.

        Args:
            nodes (list): All the nodes

        Returns:
            tuple: The two nodes with the lowest frequencies
        """
        min_node1 = nodes[0]
        min_node2 = nodes[1]
        if min_node2.frequency < min_node1.frequency:
            min_node1, min_node2 = min_node2, min_node1

        for node in nodes[2:]:
            if node.frequency < min_node1.frequency:
                min_node2 = min_node1
                min_node1 = node
            elif node.frequency < min_node2.frequency:
                min_node2 = node

        return min_node1, min_node2

    def __merge_nodes(self, nodes: list, min_node1: Node, min_node2: Node):
        """
        Merges Nodes to create a parent Node with a frequency equal to the sum
        of the frequency of the two Nodes that were merged.

        The left Node of the parent Node is the Node with the smaller frequency.
        The right Node of the parent Node is the Node with the larger frequency.

        The parent Node is appended to the list of Nodes.

        Args:
            nodes (list): List of Nodes
            min_node1 (Node): First node
            min_node2 (Node): Second Node
        """
        parent = Node(char=None, frequency=min_node1.frequency +
                      min_node2.frequency, left=min_node1, right=min_node2)
        min_node1.parent = parent
        min_node1.code = "0"
        min_node2.parent = parent
        min_node2.code = "1"

        nodes.remove(min_node1)
        nodes.remove(min_node2)
        nodes.append(parent)

    def __create_tree(self, alphabet_frequency: dict) -> Node:
        """
        Create a huffman tree from the given alphabet_frequency.
        It iterates over the alphabet_frequency and creates a node for each character.
        Then it combines the two lowest-frequency nodes until we have a single root node.

        Args:
            alphabet_frequency (dict): The alphabet_frequency dictionary.

        Returns:
            Node: The root node of the huffman tree.
        """
        nodes = []
        for char in alphabet_frequency:
            node = Node(char, frequency=alphabet_frequency[char])
            nodes.append(node)

        while len(nodes) > 1:
            # sort nodes by frequency
            nodes = sorted(nodes, key=lambda node: node.frequency)
            min_node1, min_node2 = self.__get_two_smallest_nodes(nodes)
            self.__merge_nodes(nodes, min_node1, min_node2)

        return nodes[0]

    def __build_encoding_table(self, node: Node, code: str):
        """
        Build the encoding table from the huffman tree.
        It associate each character with its encoding code of bits.

        Args:
            node (Node): The current node
            code (str): The code of bits
        """
        if node.char is not None:
            self.encoding_table[node.char] = code
        else:
            if node.left:
                self.__build_encoding_table(node.left, code + "0")
            if node.right:
                self.__build_encoding_table(node.right, code + "1")

    def __write_alphabet_frequency(self, output: str, alphabet_frequency: dict):
        """
        Write the encoding table to the output file.
        Write escape characters for special characters.
        For instance \n for newline.

        Args:
            output (str): The output file path
            alphabet_frequency (dict): The alphabet_frequency dictionary
        """
        with open(output, "w") as output_file:
            output_file.write(str(len(alphabet_frequency)) + "\n")
            for char in alphabet_frequency:
                output_file.write(repr(char)[1:-1] + " ")
                output_file.write(str(alphabet_frequency[char]) + "\n")

    def __encode(self, content: str) -> str:
        """
        Encode the content of the file in bits.

        Args:
            content (str): The content.

        Returns:
            str: The encoded content.
        """
        binary_code = ""
        for char in content:
            binary_code += self.encoding_table[char]

        return self.__pad_encoded_text(binary_code)

    def __pad_encoded_text(self, encoded_text):
        """
        Pad the encoded text to make it a multiple of 8.

        Args:
            encoded_text (str): String of bits 

        Returns:
            _type_: The padded string of bits
        """
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def __get_byte_array(self, text):
        """
        Convert a string of bits to a bytearray.

        Args:
            text (_type_): String of bits

        Returns:
            _type_: _description_
        """
        if (len(text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(text), 8):
            byte = text[i:i+8]
            b.append(int(byte, 2))
        return b

    def __write_compressed_file(self, output: str):
        """
        Write the compressed file to the output file.

        Args:
            output (str): Path to the compressed file
        """
        file_content = read_file(self.path)
        binary_code = self.__encode(file_content)

        with open(output, "wb") as f:
            f.write(self.__get_byte_array(binary_code))

    def __compute_compression_ratio(self, output: str) -> float:
        """
        Compute the compression ratio of the compressed file.

        Args:
            output (str): Path to the compressed file

        Returns:
            float: Compression ratio
        """
        uncompressed_size = os.path.getsize(self.path)
        compressed_size = os.path.getsize(output)
        ratio = 1 - (compressed_size / uncompressed_size)
        return round(ratio * 100, 2)

    def __compute_average_compressed_size_per_char(self, output: str) -> float:
        """
        Compute the average size of a character in the compressed file.

        Args:
            output (str): Path to the compressed file

        Returns:
            float: The average size (bit) of a character in the compressed file
        """
        compressed_size = os.path.getsize(output) * 8 # in bits
        number_of_chars = sum(self.alphabet_frequency.values())
        return round(compressed_size / number_of_chars, 2)

    def __get_output_path(self, entry_path: str) -> tuple:
        """
        Get the output path of the compressed file and the encoding table.

        Args:
            entry_path (str): Path to the file to compress

        Returns:
            tuple: Tuple containing the path to the compressed file and the encoding table
        """
        bin_path = entry_path.replace(".txt", "_comp.bin")
        freq_path = entry_path.replace(".txt", "_freq.txt")
        return (bin_path, freq_path)

    def compress(self):
        """
        Compress the file.
        """
        bin_path, freq_path = self.__get_output_path(self.path)
        self.alphabet_frequency = self.__create_alphabet_frequency()
        tree = self.__create_tree(self.alphabet_frequency)

        self.__build_encoding_table(tree, "")

        self.__write_alphabet_frequency(freq_path, self.alphabet_frequency)
        self.__write_compressed_file(bin_path)

        print(
            f"Compression ratio: {self.__compute_compression_ratio(bin_path)}%")
        print(
            f"Average size of a character after compression {self.__compute_average_compressed_size_per_char(bin_path)} bits")
