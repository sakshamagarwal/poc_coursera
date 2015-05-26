"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result_list = []
    for	element in line:
        if element!=0:
            result_list.append(element)
    size = len(result_list)
    for	idx in range(len(result_list),len(line)):
        result_list.append(0)
    result_list.append(0)
    for idx in range(0,size):
        if (result_list[idx]==result_list[idx+1]):
            result_list[idx] += result_list[idx+1]
            for jdx in range(idx+1,size):
                result_list[jdx] = result_list[jdx+1]
    result_list.pop()
    return result_list

print merge([8, 16, 16, 8])