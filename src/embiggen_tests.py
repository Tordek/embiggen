import unittest
from embiggen import embiggen
from nose.tools import assert_equals

def test_embiggen():
    test_cases = [{ 'short': 'br',
                    'embiggened': '<br/>\n'
                  }, {'short': 'br#id',
                      'embiggened': '<br id="id"/>\n'
                  }, {'short': 'br#id.class',
                      'embiggened': '<br class="class" id="id"/>\n'
                  }, {'short': 'br#id.class1.class2',
                      'embiggened': '<br class="class1 class2" id="id"/>\n'
                  }, {'short': 'br.class1.class2',
                      'embiggened': '<br class="class1 class2"/>\n'
                  }, {'short': 'div',
                      'embiggened': '<div>\n\t\n</div>\n'
                  }, {'short': 'a[href=http://tordek.com.ar]',
                      'embiggened': '<a href="http://tordek.com.ar">\n\t\n</a>\n'
                  }, {'short': 'a[href=http://tordek.com.ar]{ My Homepage }',
                      'embiggened': '<a href="http://tordek.com.ar">\n\tMy Homepage\n</a>\n'
                  }, {'short': 'div#header + div#footer',
                      'embiggened': '<div id="header">\n\t\n</div>\n<div id="footer">\n\t\n</div>\n'
                  }, {'short': 'h1[title]',
                      'embiggened': '<h1 title="">\n\t\n</h1>\n'
                  }, {'short': 'div > span { content } + span { content 2 } < div',
                      'embiggened': '<div>\n\t\n\t<span>\n\t\tcontent\n\t</span>\n\t<span>\n\t\tcontent 2\n\t</span>\n</div>\n<div>\n\t\n</div>\n'
                  }]

    for test_case in test_cases:
        yield check_embiggen, test_case['short'], test_case['embiggened']

def check_embiggen(short, embiggened):
    assert_equals(embiggened, embiggen(short))
