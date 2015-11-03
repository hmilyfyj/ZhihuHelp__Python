from parserTools import ParserTools
from bs4 import BeautifulSoup
from codes.baseClass import *


class AuthorInfo(ParserTools):
    """
    ʵ��һ�ѡ���������֮�������������Ժ�������������5��֮��
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
        self.info['authorName'] = u'�����û�'
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
    ʾ������
    <div tabindex="-1" class="zm-item-answer  zm-item-expanded" itemscope="" itemtype="http://schema.org/Answer" data-aid="23458712" data-atoken="70095598" data-collapsed="0" data-created="1446209879" data-deleted="0" data-helpful="1" data-isowner="0" data-copyable="1">
<a class="zg-anchor-hidden" name="answer-23458712"></a>


<div class="zm-votebar">
<button class="up" aria-pressed="false" title="��ͬ">
<i class="icon vote-arrow"></i>
<span class="label">��ͬ</span>
<span class="count">7</span>
</button>
<button class="down" aria-pressed="false" title="���ԣ�������ʾ�������">
<i class="icon vote-arrow"></i>
<span class="label">���ԣ�������ʾ�������</span>
</button>
</div>


<div class="answer-head">
<div class="zm-item-answer-author-info">
<h3 class="zm-item-answer-author-wrap">


<a data-tip="p$t$abandonstone" class="zm-item-link-avatar" href="/people/abandonstone">
<img src="https://pic2.zhimg.com/9379d0b856df5796b3a21694cee452b5_s.jpg" class="zm-list-avatar" data-source="https://pic2.zhimg.com/9379d0b856df5796b3a21694cee452b5_s.jpg">
</a>



<a data-tip="p$t$abandonstone" href="/people/abandonstone">���۳���</a>��<strong title="INFP ������ֱ �е�ƫ��" class="zu-question-my-bio">INFP ������ֱ �е�ƫ��</strong>

</h3>
</div>
<div class="zm-item-vote-info " data-votecount="7">

<span class="voters">
<span class="user-block"><a data-tip="p$t$wei-yi-jing-58" href="http://www.zhihu.com/people/wei-yi-jing-58" class="zg-link" title="��������">��������</a>��</span><span class="user-block"><a data-tip="p$t$da-shuai-bi-77" href="http://www.zhihu.com/people/da-shuai-bi-77" class="zg-link" title="Freya Zheng">Freya Zheng</a>��</span><span class="user-block"><a data-tip="p$t$weng-weng-46-17" href="http://www.zhihu.com/people/weng-weng-46-17" class="zg-link" title="wEnG WeNg">wEnG WeNg</a></span>
</span>


<a href="javascript:;" class="more"> ������ͬ</a>


</div>
</div>
<div class="zm-item-rich-text js-collapse-body" data-resourceid="7011484" data-action="/answer/content" data-author-name="���۳���" data-entry-url="/question/37011291/answer/70095598">


<div class="zh-summary summary clearfix" style="display:none;">

���Ӳ����еĽY��:��

</div>


<div class="zm-editable-content clearfix">
���Ӳ����еĽY��:��

</div>

</div>
<a class="zg-anchor-hidden ac" name="23458712-comment"></a>
<div class="zm-item-meta zm-item-comment-el answer-actions clearfix">
<div class="zm-meta-panel">

<span class="answer-date-link-wrap">
<a class="answer-date-link meta-item" target="_blank" href="/question/37011291/answer/70095598">������ ���� 20:57</a>
</span>

<a href="#" name="addcomment" class=" meta-item toggle-comment">
<i class="z-icon-comment"></i>3 ������</a>


<a href="#" class="meta-item zu-autohide" name="thanks" data-thanked="false"><i class="z-icon-thank"></i>��л</a>



<a href="#" class="meta-item zu-autohide goog-inline-block goog-menu-button" name="share" role="button" aria-expanded="false" style="-webkit-user-select: none;" tabindex="0" aria-haspopup="true"><div class="goog-inline-block goog-menu-button-outer-box"><div class="goog-inline-block goog-menu-button-inner-box"><div class="goog-inline-block goog-menu-button-caption"><i class="z-icon-share"></i>����</div><div class="goog-inline-block goog-menu-button-dropdown">&nbsp;</div></div></div></a>
<a href="#" class="meta-item zu-autohide" name="favo">
<i class="z-icon-collect"></i>�ղ�</a>




<span class="zg-bull zu-autohide">?</span>

<a href="#" name="nohelp" class="meta-item zu-autohide">û�а���</a>

<span class="zg-bull zu-autohide">?</span>
<a href="#" name="report" class="meta-item zu-autohide goog-inline-block goog-menu-button" role="button" aria-expanded="false" style="-webkit-user-select: none;" tabindex="0" aria-haspopup="true"><div class="goog-inline-block goog-menu-button-outer-box"><div class="goog-inline-block goog-menu-button-inner-box"><div class="goog-inline-block goog-menu-button-caption">�ٱ�</div><div class="goog-inline-block goog-menu-button-dropdown">&nbsp;</div></div></div></a>



<span class="zg-bull">?</span>

<a href="/terms#sec-licence-1" target="_blank" class="meta-item copyright"> ���߱���Ȩ�� </a>



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
        self.info['noRecordFlag'] = int(u'��ֹת��' in no_record_flag)
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


class Question(ParserTools):
    u"""
    ��ָQuestion��SingleAnswer�е�Question��Ϣ
    """

    def __init__(self, dom=None):
        self.set_dom(dom)
        return

    def set_dom(self, dom):
        self.info = {}
        if not (dom is None):
            self.title = dom.find('div', id='zh-question-title')
            self.detail = dom.find('div', id='zh-question-detail')
            self.comment = dom.find('div', id='zh-question-meta-wrap')
            # ��ץȡ�ش�������ͽ�����Ӷ�
            self.side_bar = dom.find('div', class_='zh-question-followers-sidebar')  # ȡ�������ע��
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        self.parse_title()
        self.parse_detail()
        self.parse_comment()
        self.parse_follower()
        return

    def parse_title(self):
        self.info['title'] = self.title.text()
        return

    def parse_detail(self):
        self.info['desc'] = self.detail.text()
        return

    def parse_comment(self):
        comment_count = self.comment.find('a', name='addcomment').text()
        self.info['commentCount'] = self.match_int(comment_count)
        return

    def parse_follower(self):
        follower_count = self.side_bar.find('div', class_='zh-question-followers-sidebar').text()
        self.info['followerCount'] = self.match_int(follower_count)
        return


class BaseParser(ParserTools):
    author_info_parser = AuthorInfo()
    answer_parser = Answer()
    question_parser = Question()

    def __init__(self, content):
        BaseClass.logger.debug(u"��ʼ������ҳ")
        self.dom = BeautifulSoup(content, 'html.parser')

    def get_answer_list(self):
        u"""
        �������ܣ���ȡ���б�
        ������
        """
        return

    def get_extro_info(self):
        """
        ��չ���ܣ���ȡ������Ϣ
        ������
        """
        return
