#!/bin/bash

# 检查参数数量
if [ "$#" -ne 2 ]; then
    echo "用法: $0 <文件名> <搜索内容>"
    exit 1
fi

# 获取参数
filename=$1
search_content=$2

# 检查文件是否存在
if [ ! -f "$filename" ]; then
    echo "错误: 文件 '$filename' 不存在"
    exit 1
fi

# 创建输出文件名（在原文件名后加 .results）
output_file="${filename}.results"

# 执行搜索并输出结果
echo "搜索结果:"
echo "----------------------------------------"
grep -n "$search_content" "$filename" > "$output_file"
cat "$output_file"
echo "----------------------------------------"
echo "结果已保存到文件: $output_file"

exit 0
