import win32file
from datetime import datetime
import os
import re

# 获取当前目录下的所有文件
def get_file_list(dir, file_list):
    new_dir = dir
    if os.path.isfile(dir):
        file_list.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            new_dir = os.path.join(dir, s)
            get_file_list(new_dir, file_list)
    return file_list

# 获取文件名标出的创建时间
def get_file_time(file_name):
    try:
        # re.findall() https://blog.csdn.net/weixin_44799217/article/details/122069533
        time_str = re.findall(r'IMG\d{14}', file_name)
        if time_str:
            time_str = time_str[0]
            time_str = time_str[:8] + ' ' + time_str[8:]
            time_str = time_str[:4] + '-' + time_str[4:6] + '-' + time_str[6:]
            time_tuple = datetime.strptime(time_str, '%Y-%m-%d %H%M%S')
            return time_tuple
        
        time_str = re.findall(r'\d{4}-\d{2}-\d{2}\s\d{6}', file_name)
        if time_str:
            time_str = time_str[0]
            time_str = time_str.replace('-', '')
            time_str = time_str[:4] + '-' + time_str[4:6] + '-' + time_str[6:]
            time_tuple = datetime.strptime(time_str, '%Y-%m-%d %H%M%S')
            return time_tuple

        time_str = re.findall(r'\d{8}_\d{6}', file_name)
        if time_str:
            time_str = time_str[0]
            time_str = time_str.replace('_', ' ')
            time_str = time_str[:4] + '-' + time_str[4:6] + '-' + time_str[6:]
            time_tuple = datetime.strptime(time_str, '%Y-%m-%d %H%M%S')
            return time_tuple
        else:
            return None
    except:
        return None

# 设置文件的创建时间
def set_file_time(file_name, time_tuple):
    # hadle是文件句柄，win32file.GENERIC_WRITE是写入权限，win32file.OPEN_EXISTING是打开已存在的文件
    handle = win32file.CreateFile(
    file_name,
    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
    0,
    None,
    win32file.OPEN_EXISTING,
    0,
    0,)
    win32file.SetFileTime(handle, time_tuple, time_tuple, time_tuple)  # 注意这里的顺序，访问时间在前，修改时间在后
    win32file.CloseHandle(handle)

def main():
    file_list = get_file_list(os.getcwd(), [])
    for file_name in file_list:
        time_tuple = get_file_time(file_name)
        if time_tuple:
            set_file_time(file_name, time_tuple)

if __name__ == '__main__':
    main()
