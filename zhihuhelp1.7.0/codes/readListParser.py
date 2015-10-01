# -*- coding: utf-8 -*-
__author__ = 'yao'
import re
from baseClass import *


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
        *   rawUrl
            *   纯净版url
                *   示例http://zhuanlan.zhihu.com/{}/{}".format(columnID, articleID)
                *   url尾部没有/分隔符
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

    def parseCommandLine(commandLine):
        u"""
        用于分析指令
        """

        def removeComment(commandLine):
            return commandLine.split('#')[0]

        def splitCommand(commandLine):
            return commandLine.split('$')

        commandLine = removeComment(commandLine)
        commandList = splitCommand(commandLine)
        urlInfoList = []
        for command in commandList:
            urlInfo = parseCommandFactory(command)
            if urlInfo['kind'] != '':
                urlInfoList.append(urlInfo)
        urlInfoDict = mergeUrlInfoList(urlInfoList)
        return urlInfoDict


def initUrlInfoDict():
    urlInfoDict = {}
    for kind in ReadListParser.urlKindList:
        urlInfoDict[kind] = {
            'kind': kind,
            'commandInfoList': [],
            'filterList': [],
            'filter': {
                'answer': '',
                'article': '',
                'infoList': [],
            }
        }
    return urlInfoDict


def mergeFilter(urlInfoDict):
    answerSql = 'select * from AnswerContent where (FALSE '
    articleSql = 'select * from ArticleContent where (FALSE '
    answerKindList = ['answer', 'question', 'author', 'collection', 'table', 'topic']
    articleKindList = ['article', 'column']

    # 版权保护，noRecord检测
    otherCondition = ''
    if SettingClass.COPYRIGHTPROTECT:
        otherCondition += 'and (noRecordFlag = 0)'


    # 合并answer选择条件
    for kind in answerKindList:
        for filterDict in urlInfoDict[kind]['filterList']:
            answerSql += " or ({}) ".format(filterDict['answer'])
    answerSql += ') {};'.format(otherCondition)

    # 合并article选择条件
    for kind in articleKindList:
        for filterDict in urlInfoDict[kind]['filterList']:
            articleSql += " or ({}) ".format(filterDict['article'])
    articleSql += ') {};'.format(otherCondition)

    # 合并info选择条件
    infoKindList = ['author', 'collection', 'table', 'topic', 'article', 'column']
    for kind in infoKindList:
        for filterDict in urlInfoDict[kind]['filterList']:
            urlInfoDict['filter']['infoList'].append(filterDict['info'])
    return urlInfoDict


def mergeUrlInfoList(urlInfoList):
    u"""
    将urlList按类别合并在一起
    """
    urlInfoDict = initUrlInfoDict()
    for urlInfo in urlInfoList:
        kind = urlInfo['kind']
        urlInfoDict[kind]['commandInfoList'].append(urlInfo['commandInfo'])
        urlInfoDict[kind]['filterList'].append(urlInfo['filter'])

    urlInfoDict = mergeFilter(urlInfoDict)
    return urlInfoDict


def parseCommandFactory(command=''):
    u"""
    分析单条命令并返回urlInfo结果
    """

    def detectCommandKind(command):
        for key in ReadListParser.urlKindList:
            result = re.search(ReadListParser.urlPattern[key], command)
            if result != None:
                return key
        return ''

    def parseQuestion(command):
        result = re.search(ReadListParser.urlPattern['question'], command)
        questionID = result.group(0)
        infoFilterBySQL = ''  # "select * from QuestionInfo where questionID = {}".format(questionID)
        answerFilterBySQL = "questionID = {}".format(questionID)
        urlInfo = {}
        urlInfo['kind'] = 'question'
        urlInfo['commandInfo'] = {}
        urlInfo['commandInfo']['questionID'] = questionID
        urlInfo['commandInfo']['rawUrl'] = "http://www.zhihu.com/question/{}".format(questionID)
        urlInfo['filter'] = {}
        urlInfo['filter']['info'] = infoFilterBySQL
        urlInfo['filter']['answer'] = answerFilterBySQL
        return urlInfo

    def parseAnswer(command):
        result = re.search(ReadListParser.urlPattern['answer'], command)
        questionID = result.group(0)
        answerID = result.group(1)
        infoFilterBySQL = ''  # "select * from QuestionInfo where questionID = {}".format(questionID)
        answerFilterBySQL = "questionID = {} and answerID = {}".format(questionID, answerID)
        urlInfo = {}
        urlInfo['kind'] = 'answer'
        urlInfo['commandInfo'] = {}
        urlInfo['commandInfo']['questionID'] = questionID
        urlInfo['commandInfo']['answerID'] = answerID
        urlInfo['commandInfo']['rawUrl'] = "http://www.zhihu.com/question/{}/answer/{}".format(questionID, answerID)
        urlInfo['filter'] = {}
        urlInfo['filter']['info'] = infoFilterBySQL
        urlInfo['filter']['answer'] = answerFilterBySQL
        return urlInfo

    def parseAuthor(command):
        result = re.search(ReadListParser.urlPattern['author'], command)
        authorID = result.group(0)
        infoFilterBySQL = "select * from AuthorInfo where authorID = {}".format(authorID)
        answerFilterBySQL = "authorID = {}".format(authorID)
        urlInfo = {}
        urlInfo['kind'] = 'author'
        urlInfo['commandInfo'] = {}
        urlInfo['commandInfo']['authorID'] = authorID
        urlInfo['commandInfo']['rawUrl'] = "http://www.zhihu.com/people/{}".format(authorID)
        urlInfo['filter'] = {}
        urlInfo['filter']['info'] = infoFilterBySQL
        urlInfo['filter']['answer'] = answerFilterBySQL
        return urlInfo

    def parseCollection(command):
        result = re.search(ReadListParser.urlPattern['collection'], command)
        collectionID = result.group(0)
        infoFilterBySQL = "select * from CollectionInfo where collectionID = {}".format(collectionID)
        answerFilterBySQL = "answerHref in (select answerHref from CollectionIndex where collectionID = {})".format(
            collectionID)
        urlInfo = {}
        urlInfo['kind'] = 'collection'
        urlInfo['commandInfo'] = {}
        urlInfo['commandInfo']['collectionID'] = collectionID
        urlInfo['commandInfo']['rawUrl'] = "http://www.zhihu.com/collection/{}".format(collectionID)
        urlInfo['filter'] = {}
        urlInfo['filter']['info'] = infoFilterBySQL
        urlInfo['filter']['answer'] = answerFilterBySQL
        return urlInfo

    def parseTable(command):
        result = re.search(ReadListParser.urlPattern['table'], command)
        tableID = result.group(0)
        infoFilterBySQL = "select * from TableInfo where tableID = {}".format(tableID)
        answerFilterBySQL = "answerHref in (select answerHref from TableIndex where tableID = {})".format(tableID)
        urlInfo = {}
        urlInfo['kind'] = 'table'
        urlInfo['commandInfo'] = {}
        urlInfo['commandInfo']['tableID'] = tableID
        urlInfo['commandInfo']['rawUrl'] = "http://www.zhihu.com/roundtable/{}".format(tableID)
        urlInfo['filter'] = {}
        urlInfo['filter']['info'] = infoFilterBySQL
        urlInfo['filter']['answer'] = answerFilterBySQL
        return urlInfo

    def parseTopic(command):
        result = re.search(ReadListParser.urlPattern['topic'], command)
        topicID = result.group(0)
        infoFilterBySQL = "select * from TopicInfo where topicID = {}".format(topicID)
        answerFilterBySQL = "answerHref in (select answerHref from TopicIndex where topicID = {})".format(topicID)
        urlInfo = {}
        urlInfo['kind'] = 'topic'
        urlInfo['commandInfo'] = {}
        urlInfo['commandInfo']['topicID'] = topicID
        urlInfo['commandInfo']['rawUrl'] = "http://www.zhihu.com/topic/{}".format(topicID)
        urlInfo['filter'] = {}
        urlInfo['filter']['info'] = infoFilterBySQL
        urlInfo['filter']['answer'] = answerFilterBySQL
        return urlInfo

    def parseArticle(command):
        result = re.search(ReadListParser.urlPattern['article'], command)
        columnID = result.group(0)
        articleID = result.group(1)
        infoFilterBySQL = "select * from ColumnInfo where columnID = {}".format(columnID)
        articleFilterBySQL = "columnID = {} and articleID = {}".format(columnID, articleID)
        urlInfo = {}
        urlInfo['kind'] = 'article'
        urlInfo['commandInfo'] = {}
        urlInfo['commandInfo']['columnID'] = columnID
        urlInfo['commandInfo']['articleID'] = articleID
        urlInfo['commandInfo']['rawUrl'] = "http://zhuanlan.zhihu.com/{}/{}".format(columnID, articleID)
        urlInfo['filter'] = {}
        urlInfo['filter']['info'] = infoFilterBySQL
        urlInfo['filter']['article'] = articleFilterBySQL
        return urlInfo

    def parseColumn(command):
        result = re.search(ReadListParser.urlPattern['column'], command)
        columnID = result.group(0)
        infoFilterBySQL = "select * from ColumnInfo where columnID = {}".format(columnID)
        articleFilterBySQL = "columnID = {}".format(columnID)
        urlInfo = {}
        urlInfo['kind'] = 'column'
        urlInfo['commandInfo'] = {}
        urlInfo['commandInfo']['columnID'] = columnID
        urlInfo['commandInfo']['rawUrl'] = "http://zhuanlan.zhihu.com/{}".format(columnIDD)
        urlInfo['filter'] = {}
        urlInfo['filter']['info'] = infoFilterBySQL
        urlInfo['filter']['article'] = articleFilterBySQL
        return urlInfo

    def parseError(command):
        BaseClass.logger.info(u"""匹配失败，未知readList类型。\n失败命令:{}""".format(command))
        urlInfo = {}
        urlInfo['kind'] = ''
        return urlInfo

    parserDict = {
        'answer': parseAnswer,
        'question': parseQuestion,
        'author': parseAuthor,
        'collection': parseCollection,
        'table': parseTable,
        'topic': parseTopic,
        'article': parseArticle,
        'column': parseColumn,
        '': parseError,
        '': parseError,
    }
    kind = detectCommandKind(command)
    return parserDict[kind](command)
