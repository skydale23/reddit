
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
=======
from cleantext import clean
from utilities.text_parsing import convert_to_alphanumeric 

reddit = praw.Reddit("reddit")
submission = reddit.submission(id="p1fj9i")

def has_status(comment):
    return True if comment.startswith("status") else False

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
    for comment in submission.comments:
        print(clean(comment.body,
            fix_unicode=True,               # fix various unicode errors
            to_ascii=True,                  # transliterate to closest ASCII representation
            lower=True,                     # lowercase text
            no_line_breaks=True,           # fully strip line breaks as opposed to only normalizing them
            no_urls=False,                  # replace all URLs with a special token
            no_emails=False,                # replace all email addresses with a special token
            no_phone_numbers=False,         # replace all phone numbers with a special token
            no_numbers=False,               # replace all numbers with a special token
            no_digits=False,                # replace all digits with a special token
            no_currency_symbols=False,      # replace all currency symbols with a special token
            no_punct=False,                 # remove punctuations
            replace_with_punct="",          # instead of removing punctuations you may replace them
            replace_with_url="<URL>",
            replace_with_email="<EMAIL>",
            replace_with_phone_number="<PHONE>",
            replace_with_number="<NUMBER>",
            replace_with_digit="0",
            replace_with_currency_symbol="<CUR>"))

        print(convert_to_alphanumeric(comment.body))
        
        comment_body = comment.body.lower()
        comment_body_alpha = convert_to_alphanumeric(comment_body)
        if has_status(comment_body_alpha):
            status = get_status(comment_body_alpha)
            comments_df = comments_df.append({"comment": comment_body
                                , "status": status}, ignore_index=True)

    for index, row in comments_df.iterrows():
        print(row['comment'].partition('\n')[0])

    print(comments_df.groupby("status").count())
    #print(comment.__dict__) #last step here --> calculate when each one was posted 
    
