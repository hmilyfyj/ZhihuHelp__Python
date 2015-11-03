__author__ = 'yao'

import re
import HTMLParser  # ת����ҳ����
import datetime  # �򵥴���ʱ��




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
        �����ı���ʽ��������������ִ�����û���򷵻�'0'
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
        ֻ������ȡbs��tag.contents�����ݣ���Ҫ�Ҵ���
        ˼·����stackoverflow��http://stackoverflow.com/questions/8112922/beautifulsoup-innerhtml
        ˧��
        """
        return "".join([unicode(x) for x in tag.contents])

    @staticmethod
    def get_attr(self, dom, attr, defaultValue=""):
        u"""
        ��ȡbs��tag.content��ָ������
        ��contentΪ�ջ���û��ָ�������򷵻�Ĭ��ֵ
        """
        if dom == None:
            return defaultValue
        return dom.get(attr, defaultValue)

    @staticmethod
    def parse_date(self, date='1357-08-12'):
        if u'����' in date:
            return self.get_yesterday()
        if u'����' in date:
            return self.get_today()
        return self.match_content(r'\d{4}-\d{2}-\d{2}', date, date)  # һ�����߰�ʮ������ʮһ�������
