import unittest
import subprocess
import os


def _run_twitter_insight(args):
    """
    Runs the twitter-insight program with the given args.
    """
    cmd = ['python3', 'twitter-insight.py'] + args
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class TestTwitterInsight(unittest.TestCase):

    def test_help(self):
        """
        Tests the help command.
        """

        expected = \
            b'''Usage:

twitter-insight.py <hashtag>

Do remember to set the envrinment variables.\n'''

        result = _run_twitter_insight([])
        self.assertEqual(result.returncode, -1)
        self.assertEqual(result.stderr, expected)

    def test_hashtag(self):
        """
        Tests the hashtag command.
        """

        result = _run_twitter_insight(['test'])
        self.assertEqual(result.returncode, 0)

    def test_hashtag_no_env(self):
        """
        Tests the hashtag command with no environment variables.
        """

        for envvar in ['GOOGLE_APPLICATION_CREDENTIALS', 'TWITTER_CONSUMER_KEY', 'TWITTER_CONSUMER_SECRET', 'TWITTER_ACCESS_KEY', 'TWITTER_ACCESS_SECRET']:
            envvar_val = os.environ.pop(envvar, None)
            result = _run_twitter_insight(['test'])
            self.assertEqual(result.returncode, -1)
            os.environ[envvar] = envvar_val


def _main():
    unittest.main()


if __name__ == '__main__':
    _main()
