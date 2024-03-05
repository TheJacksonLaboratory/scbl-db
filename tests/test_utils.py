from scbl_db.utils import get_format_string_vars


class TestGetFormatStringVars:
    def test_gets_correct_vars(self):
        assert get_format_string_vars(r'{var0}-{var1}_{var2} {var3}') == {
            'var0',
            'var1',
            'var2',
            'var3',
        }

    def test_repeated_vars(self):
        assert get_format_string_vars(r'{var0}{var0}') == {'var0'}

    def test_ignores_non_vars(self):
        assert get_format_string_vars(r'constant') == set()
