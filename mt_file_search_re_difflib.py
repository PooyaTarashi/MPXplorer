import threading
import os
from os.path import join, isdir
import re
from difflib import get_close_matches as gcm
from mp_sort import mp_sort

# this variable will contain list of paths containing our file.
# we use multiple threads to update this variable
matches = []
# we should acquire this mutex when updating matches list
mutex = threading.Lock()


# every time we call file_search function, we should make a thread
# no mather it is a recursive call or it is an ordinary call
# we need to append all threads inside the function to a list and join them in a separate loop
def file_search(root: str, filename: str) -> None:
    """
    :param root: The path to search in
    :param filename: the filename to search for
    :return: None
    """
    child_threads = []
    for file in os.listdir(root):
        full_path = join(root, file)  # concatenates root with file
        
        if len(re.findall(filename, file)) != 0 or len(gcm(filename, file.split())) != 0:
        # if filename in file:
            mutex.acquire()  # mutex
            matches.append(full_path)
            mutex.release()  # mutex
        if isdir(full_path):
            t = threading.Thread(target=file_search, args=(full_path, filename))
            t.start()
            child_threads.append(t)
    
    for thread in child_threads:
        thread.join()


def search(key, path = 'C:\\Users\\Dell\\Desktop\\tesktop', sort_type = 'by_alpha'):
    t = threading.Thread(target=file_search, args=(path, key))
    t.start()
    t.join()
    # for m in matches:
        # print(m)
    # return merge_sort_threaded(matches)
    print(matches)
    print('***********************************')
    print(mp_sort(matches))
    # return matches
    return mp_sort(matches)


if __name__ == '__main__':
    search('main')