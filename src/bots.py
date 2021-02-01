from datetime import date, datetime
from typing import Final

import pathlib
import praw
import random
import re


class HmmBot:
    def __init__(self,
                 config_name="botHmm",
                 log_dir="../logs/" + date.today().strftime("%m-%d-%y")):
        self.reddit = praw.Reddit(config_name)
        self.log_dir = log_dir
        self.username: Final = self.reddit.user.me()

        pathlib.Path(self.log_dir).touch(exist_ok=True)

    def get_new_submissions_containing_regex(self,
                                             subreddit_name: str,
                                             regex: str,
                                             submission_limit=5) -> list:
        submission_list = []
        subreddit = self.reddit.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=submission_limit):
            if re.search(regex, submission.title, re.IGNORECASE):
                # print(submission.title)
                submission_list.append(submission)

        return submission_list

    def reply_to_submission(self, submission, message):
        time_now = datetime.now().strftime("%H:%M:%S.%f"),
        # TODO submit reply
        self.document_submitted_reply(submission.id,
                                      time_now,
                                      message)

    def document_submitted_reply(self, submission_id,
                                 timestamp, message):
        with open(self.log_dir, "a+") as f:
            f.write("{}-{}-{}\n".format(submission_id,
                                        timestamp,
                                        message))

    def generate_message(self):
        return "h" + "m" * random.randint(2, 10)
