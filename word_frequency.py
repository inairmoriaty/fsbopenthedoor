import jieba
from collections import Counter
import re

# === 基本设置 ===
file_path = r"/Users/inairmoriaty/Desktop/moriaty/moriaty/脑缠笔记本/COD/导出/seeking.txt"

# === AI痕迹模式 ===
ai_english_pattern = re.compile(r"\s[A-Z][a-zA-Z]+\s")  # 空格包裹英文
weird_quantifiers = ["一抹", "一缕", "一丝", "一阵", "一团"]
suspicious_targets = ["空气", "沉默", "房间", "耳语", "空间", "身影", "情绪", "光线"]

# === 读取文本 ===
with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

# 统计英文名格式错误
english_name_matches = ai_english_pattern.findall(text)

# 分词与词频统计
text_clean = re.sub(r"[^\u4e00-\u9fff]", "", text)
words = jieba.lcut(text_clean)
filtered = [w for w in words if len(w) > 1]

counter = Counter(filtered)

# === 输出 ===
print("\n🧠 Top 30 中文词频：\n")
for word, count in counter.most_common(30):
    print(f"{word:<10}: {count} 次")

# === 英文名异常标记 ===
print("\n🔍 疑似 AI 英文名格式异常（空格包裹）:")
for match in set(english_name_matches):
    print(f"出现场景：『{match.strip()}』 → 出现次数：{text.count(match)}")

# === 可疑量词搭配检测 ===
print("\n⚠️ 可疑量词搭配：")
for q in weird_quantifiers:
    for t in suspicious_targets:
        phrase = q + t
        if phrase in text:
            print(f"命中：『{phrase}』 → 出现次数：{text.count(phrase)}")

            # ==== 重复句子检测 ====
print("\n🌀 检测完全重复的句子（6字以上）:")

# 1. 将文本按句子分割（按中文句号、问号、叹号）
sentence_list = re.split(r"[。！？]", text)
sentence_list = [s.strip() for s in sentence_list if len(s.strip()) >= 6]  # 只保留6字以上的句子

# 2. 统计重复句子
sentence_counter = Counter(sentence_list)

# 3. 输出出现两次以上的句子
repeated_sentences = {sent: count for sent, count in sentence_counter.items() if count > 1}

if repeated_sentences:
    for sent, count in repeated_sentences.items():
        print(f"🔁【{sent}】 → 出现了 {count} 次")
else:
    print("✔️ 没有发现完全重复的句子")
