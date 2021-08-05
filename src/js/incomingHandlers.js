const incomingHandlers =
{

    dataUpdate: (data) => 
    {

        switch (data.type)
        {

            case 'dropRate':
                stats.dropRate.x = window.utcArrayToLocal(data.x);
                stats.dropRate.y = data.y;
                window.updatePerformanceAnalytics();
                delete data;
                break;

            case 'likesAndRetweets':
                stats.likesAndRetweets.x          = window.utcArrayToLocal(data.x);
                stats.likesAndRetweets.y.likes    = data.likes;
                stats.likesAndRetweets.y.retweets = data.retweets;
                window.updateLikeRetweets();
                delete data;
                break;

            case 'followers':
                stats.followers.x = window.utcArrayToLocal(data.x);
                stats.followers.y = data.y;
                window.updateFollowers();
                delete data;
                break;

            case 'totalPulls':
                stats.totalPullsSet.x = window.utcArrayToLocal(data.x);
                stats.totalPullsSet.y = data.y;
                window.updateUsage();
                delete data;
                break;

            case 'totalPulls24':
                stats.totalPullsLast24.x      = data.x;
                stats.totalPullsLast24.y      = data.y;
                stats.totalPullsLast24.amount = data.amount;
                $('#requests-last-24').html(data.amount);
                window.updateUsageLast24(data.x, data.y);
                delete data;
                break;

            case 'dropHashtagIfIncludes':
                stats.resources.dropHashtagIfIncludes = data.data;
                updateEditor("drophashtagifincludes", data.data);
                delete data;
                break;
 
            case 'DropPhrases':
                stats.resources.DropPhrases = data.data;
                updateEditor("dropphrase", data.data);
                delete data;
                break;

            case 'HashTags':
                stats.resources.HashTags = data.data;
                updateEditor("hashtag", data.data);
                delete data;
                break;

            case 'constraints':
                stats.constraints = data.data;
                updateConstraints(data.data);
                delete data;
                break;

            default:
                break;
        }
    },
    logging: (data) => {
        stats.logs.push(`[${new Date().toTimeString().split(' ')[0]}] ${data}`);
        let buffer = [];
        for (let l of stats.logs){
            buffer.push([l])
        }
        window.updateLogsView(buffer)
    },
    alert: (data) => {
        window.notify(data)
    },
    ack: window.ackHandler
};