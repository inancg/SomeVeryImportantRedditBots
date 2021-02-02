"""
Collection of Reddit Bots crafted using 'praw' library.
BotBase:
    - parent class of all bots
    - contains methods that are common to all bots
HmmBot:
    - comments hm+ to the submissions that fits the regex input
    - logs the
"""

from datetime import datetime
from typing import Final
from praw import exceptions

import pathlib
import praw
import random
import re
import abc
import sys
import ray


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

    def get_new_submissions_containing_regex(self,
                                             subreddit_name: str,
                                             regex: str,
                                             submission_limit=5) -> list:
        submission_list = []
        subreddit = self.reddit.subreddit(subreddit_name)
        for submission in subreddit.new(limit=submission_limit):
            print(submission.title)  # TODO delete
            if re.search(regex, submission.title, re.IGNORECASE):
                submission_list.append(submission)

        return submission_list

    def reply_to_submission(self, submission, message: str):
        time_now = datetime.now().strftime("%H:%M:%S.%f")

        # TODO repetitive code, create new function
        if not self.does_item_exist_in_logs(submission.id):  # not replied yet
            try:
                submission.reply(message)
                print("\n*******\nreplied to submission\n*******\n",
                      submission.title)
                self.document_submitted_reply(submission.id,
                                              time_now,
                                              message)
            except praw.exceptions.RedditAPIException as e:
                print("Error message:", e.message)

                # TODO: gracefully exit (implemented now) or sleep
                sys.exit("API Limit reached, will stop execution")

    def reply_to_comment(self, comment, message: str):
        time_now = datetime.now().strftime("%H:%M:%S.%f")

        # TODO repetitive code, create new function
        if not self.does_item_exist_in_logs(comment.id):  # not replied yet
            try:
                comment.reply(message)
                print("\n*******\nreplied to comment\n*******\n", comment.body)
                self.document_submitted_reply(comment.id,
                                              time_now,
                                              message)
            except praw.exceptions.RedditAPIException as e:
                print("Error message:", e.message)

                # TODO: gracefully exit (implemented now) or sleep
                sys.exit("API Limit reached, will stop execution")

    def document_submitted_reply(self,
                                 submission_id: str,
                                 timestamp: str,
                                 message: str) -> None:
        with open(self.log_dir, "a+") as f:
            f.write("{}-{}-{}\n".format(submission_id,
                                        timestamp,
                                        message))

    def does_item_exist_in_logs(self, item_id):
        with open(self.log_dir, "r") as f:
            for line in f.readlines():
                logged_item_id = line.split("-")[0]
                if item_id == logged_item_id:
                    print("Already replied to", item_id)
                    return True
        return False

    @abc.abstractmethod
    def generate_message(self, message: str) -> str:
        return "Shouldn't reach here"


class HmmBot(BotBase):
    def __init__(self,
                 config_name="botHmm",
                 log_dir="../logs/hmmBot"):
        super().__init__(config_name, log_dir)

    def generate_message(self, message=None) -> str:
        # TODO design message logic
        return "h" + "m" * random.randint(2, 10)


class KnightBot(BotBase):
    _KNIGHT_NAMES = ["lewis", "hamilton"]

    def __init__(self,
                 config_name="knightBot",
                 log_dir="../logs/knightBot"):
        super().__init__(config_name, log_dir)

    def generate_message(self, message: str) -> str:
        return "*Sir " + message

    def get_unknighted_name(self, message):
        knight_names_re = "|".join(self._KNIGHT_NAMES)

        match_obj = re.search(knight_names_re,
                              message,
                              re.IGNORECASE)

        does_include_sir = re.search(
            r"sir\s+({})".format(knight_names_re),
            message,
            re.IGNORECASE)

        if does_include_sir:  # TODO delete
            print("includes sir ", message)

        if match_obj and not does_include_sir:
            return match_obj.group()

    @ray.remote
    def knight_comments(self, subreddit_name: str):
        print("knighting comments\n\n\n\n\n")
        for comment in self.reddit.subreddit(subreddit_name) \
                .stream.comments():
            print(comment.body)
            unknighted_name = self.get_unknighted_name(comment.body)
            if unknighted_name:
                knighted_name = self.generate_message(unknighted_name)
                self.reply_to_comment(comment=comment,
                                      message=knighted_name)

    @ray.remote
    def knight_submissions(self, subreddit_name: str):
        print("knighting submissions\n\n\n\n\n")
        for submission in self.reddit.subreddit(subreddit_name) \
                .stream.submissions():
            print(submission.title)
            unknighted_name = self.get_unknighted_name(submission.title)
            if unknighted_name:
                knighted_name = self.generate_message(unknighted_name)
                self.reply_to_submission(submission=submission,
                                         message=knighted_name)

            if submission.selftext:
                unknighted_name = self.get_unknighted_name(submission.selftext)
                if unknighted_name:
                    knighted_name = self.generate_message(unknighted_name)
                    self.reply_to_submission(submission=submission,
                                             message=knighted_name)

    def knight_everything(self, subreddit_name: str):
        ray.init()
        knight_submissions_remote = self.knight_submissions\
            .remote(self, subreddit_name=subreddit_name)

        knight_comments_remote = self.knight_comments\
            .remote(self, subreddit_name=subreddit_name)

        ray.get(knight_submissions_remote)
        ray.get(knight_comments_remote)
