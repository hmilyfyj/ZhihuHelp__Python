# -*- coding: utf-8 -*-
__author__ = 'yao'

from baseClass import *

u"""
用于将单行ReadList信息转成SQL语句
返回数段语句，
    *   第一段用于获取所有的问题信息
    *   第二段用于获取所有的答案信息
    *   第三段用于获取必要的类别信息（例如XX收藏夹，XX回答集锦，混排则返回对应类别的信息）
返回回一个单独的语句用于获取类别信息
"""

testLineList = [
    # 问题
    'http://www.zhihu.com/question/22921426'
    , 'www.zhihu.com/question/27238186'
    , 'http://www.zhihu.com/question/22719537/'
    # 答案
    , 'http://www.zhihu.com/question/21423568/answer/29751744'
    , 'www.zhihu.com/question/20894671/answer/16526661'
    , 'http://www.zhihu.com/question/22719537/answer/22733181'
    # 话题
    , 'http://www.zhihu.com/topic/19552430'
    , 'http://www.zhihu.com/topic/19551147/top-answers'
    , 'http://www.zhihu.com/topic/19554859'
    # 用户
    , 'http://www.zhihu.com/people/yolfilm'
    , 'http://www.zhihu.com/people/ying-ye-78/answers'
    , 'http://www.zhihu.com/people/bo-cai-28-7/logs '
    # 收藏夹
    , 'http://www.zhihu.com/collection/26489045'
    , 'http://www.zhihu.com/collection/19633165'
    , 'http://www.zhihu.com/collection/19641505'
    # 专栏
    , 'http://zhuanlan.zhihu.com/yolfilm '
    , 'http://zhuanlan.zhihu.com/epiccomposer'
    , 'http://zhuanlan.zhihu.com/Wisdom'
    # 专栏文章
    , 'http://zhuanlan.zhihu.com/Wisdom/19636626'
    , 'http://zhuanlan.zhihu.com/zerolib/19972661'
    , 'http://zhuanlan.zhihu.com/cogito/19968816']

for line in testLineList:
    pass


class Line2Sql(BaseClass):
    def __init__(self):
        self.whereList = []
        return

    # todo 直接拼SQL语句是不是太危险了
    def parseQuestion(self, content):
        questionID = ''
        return "questionID = {}".format(questionID)

    def parseAnswer(self, content):
        questionID = ''
        answerID = ''
        return "answerHref = 'http://www.zhihu.com/question/{0}/answer/{1}'".format(questionID, answerID)

    def parseAuthor(self, content):
        author = ''
        return "author = '{}'".format(author)

    def parseCollection(self, content):
        collectionID = ''
        return "answerHref in (select answerHref from CollectionIndex where collectionID = '{0}')".format(collectionID)

    def parseTopic(self, content):
        topicID = ''
        return "answerHref in (select answerHref from TopicIndex where topicID = '{0}')".format(topicID)

    def parseColumn(self, content):
        columnID = ''
        return "columnID = {}".format(columnID)

    def parseArticle(self, content):
        columnID = ''
        articleID = ''
        return "columnID = {0} and articleID = {1}".format(columnID, articleID)
