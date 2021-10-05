import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/Users/skylerdale/workspace/reddit')

import praw
import pandas as pd
import datetime as datetime
import os
from praw.models.reddit.more import MoreComments
#from cleantext import clean
from utilities.text_parsing import *
from utilities.date_conversion import *
from dateutil.parser import parse
 
reddit = praw.Reddit("reddit")
submission = reddit.submission(id="p1fj9i") # 2022 spring
#submission = reddit.submission(id="lqv04x") # 2021 fall

def has_status(comment):
    return True if comment.startswith("status") else False

def get_decision_date(comment):
    comment_replaced = comment.replace("*", "")
    comment_replaced = comment_replaced.replace("\n", " ")
    comment_replaced = comment_replaced.replace("\r", " ")
    date_index = comment_replaced.find("decision date:")
    comment_after_date = comment_replaced[date_index + len("decision date: "):]
    decision_date = comment_after_date.split(" ")[0]
    try:
        parsed_decision_date = parse(decision_date)
    except Exception:
        parsed_decision_date = decision_date
    return parsed_decision_date

def get_status(comment):
    status_index = comment.find("status")
    comment_after_status = comment[status_index + 6:]

    if comment_after_status.startswith("applied"):
        return "applied"
    elif comment_after_status.startswith("accepted"):
        return "accepted"
    elif comment_after_status.startswith("rejected"):
        return "rejected"
    else:
        return "unknown"


if __name__ == "__main__":
    comments_df = pd.DataFrame()

    while True:
        try:
            submission.comments.replace_more()
            break
        except PossibleExceptions:
            print("Handling replace_more exception")
            sleep(1)
    
    print(submission.comments.__len__())
    for comment in submission.comments:
        comment_body = comment.body.lower()
        comment_body_alpha = convert_to_alphanumeric(comment_body, ['/'])
        if has_status(comment_body_alpha):
            status = get_proceeding_word(comment_body_alpha, "status")
            if status == "unknown":
                print(comment_body)
            comments_df = comments_df.append({"comment": comment_body
                                , "status": status
                                , "comment_date": timestamp_to_date_string(comment.created)
                                , "comment_time": timestamp_to_date_string(comment.created, '%I:%M %p')
                                , "decision_date": get_decision_date(comment_body)}
                                , ignore_index=True)


    print(comments_df.groupby("status").count().sort_values(by = "decision_date"))
    print(comments_df[comments_df.status == 'accepted'].groupby('decision_date').count())
    #comments_df[comments_df.status == 'accepted'].groupby('decision_date').count().to_csv('omscs_stats.csv')