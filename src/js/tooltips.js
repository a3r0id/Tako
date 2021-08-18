// CONSTRAINTS EDITOR

tippy('#tip-max_dataset_length', {
    content: 'Maximum length of data-points for statistics keeping. Range 25-1000 points.',
});

tippy('#tip-interval_time_seconds', {
    content: 'Amount of time between queries in seconds. At least a small amount of time is reccommended in order to keep requests rates low. Range 10-300 seconds.',
});

tippy('#tip-required_retweets', {
content: 'The required amount of retweets of each tweets we come across in order for us to interact with them. This keeps us from interacting with spam. There is no range.',
});

tippy('#tip-required_favorites', {
    content: 'The required amount of likes of each tweets we come across in order for us to interact with them. This keeps us from interacting with spam. There is no range.',
});

tippy('#tip-query_amount', {
    content: 'The amount of tweets to fetch per query. This shouldn\'t be set too high as you will be rate-limited by Twitter. Range 1-500',
});

tippy('#tip-max_hashtags', {
    content: 'The maximum amount of hashtags included in tweets we come across before we ignore them. This keeps us from interacting with spam. Range 1-100',
});

