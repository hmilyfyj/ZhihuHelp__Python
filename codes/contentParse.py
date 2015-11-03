# -*- coding: utf-8 -*-
import re
import HTMLParser  # 转换网页代码
import datetime  # 简单处理时间

from baseClass import *
from bs4 import BeautifulSoup


class ParserTools(BaseClass):
    @staticmethod
    def get_yesterday(self):
        today = datetime.date.today()
        one = datetime.timedelta(days=1)
        yesterday = today - one
        return yesterday.isoformat()

    @staticmethod
    def get_today(self):
        return datetime.date.today().isoformat()

    @staticmethod
    def match_content(self, patten, content, default=""):
        result = re.search(patten, str(content))
        if result is None:
            return default
        return result.group(0)

    @staticmethod
    def match_int(self, content):
        u"""
        返回文本形式的文字中最长的数字串，若没有则返回'0'
        """
        return self.match_content("\d+", content, "0")

    @staticmethod
    def matchQuestionID(self, rawLink):
        return self.match_content("(?<=question/)\d{8}", rawLink)

    @staticmethod
    def match_answer_id(self, rawLink):
        return self.match_content("(?<=answer/)\d{8}", rawLink)

    @staticmethod
    def match_author_id(self, rawLink):
        return self.match_content("""(?<=people/)[^/'"]+""", rawLink)

    @staticmethod
    def get_tag_content(self, tag):
        u"""
        只用于提取bs中tag.contents的内容，不要乱传参
        思路来自stackoverflow，http://stackoverflow.com/questions/8112922/beautifulsoup-innerhtml
        帅！
        """
        return "".join([unicode(x) for x in tag.contents])

    @staticmethod
    def get_attr(self, dom, attr, defaultValue=""):
        u"""
        获取bs中tag.content的指定属性
        若content为空或者没有指定属性则返回默认值
        """
        if dom == None:
            return defaultValue
        return dom.get(attr, defaultValue)

    @staticmethod
    def parse_date(self, date='1357-08-12'):
        if u'昨天' in date:
            return self.get_yesterday()
        if u'今天' in date:
            return self.get_today()
        return self.match_content(r'\d{4}-\d{2}-\d{2}', date, date)  # 一三五七八十腊，三十一天永不差！


class AuthorInfo(ParserTools):
    """
    实践一把《代码整洁之道》的做法，以后函数尽量控制在5行之内
    """

    def __init__(self, dom=None):
        self.set_dom(dom)
        return

    def set_dom(self, dom):
        self.info = {}
        if not (dom is None):
            self.dom = dom.find('div', class_='zm-item-answer-author-info')
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        if self.dom.find('img') is None:
            self.parse_anonymous_info()
        else:
            self.parse_author_info()
        return

    def parse_author_info(self):
        self.parse_anonymous_info()
        self.parse_anonymous_info()
        self.parse_anonymous_info()
        self.parse_anonymous_info()
        return

    def parse_anonymous_info(self):
        self.info['authorID'] = u"coder'sGirlFriend~"
        self.info['authorSign'] = u''
        self.info['authorLogo'] = u'http://pic1.zhimg.com/da8e974dc_s.jpg'
        self.info['authorName'] = u'匿名用户'
        return

    def parse_author_id(self):
        author = self.dom.find('a', class_='zm-item-link-avatar')
        link = self.get_attr(author, 'href')
        self.info['authorID'] = self.match_answer_id(link)
        return

    def parse_author_sign(self):
        sign = self.dom.find('strong', class_='zu-question-my-bio')
        self.info['authorSign'] = self.get_attr(sign, 'title')
        return

    def parse_author_logo(self):
        self.info['authorLogo'] = self.get_attr(self.dom.find('img'), 'src')
        return

    def parse_author_name(self):
        self.info['authorName'] = self.dom.find('a')[-1].text
        return


class Answer(ParserTools):
    """
    示例代码
    <div tabindex="-1" class="zm-item-answer  zm-item-expanded" itemscope="" itemtype="http://schema.org/Answer" data-aid="23458712" data-atoken="70095598" data-collapsed="0" data-created="1446209879" data-deleted="0" data-helpful="1" data-isowner="0" data-copyable="1">
<a class="zg-anchor-hidden" name="answer-23458712"></a>


<div class="zm-votebar">
<button class="up" aria-pressed="false" title="赞同">
<i class="icon vote-arrow"></i>
<span class="label">赞同</span>
<span class="count">7</span>
</button>
<button class="down" aria-pressed="false" title="反对，不会显示你的姓名">
<i class="icon vote-arrow"></i>
<span class="label">反对，不会显示你的姓名</span>
</button>
</div>


<div class="answer-head">
<div class="zm-item-answer-author-info">
<h3 class="zm-item-answer-author-wrap">


<a data-tip="p$t$abandonstone" class="zm-item-link-avatar" href="/people/abandonstone">
<img src="https://pic2.zhimg.com/9379d0b856df5796b3a21694cee452b5_s.jpg" class="zm-list-avatar" data-source="https://pic2.zhimg.com/9379d0b856df5796b3a21694cee452b5_s.jpg">
</a>



<a data-tip="p$t$abandonstone" href="/people/abandonstone">噶愛成神</a>，<strong title="INFP 彎而正直 中等偏下" class="zu-question-my-bio">INFP 彎而正直 中等偏下</strong>

</h3>
</div>
<div class="zm-item-vote-info " data-votecount="7">

<span class="voters">
<span class="user-block"><a data-tip="p$t$wei-yi-jing-58" href="http://www.zhihu.com/people/wei-yi-jing-58" class="zg-link" title="妖都妖子">妖都妖子</a>、</span><span class="user-block"><a data-tip="p$t$da-shuai-bi-77" href="http://www.zhihu.com/people/da-shuai-bi-77" class="zg-link" title="Freya Zheng">Freya Zheng</a>、</span><span class="user-block"><a data-tip="p$t$weng-weng-46-17" href="http://www.zhihu.com/people/weng-weng-46-17" class="zg-link" title="wEnG WeNg">wEnG WeNg</a></span>
</span>


<a href="javascript:;" class="more"> 等人赞同</a>


</div>
</div>
<div class="zm-item-rich-text js-collapse-body" data-resourceid="7011484" data-action="/answer/content" data-author-name="噶愛成神" data-entry-url="/question/37011291/answer/70095598">


<div class="zh-summary summary clearfix" style="display:none;">

老子不和男的結婚:）

</div>


<div class="zm-editable-content clearfix">
老子不和男的結婚:）

</div>

</div>
<a class="zg-anchor-hidden ac" name="23458712-comment"></a>
<div class="zm-item-meta zm-item-comment-el answer-actions clearfix">
<div class="zm-meta-panel">

<span class="answer-date-link-wrap">
<a class="answer-date-link meta-item" target="_blank" href="/question/37011291/answer/70095598">发布于 昨天 20:57</a>
</span>

<a href="#" name="addcomment" class=" meta-item toggle-comment">
<i class="z-icon-comment"></i>3 条评论</a>


<a href="#" class="meta-item zu-autohide" name="thanks" data-thanked="false"><i class="z-icon-thank"></i>感谢</a>



<a href="#" class="meta-item zu-autohide goog-inline-block goog-menu-button" name="share" role="button" aria-expanded="false" style="-webkit-user-select: none;" tabindex="0" aria-haspopup="true"><div class="goog-inline-block goog-menu-button-outer-box"><div class="goog-inline-block goog-menu-button-inner-box"><div class="goog-inline-block goog-menu-button-caption"><i class="z-icon-share"></i>分享</div><div class="goog-inline-block goog-menu-button-dropdown">&nbsp;</div></div></div></a>
<a href="#" class="meta-item zu-autohide" name="favo">
<i class="z-icon-collect"></i>收藏</a>




<span class="zg-bull zu-autohide">•</span>

<a href="#" name="nohelp" class="meta-item zu-autohide">没有帮助</a>

<span class="zg-bull zu-autohide">•</span>
<a href="#" name="report" class="meta-item zu-autohide goog-inline-block goog-menu-button" role="button" aria-expanded="false" style="-webkit-user-select: none;" tabindex="0" aria-haspopup="true"><div class="goog-inline-block goog-menu-button-outer-box"><div class="goog-inline-block goog-menu-button-inner-box"><div class="goog-inline-block goog-menu-button-caption">举报</div><div class="goog-inline-block goog-menu-button-dropdown">&nbsp;</div></div></div></a>



<span class="zg-bull">•</span>

<a href="/terms#sec-licence-1" target="_blank" class="meta-item copyright"> 作者保留权利 </a>



</div>
</div>
</div>
    """

    def __init__(self, dom=None):
        self.set_dom(dom)
        return

    def set_dom(self, dom):
        self.info = {}
        if not (dom is None):
            self.header = dom.find('div', class_='zm-item-vote-info')
            self.body = dom.find('div', class_='zm-editable-content')
            self.footer = dom.find('div', class_='zm-meta-panel')
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        self.parse_header_info()
        self.parse_answer_content()
        self.parse_footer_info()
        return

    def parse_header_info(self):
        self.parse_vote_count()
        return

    def parse_footer_info(self):
        self.parse_date_info()
        self.parse_comment_count()
        self.parse_no_record_flag()
        self.parse_href_info()
        return

    def parse_vote_count(self):
        self.info['answerAgreeCount'] = self.get_attr(self.header, 'data-votecount')
        return self.info['answerAgreeCount']

    def parse_answer_content(self):
        self.info['answerContent'] = self.body.text()
        return

    def parse_date_info(self):
        data_block = self.footer.find('a', class_='answer-date-link')
        commit_date = self.get_attr(data_block, 'data-tip')
        if commit_date == '':
            commit_date = data_block.text()
            self.info['editDate'] = self.info['commitDate'] = self.parse_date(commit_date)
        else:
            update_date = data_block.text()
            self.info['editDate'] = self.parse_date(update_date)
            self.info['commitDate'] = self.parse_date(commit_date)

    def parse_comment_count(self):
        comment = self.footer.find('a', name='addcomment').text()
        self.info['answerCommentCount'] = self.match_int(comment)
        return

    def parse_no_record_flag(self):
        no_record_flag = self.footer.find('a', class_='copyright').text()
        self.info['noRecordFlag'] = int(u'禁止转载' in no_record_flag)
        return

    def parse_href_info(self):
        href_tag = self.footer.find('a', class_='answer-date-link')
        href = self.get_attr(href_tag, 'href')
        self.parse_question_id(href)
        self.parse_answer_id(href)
        self.info['answerHref'] = "http://www.zhihu.com/question/{questionID}/answer/{answerID}".format(**self.info)
        return

    def parse_question_id(self, href):
        self.info['questionID'] = self.matchQuestionID(href)
        return

    def parse_answer_id(self, href):
        self.info['answerID'] = self.match_answer_id(href)
        return


class Parse(ParserTools):
    def __init__(self, content):
        BaseClass.logger.debug(u"开始解析网页")
        self.dom = BeautifulSoup(content, 'html.parser')
        self.rawContent = content
        self.init_property()

    def init_property(self):
        """
        初始化基本属性
        """
        self.authorInfo = AuthorInfo()
        return

    def get_author_info(self, dom):
        self.authorInfo.set_dom(dom)
        return self.authorInfo.get_info()

    def get_answer_list(self):
        u"""
        取得答案列表
        需重载
        """
        return self.dom.find_all('div')

    def get_answer(self, dom):
        u"""
        content作为已经切分好了的答案bs_tag对象传入
        不要乱传参
        """


class ParseQuestion(Parse):
    u'''
    输入网页内容，返回两个dict，一个是问题信息dict，一个是答案dict列表
    '''

    def getAnswerContentList(self):
        return self.content.find_all("div", {"class": "zm-item-answer "})

    def getInfoDict(self):
        "列表长度有可能为0(没有回答),1(1个回答),2(2个回答)...,需要分情况处理"
        contentList = self.getAnswerContentList()
        questionInfoDictList = []
        answerDictList = []
        questionInfoDictList.append(self.getQuestionInfoDict())
        if len(contentList) != 0:
            for content in contentList:
                answerDictList.append(self.getAnswerDict(content))
        return questionInfoDictList, answerDictList

    def getQuestionInfoDict(self):
        questionInfoDict = {}
        bufString = self.content.find("div", {"id": "zh-question-title"}).get_text()
        questionInfoDict['questionTitle'] = bufString
        bufString = self.content.find("a", {"name": "addcomment"}).get_text()
        questionInfoDict['questionCommentCount'] = self.match_int(bufString)
        questionInfoDict['questionDesc'] = self.get_tag_content(
            self.content.find("div", {"id": "zh-question-detail"}).find('div'))
        bufString = self.get_attr(self.content.find("h3", {"id": "zh-question-answer-num"}), 'data-num')
        questionInfoDict['questionAnswerCount'] = self.match_int(bufString)

        bufString = self.content.find("div", {"id": "zh-question-side-header-wrap"}).find("div", {
            "class": "zg-gray-normal"}).a.strong.text
        questionInfoDict['questionFollowCount'] = self.match_int(bufString)
        bufString = self.content.find("div", {"id": "zh-question-side-header-wrap"}).find("div", {
            "class": "zg-gray-normal"}).a.strong.text
        questionInfoDict['questionViewCount'] = self.match_int(bufString)
        bufString = \
            self.content.find("div", {"class": "zu-main-sidebar"}).find_all("div", {"class": "zm-side-section"})[
                -1].find_all("div", {"class": "zg-gray-normal"})[1].find("strong").text
        questionInfoDict['questionViewCount'] = bufString
        questionInfoDict['questionIDinQuestionDesc'] = self.get_attr(
            self.content.find("div", {'id': 'zh-single-question-page'}), 'data-urltoken')
        return questionInfoDict


class ParseAnswer(ParseQuestion):
    def getQuestionInfoDict(self):
        questionInfoDict = {}
        bufString = self.content.find("div", {"id": "zh-question-title"}).get_text()
        questionInfoDict['questionTitle'] = bufString
        bufString = self.content.find("a", {"name": "addcomment"}).get_text()
        questionInfoDict['questionCommentCount'] = self.match_int(bufString)
        questionInfoDict['questionDesc'] = self.get_tag_content(
            self.content.find("div", {"id": "zh-question-detail"}).find('div'))
        bufString = self.content.find("div", {"class": "zh-answers-title"}).find('a', {
            'class': 'zg-link-litblue'}).get_text()
        questionInfoDict['questionAnswerCount'] = self.match_int(bufString)

        bufString = self.content.find("div", {"id": "zh-question-side-header-wrap"}).find("div", {
            "class": "zg-gray-normal"}).a.strong.text
        questionInfoDict['questionFollowCount'] = self.match_int(bufString)
        bufString = self.content.find("div", {"id": "zh-question-side-header-wrap"}).find("div", {
            "class": "zg-gray-normal"}).a.strong.text
        questionInfoDict['questionViewCount'] = self.match_int(bufString)
        bufString = self.content.find("div", {"class": "zu-main-sidebar"}).find("div",
                                                                                {"class": "zm-side-section"}).find(
            "div", {"class": "zg-gray-normal"}).find("strong").text
        questionInfoDict['questionViewCount'] = bufString
        rawLink = self.get_attr(self.content.find("link", {'rel': 'canonical'}), 'href')
        questionInfoDict['questionIDinQuestionDesc'] = self.matchQuestionID(rawLink)
        return questionInfoDict

    def getAnswerContentList(self):
        return self.content.find_all("div", {"id": "zh-question-answer-wrap"})


class ParseAuthor(Parse):
    u'''
    输入网页内容，返回一个dict，答案dict列表
    '''

    def getAnswerContentList(self):
        u"""
        返回答案内容列表
        用户界面中一定会有#zh-profile-answer-list元素
        所以不必担心
        """
        return self.content.find(id="zh-profile-answer-list").find_all("div", {"class": "zm-item"})

    def getInfoDict(self):
        contentList = self.getAnswerContentList()
        answerDictList = []
        questionInfoDictList = []
        for content in contentList:
            answerDict = self.getAnswerDict(content)
            if len(answerDict['answerID']) == 0:
                continue
            answerDictList.append(answerDict)
            lastQuestionInfoDict = {}
            if len(questionInfoDictList) > 0:
                lastQuestionInfoDict = questionInfoDictList[
                    -1]  # 在话题和收藏夹里，同一问题下的答案会被归并到一起，造成questionDict信息丢失，所以需要额外传入问题信息数据
            questionInfoDictList.append(self.getQuestionInfoDict(content, lastQuestionInfoDict))
        return questionInfoDictList, answerDictList

    def getQuestionInfoDict(self, content, lastQuestionInfoDict={}):
        questionInfoDict = {}
        questionTitle = content.find("a", {'class': "question_link"})
        if questionTitle is None:
            return lastQuestionInfoDict
        questionInfoDict['questionTitle'] = questionTitle.get_text()
        rawLink = self.get_attr(content.find("a", {'class': "question_link"}), 'href')
        questionInfoDict['questionIDinQuestionDesc'] = self.matchQuestionID(rawLink)
        return questionInfoDict


class ParseCollection(ParseAuthor):
    u"""
    直接继承即可
    """

    def getAnswerContentList(self):
        return self.content.find_all("div", {"class": "zm-item"})

    def getQuestionInfoDict(self, content, lastQuestionInfoDict={}):
        questionInfoDict = {}
        questionTitle = content.find('h2', {'class': 'zm-item-title'})
        if questionTitle is None:
            return lastQuestionInfoDict
        questionInfoDict['questionTitle'] = content.find('h2', {'class': 'zm-item-title'}).get_text()
        rawLink = self.get_attr(content.find('h2', {'class': 'zm-item-title'}).a, 'href')
        questionInfoDict['questionIDinQuestionDesc'] = self.matchQuestionID(rawLink)
        return questionInfoDict


class ParseTopic(ParseAuthor):
    def getAnswerContentList(self):
        return self.content.find("div", {"id": "zh-topic-top-page-list"}).find_all("div", {"itemprop": "question"})


'''
class ParseColumn:
class ParseTable:
'''


# ParseFrontPageInfo
class AuthorInfoParse(Parse):
    u'标准网页：/about'

    def getInfoDict(self):
        infoDict = {}

        infoDict['dataID'] = self.get_attr(self.content.find("button", {'class': 'zm-rich-follow-btn'}), 'data-id')
        infoDict['authorLogoAddress'] = self.get_attr(self.content.find('img', {'class': 'avatar-l'}), 'src')
        infoDict['weiboAddress'] = self.get_attr(self.content.find('a', {'class': 'zm-profile-header-user-weibo'}),
                                                 'href')
        infoDict['watched'] = self.match_int(
            self.content.find_all('div', {'class': 'zm-side-section-inner'})[-1].span.strong.get_text())
        infoDict['authorID'] = self.match_author_id(
            self.get_attr(self.content.find('div', {'class': 'title-section'}).a, 'href'))
        infoDict['name'] = self.content.find('div', {'class': 'title-section'}).find(attrs={'class': 'name'}).get_text()
        infoDict['sign'] = self.get_attr(
            self.content.find('div', {'class': 'title-section'}).find(attrs={'class': 'bio'}), 'title')

        try:
            infoDict['desc'] = self.content.find('div', {'class': 'zm-profile-header-description'}).find('span', {
                'class': 'fold-item'}).get_text()
        except AttributeError:
            infoDict['desc'] = ''

        infoList = self.content.find('div', {'class': 'profile-navbar'}).find_all('span', {'class': 'num'})
        kindList = ['ask', 'answer', 'post', 'collect', 'edit']
        i = 0
        for kind in kindList:
            infoDict[kind] = self.match_int(self.get_tag_content(infoList[i]))
            i += 1

        infoList = self.content.find('div', {'class': 'zm-profile-side-following'}).find_all('a', {'class': 'item'})
        infoDict['followee'] = self.match_int(infoList[0].get_text())
        infoDict['follower'] = self.match_int(infoList[1].get_text())

        infoList = self.content.find('div', {'class': 'zm-profile-details-reputation'}).find_all('i', {
            'class': 'zm-profile-icon'})
        kindList = ['agree', 'thanks', 'collected', 'shared']
        i = 0
        for kind in kindList:
            infoDict[kind] = self.match_int(self.get_tag_content(infoList[i]))
            i += 1
        return infoDict


class TopicInfoParse(Parse):
    u'标准网页:正常值'

    def getInfoDict(self):
        infoDict = {}
        infoDict['title'] = self.content.find('h1', {'class': 'zm-editable-content'}).get_text()
        infoDict['description'] = self.get_tag_content(
            self.content.find('div', {'id': 'zh-topic-desc'}).find('div', 'zm-editable-content'))
        infoDict['topicID'] = self.match_int(
            self.get_attr(self.content.find('a', {'id': 'zh-avartar-edit-form'}), 'href'))
        infoDict['logoAddress'] = self.get_attr(self.content.find('img', {'class': 'zm-avatar-editor-preview'}), 'src')
        infoDict['logoAddress'] = self.match_int(
            self.get_tag_content(self.content.find('div', {'class': 'zm-topic-side-followers-info'})))
        return infoDict


class CollectionInfoParse(Parse):
    u'标准网页:正常值'

    def getInfoDict(self):
        infoDict = {}
        infoDict['title'] = self.get_tag_content(self.content.find('h2', {'id': 'zh-fav-head-title'}))
        infoDict['description'] = self.get_tag_content(self.content.find('div', {'id': 'zh-fav-head-description'}))
        infoDict['collectionID'] = self.match_int(
            self.get_attr(self.content.find('div', {'id': 'zh-list-meta-wrap'}).find_all('a')[1], 'href'))
        infoDict['commentCount'] = self.match_int(self.get_tag_content(
            self.content.find('div', {'id': 'zh-list-meta-wrap'}).find('a', {'name': 'addcomment'})))
        infoDict['followerCount'] = self.match_int(
            self.content.find_all('div', {'class': 'zm-side-section'})[2].find_all('div', {'class': 'zg-gray-normal'})[
                1].a.get_text())

        infoDict['authorID'] = self.match_author_id(
            self.get_attr(self.content.find('a', {'class': 'zm-list-avatar-link'}), 'href'))
        infoDict['authorSign'] = self.content.find('div', {'id': 'zh-single-answer-author-info'}).find('div',
                                                                                                       'zg-gray-normal').get_text()
        infoDict['authorName'] = self.content.find('div', {'id': 'zh-single-answer-author-info'}).a.get_text()
        return infoDict
