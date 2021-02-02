"""
Main class to run the collection of bots.
"""

__author__ = "Inanc Gurkan"
__copyright__ = "Copyright 2021, inancg"
__credits__ = ["Inanc Gurkan"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Inanc Gurkan"
__email__ = "inanc.gurkan@yahoo.com"
__status__ = "Development"

import bots
import ray


def run_hmm_bot():
    hmm_bot = bots.HmmBot()
    submission_list = hmm_bot \
        .get_hot_submissions_containing_regex(subreddit_name="formuladank",
                                              regex="")
    for submission in submission_list:
        message = hmm_bot.generate_message()
        hmm_bot.reply_to_submission(submission, message)


def run_knight_bot():
    knight_bot = bots.KnightBot()
    knight_bot.knight_everything("formuladank")

if __name__ == "__main__":
    run_knight_bot()
