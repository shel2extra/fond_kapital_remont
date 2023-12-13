import os


files = os.listdir('orders/')
list_folder = []
for folder in files:
    files_sub_folders = os.listdir(f'orders/{folder}/')
    if files_sub_folders:
        list_folder.append(folder)
print(list_folder)