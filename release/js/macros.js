
let macros = {
    retweets: 0,
    likes: 0,
    totalPulls: 0,
    efficiencyAvg: 0.00,
    acks: 0,
    lastPing: 0,
    followers: {
        x: [new Date().toTimeString()],
        y: [0]
    },
    logs: [],
    myTweets: [],
    streamFollowing: [],
    streamRunning: false,
    dropRate: {
        x: [new Date().toTimeString()],
        y: [0]
    },
    likesAndRetweets: {
        x: [new Date().toTimeString()],
        y: {likes: [0], retweets: [0]}
    },
    totalPullsSet: {
        x: [new Date().toTimeString()],
        y: [0],
        amount: 0
    },
    totalPullsLast24: {
        x: [new Date().toTimeString()],
        y: [0],
        amount: 0
    },
    resources: {
        dropHashtagIfIncludes: [],
        DropPhrases: [],
        HashTags: []
    },
    constraints: {
        max_dataset_length: null,
        interval_time_seconds: null,
        required_retweets: null,
        required_favorites: null,
        query_amount: null,
        max_hashtags: null,
        interactions_like: null,
        interactions_rt: null
    }
};
