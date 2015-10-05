# -*- coding: utf-8 -*-

from worker import *
from init import *
from login import *
from simpleFilter import *
from epubBuilder.epubBuilder import *
from readListParser import ReadListParser


class ZhihuHelp(BaseClass):
    def __init__(self):
        u"""
        配置文件使用$符区隔，同一行内的配置文件归并至一本电子书内
        """
        if TestClass.test_catchAnswerData_flag:
            print u'测试期间，移除检查更新模块，测试完成后请删除'
        else:
            self.checkUpdate()
        init = Init()
        self.conn = init.getConn()
        self.cursor = self.conn.cursor()
        self.baseDir = os.path.realpath('.')
        self.config = Setting()
        self.commandParser = ReadListParser()
        return

    def baseConfig(self):
        u"""
        登陆以及进行基础设置
        """
        # 登陆
        login = Login(self.conn)
        if SettingClass.REMEMBERACCOUNT:
            print   u'检测到有设置文件，是否直接使用之前的设置？(帐号、密码、图片质量、最大线程数)'
            print   u'直接点按回车使用之前设置，敲入任意字符后点按回车进行重新设置'
            if raw_input() == '':
                login.setCookie()
            else:
                login.login()
                SettingClass.MAXTHREAD = self.config.guideOfMaxThread()
                SettingClass.PICQUALITY = self.config.guideOfPicQuality()
        else:
            login.login()
            SettingClass.MAXTHREAD = self.config.guideOfMaxThread()
            SettingClass.PICQUALITY = self.config.guideOfPicQuality()
        # 储存设置
        self.config.save()
        return

    def helperStart(self):
        self.baseConfig()
        # 主程序开始运行
        BaseClass.logger.info(u"开始读取ReadList.txt设置信息")
        readList = open('./ReadList.txt', 'r')
        bookCount = 1

        for line in readList:
            # 一行内容代表一本电子书
            chapter = 1
            BaseClass.logger.info(u"正在制作第 {0} 本电子书".format(bookCount))
            commandInfoDict = self.commandParser.parseCommandLine(line)
            WorkerFactory(self.conn, commandInfoDict)
            BaseClass.logger.info(u"电子书数据抓取完毕，开始生成电子书")

            try:
                if self.epubContent:
                    Zhihu2Epub(self.epubContent)
                del self.epubContent
            except AttributeError:
                pass
            BaseClass.logger.info(u"第 {0} 本电子书生成完毕".format(bookCount))
            self.resetDir()
            bookCount += 1
        return

    def resetDir(self):
        chdir(self.baseDir)
        return

    def checkUpdate(self):  # 强制更新
        u"""
            *   功能
                *   检测更新。
                *   若在服务器端检测到新版本，自动打开浏览器进入新版下载页面
                *   网页请求超时或者版本号正确都将自动跳过
            *   输入
                *   无
            *   返回
                *   无
        """
        print   u"检查更新。。。"
        try:
            updateTime = urllib2.urlopen(u"http://zhihuhelpbyyzy-zhihu.stor.sinaapp.com/ZhihuHelpUpdateTime.txt",
                                         timeout=10)
        except:
            return
        time = updateTime.readline().replace(u'\n', '').replace(u'\r', '')
        url = updateTime.readline().replace(u'\n', '').replace(u'\r', '')
        updateComment = updateTime.read()
        if time == SettingClass.UPDATETIME:
            return
        else:
            print u"发现新版本，\n更新说明:{}\n更新日期:{} ，点按回车进入更新页面".format(updateComment, time)
            print u'新版本下载地址:' + url
            raw_input()
            import webbrowser
            webbrowser.open_new_tab(url)
        return
