import os
#from sklearn import svm
#from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, LassoCV, LassoLarsCV
import joblib
import jieba
import jieba.analyse

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


# 读入一个数据文件，返回得分、性别和自我描述
def read_swls_file(fname):
    fr_swls = open(fname, 'r', encoding='UTF-8-sig')
    x_swls_strs = fr_swls.readlines()

    fr_score = int(x_swls_strs[0].strip('\n'))
    fr_gender = x_swls_strs[1].strip('\n')

    fr_desc = ''
    # 删除得分和性别行
    x_swls_strs.pop(0)
    x_swls_strs.pop(0)
    for swls_str in x_swls_strs:
        fr_desc += swls_str.strip().strip('\n') + ' '
    fr_swls.close()
    return fr_score, fr_gender, fr_desc


# 载入情感词典
def load_affect_dict(filepath):
    m_affectdict = []
    for m_col in affect_col_list:
        m_col = []
        m_affectdict.append(m_col)

    for m_line in open(filepath, 'r', encoding='utf-8').readlines():  # 打开并读取文件
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

# 特征提取并训练模型
x_kws = []
y_score = []

dirs = 'swls/'
subdir = os.listdir(dirs)  # 定义返回指定文件下的列表
for f in subdir:  # 遍历文件夹下的文件
    print('.', end='')  # 末尾不换行，加.
    x_score, x_gender, x_desc = read_swls_file(dirs + f)
    item = feature_extraction(x_desc)  # 特征提取
    x_kws.append(item)
    y_score.append((x_score - 5) / 30)

# 训练模型
clf_lasso = LassoCV()
clf_lasso.fit(x_kws, y_score)

# 保存训练得到的模型
mod_file = 'out/swls.mod'
joblib.dump(clf_lasso, mod_file)
print('SWLS model saved!')  # 输出结果
