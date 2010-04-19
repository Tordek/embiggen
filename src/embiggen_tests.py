import unittest
from embiggen import embiggen
from nose.tools import assert_equals

def test_embiggen():
    test_cases = [{ 'short': 'br',
                    'embiggened': '<br/>\n'
                  }, {'short': 'br#id',
                      'embiggened': '<br id="id"/>\n'
                  }, {'short': 'br #id',
                      'embiggened': '<br id="id"/>\n'
                  }, {'short': 'br#id.class',
                      'embiggened': '<br class="class" id="id"/>\n'
                  }, {'short': 'br#id.class1.class2',
                      'embiggened': '<br class="class1 class2" id="id"/>\n'
                  }, {'short': 'br.class1.class2',
                      'embiggened': '<br class="class1 class2"/>\n'
                  }, {'short': 'br .class1 .class2',
                      'embiggened': '<br class="class1 class2"/>\n'
                  }, {'short': 'div',
                      'embiggened': '<div>\n\t\n</div>\n'
                  }, {'short': 'a',
                      'embiggened': '<a href=""></a>\n'
                  }, {'short': 'a[href=http://tordek.com.ar]',
                      'embiggened': '<a href="http://tordek.com.ar"></a>\n'
                  }, {'short': 'a[href=http://tordek.com.ar]{ My Homepage }',
                      'embiggened': '<a href="http://tordek.com.ar">My Homepage</a>\n'
                  }, {'short': 'div#header + div#footer',
                      'embiggened': '<div id="header">\n\t\n</div>\n<div id="footer">\n\t\n</div>\n'
                  }, {'short': '#header + #footer',
                      'embiggened': '<div id="header">\n\t\n</div>\n<div id="footer">\n\t\n</div>\n'
                  }, {'short': 'h1[title]',
                      'embiggened': '<h1 title=""></h1>\n'
                  }, {'short': 'div > span { content } + span { content 2 } < div',
                      'embiggened': '<div>\n\t<span>content</span>\n\t<span>content 2</span>\n</div>\n<div>\n\t\n</div>\n'
                  }]

    for test_case in test_cases:
        yield check_embiggen, test_case['short'], test_case['embiggened']

def check_embiggen(short, embiggened):
    assert_equals(embiggened, embiggen(short, '\t', '\n'))

def test_close_tag_comments():
    assert_equals('<div id="tagged">\n\t\n</div><!-- /#tagged -->\n',
                  embiggen('div#tagged', '\t', '\n', True))
