# Efficient-Text-Compression-Using-Huffman-Coding
A Python-based program that compresses and decompresses text files using the Huffman Coding algorithm. It reduces file size without losing any data, making storage and transmission more efficient.

# HuffZip 
Efficient Text Compression & Decompression using Huffman Coding

##  Overview
In today’s world of growing digital communication, reducing the size of text files is more important than ever. **HuffZip** is a Python project that implements Huffman Coding to compress and decompress text data without any loss, reducing storage needs and improving transmission speeds.

## Features
- Compresses text files using Huffman Coding
- Decompresses files to their original content
- Efficient use of memory and space
- Reversible and lossless compression
- Command-line friendly interface

## How It Works

### Compression:
1. Reads text input
2. Calculates frequency of characters
3. Builds a **Huffman Tree**
4. Encodes characters into binary strings
5. Stores the binary-encoded data and encoding map

### Decompression:
1. Reads compressed binary data
2. Rebuilds the Huffman Tree using the saved map
3. Decodes binary strings back into original text

## Algorithm & Justification

- **Data Structure:** Huffman Tree (binary tree based on frequency priority)
- **Approach:**
  - Dictionary to count frequencies
  - Min-heap (priority queue) to build the Huffman Tree
  - Binary codes assigned from tree paths
  - Compression using encoded map
  - Decompression using reverse traversal

## Time & Space Complexity

| Function                  | Time       | Explanation                                      |
|--------------------------|------------|--------------------------------------------------|
| Calculate frequencies    | O(n)       | One pass through text of length n               |
| Priority queue enqueue   | O(log k)   | k = number of unique characters                  |
| Priority queue dequeue   | O(log k)   | Remove root and possibly shift elements          |

