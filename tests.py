import unittest
from unittest import TestCase
from proxy import process_page_links, add_copyright_symbol_to_6_letters_words, TARGET_SERVER_BASE_URL


class TestLinkProcessing(TestCase):
    def setUp(self) -> None:
        self.target_host = TARGET_SERVER_BASE_URL
        self.proxy_host = 'http://localhost:8585/'

    def test_change_links_which_needed(self):
        sample = f'<a href="{self.target_host}bla_bla/">link</a>bla bla bla'
        result = process_page_links(sample, self.target_host, self.proxy_host)
        self.assertEqual(f'<a href="{self.proxy_host}bla_bla/">link</a>bla bla bla', result)

    def test_not_changed_links_not_target_host(self):
        sample = f'<a href="https://example.com/bla_bla/">link</a>bla bla bla'
        result = process_page_links(sample, self.target_host, self.proxy_host)
        self.assertEqual(sample, result)

    def test_broken_links_without_href_will_be_same_and_not_raise_error(self):
        sample = f'<a>link</a>bla bla bla'
        result = process_page_links(sample, self.target_host, self.proxy_host)
        self.assertEqual(sample, result)


class TestTextMutation(TestCase):
    def test_add_symbol_to_6_letters_word(self):
        sample = '<p>worked</p>'

        result = add_copyright_symbol_to_6_letters_words(sample)

        self.assertEqual('<p>worked™</p>', result)

    def test_add_symbol_to_6_letters_word_inside_html(self):
        sample = '<html><body>bla mother bla bla worked worked bla badaaboooka</body></html>'
        result = add_copyright_symbol_to_6_letters_words(sample)
        self.assertEqual('<html><body>bla mother™ bla bla worked™ worked™ bla badaaboooka</body></html>', result)

    def test_not_add_additional_symbol_to_tags(self):
        sample = '<mark> bla bla </mark> <strike> bla </strike>'
        result = add_copyright_symbol_to_6_letters_words(sample)
        self.assertEqual(sample, result)

    def test_can_process_text_on_different_levels_dom(self):
        sample = '<html><body>bla change <p> mother bla<span>Victor</span> bla </p>worked bla</body></html>'
        result = add_copyright_symbol_to_6_letters_words(sample)
        self.assertEqual(
            '<html><body>bla change™ <p> mother™ bla<span>Victor™</span> bla </p>worked™ bla</body></html>', result
        )

    def test_work_well_with_multiline_html(self):
        sample = '<html><body>\nbla change \n<p> mother\n bla<span>Victor</span> bla \n</p>\nworked bla</body></html>'
        result = add_copyright_symbol_to_6_letters_words(sample)
        self.assertEqual(
            '<html><body>\nbla change™ \n<p> mother™\n bla<span>Victor™</span> bla \n</p>\nworked™ bla</body></html>',
            result
        )

    def test_dont_change_anything_inside_script_tag(self):
        sample = ('<html><body><script>function () { var b= "<p>test</p>"; return 0 }</script>'
                  'bla mother bla bla worked worked bla badaaboooka</body></html>')
        result = add_copyright_symbol_to_6_letters_words(sample)
        self.assertEqual('<html><body><script>function () { var b= "<p>test</p>"; return 0 }</script>'
                         'bla mother™ bla bla worked™ worked™ bla badaaboooka</body></html>', result)


if __name__ == '__main__':
    unittest.main()
