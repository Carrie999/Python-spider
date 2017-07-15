# -*- coding: utf-8 -*-
'''
对抓取来的网易云评论数据以一首歌七里香为例进行简单的可视化分析
'''
import requests
import matplotlib.dates as mdates
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 防止无法显示中文
import matplotlib.pyplot as plt
from datetime import datetime
import re
import time
import pandas as pd
import codecs
import jieba
from wordcloud import WordCloud
from os import path
import os

class NetCloudProcessor():
    # 读取评论文本数据，返回一个列表，列表的每个元素为一个字典，字典中包含用户id，评论内容等
    def read_comments_file(self):
        list_comments = [] # 评论数据列表
        with open('七里香.txt','r',encoding='utf-8') as f:
            comments_list = f.readlines() # 读取文本，按行读取，返回列表
            del comments_list[0] # 删除首个元素
            comments_list = list(set(comments_list)) # 去除重复数据
            count_ = -1 # 记录评论数
            for comment in comments_list:
                comment = comment.replace("\n","") # 去除末尾的换行符
                try:
                    if (re.search(re.compile(r'^\d+?'),comment)): # 如果以数字开头
                        comment_split = comment.split(' ',5) # 以空格分割(默认)
                        comment_dict = {}
                        comment_dict['userID'] = comment_split[0] # 用户ID
                        comment_dict['nickname'] = comment_split[1] # 用户昵称
                        comment_dict['avatarUrl'] = comment_split[2] # 用户头像地址
                        comment_dict['comment_time'] = int(comment_split[3])# 评论时间
                        comment_dict['likedCount'] = int(comment_split[4])# 点赞总数
                        comment_dict['comment_content'] = comment_split[5] # 评论内容
                        list_comments.append(comment_dict)
                        count_ += 1
                    else:
                        list_comments[count_]['comment_content'] += comment  # 将评论追加到上一个字典
                except Exception:
                    print(e)
        list_comments.sort(key= lambda x:x['comment_time'])
        print("去除重复之后有%d条评论!" % (count_+1))
        return (count_+1,list_comments) # 返回评论总数以及处理完的评论内容
    
    # 将网易云的时间戳转换为年-月-日的日期函数
    # 时间戳需要先除以1000才能得到真实的时间戳
    # format 为要转换的日期格式
    def from_timestamp_to_date(self,time_stamp,format):
        time_stamp = time_stamp*0.001
        real_date = time.strftime(format,time.localtime(time_stamp))
        return real_date

     # 统计相关数据写入文本文件
    def count_comments_info(self,comments_list,count_,song_name):
        x_date_Ymd = [] # 评论数按年月日进行统计
        x_likedCount = [] # 点赞总数分布
        for i in range(count_):
            time_stamp = comments_list[i]['comment_time'] # 时间戳
            real_date_Ymd = self.from_timestamp_to_date(time_stamp,'%Y-%m-%d') # 按年月日统计
            likedCount = comments_list[i]['likedCount'] # 点赞总数
            x_date_Ymd.append(real_date_Ymd)
            x_likedCount.append(likedCount)
        x_date_Ymd_no_repeat = []
        y_date_Ymd_count = []
        x_likedCount_no_repeat = []
        y_likedCount_count = []
        
        # 按年月日统计评论次数
        for date_ in x_date_Ymd:
            if date_ not in x_date_Ymd_no_repeat:
                x_date_Ymd_no_repeat.append(date_)
                y_date_Ymd_count.append(x_date_Ymd.count(date_))
        # 按被点赞数统计个数
        for likedCount in x_likedCount:
            if likedCount not in x_likedCount_no_repeat:
                x_likedCount_no_repeat.append(likedCount)
                y_likedCount_count.append(x_likedCount.count(likedCount))

        # 将统计的数据存入txt文件
        with open("%s/comments_num_by_Ymd.txt" % song_name,"w") as f:
            f.write("date_Ymd comments_num\n")
            for index,date_Ymd in enumerate(x_date_Ymd_no_repeat):
                f.write(x_date_Ymd_no_repeat[index] + " " + str(y_date_Ymd_count[index]) + "\n")
            print("成功写入comments_num_by_Ymd.txt!")
        with open("%s/likedCount.txt" % song_name,"w") as f:
            f.write("likedCount count_num\n")
            for index,likedCount in enumerate(x_likedCount_no_repeat):
                f.write(str(x_likedCount_no_repeat[index]) + " " + str(y_likedCount_count[index]) + "\n")
            print("成功写入likedCount.txt!")
    def get_comments_list(self,filename):
        with codecs.open(filename,"r",encoding='utf-8') as f:
            lists = f.readlines()
            comments_list = []
        for comment in lists:
            if(re.match(r"^\d.*",comment)):
                try:
                    comments_list.append(comment.split(" ",5)[5].replace("\n",""))
                except Exception:
                    pass
            else:
                comments_list.append(comment)
        return comments_list

    # 绘制图形展示歌曲评论以及点赞分布
    # plot_type:为 'plot' 绘制散点图   为 'bar' 绘制条形图
    # date_type 为日期类型
    # time_distance 为时间间隔(必填)例如:5D 表示5天,1M 表示一个月
    # min_liked_num 为绘图时的最小点赞数
    # max_liked_num 为绘图时的最大点赞数
    # min_date_Ymd 为最小日期(年-月-日形式)
    # max_date_Ymd 为最大日期(年-月-日形式)
    def plot_comments(self,song_name,settings):
        comment_type = settings['comment_type']
        date_type = settings['date_type']
        plot_type = settings['plot_type']
        bar_width = settings['bar_width']
        rotation = settings['rotation']
        time_distance = settings['time_distance']
        min_date_Ymd = settings['min_date_Ymd']
        max_date_Ymd = settings['max_date_Ymd']
        if(comment_type):  # 评论
            if(date_type == '%Y-%m-%d'):
                count_file_name = "%s/comments_num_by_Ymd.txt" % song_name
            else:
                count_file_name = "%s/comments_num_by_Ym.txt" % song_name
        else:
            count_file_name = "%s/likedCount.txt" % song_name
        with open(count_file_name,'r') as f:
            list_count = f.readlines()
            del list_count[0]
            if(comment_type): # 如果是评论
                x_date = []
                y_count = []
                for content in list_count:
                    content.replace("\n","")
                    res = content.split(' ')
                    if(date_type == '%Y-%m-%d'):
                        if(int("".join(res[0].split("-"))) >= int("".join(min_date_Ymd.split("-"))) and int("".join(res[0].split("-"))) <=  int("".join(max_date_Ymd.split("-")))):
                             x_date.append(res[0])
                             y_count.append(int(res[1]))
                    else:
                        if(int("".join(res[0].split("-"))) >= int("".join(min_date_Ym.split("-"))) and int("".join(res[0].split("-"))) <=  int("".join(max_date_Ym.split("-")))):
                             x_date.append(res[0])
                             y_count.append(int(res[1]))
            else: # 如果是点赞
                # 分为10-100,100-1000,1000-10000,10000以上这5个区间，由于绝大多数歌曲评论点赞数都在10赞一下
                # 超过99%，所以10赞以下暂时忽略
                x_labels = ['10-100','100-1000','1000-10000','10000以上']
                y_count = [0,0,0,0]
                for content in list_count:
                    content.replace("\n","")
                    res = content.split(' ')
                    if(int(res[0]) <= 100 and int(res[0]) >= 10):
                        y_count[0] += int(res[1])
                    elif(int(res[0]) <= 1000):
                        y_count[1] += int(res[1])
                    elif(int(res[0]) <= 10000):
                        y_count[2] += int(res[1])
                    else:
                        y_count[3] += int(res[1])
        # 如果是评论
        if(comment_type):
            type_text = "评论"
            x = [datetime.strptime(d, date_type).date() for d in x_date]
            # 配置横坐标为日期类型
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%s' % date_type))
            if(date_type == '%Y-%m-%d'):
                plt.gca().xaxis.set_major_locator(mdates.DayLocator())
            else:
                plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
            if(plot_type == 'plot'):
                plt.plot(x,y_count,color = settings['color'])
            elif(plot_type == 'bar'):
                plt.bar(x,y_count,width=bar_width,color = settings['color'])
            else:
                plt.scatter(x,y_count,color = settings['color'])
            #plt.gcf().autofmt_xdate(rotation=rotation)  # 自动旋转日期标记
            plt.title("网易云音乐歌曲《" + song_name + "》" + type_text + "数目分布")
            plt.xlabel("日期")
            plt.ylabel("数目")
             #设置x轴刻度显示时间格式
            #plt.gca().xaxis.set_major_formatter(mdate.DateFormatter('%y-%m-%d')) #x轴上的label格式为"年-月-日",其中年取后两位
            time_distance="3M"
            plt.xticks(pd.date_range(x[0],x[-1],freq="%s" % time_distance)) # 设置日期间隔
            plt.show()
        else:  # 如果是点赞
            x = y_count
            type_text = "点赞"
            pie_colors = settings['pie_colors']
            auto_pct = settings['auto_pct'] # 百分比保留几位小数
            expl = settings['expl'] # 每块距离圆心的距离
            plt.pie(x,labels = x_labels,explode=expl,colors = pie_colors,autopct = auto_pct)
            plt.title("网易云音乐歌曲《" + song_name + "》" + type_text + "数目分布")
            plt.legend(xlabels)
            plt.show()
        plt.close()

     # plot_comments 函数测试
    def plot_comments_test(self):
        song_name = "七里香"
        settings = {
            "comment_type":True,
            "date_type":"%Y-%m-%d",
            "plot_type":"plot",
            "bar_width":0.8,
            "rotation":20,
            "color":"purple",
            "pie_colors":["blue","red","coral","green","yellow"],
            "auto_pct":'%1.1f%%',
            "expl" :[0,0,0.1,0.3],   # 离开圆心的距离
            "time_distance":"3M",
            "min_date_Ymd":"2013-12-01",
            "max_date_Ymd":"2017-12-31",
            "min_date_Ym":"2013-01",
            "max_date_Ym":"2017-12"
        }
        self.plot_comments('七里香',settings)

    # 绘制词云
    # pic_path 为词云背景图片地址
    # singer_name 为 False 时，则读取歌曲评论文件，否则读取歌手热评文件
    # isFullComments = True 时，读取全部评论，否则只读取热评
    def draw_wordcloud(self,song_name,singer_name,pic_path = "JayZhou.jpg",isFullComments = True):
        singer_name= False
        if singer_name == False:
            if isFullComments == True:
                filename = "%s/%s.txt" % (song_name,song_name) # 全部评论
            else:
                filename = "%s/hotcomments.txt" % song_name # 一首歌的热评
        else:
            filename = "%s/hotcomments.txt" % singer_name
        comments_list = self.get_comments_list('七里香.txt')
        comments_text = "".join(comments_list)
        cut_text = " ".join(jieba.cut(comments_text)) # 将jieba分词得到的关键词用空格连接成为字符串
        d = path.dirname(__file__) # 当前文件文件夹所在目录
        color_mask = imread(pic_path) # 读取背景图片
        cloud = WordCloud(font_path=path.join(d,'simsun.ttc'),background_color='white',mask=color_mask,max_words=2000,max_font_size=40)
        word_cloud = cloud.generate(cut_text) # 产生词云
        if singer_name == False:
            name = song_name
        else:
            name = singer_name
        word_cloud.to_file("%s/%s.jpg" % (name,name))
        print(u"成功生成%s.jpg" % name)

if __name__ == '__main__':
    Processor = NetCloudProcessor()
    count_,list_comments = Processor.read_comments_file()
    Processor.count_comments_info(list_comments,count_,'七里香')
    Processor.plot_comments_test()
    Processor.draw_wordcloud('七里香','周杰伦')
    print('end')
