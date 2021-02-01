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


def run_hmm_bot():
    hmm_bot = bots.HmmBot()
    submission_list = hmm_bot\
        .get_new_submissions_containing_regex("formuladank", "pierre")
    for submission in submission_list:
        message = hmm_bot.generate_message()
        hmm_bot.reply_to_submission(submission, message)


if __name__ == "__main__":
    run_hmm_bot()
