import unittest
from embiggen import embiggen
from nose.tools import assert_equals

def test_embiggen():
    test_cases = [{ 'short': 'br',
                    'embiggened': '<br/>'
                  }, {'short': 'br#id',
                      'embiggened': '<br id="id"/>'
                  }, {'short': 'br#id.class',
                      'embiggened': '<br class="class" id="id"/>'
                  }, {'short': 'br#id.class1.class2',
                      'embiggened': '<br class="class1 class2" id="id"/>'
                  }, {'short': 'br.class1.class2',
                      'embiggened': '<br class="class1 class2"/>'
                  }]

    for test_case in test_cases:
        yield check_embiggen, test_case['short'], test_case['embiggened']

def check_embiggen(short, embiggened):
    assert_equals(embiggened, embiggen(short))
