with open('name.txt', 'r') as f:
    names = list(set(name.strip() for name in f.readlines()))
with open('xiangsi.txt', 'r', encoding='gbk') as f:
    content = list(line.strip() for line in f.readlines())
def shu():
    novel = ''.join(content)
    counts = []
    for name in names:
        counts.append([name, novel.count(name)])
    # 将列表通过出现次数排序
    counts.sort(key=lambda v: v[1], reverse=True)
    return counts

import pandas as pd
show = pd.DataFrame(shu(), columns=['names', 'cous'])
print(show)

# 用matplotlib绘制直方图展示：
import matplotlib.pyplot as plt
from pylab import mpl
# 设置中文子字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
# 展示的姓名和数据
data = list(show.cous)
index = list(show.names)
# 绘制直方图
plt.bar(range(len(data)), data, tick_label=index)
plt.xlabel('出现的人物')
plt.ylabel('出现的次数')
plt.title('一寸相思人物出现频次图')
plt.savefig('xiangsi.jpg')
plt.show()

# 用jieba绘制直方图展示：
import jieba
import jieba.analyse
# 获取关键词 最多的二十个
tags = jieba.analyse.extract_tags(' '.join(content), topK=20, withWeight=True)
print('关键词:')
for k, v in tags:
    print('关键词：{}   权重：{:.3f}'.format(k, v))

# 利用关键词制作图云：
from wordcloud import WordCloud
txt = ''.join([v + ',' for v, x in tags])
wordcloud = WordCloud(background_color='white',font_path='ziti.ttf', max_font_size=40).generate(txt)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
wordcloud.to_file('ciyun.jpg')
