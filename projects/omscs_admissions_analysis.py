
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
from utilities import dataframe_utilities
from dateutil.parser import parse
from cleantext import clean

pd.set_option('max_rows', 500)


# function for the df building piece? Like build from df from list

def omscs_analysis(submission):
    comments_df = pd.DataFrame()
    submission = reddit_utilities.get_all_comments(submission)

    for comment in submission.comments:

        comment_body = comment.body.lower()
        comment_body_alpha = text_parsing.convert_to_alphanumeric(comment_body, ['/'])

        if comment_body_alpha.startswith("status"):
            status = text_parsing.get_proceeding_word(comment_body_alpha, "status")
            decision_date_original = text_parsing.get_proceeding_word(comment_body_alpha, "decision date")
            decision_date = text_parsing.convert_to_numeric(str(decision_date_original))
            comments_df = comments_df.append({"comment": comment_body
                                , "status": status
                                , "comment_date": date_conversion.timestamp_to_date_string(comment.created)
                                , "comment_time": date_conversion.timestamp_to_date_string(comment.created, '%I:%M %p')
                                , "decision_date": decision_date}
                                , ignore_index=True)

    comments_df = dataframe_utilities.datetime_conversion(
        comments_df, 'decision_date', ['%d%m%Y','%d%m%y', '%d%M%y', '%d%M%Y'], 'decision_date_clean')

    comments_df = comments_df[~comments_df.decision_date_clean.isnull()]

    comments_df['decision_weekday'] = comments_df['decision_date_clean'].apply(lambda x: x.strftime("%A"))
    print(comments_df.groupby("status").count().sort_values(by = "decision_date_clean"))
    print(comments_df[comments_df.status == 'accepted'].groupby('decision_date_clean').count())
    print(comments_df[comments_df.status == 'accepted'].groupby('decision_weekday').count())

if __name__ == "__main__":
    reddit = praw.Reddit("reddit")
    #submission = reddit.submission(id="lqv04x") # 2021 fall
    submission = reddit.submission(id="p1fj9i") #2022 spring
    omscs_analysis(submission)

 