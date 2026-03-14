import os
import joblib
import jieba
import jieba.analyse
from sklearn.linear_model import LassoCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 情感分类标签
affect_col_list = [
    'PA', 'PE', 'PD', 'PH', 'PG', 'PB', 'PK',
    'NA', 'NB', 'NJ', 'NH', 'PF', 'NI', 'NC',
    'NG', 'NE', 'ND', 'NN', 'NK', 'NL', 'PC',
    'MH', 'MS', 'MA', 'MD', 'ME',
    'P', 'N', 'Ne'
]


# 读入数据文件，返回得分、性别和自我描述
def read_swls_file(fname):
    with open(fname, 'r', encoding='UTF-8-sig') as fr_swls:
        x_swls_strs = fr_swls.readlines()
    fr_score = int(x_swls_strs[0].strip('\n'))

    return fr_score


# 载入情感词典
def load_affect_dict(filepath):
    m_affectdict = {col: [] for col in affect_col_list}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            kwd, col = line.strip().split('\t')
            m_affectdict[col].append(kwd)
    return m_affectdict


# 创建停用词列表
def load_stopwords(filepath):
    return [line.strip() for line in open(filepath, 'r', encoding='utf-8')]


# 特征提取
def feature_extraction(x_buf, stopwords, affect_dict):
    m_tags = jieba.cut(x_buf, cut_all=False)
    key_wrds = [s.strip() for s in m_tags if s.strip() and s not in stopwords]
    cnt_tags = len(key_wrds)

    features = []
    for col in affect_col_list:
        affect_cnt = sum(1 for word in key_wrds if word in affect_dict[col])
        r_affect = affect_cnt / cnt_tags if cnt_tags > 0 else 0.0
        features.append(r_affect)

    return features


# 载入停用词表和情感词典
stop_word_file = 'stop_words_cn.txt'
affect_dict_file = 'dict-affect.txt'
stopwords = load_stopwords(stop_word_file)
affect_dict = load_affect_dict(affect_dict_file)

# 载入情感词典中的词作为自定义词典（如果需要）
# jieba.load_userdict('jiebaload_affect_dict.txt')  # 这一步通常用于加载不在默认词典中的词

# 加载数据并提取特征
x_kws, y_score = [], []
dirs = '数据/'
for f in os.listdir(dirs):
    score, gender, desc = read_swls_file(os.path.join(dirs, f))
    features = feature_extraction(desc, stopwords, affect_dict)
    x_kws.append(features)
    y_score.append((score - 5) / 30)

# 划分训练集和测试集（可选，但为了验证模型性能通常建议这样做）
X_train, X_test, y_train, y_test = train_test_split(x_kws, y_score, test_size=0.2, random_state=42)

# 训练模型并保存
models = {
    'LassoCV': LassoCV(),
    'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
    'DecisionTree': DecisionTreeRegressor(random_state=42),
    'SVR': SVR(kernel='linear', C=1.0, epsilon=0.1)
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'{name} MSE: {mse}')

    # 保存模型
    mod_file = f'{name}.mod'
    joblib.dump(model, mod_file)
    print(f'{name} model saved!')

# 注意：在实际应用中，你可能不需要打印每个模型的MSE或保存每个模型，
# 这取决于你的具体需求和资源限制。上面的代码主要是为了演示如何训练和保存多个模型。
