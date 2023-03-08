from Compressor import Compressor

if __name__ == '__main__':
    path = "./donnees/alice.txt"
    compressor = Compressor(path)
    compressor.compress()
