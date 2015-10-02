# -*- coding: utf-8 -*-

from baseClass import *


class ImgDownloader(BaseClass, HttpBaseClass):
    u'''
     负责下载图片到指定文件夹内 
    '''

    def __init__(self, targetDir='', imgDict={}):
        u'''
        imgDict中, key为文件名，value为下载地址
        '''
        self.targetDir = targetDir
        self.imgDict = imgDict
        self.waitFor = 20  # 图片动则数M，所以以20s作为超时时间（在100k的网络下20s可以下载2M的图片，够用了）
        self.maxTry = 5
        self.cleanImgDict()

    def leader(self):
        times = 0
        while times < self.maxTry and len(self.imgDict) > 0:
            print u'开始第{}/{}遍图片下载'.format(times, self.maxTry)
            self.downloader()
            times += 1
        print u'所有图片下载完毕'
        return

    def downloader(self):
        u'''
        返回下载成功的图片列表
        '''
        threadPool = []
        for fileName in self.imgDict.keys():
            threadPool.append(threading.Thread(target=self.worker, kwargs={'fileName': fileName}))

        for thread in threadPool:
            ThreadClass.startRegisterThread()
            thread.start()
            ThreadClass.waitForThreadRunningCompleted()
            BaseClass.logger.info(u'正在下载图片，还有{}张图片等待下载'.format(len(self.imgDict)))
        ThreadClass.waitForThreadRunningCompleted(0)  #等待所有线程执行完毕
        return

    def worker(self, fileName=''):
        u"""
        worker只执行一次，待全部worker执行完毕后由调用函数决定哪些worker需要再次运行
        重复的次数由self.maxTry指定
        这样可以给知乎服务器留出生成页面缓存的时间
        """
        link = self.imgDict[fileName]

        threadID = ThreadClass.getUUID()
        BaseClass.logger.debug(u'imgDownloaderWorker开始等待执行， threadID = {}'.format(threadID))
        # todo 此处可以利用闭包实现
        while not ThreadClass.acquireThreadPoolPassport(threadID):
            time.sleep(0.1)
        content = self.getHttpContent(url=link, timeout=self.waitFor)
        if content != '':
            imgFile = open(self.targetDir + fileName, 'wb')
            imgFile.write(content)
            imgFile.close()
            del self.imgDict[fileName]
        ThreadClass.releaseThreadPoolPassport(threadID)
        return

    def cleanImgDict(self):
        u'''
        移除imgDict中已下载过的文件
        '''
        cacheSet = set(os.listdir(self.targetDir))
        for fileName in self.imgDict.keys():
            if fileName in cacheSet:
                del self.imgDict[fileName]
        return