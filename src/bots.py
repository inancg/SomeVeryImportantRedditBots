"""
Collection of Reddit Bots crafted using 'praw' library.
BotBase:
    - parent class of all bots
    - contains methods that are common to all bots
HmmBot:
    - comments hm+ to the submissions that fits the regex input
    - logs the
"""

from datetime import date, datetime
from typing import Final

import pathlib
import praw
import random
import re
import abc


class BotBase(abc.ABC):
    def __init__(self, config_name: str, log_dir: str):
        self.reddit = praw.Reddit(config_name)
        self.log_dir = log_dir
        self.username: Final = self.reddit.user.me()

        pathlib.Path(self.log_dir).touch(exist_ok=True)

    def get_hot_submissions_containing_regex(self,
                                             subreddit_name: str,
                                             regex: str,
                                             submission_limit=5) -> list:
        submission_list = []
        subreddit = self.reddit.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=submission_limit):
            if re.search(regex, submission.title, re.IGNORECASE):
                submission_list.append(submission)

        return submission_list

    def reply_to_submission(self, submission, message: str):
        time_now = datetime.now().strftime("%H:%M:%S.%f")
        # TODO submit reply, if not commented already
        self.document_submitted_reply(submission.id,
                                      time_now,
                                      message)

    def reply_to_comment(self, comment, message: str):
        time_now = datetime.now().strftime("%H:%M:%S.%f")
        # TODO submit reply, if not commented already
        self.document_submitted_reply(comment.id,
                                      time_now,
                                      message)

    def document_submitted_reply(self,
                                 submission_id: str,
                                 timestamp: str,
                                 message: str) -> None:
        with open(self.log_dir, "a+") as f:
            f.write("{}-{}-{}\n".format(submission_id,
                                        timestamp,
                                        message))

    @abc.abstractmethod
    def generate_message(self, message: str) -> str:
        return "Shouldn't reach here"


class HmmBot(BotBase):
    def __init__(self,
                 config_name="botHmm",
                 log_dir="../logs/hmmBot_"
                         + date.today().strftime("%y-%m-%d")):
        super().__init__(config_name, log_dir)

    def generate_message(self, message=None) -> str:
        # TODO design message logic
        return "h" + "m" * random.randint(2, 10)


class KnightBot(BotBase):
    _KNIGHT_NAMES = ["lewis", "hamilton"]

    def __init__(self,
                 config_name="botHmm",
                 log_dir="../logs/mannersBot_"
                         + date.today().strftime("%y-%m-%d")):
        super().__init__(config_name, log_dir)

    def generate_message(self, message: str) -> str:
        return "*Sir " + message

    def get_unknighted_name(self, message):
        # TODO handle if the knighted name is used : Sir + _KNIGHT_NAMES[x]
        match_obj = re.search("|".join(self._KNIGHT_NAMES),
                              message,
                              re.IGNORECASE)
        if match_obj:
            print("here is the message", message)
            return match_obj.group()