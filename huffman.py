from collections import Counter
import heapq

class HufTree:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

if __name__ == "__main__":
    source = open('source.txt', mode='rb')
    bytes = source.read()
    source.close()
    bytes_freq = dict(Counter(bytes))

    tree = [ HufTree(char, freq) for char, freq in bytes_freq.items() ]
    heapq.heapify(tree) # доп эффективность

    while len(tree) > 1:
        left = heapq.heappop(tree)
        right = heapq.heappop(tree)
        
        merge = HufTree(None, left.freq + right.freq)
        merge.left = left
        merge.right = right
        
        heapq.heappush(tree, merge)
    
    root = tree[0] # корень

    # print(bytes_freq)