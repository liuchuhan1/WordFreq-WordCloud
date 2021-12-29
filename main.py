#encoding='utf-8'
import os
import sys

import jieba as jieba
import matplotlib.pyplot as plt  # 图像展示库
from wordcloud import WordCloud  # 图云库'''

print(
    '''
*********************使用前请仔细阅读该文档********************
本程序仅用于学习交流，并完全免费，切勿用于商业用途。分
词部分采用结巴分词库，绘制部分采用图云库。
使用时需提供三个文档，分别命名为“武汉过滤版.txt”、
“武汉旅游词库.txt”、“stopwords”，其内容分别为
过滤广告等内容的网络爬取内容、自定义的词汇、自定义的
停用词。均使用UTF-8编码，其中stopwords请使用原文件
以记事本打开直接修改内容，改完后不要更改其编码方式，
直接点保存，否则将出现GBK、UTF-8的未知编码错误。
建议开启新词发现功能。
分词方式分为3种
精确：普通模式，较为常用，即将文字分割成多个词。
全模式：会对相临字词进行排列组合，例如黄鹤楼，使用该模
式会出现黄鹤和黄鹤楼两个词语。
搜索引擎模式：会在精确模式分词的基础上，将长词再次进行
切分。（未知，不建议使用）
本程序会输出一个文件“武汉过滤版词频.txt”包含词语和对
应频率，输出默认保存频数前50的词语。同时输出绘制的云图。
Powered by liuchuhan  
Email：liuchuhanhan@gmail.com
***********************************************************
'''
)

stopwords1 = []  # 停用词数组定义
for word in open((os.path.join(os.path.dirname(sys.executable), 'stopwords')), 'r',encoding='utf-8'):  # 加载停用词
    stopwords1.append(word.strip())
article = open(os.path.join(os.path.dirname(sys.executable), '武汉过滤版.txt'),encoding='utf-8').read()  # 加载游记
print("读取游记文件"+os.path.join(os.path.dirname(sys.executable), '武汉过滤版.txt'))

if len(article) < 50:
    x3 = input("你的游记太短了，无法分析,按任意键关闭窗口")
    sys.exit()

jieba.load_userdict(os.path.join(os.path.dirname(sys.executable), '武汉旅游词库.txt'))  # 加载自定义词库
print("读取自定义词库"+os.path.join(os.path.dirname(sys.executable), '武汉旅游词库.txt'))
ifopen=input(
    '''
****************************************
1、开启（默认）
2、不开启
****************************************
请选择是否开启新词查找:'''
           )

if ifopen == "2":
        x1=False
else:
        print("使用默认配置开启新词查找！")
        x1=True

mode=input('''
****************************************
1、精确模式（默认）
2、全模式
3、搜索引擎模式
****************************************
请输入分词模式对应数字:''')


def modeguess2(o,mo):
    if mo == "2":
        x2 = jieba.cut(article, cut_all=True, HMM=o)
    elif mo == "3":
        x2 = jieba.cut_for_search (article, HMM=o)
    else:
        x2 = jieba.cut(article, cut_all=False,HMM=o)
        print("将使用默认配置精确模式！")
    return x2


words = modeguess2(x1,mode)  # 进行分词
word_freq = {}  # 定义词汇频率数组
object_list = []  # 定义分词词表数组
for word in words:
    if len(word) > 1 and not (word.isdigit()):  # 定义长度超过1并且不是数字的词才有效
        if word not in stopwords1:  # 检验是否在停用词表
            object_list.append(word)  # 向分词词表数组添加元素
            if word in word_freq:  # 判断词语是否出现
                word_freq[word] += 1  # 每出现一次加一
            else:
                word_freq[word] = 1  # 只出现一次就为1

freq_word = []  # 定义词频数组


for word, freq in word_freq.items():
    freq_word.append((word, freq))  # 将词语和频率添加到词频数组中
freq_word.sort(key=lambda x: x[1], reverse=True)  # 整理数组的顺序按从多到少排列
len_freq_word = len(freq_word)


def inputnum(m, lenfw):
    if m == 0:
        if lenfw < 50:
             x = lenfw
        else:
             print("您输错了三次，默认使用50！")
             x = 50                                      # 默认显示排名前50的词组
        return x
    else:
        max_number = input("请输入想保留频数排名前多少位:")
        if len(max_number) == 0:
            print("请输入内容！")
            m = m - 1
            return inputnum(m, lenfw)

        elif not (max_number.isdigit()):
            print("请输入数字！")
            m = m - 1
            return inputnum(m, lenfw)
        elif (int(max_number)) > lenfw:
            print("请输入小于" + str(lenfw) + "的数字！")
            m = m - 1
            return inputnum(m, lenfw)

        else:
            num = int(max_number)
            return num


maxnumber = inputnum(3, len_freq_word)
f = open((os.path.join(os.path.dirname(sys.executable), '武汉过滤版词频.txt')),  'w',encoding='utf-8')
print('输出文件保存至'+os.path.join(os.path.dirname(sys.executable), '武汉过滤版词频.txt'))
f.write("")
for word, freq in freq_word[:maxnumber]:  # 对词频数组前50项进行遍历
    # print(word, freq)  # 打印前50的词语和频数
    freqtran = str(freq)  # 转换频数int为string
    f = open((os.path.join(os.path.dirname(sys.executable), '武汉过滤版词频.txt')), 'a',encoding='utf-8')  # 打开词频输出文档
    f.write(word + "\t" + freqtran + "\n")  # 写入词频和频数
wl_split = ' '.join(object_list)
mywc = WordCloud().generate(wl_split)  # 生成图云
plt.imshow(mywc)  # 绘制显示图云
plt.axis("off")
plt.show()
