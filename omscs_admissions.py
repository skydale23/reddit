import praw
import pandas as pd
import datetime as datetime
import os
from praw.models.reddit.more import MoreComments

reddit = praw.Reddit("reddit")
submission = reddit.submission(id="p1fj9i")

def get_comment_alpha(comment):
    comment_alpha_filter = filter(str.isalnum, comment)
    comment_alpha = "".join(comment_alpha_filter)
    return comment_alpha

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
        comment_body = comment.body.lower()
        comment_body_alpha = get_comment_alpha(comment_body)
        if has_status(comment_body_alpha):
            status = get_status(comment_body_alpha)
            comments_df = comments_df.append({"comment": comment_body
                                , "status": status}, ignore_index=True)

    for index, row in comments_df.iterrows():
        print(row['comment'].partition('\n')[0])

    print(comments_df.groupby("status").count())
    #print(comment.__dict__) #last step here --> calculate when each one was posted 
        