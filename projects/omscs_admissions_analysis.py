import sys
sys.path.insert(1, '/Users/skylerdale/workspace/reddit')

import praw
import pandas as pd
import datetime as datetime
import os
from praw.models.reddit.more import MoreComments
#from cleantext import clean
from utilities import text_parsing
from utilities import date_conversion 
from utilities import reddit_utilities
from dateutil.parser import parse
 
# function for the df building piece? Like build from df from list

def omscs_analysis(submission):
    comments_df = pd.DataFrame()
    submission = reddit_utilities.get_all_comments(submission)

    print(submission.comments.__len__())
    for comment in submission.comments:
        comment_body = comment.body.lower()
        comment_body_alpha = text_parsing.convert_to_alphanumeric(comment_body, ['/'])
        if comment_body_alpha.startswith("status"):
            status = text_parsing.get_proceeding_word(comment_body_alpha, "status")
            decision_date = text_parsing.parse_date(text_parsing.get_proceeding_word(comment_body_alpha, "decision date"))
            comments_df = comments_df.append({"comment": comment_body
                                , "status": status
                                , "comment_date": date_conversion.timestamp_to_date_string(comment.created)
                                , "comment_time": date_conversion.timestamp_to_date_string(comment.created, '%I:%M %p')
                                , "decision_date": decision_date}
                                , ignore_index=True)


    comments_df['decision_date'] = pd.to_datetime(comments_df['decision_date'], errors = 'coerce')
    comments_df = comments_df[~comments_df.decision_date.isnull()]
    comments_df['decision_weekday'] = comments_df['decision_date'].apply(lambda x: x.date().strftime("%A"))
    print(comments_df.dtypes)
    print(comments_df.groupby("status").count().sort_values(by = "decision_date"))
    print(comments_df[comments_df.status == 'accepted'].groupby('decision_date').count())
    print(comments_df[comments_df.status == 'accepted'].groupby('decision_weekday').count())

    #comments_df[comments_df.status == 'accepted'].groupby('decision_date').count().to_csv('omscs_stats.csv')

if __name__ == "__main__":
    reddit = praw.Reddit("reddit")
    #2022 spring
    #submission = reddit.submission(id="lqv04x") # 2021 fall
    submission = reddit.submission(id="p1fj9i")
    omscs_analysis(submission)