import os
import hashlib
import sys
from tkinter import Label, Button, Tk, filedialog, messagebox

def file_hash(filepath):
    """计算文件的SHA-256哈希值"""
    if not os.path.exists(filepath):
        print(f"文件不存在: {filepath}")
        return None  # 返回None表示文件不存在，不进行哈希计算

    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def count_files(directory):
    """计算目录中文件的总数"""
    total_files = 0
    for root, dirs, files in os.walk(directory):
        total_files += len([f for f in files if f.lower().endswith(('.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.ts', '.mpg'))])
    return total_files

def find_and_delete_duplicates(directory, total_files):
    hashes = {}
    processed_files = 0  # 已处理的文件数

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(('.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.ts', '.mpg')):
                filepath = os.path.join(root, filename)
                try:
                    file_hash_value = file_hash(filepath)
                    if file_hash_value is None:
                        continue

                    if file_hash_value in hashes:
                        duplicate_path = hashes[file_hash_value]
                        print(f"Deleting duplicate file: {duplicate_path}")
                        os.remove(duplicate_path)
                        print(f"File {filepath} is a duplicate of {duplicate_path}")
                    else:
                        hashes[file_hash_value] = filepath

                except FileNotFoundError as e:
                    print(f"找不到文件: {e}")
                    continue

                processed_files += 1
                percentage = (processed_files / total_files) * 100
                print_progress_bar(percentage, total_files, processed_files)

    print("\n完成删除重复文件。")

def print_progress_bar(percentage, total_files, processed_files):
    """打印进度条"""
    bar_length = 50
    num_bars = int((percentage / 100) * bar_length)
    progress_bar_str = '█' * num_bars + '-' * (bar_length - num_bars)
    sys.stdout.write(f'\r[{progress_bar_str}>] {percentage:.2f}% ({processed_files}/{total_files})')
    sys.stdout.flush()

def center_window(root):
    width = root.winfo_reqwidth()
    height = root.winfo_reqheight()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

def choose_directory():
    root = Tk()
    root.title("选择目录")
    root.geometry("800x600")
    
    # 使窗口居中
    center_window(root)
    
    Label(root, text="请确保备份重要数据:").pack(pady=10)

    def open_directory():
        directory = filedialog.askdirectory()
        if directory:
            root.destroy()  # 关闭选择目录的窗口
            total_files = count_files(directory)  # 计算总文件数
            find_and_delete_duplicates(directory, total_files)  # 开始查找和删除重复文件

    Button(root, text="选择重复文件目录", command=open_directory).pack(side="left", padx=10)
    Button(root, text="取消", command=root.destroy).pack(side="right", padx=10)

    root.mainloop()

choose_directory()