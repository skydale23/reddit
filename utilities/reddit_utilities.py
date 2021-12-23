

def get_all_comments(submission):
    """expands full set of comments"""
    while True:
        try:
            submission.comments.replace_more()
            break
        except PossibleExceptions:
            print("Handling replace_more exception")
            sleep(1)
    return submission
