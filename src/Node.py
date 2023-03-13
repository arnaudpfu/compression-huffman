class Node:
    """
    Node class for Huffman Tree
    """

    def __init__(self, char=None, frequency=0, left=None, right=None, parent=None):
        self.char: str | None = char
        self.frequency: int = frequency
        self.left: Node | None = left
        self.right: Node | None = right
        self.parent: Node | None = parent
        self.code: str = ""

    def __lt__(self, other):
        return self.frequency < other.frequency
