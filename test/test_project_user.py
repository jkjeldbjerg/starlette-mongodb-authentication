""" Unit test of static methods for ProjectUser """

import unittest

from authentication.project_user import ProjectUser, generate_set


class ProjectUserTest(unittest.TestCase):

    password_tests: list = [
        {'pwd': '', 'flag': None},
        {'pwd': 'shA1!', 'flag': 'short'},
        {'pwd': 'lowercase', 'flag': 'only_lower'},
        {'pwd': 'UPPERCASE', 'flag': 'only_upper'},
        {'pwd': '1234567890', 'flag': 'only_digits'},
        {'pwd': '#€%&/()"€;:_.,', 'flag': 'only_symbols'},
        {'pwd': 'ASDFAG€%"#€%623', 'flag': 'no_lower'},
        {'pwd': 'sdfas€%€%gfb234', 'flag': 'no_upper'},
        {'pwd': 'dafdERETye234', 'flag': 'no_symbols'},
        {'pwd': 'dDgERghFBsfge42%fbsdf&', 'flag': None}
    ]

    def test_password_encode_decode(self):
        """ test the coding and decoding of a password (slow!) """
        for case in ProjectUserTest.password_tests:
            encoded = ProjectUser.encode_password(case['pwd'])
            assert type(encoded) is str
            assert ProjectUser.check_password(case['pwd'], encoded)

    def test_password_quality(self):
        """ test the results from password quality method """
        for case in ProjectUserTest.password_tests:
            result: dict = ProjectUser.password_quality(case['pwd'])
            assert result[case['flag']] if case['flag'] is not None else True, \
                f"Found case: {case['pwd']} : {case['flag']} : {result[case['flag']]}"

    def test_generate_set(self):
        """ test that the generate_set function produces the correct set """
        sets: [set] = [
            {'A', 'a', 'C', '1234'},
            {'D'}
        ]
        for test_set in sets:
            test_str: str = ' '.join(test_set) if len(test_set) > 0 else ''
            generated = generate_set({'s': test_str}, 's')
            assert generated == test_set
        assert len(generate_set({'s': set()}, 's')) == 0


if __name__ == '__main__':
    unittest.main()
