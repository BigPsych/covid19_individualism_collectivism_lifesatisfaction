
import os
import pandas as pd


def merge_csv_files(folder_path, output_file):
    # 初始化一个空的DataFrame用于存储合并结果
    merged_df = pd.DataFrame()

    # 获取文件夹中的所有csv文件
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # 遍历每个csv文件
    for file_name in csv_files:
        # 读取csv文件
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)

        # 提取年份和季度信息
        year_quarter = os.path.splitext(file_name)[0].split('-')[0]  # 去除扩展名并提取年份季度

        # 将年份季度信息作为新的一列添加到DataFrame中
        df['Year_Quarter'] = year_quarter

        # 如果是第一个文件，初始化列名
        if merged_df.empty:
            merged_df = df.set_index('Year_Quarter').T
        else:
            # 合并当前DataFrame到已有DataFrame
            current_df = df.set_index('Year_Quarter').T
            merged_df = pd.concat([merged_df, current_df], axis=1)

    # 重置索引以确保第一行为列名
    merged_df.reset_index(inplace=True)
    merged_df.columns = ['User_ID'] + list(merged_df.columns[1:])

    # 保存合并后的DataFrame为新的CSV文件
    merged_df.to_csv(output_file, index=False)
    print(f"合并完成，结果已保存到: {output_file}")


# 调用函数，传入你的文件夹路径和输出文件名
folder_path = r'D:\毕业论文数据\生活满意度分数计算\结果合并\1.输出结果'  # 替换为实际的文件夹路径
output_file = '合并结果.csv'  # 输出文件名
merge_csv_files(folder_path, output_file)