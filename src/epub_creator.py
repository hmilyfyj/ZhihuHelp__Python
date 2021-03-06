# -*- coding: utf-8 -*-

from rawbook import RawBook
from epub import Book
from src.tools.debug import Debug
from src.tools.extra_tools import ExtraTools
from src.tools.path import Path


class EpubCreator(object):
    """
    一次只做一本书
    而且只做知乎相关书目
    """

    def __init__(self, epub_book):
        self.book = epub_book
        self.book_list = epub_book.book_list
        self.image_container = epub_book.image_container
        return

    def create(self):
        self.image_container.set_save_path(Path.image_pool_path)
        self.image_container.start_download()
        title = '_'.join([book.property.epub.title for book in self.book_list])
        title = title.strip()
        Path.chdir(Path.base_path + u'/知乎电子书临时资源库/')
        epub = Book(title, 27149527)
        html_tmp_path = Path.html_pool_path + '/'
        image_tmp_path = Path.image_pool_path + '/'
        for book in self.book_list:
            page = book.page_list[0]
            with open(html_tmp_path + page.filename, 'w') as html:
                html.write(page.content)
            epub.createChapter(html_tmp_path + page.filename, ExtraTools.get_time(), page.title)

            for page in book.page_list[1:]:
                with open(html_tmp_path + page.filename, 'w') as html:
                    html.write(page.content)
                epub.addHtml(html_tmp_path + page.filename, page.title)
        for image in self.book['image_list']:
            epub.addImg(image_tmp_path + image['filename'])
        epub.addLanguage('zh-cn')
        epub.addCreator('ZhihuHelp1.7.0')
        epub.addDesc(u'该电子书由知乎助手生成，知乎助手是姚泽源为知友制作的仅供个人使用的简易电子书制作工具，源代码遵循WTFPL，希望大家能认真领会该协议的真谛，为飞面事业做出自己的贡献 XD')
        epub.addRight('CC')
        epub.addPublisher('ZhihuHelp')
        Debug.logger.debug(u'当前目录为')
        Path.pwd()
        epub.addCss(Path.base_path + u'/epubResource/markdown.css')
        epub.addCss(Path.base_path + u'/epubResource/front.css')
        epub.buildingEpub()
        return


def create_epub(task_package):
    """
    传入的为一个list的电子书，不能明确电子书的种类，也不能知道list中有多少电子书
    所以最终生成的时候，需要将所有电子书都合并在一个包里，每本书为一个章节
    """
    raw_book = RawBook(task_package.book_list)
    epub_book_list = raw_book.get_book_list()
    for book in epub_book_list:
        epub = EpubCreator(book)
        epub.create()
    return
