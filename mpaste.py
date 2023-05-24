import shutil
from threading import Thread

def copy_file(source_path, destination_path):
    shutil.copy(source_path, destination_path)

def mpcopy(destination_path:str, source_paths:list):
    threads = []
    for source_path in source_paths:
        t = Thread(target=copy_file, args=(source_path, destination_path))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def move_file(source_path, destination_path):
    shutil.move(source_path, destination_path)

def mpmove(destination_path:str, source_paths:list):
    threads = []
    for source_path in source_paths:
        t = Thread(target=move_file, args=(source_path, destination_path))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    destination_path = 'C:\\Users\\Dell\\Desktop\\tesktop\\aaaawwww\\dst'
    source_paths = ['C:\\Users\\Dell\\Desktop\\tesktop\\aaaawwww\\2.txt', 'C:\\Users\\Dell\\Desktop\\tesktop\\aaaawwww\\new.txt']

    main(destination_path, source_paths)
