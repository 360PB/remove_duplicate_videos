# remove_duplicate_videos
用于删除指定目录及其子目录下的所有重复视频文件

注意：
运行此脚本将删除文件，所以在运行之前请确保备份重要数据。

此脚本仅适用于视频文件，如果你需要检查其他类型的文件，请修改endswith中的文件扩展名列表。

if filename.lower().endswith(('.mp4','.avi','.mov','.wmv','.flv','.mkv','.ts','.mpg'))
