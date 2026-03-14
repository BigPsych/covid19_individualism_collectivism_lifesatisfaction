from http.cookies import SimpleCookie

import csv

def qc():
    # 使用集合来跟踪已经遇到的行（转换为字符串后）
    seen = set()
    output_rows = []

    # 读取原始CSV文件
    with open('评论数据-1.csv', 'r', encoding='utf-8') as f:
        cd = csv.reader(f)
        for row in cd:
            row_str = ''.join(row)  # 将整行转换为字符串作为唯一标识
            if row_str not in seen:
                seen.add(row_str)
                output_rows.append(row)  # 添加到输出行列表中

    # 将去重后的数据写入新的CSV文件
    with open('评论数据.csv', 'w', encoding='utf-8-sig', newline='') as fi:
        writer = csv.writer(fi)
        writer.writerows(output_rows)  # 写入所有去重后的行

    print(f"去重后的行数: {len(output_rows)}")

# 调用函数
qc()