import os
import re
import pandas as pd

# 专业认同度字典
professional_dict_file = "2_ind_lexicon.xlsx"
professional_dict_df = pd.read_excel(professional_dict_file, header=None, names=["words", "weight"])
professional_dict = dict(zip(professional_dict_df["words"], professional_dict_df["weight"]))

# 否定词字典
deny_words_file = "3_deny_words.xlsx"
deny_words_df = pd.read_excel(deny_words_file, header=None, names=["words", "weight"])
deny_words_dict = dict(zip(deny_words_df["words"], deny_words_df["weight"]))

# 程度词字典
degree_words_file = "3_degree_words.xlsx"
degree_words_df = pd.read_excel(degree_words_file, header=None, names=["words", "weight"])
degree_words_dict = dict(zip(degree_words_df["words"], degree_words_df["weight"]))

def cut_sentences(text):
    sentences = re.split(r'[。！？；、]', text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def cut_paragraphs(text):
    paragraphs = text.split('\n')  # 根据换行符分割段落
    return [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]


def calculate_professionalism(sentence, professional_dict, deny_words_dict, degree_words_dict):
    words = re.findall(r'\b\w+\b', sentence)
    professionalism_score = 0
    word_frequency = {}
    i = 0

    while i < len(words):
        word_lower = words[i].lower()

        if word_lower in word_frequency:
            word_frequency[word_lower] += 1
        else:
            word_frequency[word_lower] = 1

        if word_lower in professional_dict:
            if isinstance(professional_dict[word_lower], (int, float)) and isinstance(word_frequency[word_lower], int):
                professionalism_score += professional_dict[word_lower] * word_frequency[word_lower]

                # 考虑程度词
                if i + 1 < len(words) and words[i + 1].lower() in degree_words_dict and isinstance(
                        degree_words_dict[words[i + 1].lower()], (int, float)):
                    professionalism_score += degree_words_dict[words[i + 1].lower()] * word_frequency.get(
                        words[i + 1].lower(), 0)

                    # 考虑否定词
                    # 考虑否定词
                    if i + 2 < len(words) and words[i + 2].lower() in deny_words_dict and isinstance(
                            deny_words_dict[words[i + 2].lower()], (int, float)):
                        # 修改此部分以考虑否定词的奇偶性
                        negation_multiplier = -1 if (word_frequency.get(words[i + 2].lower(), 0) % 2 == 0) else 1
                        professionalism_score += negation_multiplier * deny_words_dict[
                            words[i + 2].lower()] * word_frequency.get(
                            words[i + 2].lower(), 0)


            else:
                print(f"Warning: Invalid weight or frequency for word '{word_lower}' in professional dictionary.")

        i += 1

    return professionalism_score


def calculate_paragraph_professionalism(paragraph, professional_dict, deny_words_dict, degree_words_dict):
    paragraph_professionalism = 0
    for sentence in cut_sentences(paragraph):
        sentence_professionalism = calculate_professionalism(sentence, professional_dict, deny_words_dict, degree_words_dict)
        paragraph_professionalism += sentence_professionalism
    return paragraph_professionalism

def process_txt_file(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    file_name = os.path.basename(txt_file_path)
    total_professionalism = 0

    for paragraph in cut_paragraphs(text):
        paragraph_professionalism = calculate_paragraph_professionalism(paragraph, professional_dict, deny_words_dict, degree_words_dict)
        total_professionalism += paragraph_professionalism

    return file_name, total_professionalism

if __name__ == "__main__":
    txt_folder = "分组完成最终版/2019Q1"  # 替换为包含txt文件的文件夹路径
    results = []

    for txt_file in os.listdir(txt_folder):
        if txt_file.endswith(".txt"):
            txt_file_path = os.path.join(txt_folder, txt_file)
            file_name, professionalism = process_txt_file(txt_file_path)
            results.append({"File Name": file_name, "Professionalism": professionalism})

    result_df = pd.DataFrame(results)
    result_df.to_csv("professionalism_results-1.csv", index=False)
    print("Results saved to professionalism_results.csv")
