library(httr)
library(jsonlite)

# Set your Reddit API credentials
client_id <- "YOUR_CLIENT_ID"
client_secret <- "YOUR_CLIENT_SECRET"
user_agent <- "YOUR_USER_AGENT"

# Authenticate with Reddit API
auth <- oauth_app("reddit", client_id, client_secret)
token <- oauth2.0_token(oauth_endpoints("reddit"), auth, user_agent = user_agent)
httr::config(token = token)

# Define your search query and parameters
search_query <- "YOUR SEARCH TERM HERE"  # Replace with your desired search term(s)
limit <- 10  # Number of posts to retrieve

# Format the search query to include multiple words
search_query <- gsub(" ", "+", search_query)

# Send a GET request to Reddit API
url <- paste0("https://www.reddit.com/r/all/search.json?q=", search_query, "&limit=", limit)
response <- GET(url, add_headers("User-Agent" = user_agent))

# Check if the request was successful
if (http_status(response)$status_code == 200) {
  # Parse JSON response
  data <- fromJSON(content(response, "text"))
  
  # Extract information from the Reddit posts
  posts <- data$data$children
  
  # Create an empty data frame to store the collected information
  reddit_data <- data.frame(
    Subreddit_Title = character(0),
    Post_Title = character(0),
    Post_Text = character(0),
    Author_Username = character(0),
    Upvote_Count = numeric(0),
    Downvote_Count = numeric(0),
    Number_of_Comments = numeric(0)
  )
  
  for (post in posts) {
    post_data <- post$data
    subreddit_title <- post_data$subreddit
    post_title <- post_data$title
    post_text <- post_data$selftext
    author_username <- post_data$author
    upvote_count <- post_data$ups
    downvote_count <- post_data$downs
    num_comments <- post_data$num_comments
    
    # Append the collected information to the data frame
    reddit_data <- rbind(reddit_data, data.frame(
      Subreddit_Title = subreddit_title,
      Post_Title = post_title,
      Post_Text = post_text,
      Author_Username = author_username,
      Upvote_Count = upvote_count,
      Downvote_Count = downvote_count,
      Number_of_Comments = num_comments
    ))
  }
  
  # Save the data frame to a CSV file
  write.csv(reddit_data, file = "reddit_data.csv", row.names = FALSE)
  
  cat("Data saved to reddit_data.csv\n")
} else {
  cat("Failed to retrieve data from Reddit API.\n")
}
