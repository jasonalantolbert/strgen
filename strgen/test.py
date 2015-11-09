# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
from strgen import StringGenerator



class TestStringGenerator(unittest.TestCase):

    def test_string_generator(self):
        """Test various templates."""
        test_list = [
            u"[a-z][\c]{10}(.|_)[\c]{5:10}@[\c]{3:12}.(com|net|org)",
            u"[\[\]\(\)\{\}\&\|\-\$_+=;\'\"<>,.?:!#%^`~*@\\\]{4}",
            u"[a-z\d\d\d\d]{8}",
            u"[\l]{6:10}&[\d]{2}",
            u"([a-z]{4}|[0-9]{9})",
            u"[\d]&[\c]&[\w\p]{6}",
        ]

        for t in test_list:
            result = StringGenerator(t).render()
            print(u"%s == %s" % (t, result))
            self.assertTrue(not result is None)

    def test_unicode(self):
        test_list = [
            u'idzie wąż wąską dróżką',
            u'༣ཁངཱུངྵ',
            u'ᚠᚳᛦᛰ',
            u'[ą-ż]{8}',
            u'\xe6\xbf\xe5, \xe9\xe5\xa9\xe5\xe5\xad\xe6\xaf\xe7\xe9\xba\xbc\xe6\xe6',
        ]

        for t in test_list:
            result = StringGenerator(t).render()
            print(u"%s == %s" % (t, result))
            # TODO: must be a better test than testing for None
            self.assertTrue(not result is None)

    def test_list(self):
        list_length = 10
        test_list = [
            u"[a-z][\c]{10}(.|_)[\c]{5:10}@[\c]{3:12}.(com|net|org)",
            u"[a-z\d\d\d\d]{8}",
            u"[\l]{6:10}&[\d]{2}",
            u"[\l]{6-10}&[\d]{2}",  # support both hyphen and colon for ranges
            u"([a-z]{4}|[0-9]{9})",
            u"[\d]&[\c]&[\w\p]{6}",
            u"[\w\p]",
            u"[\w\p]{6}",
            u"[\w\p]{-6},"
            u"[\w\p]{:6}",
            u"[\w\p]{0:6}",
        ]

        for t in test_list:
            result = StringGenerator(t).render_list(list_length)
            print("Pattern [{}] list length == {}".format(t, len(result)))
            self.assertTrue(isinstance(result, list) and len(result) == list_length)

    def test_syntax_exception(self):
        """Make sure syntax errors in template are caught."""
        test_list = [
            u"[a-z]{a}",  # not a valid quantifier
            u"[a-]",  # invalid class range
            u"[[1-9]",  # unescaped chars
            u"((foo)(bar)))",  # extra parens
            u"foo&",  # binary operator error
            u"|foo",  # binary operator error
            u"[\w]{10:}",  # cannot have open range in quantifier
        ]
        for t in test_list:
            # using 2.7 specific context manager here
            # so, test won't work on < 2.7 but everything else should do
            #with self.assertRaises(StringGenerator.SyntaxError) as context:
            #    StringGenerator(t).render()
            self.assertRaises(StringGenerator.SyntaxError, lambda: StringGenerator(t).render())
            
            #print("Exception {}: {}".format(t, context.exception))

    def test_uniqueness_error(self):
        """Make sure we throw an exception if we can't generate list."""
        #with self.assertRaises(StringGenerator.UniquenessError) as context:
        #    t = "[123]"
        #    StringGenerator(t).render_list(100, unique=True)
        t = "[123]"
        self.assertRaises(StringGenerator.UniquenessError, lambda: StringGenerator(t).render_list(100, unique=True))
        #print("Exception {}: {}".format(t, context.exception))

if __name__ == '__main__':
    unittest.main()
