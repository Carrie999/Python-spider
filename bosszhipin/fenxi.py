import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
import jieba
import jieba.analyse
from wordcloud import WordCloud


class BossZProcessor():
   
    def read_comments_file(self):
        bb = []  # 评论数据列表
        message = []
        jingyan = []
        xueli = []
        with open('zp.txt', 'r', encoding='utf-8') as f:
            bb = f.readlines()  # 读取文本，按行读取，返回列表
            i = 0
        for cc in bb:
            if (i == 2):
                message.append(cc)
            if ((i - 2) % 5 == 0):
                message.append(cc)
            i += 1
        q = 0
        # print(message)
        # print(len(message))
        for cc in message:
            jingyan.append(cc[20:24])
            xueli.append(cc[28:31].replace("'", ""))
        return (jingyan, xueli)

    def show(self, jingyan, xueli):
        counts1 = []
        counts2 = []
        shijian = ['不限', '1-3年', '3-5年', '5-10', '1年以内']
        xue = ['不限', '本科', '大专', '硕士']

        def shu():
            for s in shijian:
                counts1.append([s, jingyan.count(s)])
            counts1.sort(key=lambda v: v[1], reverse=True)
            return counts1

        def shu2():
            for x in xue:
                counts2.append([x, xueli.count(x)])
            counts2.sort(key=lambda v: v[1], reverse=True)
            # print(counts2)
            return counts2

        show1 = pd.DataFrame(shu(), columns=['shijian', 'cous'])
        show2 = pd.DataFrame(shu2(), columns=['xue', 'cous'])
        print(show1)
        print(show2)

        # 用matplotlib绘制直方图展示：

        # 设置中文子字体
        mpl.rcParams['font.sans-serif'] = ['SimHei']
       

        # 用matplotlib绘制直方图展示2：

        # 展示的学历和次数
        data2 = list(show2.cous)
        index = list(show2.xue)
        # 绘制直方图2
        plt.bar(range(len(data2)), data2, tick_label=index)
        plt.xlabel('学历')
        plt.ylabel('次数（最近3个月内）')
        plt.title('北京Python爬虫工程师要求学历分布图')
        plt.savefig('xueli.jpg')
        # plt.show()

        # 用jieba绘制直方图展示：
        with open('zz.txt', 'r', encoding='utf-8') as f:
            dd = f.readlines()  # 读取文本，按行读取，返回列表
        w = 0
        require = []
        for d in dd:
            w += 1
            if (w == 5):
               require.append(d)
            if ((w - 5) % 6 == 0):
               require.append(d)

        require = str(require)
        require = require.replace('requirement','').replace('岗位职责','').replace('任职要求','').replace('\\n','').replace('\\','')
        
        require = ''.join(require)
        print(require)
        # 获取关键词 最多的二十个
        cut_text = " ".join(jieba.cut(require))
        #d = path.dirname(__file__) # 当前文件文件夹所在目录
       
        cloud = WordCloud(font_path='ziti.ttf',background_color='white',max_words=2000,max_font_size=40)
        #cloud = WordCloud(font_path=path.join(d,'simsun.ttc'),background_color='white',,max_words=2000,max_font_size=40)
        word_cloud = cloud.generate(cut_text) # 产生词云
        word_cloud.to_file('require.jpg')
        print("成功生成require.jpg" )
        

if __name__ == '__main__':
    Processor = BossZProcessor()
    aa, bb = Processor.read_comments_file()
    Processor.show(aa, bb)
    print('end')
