import bots


def run_hmm_bot():
    hmm_bot = bots.HmmBot()
    submission_list = hmm_bot\
        .get_new_submissions_containing_regex("formuladank", "pierre")
    for submission in submission_list:
        message = hmm_bot.generate_message() #TODO design message logic
        hmm_bot.reply_to_submission(submission, message)


if __name__ == "__main__":
    run_hmm_bot()
