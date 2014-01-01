import os.path
import unittest

from wpull.document import HTMLScraper
from wpull.http import Request, Response, Body
import wpull.util
import shutil


class TestDocument(unittest.TestCase):
    def test_html_scraper_links(self):
        scraper = HTMLScraper()
        request = Request.new('http://example.com/')
        response = Response('HTTP/1.0', 200, 'OK')

        with wpull.util.reset_file_offset(response.body.content_file):
            html_file_path = os.path.join(os.path.dirname(__file__),
                'testing', 'samples', 'many_urls.html')
            with open(html_file_path, 'rb') as in_file:
                shutil.copyfileobj(in_file, response.body.content_file)

        inline_urls, html_urls = scraper.scrape(request, response)

        self.assertEqual({
            'http://example.com/style_import_url.css',
            'http://example.com/style_import_quote_url.css',
            'http://example.com/style_single_quote_import.css',
            'http://example.com/style_double_quote_import.css',
            'http://example.com/link_href.css',
            'http://example.com/script.js',
            'http://example.com/body_background.png',
            'http://example.com/images/table_background.png',
            'http://example.com/images/td_background.png',
            'http://example.com/images/th_background.png',
            'http://example.com/style_url1.png',
            'http://example.com/style_url2.png',
            'http://example.com/applet/',  # returned by lxml
            'http://example.com/applet/applet_code.class',
            'http://example.com/applet/applet_src.class',
            'http://example.com/bgsound.mid',
            'http://example.com/audio_src.wav',
            'http://example.net/source_src.wav',
            'http://example.com/embed_src.mov',
            'http://example.com/fig_src.png',
            'http://example.com/frame_src.html',
            'http://example.com/iframe_src.html',
            'http://example.com/img_href.png',
            'http://example.com/img_lowsrc.png',
            'http://example.com/img_src.png',
            'http://example.com/input_src.png',
            'http://example.com/layer_src.png',
            'http://example.com/object/',  # returned by lxml
            'http://example.com/object/object_data.swf',
            'http://example.com/object/object_archive.dat',
            'http://example.com/overlay_src.html',
            },
            inline_urls
        )
        self.assertEqual({
            'http://example.net/soup.html',
            'http://example.com/a_href.html',
            'http://example.com/area_href.html',
            'http://example.com/frame_src.html',
            'http://example.com/embed_href.html',
            'http://example.com/embed_src.mov',
            'http://example.com/iframe_src.html',
            'http://example.com/layer_src.png',
            'http://example.com/overlay_src.html',
            },
            html_urls
        )

    def test_html_soup(self):
        scraper = HTMLScraper()
        request = Request.new('http://example.com/')
        response = Response('HTTP/1.0', 200, '')

        with wpull.util.reset_file_offset(response.body.content_file):
            html_file_path = os.path.join(os.path.dirname(__file__),
                'testing', 'samples', 'soup.html')
            with open(html_file_path, 'rb') as in_file:
                shutil.copyfileobj(in_file, response.body.content_file)

        inline_urls, html_urls = scraper.scrape(request, response)

        self.assertEqual(
            {'http://example.com/ABOUTM~1.JPG'},
            inline_urls
        )
        self.assertEqual(
            {'http://example.com/BLOG'},
            html_urls
        )
