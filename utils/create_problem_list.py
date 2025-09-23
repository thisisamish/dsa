file_path = "example.md"

start_num = 11
end_num = 27
titles = ["Binary Search", "Heap", "Stack and Queue 1", "Stack and Queue 2", "String 1", "String 2", "Binary Tree 1", "Binary Tree 2", "Binary Tree 3", "Binary Search Tree 1", "Binary Search Tree 2", "Binary Tree Misc", "Graph 1", "Graph 2", "DP 1", "DP 2", "Trie"]
problem_num = [8, 6, 7, 10, 6, 6, 12, 8, 7, 7, 8, 6, 12, 6, 7, 8, 7]
text_to_append = ""
if end_num - start_num + 1 != len(titles) or len(problem_num) != len(titles):
    raise RuntimeError("The number of headings, titles, and problem numbers don't match.")

for i in range(start_num, end_num + 1):
    text_to_append += "# Day " + str(i) + ": " + titles[i - start_num]
    text_to_append += "\n"
    for j in range(problem_num[i - start_num]):
        text_to_append += "\n" + str(j + 1) + ". LC "
    text_to_append += "\n\n"

try:
    with open(file_path, 'a') as file:
        file.write(text_to_append)
    print(f"Successfully appended to {file_path}")
except FileNotFoundError:
    print(f"The file {file_path} does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")
