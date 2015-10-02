# -*- coding: utf-8 -*-
import re

from baseClass import *

u"""
今天把这个的数据结构解决一下
分为两块
    *   问题包
    *   答案包
以问题作为一级页，问题之上还可以再加章节
基础元素是问题
问题 + 问题 => 小节
小节 + 小节 => 章
章 + 章 => 书
书 + 书 => 书

答案结构
    *   答案相关属性

问题结构
    *   问题
        *   问题输出方法
            *   指将问题转换为可读的dict/list的方法
        *   题目必要信息
            *   题目相关属性
            *   题目内容
        *   答案列表
            *   答案abc
            *   答案列表属性
            *   答案输出方法

章节结构
    *   节
        *   小节属性
            *   与小节相关的属性
        *   小节目录
        *   问题列表
            *   其内为一个一个的问题
        *   问题输出方法
            *   控制节内问题的排序，展示

    *   章
        *   章属性
        *   章目录
        *   小节列表
        *   小节输出方法
        *   章前言
"""


class Content():
    u"""
    用于承载html内容，自动整理格式，提取图片内容链接
    """

    def __init__(self, content=''):
        self.setContent(content)
        return

    def setContent(self, content):
        self.rawContent = content
        self.content = content
        self.removeTag(['noscript'])
        self.imgDict = {}
        self.fixPic()
        return

    def fixPic(self):
        if SettingClass.PICQUALITY == 0:
            self.removeTag(['img'])
        content = self.content
        for imgTag in re.findall(r'<img.*?>', self.content):
            self.content = content.replace(imgTag, self.fixImgTag(imgTag))
        return

    def fixImgTag(self, imgContent):
        src = ''
        try:
            # 判断是否为tex图片
            imgContent.index('equation?tex=')
            result = re.search(r'zhihu.com/equation\?tex=[^"]+', imgContent)
            if result != None:
                src = result.group(0)
            fileSrc = '../images/{0}.jpg'.format(BaseClass.md5(src))
        except:
            try:
                imgContent.index('data-actualsrc')
                src = re.search(r"""(?<=data-actualsrc\="//)[^"]+""", imgContent).group(0)
                if SettingClass.PICQUALITY == 2:
                    result = re.search(r"""(?<=data-original\="//)[^"]+""", imgContent)
                    if result != None:
                        src = result.group(0)
            except:
                pass
            finally:
                fileSrc = '../images/{0}'.format(BaseClass.getHttpFileName(src))
        imgContent = '''
                        <div class="duokan-image-single">\n
                            <img src="{0}"></img>\n
                        </div>\n
                     '''.format(fileSrc)
        self.imgDict[fileSrc] = src
        return imgContent

    def getImgDict(self):
        return self.imgDict

    def removeTag(self, tagname=[]):
        for tag in tagname:
            self.content = self.content.replace('</' + tag + '>', '')
            self.content = re.sub(r"<" + tag + r'.*?>', '', self.content)
        return self


class BaseItem(BaseClass):
    def __init__(self, property={}):
        #   初始化属性
        self.initProperty()
        #   将属性存入记录中
        for key in property:
            self.property[key] = property[key]
        self.customerInit()
        return

    def customerInit(self):
        #   在此自定义init函数
        return

    def initProperty(self):
        self.property = {}
        self.itemList = []
        return

    def getProperty(self, key):
        return self.property.get(key, '')


class AnswerItem(BaseItem):
    u"""
    基础类，仅用于保存数据，不提供额外行为
    """

    def initProperty(self):
        self.property = {
            'authorID': 0,
            'authorSign': '',
            'authorLogo': '',
            'authorName': '',
            'questionID': 0,
            'answerID': 0,
            'content': Content(),
            'updateDate': '2000-01-01',
            'agreeCount': 0,
            'commentCount': 0,
            'collectCount]': 0,
        }
        return

    def getPicDict(self):
        return self.getProperty('content').getImgDict()


class QuestionItem(BaseItem):
    def initProperty(self):
        self.property = {
            'questionID': 0,
            'followCount': 0,
            'viewCount': 0,
            'commentCount': 0,
            'answerCount': 0,
            'questionTitle': '',
            'desc': Content(),
            'collapsedCount': '0',
            'answerDict': {},
            'length': self.__len__(),
        }
        return self

    def addAnswer(self, answer):
        self.getProperty('answerDict')[answer.getProperty('answerID')] = answer
        return self

    def __len__(self):
        return len(self.getProperty('answerDict'))

    def getPicDict(self):
        picDict = {}
        for key in self.getProperty('answerDict'):
            picDict.update(self.getProperty('answerDict')[key].getPicDict())
        picDict.update(self.getProperty('desc').getPicDict())
        return picDict

    """
    暂时废弃这个功能
    def sortBy(self, key, reverse=True):
        u'''
        对answerList按指定属性进行排序
        todo 需要测试正确性
        '''
        self.getProperty('answerList').sort(cmp=lambda x, y: x.getProperty(key) > y.getProperty(key), reverse=reverse)
        return self
    """

    def addQuestion(self, question):
        u"""
        问题 + 问题 => 节
        """
        if question.getProperty('questionID') == self.getProperty('questionID'):
            self.getProperty('answerDict').update(question.getProperty('answerDict'))
            return self
        else:
            section = SectionItem()
            section.addQuestion(self)
            section.addQuestion(question)
            return section


class SectionItem(BaseItem):
    def initProperty(self):
        self.property = {
            'sectionTitle': '',
            'sectionDesc': Content(),
            'questionDict': {},
        }
        return self

    def addQuestion(self, question):
        key = question.getProperty('questionID')
        if key in self.getProperty('questionDict'):
            self.getProperty('questionDict').addQuestion(question)
        else:
            self.getProperty('questionDict')[key] = question
        return self

    def getPicDict(self):
        picDict = {}
        for key in self.getProperty('questionDict'):
            picDict.update(self.getProperty('questionDict')[key].getPicDict())
        picDict.update(self.getProperty('sectionDesc').getPicDict())
        return picDict

    def __len__(self):
        length = 0
        questionDict = self.getProperty('questionDict')
        for key in questionDict:
            length += len(questionDict[key])
        return length

    def addSection(self, section):
        chapter = ChapterItem()
        chapter.addSection(self)
        chapter.addSection(section)
        return chapter


class AuthorSection(SectionItem):
    u"""
    用于生成用户信息页
    """

    def initProperty(self):
        self.property = {
            'sectionTitle': '',
            'sectionDesc': Content(),
            'questionDict': {},
        }
        return self


class ChapterItem(BaseItem):
    def initProperty(self):
        self.property = {
            'chapterTitle': '',
            'chapterDesc': Content(),
            'sectionList': [],
        }
        return self

    def addQuestion(self, question):
        if len(self.getProperty('sectionList')) == 0:
            section = SectionItem()
            section.addQuestion(question)
            self.addSection(section)
        else:
            section = self.getProperty('sectionList')[-1]
            section.addQuestion(question)
        return self

    def addSection(self, section):
        self.getProperty('sectionList').append(section)
        return self

    def addChapter(self, chapter):
        book = BookItem()
        book.addChapter(self)
        book.addChapter(chapter)
        return book


class BookItem(BaseItem):
    u"""
    仅用于保存数据
    """

    def initProperty(self):
        self.property = {
            'bookTitle': '',
            'bookDesc': Content(),
            'chapterList': [],
        }
        return

    def addChapter(self, chapter):
        self.getProperty('chapterList').append(chapter)
        return

class Package(BaseClass):
    u'''
    package基础类
    用于保存Filer中取出的数据
    PS:取出的数据还可以再打一层包XD
    '''

    def __init__(self):
        self.package = {}
        self.initPackage()
        return

    def initPackage(self):
        return

    def setPackage(self, dataDict):
        for key in dataDict:
            self.package[key] = dataDict[key]
        return

    def getResult(self):
        return self.package

    # 重载[]与[] =操作符
    def __getitem__(self, key):
        return self.package[key]

    def __setitem__(self, key, val):
        return self.package.__setitem__(key, val)


class ContentPackage(Package):
    u'''
    字典结构
    *   creatorID
    *   creatorSign
    *   creatorName
    *   creatorLogo
    *   ID
        *   专栏/话题/收藏夹的ID
    *   kind
        *   类别（专栏/话题/收藏夹/问题合集）
    *   title
    *   logo
    *   description
    *   followerCount
    *   commentCount
    *   contentCount
        *   文章总数/答案总数/问题总数等
    *   extraKey
        *   留作日后扩展
    *   questionDict
        *   用于存储问题内容/专栏文章内容
        *   以[question_{questionID}或{columnID}_{articleID}]为key值
    '''

    def initPackage(self):
        self.package['creatorID'] = ''
        self.package['creatorSign'] = ''
        self.package['creatorName'] = ''
        self.package['creatorLogo'] = ''
        self.package['ID'] = ''
        self.package['kind'] = ''
        self.package['title'] = ''
        self.package['logo'] = ''
        self.package['description'] = ''
        self.package['followerCount'] = 0
        self.package['commentCount'] = 0
        self.package['followerCount'] = 0
        self.package['contentCount'] = 0
        self.package['extraKey'] = {}
        self.package['questionDict'] = {}

        self.questionDict = self.package['questionDict']

    def addQuestion(self, questionPackage):
        questionID = questionPackage['questionID']
        if questionID in self.questionDict:
            self.questionDict[questionID].merge(questionPackage)
        else:
            self.questionDict[questionID] = questionPackage
        return

    def merge(self, contentPackage):
        u'''
        把内容合并后再把种类改成merge即可。
        合并产生的内容没有必要再去控制它的额外属性了。
        没有意义
        最后发布前自己想一个填充上即可
        '''
        self.package['kind'] = 'merge'
        self.package['title'] = u'自定义'
        self.package['ID'] = 'merge'
        self.package['logo'] = ''

        self.package['description'] = '{0}+{1}'.format(self.package['description'], self.package['title'])

        for key in contentPackage['questionDict']:
            self.addQuestion(contentPackage['questionDict'][key])
        return

    def getResult(self):
        self.package['contentCount'] = len(self.questionDict)
        return self.package

    def format_sortBy_agree_desc(self):
        u'''
        排序后输出结果List,按赞同数降序排列
        '''
        questionList = []
        for key in self.questionDict:
            question = self.questionDict[key].getResult()
            answerList = []
            for key in question['answerDict']:
                answerList.append(question['answerDict'][key])
            answerList = sorted(answerList, key=lambda content: content['agreeCount'], reverse=True)
            question['answerList'] = answerList
            questionList.append(question)
        questionList = sorted(questionList, key=lambda content: content['agreeCount'], reverse=True)
        return questionList

    def format_sortBy_updateDate_asc(self):
        u'''
        排序后输出结果List,按更新日期升序排列
        '''
        questionList = []
        for key in self.questionDict:
            question = self.questionDict[key].getResult()
            answerList = []
            for key in question['answerDict']:
                answerList.append(question['answerDict'][key])
            answerList = sorted(answerList, key=lambda content: content['updateDate'], reverse=False)
            question['answerList'] = answerList
            # 问题的最后更新日期为问题中答案的最后更新日期
            question['updateDate'] = answerList[0]['updateDate']
            questionList.append(question)
        questionList = sorted(questionList, key=lambda content: content['updateDate'], reverse=False)
        return questionList


class QuestionPackage(Package):
    u'''
    专栏文章和问题的kind要分开
    其ID命名规则为
    问题ID为"question_{questionID}".format(questionID)
    专栏ID为"{columnID}_{articleID}".format(columnID, articleID)
    其中titleLogo项专为专栏文章使用
    字典结构:
    *   Question
        *   questionID
        *   kind
        *   title
        *   titleLogo
        *   description
        *   updateDate
        *   commentCount
        *   followerCount
        *   viewCount
        *   answerCount
        *   agreeCount
            *   赞同数总和，方便排序
        *   extraKey
            *   留作日后扩展
        *   answerDict
            *   存储答案内容，使用answerID/articleID做key
    '''

    def initPackage(self):
        self.package['questionID'] = ''
        self.package['kind'] = ''
        self.package['title'] = ''
        self.package['titleLogo'] = ''
        self.package['description'] = ''
        self.package['updateDate'] = ''
        self.package['commentCount'] = 0
        self.package['viewCount'] = 0
        self.package['answerCount'] = 0
        self.package['followerCount'] = 0
        self.package['extraKey'] = {}
        self.package['answerDict'] = {}

        self.answerDict = self.package['answerDict']

    def addAnswer(self, answerPackage):
        u'''
        answer中没有多少需要合并的信息，所以不对answer调用merge方法
        '''
        answerID = answerPackage['answerID']
        if not answerID in self.answerDict:
            self.answerDict[answerID] = answerPackage
        return

    def merge(self, questionPackage):
        if questionPackage['kind'] != self.package['kind']:
            return
        for key in ['title', 'titleLogo', 'description', 'updateDate']:
            if questionPackage[key] != '':
                self.package[key] = questionPackage[key]

        for key in questionPackage['answerDict']:
            self.addAnswer(questionPackage['answerDict'][key])
        return

    def getResult(self):
        self.package['answerCount'] = len(self.answerDict)
        agreeCount = 0
        for key in self.answerDict:
            agreeCount += self.answerDict[key]['agreeCount']
        self.package['agreeCount'] = agreeCount
        return self.package


class AnswerPackage(Package):
    u'''
    数据结构
    其中，对于Article而言，questionID即为columnID,answerID即为articleID
    *   Answer
        *   authorID
        *   authorSign
        *   authorLogo
        *   authorName
        *   questionID
        *   answerID
        *   content
        *   updateDate
        *   agreeCount
        *   commentCount
        *   collectCount
        *   extraKey
            *   留作日后扩展
    '''

    def initPackage(self):
        self.package['authorID'] = ''
        self.package['authorSign'] = ''
        self.package['authorLogo'] = ''
        self.package['authorName'] = ''
        self.package['questionID'] = ''
        self.package['answerID'] = ''
        self.package['content'] = ''
        self.package['updateDate'] = ''
        self.package['agreeCount'] = 0
        self.package['commentCount'] = 0
        self.package['collectCount'] = 0
        self.package['extraKey'] = {}
        return
