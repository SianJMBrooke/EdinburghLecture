"""
This script collects posts, comments, and replies from a specified subreddit.

To Do:
- Why are some posts missing? compared to the view on reddit I'm not getting all the posts

"""

import praw
from datetime import datetime
import pandas as pd


reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=SECRET_TOKEN, password=PASSWORD, username=USERNAME,
    redirect_uri="http://localhost:8080",
    user_agent="test script by u/DrSJBrooke",
)

# Specify the subreddit and date
subreddit_name = 'BarbieTheMovie'
since_date = datetime(2015, 1, 1)
query_set = "(barbie OR oppenheimer OR barbenheimer)"

# Initialize lists to store data
posts_data = []
comments_data = []
replies_data = []

# Collect posts since the specified date with the desired key terms
try:

    for submission in reddit.subreddit("movies").search(query_set, sort="top",
                                                        syntax="cloudsearch", limit=None):

        # Check if any of the desired terms are present in the post title or body
        if submission.created_utc >= since_date.timestamp():
            post_data = {
                'Post Title': submission.title,
                'Post URL': submission.url,
                'Post Date': datetime.utcfromtimestamp(submission.created_utc),
                'Number of Comments': submission.num_comments,
                'Author': submission.author.name if submission.author else 'Deleted'
            }
            posts_data.append(post_data)

            # Count the posts (ouput)
            print(f"Post {len(posts_data)}: {submission.title}")

            # Collect comments on the post
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                comment_data = {
                    'Post Title': submission.title,
                    'Comment': comment.body,
                    'Comment Date': datetime.utcfromtimestamp(comment.created_utc),
                    'Author': comment.author.name if comment.author else 'Deleted'
                }
                comments_data.append(comment_data)

                # Collect replies to the comment
                comment.replies.replace_more(limit=None)
                for reply in comment.replies.list():
                    reply_data = {
                        'Post Title': submission.title,
                        'Post Body': submission.selftext if submission.selftext else 'None',
                        'Number of Post and Comments': submission.num_comments,
                        'Post URL': submission.url,
                        'Post Date': datetime.utcfromtimestamp(submission.created_utc),
                        'Post Author': submission.author.name if submission.author else 'Deleted',
                        'Comment': comment.body,
                        'Comment Date': datetime.utcfromtimestamp(comment.created_utc),
                        'Comment Author': comment.author.name if comment.author else 'Deleted',
                        'Reply': reply.body,
                        'Reply Date': datetime.utcfromtimestamp(reply.created_utc),
                        'Reply Author': reply.author.name if reply.author else 'Deleted'
                    }
                    replies_data.append(reply_data)

        # time.sleep(1)  # Add a small delay to avoid rate limiting
except Exception as e:
    print(f"An error occurred: {str(e)}")
    # Handle the error here (e.g., log the error, retry, or exit gracefully)

# Convert lists to DataFrames
posts_df = pd.DataFrame(posts_data)
comments_df = pd.DataFrame(comments_data)
replies_df = pd.DataFrame(replies_data)

# Save DataFrames to CSV files
posts_df.to_csv('Barbenheimer_Reddit_Posts.csv', index=False)
comments_df.to_csv('Barbenheimer_Reddit_Comments.csv', index=False)
replies_df.to_csv('Barbenheimer_Reddit_Replies.csv', index=False)

print('----- Done. -----\nTotal Posts:', len(posts_df),
      '\nTotal Comments: ', len(comments_df),
      '\nTotal Replies: ', len(replies_df))
