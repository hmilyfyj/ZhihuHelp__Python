# -*- coding: utf-8 -*-
__author__ = 'yao'
import re


class ReadListParser():
    u"""
    通过Parser类，生成任务列表以及查询列表，统一存放于urlInfo中
    urlInfo结构
    *   kind
        *   urlInfo类别
            *   'answer', 'question', 'author', 'collection', 'table', 'topic', 'article', 'column'
    *   commandInfo
        *   命令相关信息
        *   questionID, answerID, columnID等, 随kind相异而不同
    *   filter
        *   用于在数据库中提取数据
            *   info
                *   用于提取信息的SQL语句
            *   answer
                *   用于提取答案列表的*条件*
    """
    # 先检测专栏，再检测文章，文章比专栏网址更长，类似问题与答案的关系，取信息可以用split('/')的方式获取
    urlKindList = ['answer', 'question', 'author', 'collection', 'table', 'topic', 'article', 'column']

    # url模式
    urlPattern = {}
    urlPattern['answer'] = r'(?<=zhihu\.com/)question/\d{8}/answer/\d{8}'
    urlPattern['question'] = r'(?<=zhihu\.com/)question/\d{8}'
    urlPattern['author'] = r'(?<=zhihu\.com/)people/[^/\n\r]*'
    urlPattern['collection'] = r'(?<=zhihu\.com/)collection/\d*'
    urlPattern['table'] = r'(?<=zhihu\.com/)roundtable/[^/\n\r]*'
    urlPattern['topic'] = r'(?<=zhihu\.com/)topic/\d*'
    urlPattern['article'] = r'(?<=zhuanlan\.zhihu\.com/)[^/]*/\d{8}'
    urlPattern['column'] = r'(?<=zhuanlan\.zhihu\.com/)[^/\n\r]*'

    def __init__(self):
        self.initProperty()

    def read(self, command):
        command = self.removeComment(command)
        commandList = self.splitCommand(command)
        for command in commandList:
            commandKind = self.detectCommandKind(command)
            if commandKind == '':
                continue

    @staticmethod
    def removeComment(comment=''):
        return comment.split('#')[0]

    @staticmethod
    def splitCommand(command=''):
        return command.split('$')

    def detectCommandKind(self, command=''):
        for key in ReadListParser.urlKindList:
            result = re.search(ReadListParser.urlPattern[key], command)
            if result != None:
                return key
        return ''

    @staticmethod
    def parseQuestion(command):
        result = re.search(ReadListParser.urlPattern['question'], command)
        questionID = result.group(0)
        infoFilterBySQL = "select * from QuestionInfo where questionID = {}".format(questionID)
        answerFilterBySQL = "questionID = {}".format(questionID)
        urlInfo = {}
        urlInfo['kind'] = 'question'
        urlInfo['commandInfo'] = {}
        urlInfo['commandInfo']['questionID'] = questionID
        urlInfo['filter'] = {}
        urlInfo['filter']['info'] = infoFilterBySQL
        urlInfo['filter']['answer'] = answerFilterBySQL
        return urlInfo

    @staticmethod
    def parseAnswer(command):
        result = re.search(ReadListParser.urlPattern['answer'], command)
        questionID = result.group(0)
        answerID = result.group(1)
        infoFilterBySQL = "select * from QuestionInfo where questionID = {}".format(questionID)
        answerFilterBySQL = "questionID = {} and answerID = {}".format(questionID, answerID)
        urlInfo = {}
        urlInfo['kind'] = 'answer'
        urlInfo['commandInfo'] = {}
        urlInfo['commandInfo']['questionID'] = questionID
        urlInfo['commandInfo']['answerID'] = answerID
        urlInfo['filter'] = {}
        urlInfo['filter']['info'] = infoFilterBySQL
        urlInfo['filter']['answer'] = answerFilterBySQL
        return urlInfo

    @staticmethod
    def parseAuthor(command):
        result = re.search(ReadListParser.urlPattern['author'], command)
        authorID = result.group(0)
        infoFilterBySQL = "select * from AuthorInfo where authorID = {}".format(authorID)
        answerFilterBySQL = "authorID = {}".format(authorID)
        urlInfo = {}
        urlInfo['kind'] = 'author'
        urlInfo['commandInfo'] = {}
        urlInfo['commandInfo']['authorID'] = authorID
        urlInfo['filter'] = {}
        urlInfo['filter']['info'] = infoFilterBySQL
        urlInfo['filter']['answer'] = answerFilterBySQL
        return urlInfo

    @staticmethod
    def parseCollection(command):
        result = re.search(ReadListParser.urlPattern['collection'], command)
        collectionID = result.group(0)
        infoFilterBySQL = "select * from CollectionInfo where collectionID = {}".format(collectionID)
        answerFilterBySQL = "answerHref in (select answerHref from CollectionIndex where collectionID = {})".format(collectionID)
        urlInfo = {}
        urlInfo['kind'] = 'collection'
        urlInfo['commandInfo'] = {}
        urlInfo['commandInfo']['collectionID'] = collectionID
        urlInfo['filter'] = {}
        urlInfo['filter']['info'] = infoFilterBySQL
        urlInfo['filter']['answer'] = answerFilterBySQL
        return urlInfo

class CommandParser():
    # todo 直接拼SQL语句是不是太危险了


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
