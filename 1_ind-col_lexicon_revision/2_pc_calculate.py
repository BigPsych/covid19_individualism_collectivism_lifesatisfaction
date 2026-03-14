import csv
from math import factorial


def calculate_pc(n, A):
    combinations = factorial(n) // (factorial(A) * factorial(n - A))
    pc = combinations * (0.5 ** n)
    return pc


def read_and_calculate_pcs(file_path, n, output_file_path):
    # 使用'utf-8'编码打开文件
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        fieldnames = csvreader.fieldnames  # 获取原始CSV文件的列名
        fieldnames.append('PC值')  # 添加新列名'PC值'

        # 打开输出文件，并写入列名
        with open(output_file_path, mode='w', newline='', encoding='utf-8') as outputfile:
            csvwriter = csv.DictWriter(outputfile, fieldnames=fieldnames)
            csvwriter.writeheader()

            for row in csvreader:
                item_number = row['条目编号']
                A = int(row['A'])
                pc = round(calculate_pc(n, A), 3)  # 保留三位小数

                # 创建一个新字典，包含原始行的数据和计算出的PC值（已格式化为字符串）
                new_row = row.copy()
                new_row['PC值'] = f"{pc:.3f}"  # 也可以直接使用str(pc)如果round已经足够

                # 写入输出文件
                csvwriter.writerow(new_row)


# 示例使用
input_file_path = 'D:\\毕业论文数据\\词典修订\\input.csv'  # 确保路径正确
output_file_path = 'D:\\毕业论文数据\\词典修订\\output_pc_values.csv'  # 输出文件路径
n = 6  # 专家总人数

# 计算每个条目的PC值并写入新文件
read_and_calculate_pcs(input_file_path, n, output_file_path)
