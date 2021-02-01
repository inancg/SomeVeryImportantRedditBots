import praw, re, pathlib, random
from datetime import date
from typing import Final


class BotHmm:
    def __init__(self, config_name="botHmm", log_dir="./logs/" + date.today().strftime("%m/%d/%y")):
        self.reddit = praw.Reddit(config_name)
        self.log_dir = log_dir
        self.username: Final = self.reddit.user.me()

        pathlib.Path(self.log_dir).touch(exist_ok=True)

    def get_new_submissions_containing_regex(self, subreddit_name, regex, submission_limit=10):
        subreddit = self.reddit.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=submission_limit):
            if re.search(regex, submission.title, re.IGNORECASE):
                self.reply_to_submission(submission, message=self.generate_message())
        return

    def reply_to_submission(self, submission, message):
        # replies to #submission_id with message
        # logs the submission id using document_submitted_reply(submission_id)
        pass

    def document_submitted_reply(self, submission_id):
        # write username, submission_id, time (and maybe more?) to file (or db?)
        pass

    def generate_message(self):
        # only hmm's so far, TODO implement
        return "h" + "m"*random.randint(1, 10)
