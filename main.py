# -*- coding: utf-8 -*-

import cgi
import os
import re
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from parts_editor import *
import v3editor as V3

# vocarus.net/
class IndexPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/index.html')
        self.response.out.write(template.render(path, template_values))


# vocarus.net/service
class ContentPage1(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/service.html')
        self.response.out.write(template.render(path, template_values))

# vocarus.net/howtouse
class ContentPage2(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/howtouse.html')
        self.response.out.write(template.render(path, template_values))


# vocarus.net/contact
class ContentPage3(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/contact.html')
        self.response.out.write(template.render(path, template_values))


# Failed to parse vsq/vsqx ==> parse error
class ParseError1(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/parse_error.html')
        self.response.out.write(template.render(path, template_values))


# Failed to parse vsq/vsqx ==> file not found
class ParseError2(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/parse_notfound.html')
        self.response.out.write(template.render(path, template_values))


# vocarus.net/parse
class ParsePage(webapp.RequestHandler):
    def post(self):
        data = self.request.get('file')
        try:
            """Exceptions
            AttributeError: ファイル選択せずUpload
            TypeError     :
            IndexError    : 違う形式のファイルUpload
            KeyError      : vsqファイルの破損
            """
            file_name = self.request.body_file.vars['file'].filename.encode('utf-8')
            is_score = False
            
            if self.request.POST.has_key('chorus1'):
                parts = 1
            elif self.request.POST.has_key('chorus2'):
                parts = 2
            elif self.request.POST.has_key('chorus3'):
                parts = 3
            elif self.request.POST.has_key('lyric_card'):
                parts = 0
                is_score = True

            ### ChordText (VSQ)
            if is_score == True:
                editor = PartsEditor(parts, binary = data)
                self.response.headers['Content-Type'] = 'application/x-vsq; charset=Shift_JIS'
                self.response.headers['Content-disposition'] = (
                u'filename=' + (os.path.splitext(file_name.encode('utf-8'))[0])+u'.txt')
                self.response.out.write(editor.generate_chordtext())
            ### ChordText (VSQX)
                ''' FIXME
            elif (is_score == True and
                  re.search('.+\.[vV][sS][qQ][xX]$', file_name)):
                print("FIXME")
                '''
            ### VSQX
            elif re.search('.+\.[vV][sS][qQ][xX]$', file_name):
                self.response.headers['Content-Type'] = 'application/x-vsq; charset=Shift_JIS'
                self.response.headers['Content-disposition'] = (
                    u'filename=' + (os.path.splitext(file_name.encode('utf-8'))[0])+u' [part%d].vsqx' % parts)
                self.response.out.write(V3.V3Editor(data, parts).parse())
            ### VSQ
            else:
                editor = PartsEditor(parts, binary = data)
                memcache.set_multi(
                    {"editor": editor, "name": file_name, "part": parts},
                    key_prefix="vsq_",
                    time=3600)
                template_values = {
                    'parts' : parts,
                    'editor' : editor,
                    'dd' : 2 ** editor.dd}
                variable.nn = editor.nn
                variable.dd = 2**editor.nn
                self.response.headers['Content-Type'] = 'application/x-vsq; charset=Shift_JIS'
                self.response.headers['Content-disposition'] = (
                    u'filename=' + (os.path.splitext(file_name.encode('utf-8'))[0])+u' [part%d].vsq' % parts)
                self.response.out.write(editor.unparse())
        except (AttributeError): # file is not found
            template_values = { }
            path = os.path.join(os.path.dirname(__file__), 'html/parse_notfound.html')
            self.response.out.write(template.render(path, template_values))
        except (ValueError): # file is too big
            template_values = { }
            path = os.path.join(os.path.dirname(__file__), 'html/parse_toobig.html')
            self.response.out.write(template.render(path, template_values))
        except: # else
            template_values = { }
            path = os.path.join(os.path.dirname(__file__), 'html/parse_error.html')
            self.response.out.write(template.render(path, template_values))


# vocarus.net/download
class DownloadPage(webapp.RequestHandler):
    def post(self):
        editor = memcache.get('vsq_editor')
        file_name = memcache.get('vsq_name')
        if editor is None or file_name is None:
            print 'Content-Type: text/plain'
            print ''
            print '<p>セッション切れです。\
                     <a href='/'>トップ</a>へ戻ってもう一度作業してください。</p>'
        else:
            self.response.headers['Content-Type'] = 'application/x-vsq; charset=Shift_JIS'
            self.response.headers['Content-disposition'] = (
                u'filename=' + file_name.encode('utf-8'))
            self.response.out.write(editor.unparse())


# Pages
application = webapp.WSGIApplication(
                [('/', IndexPage),
                ('/service', ContentPage1),
                ('/howtouse', ContentPage2),
                ('/contact', ContentPage3),
                ('/parse', ParsePage),
                ('/parse_error', ParseError1),
                ('/parse_error', ParseError2),
                ('/download', DownloadPage)],
                debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
