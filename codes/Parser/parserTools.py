__author__ = 'yao'

import re
import HTMLParser  # 转换网页代码
import datetime  # 简单处理时间




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
