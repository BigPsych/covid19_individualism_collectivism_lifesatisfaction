import os
import joblib
import jieba
import jieba.analyse
import numpy as np
import pandas as pd
# 大连理工情感词典，21个情感分类
# 快乐(PA)，安心(PE)，尊敬(PD)，赞扬(PH)，相信(PG)，喜爱(PB)，祝愿(PK)
# 愤怒(NA)，悲伤(NB)，失望(NJ)，疚(NH)，思(PF)，慌(NI)，恐惧(NC)
# 羞(NG)，烦闷(NE)，憎恶(ND)，贬责(NN)，妒忌(NK)，怀疑(NL)，惊奇(PC)
# 微博客基本情绪词库，5个分类
# 快乐(MH), 悲伤(MS), 愤怒(MA), 恐惧(MD), 厌恶(ME)
# 对不同词类的标识进行定义
affect_col_list = ['PA', 'PE', 'PD', 'PH', 'PG', 'PB', 'PK',
                   'NA', 'NB', 'NJ', 'NH', 'PF', 'NI', 'NC',
                   'NG', 'NE', 'ND', 'NN', 'NK', 'NL', 'PC',
                   'MH', 'MS', 'MA', 'MD', 'ME',
                   'P', 'N', 'Ne']


# 载入情感词典
def load_affect_dict(filepath):
    m_affectdict = []
    for m_col in affect_col_list:
        m_col = []
        m_affectdict.append(m_col)

    for m_line in open(filepath, 'r', encoding='utf-8').readlines():  # 打开并读取文件
    #for m_line in open(filepath, 'r', encoding='latin-1', errors='ignore').readlines():  # 打开并读取文件
        m_line = m_line.strip()  # 删除数据中的换行符
        kwd = m_line.split('\t')[0].strip()
        col = m_line.split('\t')[1].strip()
        m_affectdict[affect_col_list.index(col)].append(kwd)

    return m_affectdict  # 返回文件


# 创建停用词list
def load_stopwords(filepath):
    m_stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return m_stopwords


# 特征提取
def feature_extraction(x_buf):
    item = []

    # 精确切分
    m_tags = jieba.cut(x_buf, cut_all=False)

    key_wrds = []
    # 去停词
    for s in m_tags:
        s = s.strip()
        # 删除停词
        if (len(s) > 0) and (s not in stopwords):
            key_wrds.append(s)

    # 切词后词的总数
    cnt_tags = len(key_wrds)
    # print(cnt_tags)

    # 提取每个情感词类的词频比率
    idx = 0
    for g_col in affect_col_list:

        # 切词后，其中包含情感词的总数
        affect_cnt = 0

        # 统计每个词类下关键词出现的总频次affect_cnt
        for i in range(cnt_tags):
            s = key_wrds[i]
            if (s in affect_dict[idx]):
                affect_cnt += 1

        # 计算比率
        r_affect = 0.0
        if (cnt_tags > 0):
            r_affect = affect_cnt / cnt_tags

        item.append(r_affect)

        idx += 1

    return item


# 载入停词表
stop_word_file = '调用文件/stop_words_cn.txt'
stopwords = load_stopwords(stop_word_file)

# 载入情感词典
affect_dict_file = '调用文件/dict-affect.txt'
affect_dict = load_affect_dict(affect_dict_file)

# 载入情感词典中的词做为自定义词典
jieba.load_userdict('调用文件/jiebaload_affect_dict.txt')

apply_kws = []
wz_list = []
# 特征提取、赋值
testdirs = '分组完成最终版/2023Q4/'
testsubdir = os.listdir(testdirs)

for f in testsubdir:  # 遍历文件夹下的文件
    print(testdirs + f)
    #buf = open(testdirs + f, 'r', encoding='utf-8').read()  # 打开并读取文件
    buf = open(testdirs + f, 'r', encoding='utf-8', errors='replace').read()  #读取有错时使用这行替换跑一下试试
    item = feature_extraction(buf)
    # print(item)
    apply_kws.append(item)
    wz_list.append(f)
    #np.save('primary_school_users.npy', wz_list)
    #np.save('primary_school_affect_dic.npy', apply_kws)
    np.save('out/2023Q4_users.npy', wz_list)
    np.save('out/2023Q4_affect_dic.npy', apply_kws)

# 训练模型
mod_file = 'out/swls.mod'
clf = joblib.load(mod_file)  # 保存并读取文件
result = clf.predict(apply_kws)  # 结果预测
print(result)  # 输出结果

#导出词频
wz_cipin = np.load('out/2023Q4_affect_dic.npy')#加载词频np文件
pd.DataFrame(wz_cipin).to_csv('out/2023Q4_affect_dic.csv')#导出词频np文件为csv文件

# 导出文件
wz_predict_file = 'out/2023Q4-预测结果.csv'  # 定义文件名
dstfp = open(wz_predict_file, 'w', encoding='utf_8_sig')  # 打开文件
dstfp.write('生活满意度/n')  # 新建文件
dstfp.flush()  # 强制把数据输出，清空缓冲区
idx = 0  # 从0开始
for f in wz_list:
    dstfp.write(f)
    dstfp.write(',')  # 写入逗号
    dstfp.write(str(result[idx]))
    dstfp.write('\n')  # 写入换行符
    dstfp.flush()  # 强制把数据输出，清空缓冲区
    idx += 1

dstfp.close()  # 关闭文件

print('已完成生活满意度预测!')  # 输出结果
