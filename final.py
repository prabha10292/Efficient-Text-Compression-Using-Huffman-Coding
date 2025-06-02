#to run decode copy key from here
#  {'u': '0000', 'p': '0001', 'h': '0010', 'n': '0011', 'e': '010', ' ': '011', 'o': '100', 's': '101', 'l': '1100', 'r': '1101', 'f': '11100', 'g': '11101', 't': '11110', 'y': '11111'}
#file name
#10_compressed.bin

def new_node(char=None,freq=0,left=None,right=None): #o(1): constant time complexity, just creates and returns the dict.
    '''
    Defines a new node for the Huffman tree.
    
    char (str): The character to be stored in the node (None for internal nodes).
    freq (int): Frequency of the character.
    left (NoneType): Left child node (used during tree construction).
    right (NoneType): Right child node (used during tree construction).

    Returns:
    dict1 (dict): A dictionary representing a node in the format:
        { "char": char, "freq": freq, "left": left, "right": right }
    '''
    dict1={}
    dict1["char"]=char
    dict1["freq"]=freq  
    dict1["left"]=left
    dict1["right"]=right    
    return dict1

def calculate_frequencies(text): #o(n) iterates through each char once where n is the input text
    '''
    Calculates the frequency of each character in the input text and returns a list of nodes.

    Parameters:
    text (str): The text from the file.

    Returns:
    result (list): A list of dictionary representing frequency in the format:
        { "char": character, "freq": frequency, "left": None, "right": None }
    ''' 
    frequency={} 
    for char in text:
        if char in frequency:
            frequency[char]=frequency[char]+1
        else:
            frequency[char]=1  
    result=[] # adding frequency dictionary into the result list.
    for char,freq in frequency.items():
        result.append(new_node(char,freq))
    return result
#prabha
def priority_queueenqueue(priority_queue,item): # o(logn) a node might move from bottom to top (or the other way)
    '''
    Adds a new item to the priority queue (represented as a list of tuples) and places it
    in the correct position based on its priority.

    Parameters:
    priority_queue (list): A list of tuples where each tuple represents (frequency, count, node)
    item (tuple): The item to be inserted into the priority queue

    Returns: None
    ''' 
    priority_queue.append(item) #(leaf["freq"], count, leaf) 
    idx=len(priority_queue)-1
    #while the new node is smaller than its parent, swap them.
    while idx>0:
        parent=(idx-1)//2 #formula to find the parent of a node in a binary tree
        if priority_queue[idx]<priority_queue[parent]:
            priority_queue[idx],priority_queue[parent]=priority_queue[parent],priority_queue[idx]
            idx=parent
        else:
            break
#prabha
def priority_queuedequeue(priority_queue): #o(logn) 
    '''
    Removes and returns the item with the smallest frequency from the priority queue (represented as a list of 
    tuples). After removal, the queue is reordered to maintain correct priority positions. 

    Parameters:
    priority_queue (list): A list of tuples where each tuple is in the form (frequency, count, node).

    Returns:
    item (tuple): The item with the smallest frequency, removed from the priority queue.
    '''
    if not priority_queue:
        raise IndexError("pop from empty priority_queue")
    # Swap the first element with the last and remove the last (smallest element).
    priority_queue[0],priority_queue[-1]=priority_queue[-1],priority_queue[0]
    item=priority_queue.pop()
    idx=0
    n=len(priority_queue)
    # Ensure the new root element moves to its correct position.
    while True:
        left=2*idx+1
        right=2*idx+2
        smallest = idx
        if left < n and priority_queue[left] < priority_queue[smallest]:
            smallest = left
        if right < n and priority_queue[right] < priority_queue[smallest]:
            smallest = right
        if smallest != idx:
            priority_queue[idx], priority_queue[smallest] = priority_queue[smallest], priority_queue[idx]
            idx = smallest
        else:
            break
    return item
#divya
def build_huffman_tree(leaves): #o(nlogn) n for for loop and log n for enqueue dequeue
    '''
    Constructs the Huffman tree by repeatedly combining the two nodes with the lowest frequencies
    until only a single root node remains.

    Parameters:
    leaves (list): A list of dictionaries where each dictionary represents a character node with 
                   keys "char", "freq", "left", and "right"

    Returns:
    priority queue (dict): The root node of the final Huffman tree
    '''
    priority_queue=[]
    count=0  # Tie-breaker count in case frequencies are equal
    for leaf in leaves:
        # Push a tuple of (frequency, count, node) into the priority_queue
        priority_queueenqueue(priority_queue, (leaf["freq"], count, leaf))
        count += 1

    # Build the Huffman tree by merging the two smallest nodes repeatedly
    while len(priority_queue)>1:
        freq1, _, left = priority_queuedequeue(priority_queue)
        freq2, _, right = priority_queuedequeue(priority_queue)
        merged = new_node(None, freq1 + freq2, left, right)
        priority_queueenqueue(priority_queue, (merged["freq"], count, merged))
        count += 1

    # The remaining node is the root of the Huffman tree
    
    return priority_queue[0][2]
#divya
def generate_huffman_codes(node, prefix="", codes=None): #o(n) we are visiting each node in the tree once
    '''
    Generates unique code for aeach character

    Parameters:
    node (dict): A node in the Huffman tree, represented as a dictionary with keys "char", "freq", "left", and "right".
    prefix (str): The current binary prefix being built during the traversal (default is "")
    codes (dict):  A dictionary to store the final Huffman codes. If None, a new one is created.

    Returns:
    codes (dict): A dictionary mapping each character to its unique Huffman binary code.
    '''
    if codes is None:
        codes={}
    if node["char"] is not None: 
        codes[node["char"]]=prefix
    else:
        generate_huffman_codes(node["left"],  prefix + '0', codes)
        generate_huffman_codes(node["right"], prefix + '1', codes)
    return codes
#zaina
def huffman_encode_file(filename): #o(n)
    '''
    Reads a text file, builds the Huffman tree, generates codes for each character,
    and encodes the text into a binary bit string.

    Parameters:
    filename (str): The path to the input text file.

    Returns:
    text_in_file (str): The original text content from the file.
    bit_string (str): The final encoded binary string representing the compressed text.
    codes (dict): A dictionary mapping each character to its corresponding Huffman binary code.
    '''
    # 1) read and strip
    with open(filename, encoding='utf-8', errors='ignore') as f: #utf-8: text file can handle a wide variety of characters
        text_in_file=f.read().strip()

    # 2) build leaves and tree
    leaves=calculate_frequencies(text_in_file) #on

    root=build_huffman_tree(leaves) #nlogn

    # 3) generate codes
    codes=generate_huffman_codes(root) #on

    # 4) encode
    bit_string=''.join(codes[ch] for ch in text_in_file)

    return text_in_file,bit_string,codes
#zaina
def huffman_decode_file(encoded_file, codes): #o(n) 
    """
    Decodes a binary-encoded file using the provided Huffman codes by reconstructing the original text.

    Parameters:
    encoded_file (str): The path to the binary file containing the encoded data.
    codes (dict): A dictionary mapping characters to their Huffman binary codes.

    Returns:
    decoded_txt (str): The decoded original text.
    """
    reverse_codes = {}
    for k, v in codes.items():
        reverse_codes[v]=k

    with open(encoded_file, 'rb') as f:
        byte_data = f.read()

    bit_string = ''.join([format(byte, '08b') for byte in byte_data])

    current_code = ''
    decoded_text = ''
    for bit in bit_string:
        current_code += bit
        if current_code in reverse_codes:
            decoded_text += reverse_codes[current_code]
            current_code = ''

    return decoded_text
#zaina
def testcases_encode(check): 
    if check=="y":
        actual_text1, encoded_output1 ,all_the_values1=huffman_encode_file("testcase1.txt")
        if encoded_output1=="01101000001010111100000101010011111010110111101011010010101011110010110101100100111001100111110110001010111000101111100010110011010111100100111011111010000010111001110111011100100100111110110001010111100000111101101011111011100111110000001000010101010100011101111010011100100011111001010101111000010011010111111010101110010011110110001110110110111100001111010011011111001011110000100100011010101111100110000110001100010110101010111111011000101011110001100110101001110111110111101001110110111000010000110011011100101000111011100110000011011100011010010110001011100100100111110101100001110110011011100001010001110111101001110000111110100100000110011010101000010101100101111001101100100000111011011000":
            print("testcase1: OK")
        else:
            print("testcase1: does not match")
        actual_text2, encoded_output2 ,all_the_values2=huffman_encode_file("testcase2.txt")
        if encoded_output2=="101110011011110111101001010000":
            print("testcase2: OK")
            #{'s': '0000', 'g': '0001', 'l': '00100', 'z': '00101', ',': '00110', 'j': '00111', 'u': '01000', 'r': '01001', '-': '01010', 'v': '01011', 'i': '01100', 'd': '01101', 'm': '0111', 'o': '1000', 'e': '1001', ' ': '101', '.': '11000', 'I': '11001', 'n': '1101', '’': '11100', 't': '11101', 'a': '11110', 'y': '11111'}
        else:
            print("testcase2: does not match")
        actual_text3, encoded_output3 ,all_the_values3=huffman_encode_file("testcase3.txt")
        if encoded_output3=="01101101110000010100101111111111":
            print("testcase3: OK")
        else:
            print("testcase3: does not match")

#zaina
def testcases_decode(check):
    if check=="y" or check=="Y":
        c1={'a': '0000', 'h': '0001', 'g': '00100', 'u': '001010', 'b': '001011', 'w': '001100', 'z': '001101', ',': '001110', 'k': '001111', 'e': '010', '.': '011000', 'm': '011001', 'T': '0110100', 'y': '0110101', 'A': '0110110', 'j': '0110111', 'o': '0111', 's': '1000', 'n': '1001', 'f': '10100', 'd': '10101', 'i': '1011', 'r': '11000', 'l': '110010', 'c': '110011', 'p': '11010', 't': '11011', ' ': '111'}
        decoded_text1 = huffman_decode_file("testcase1_compressed.bin", c1)
        if decoded_text1=="The sun dipped below the horizon, painting the sky in shades of gold and pink. A soft breeze carried the scent of jasmine, whispering promises of a peaceful night.a":
            print("testcase1: OK")
        else:
            print("testcase1: does not match")
        


if __name__ == "__main__":
    value=input("Do you want to compress or decompress? (C/D):")
    if value=='C' or value=="c":
        filen = input("Enter the filename and write its extension(.txt/.bin) : ")
        actual_text, encoded_text, all_the_codes = huffman_encode_file(filen)
        print("Word:", actual_text)
        print("Huffman code:", encoded_text)
        print("Converted values:", all_the_codes)

        padded_bit_string = encoded_text + '0' * ((8 - len(encoded_text) % 8) % 8)  # pad to full bytes
        
        byte_array = bytearray() #initializing byte array to store the bytes

        for i in range(0, len(padded_bit_string), 8):
            byte = padded_bit_string[i:i+8]
            byte_array.append(int(byte, 2))

        filename=filen.replace('.txt', '_compressed.bin')
        with open(filename, "wb") as bin_file:
            bin_file.write(byte_array)

        print("\nEncoding complete. Compressed data written to 'compressed_output.bin'\n")
        
        check=input("Do you want to run testcases? (Y/N):")
        testcases_encode(check)
        
    if value=='D' or value=="d":
    # choice = input("Do you want to decode the file? (yes/no): ")
    # if choice.lower() == 'yes':
        c=eval(input("Enter the key for this compressed file: ")) #eval: turns the string into a dictionary
        filen = input("Enter the name of the compressed (.bin) file: ")
        decoded_text = huffman_decode_file(filen, c)
        print("\nDecoded text:", decoded_text)
        with open("decoded_output.txt", "w", encoding="utf-8") as out:
            out.write(decoded_text)
        print("\nDecoded text written to 'decoded_output.txt'")
        check=input("Do you want to run testcases? (Y/N):")
        testcases_decode(check)
