const incomingHandlers =
{

    dataUpdate: (data) => 
    {

        switch (data.type)
        {

            case 'dropRate':
                macros.dropRate.x = window.utcArrayToLocal(data.x);
                macros.dropRate.y = data.y;
                window.updatePerformanceAnalytics();
                delete data;
                break;

            case 'likesAndRetweets':
                macros.likesAndRetweets.x          = window.utcArrayToLocal(data.x);
                macros.likesAndRetweets.y.likes    = data.likes;
                macros.likesAndRetweets.y.retweets = data.retweets;
                window.updateLikeRetweets();
                delete data;
                break;

            case 'followers':
                macros.followers.x = window.utcArrayToLocal(data.x);
                macros.followers.y = data.y;
                window.updateFollowers();
                delete data;
                break;

            case 'totalPulls':
                macros.totalPullsSet.x      = window.utcArrayToLocal(data.x);
                macros.totalPullsSet.y      = data.y;
                macros.totalPullsSet.amount = data.amount;
                window.updateUsage();
                delete data;
                break;

            case 'totalPulls24':
                macros.totalPullsLast24.x      = data.x;
                macros.totalPullsLast24.y      = data.y;
                macros.totalPullsLast24.amount = data.amount;
                $('#requests-last-24').html(data.amount);
                window.updateUsageLast24(data.x, data.y);
                delete data;
                break;

            case 'dropHashtagIfIncludes':
                macros.resources.dropHashtagIfIncludes = data.data;
                updateEditor("drophashtagifincludes", data.data);
                delete data;
                break;
 
            case 'DropPhrases':
                macros.resources.DropPhrases = data.data;
                updateEditor("dropphrase", data.data);
                delete data;
                break;

            case 'HashTags':
                macros.resources.HashTags = data.data;
                updateEditor("hashtag", data.data);
                delete data;
                break;

            case 'constraints':
                macros.constraints = data.data;
                for (let action of ["interaction-like", "interaction-rt", "interaction-follow"]){
                    if (data[action]){
                        $( "#" + action ).prop( "checked", true );
                    }
                    else{
                        $( "#" + action ).prop( "checked", false );
                    }
                }
                updateConstraints(data.data);
                delete data;
                break;

            case 'myTweets':
                macros.myTweets = data.data;
                window.buildTweetScheduler();
                delete data;
                break;

            case 'interactions':
                macros.interactions_like     = data.like;
                macros.interactions_rt       = data.rt;
                macros.interactions_follow   = data.follow;
                window.updateInteractions();
                delete data;
                break;
            
            case 'streamFollowing':
                macros.streamFollowing = data.data;
                window.StreamEditor.updateStream();
                delete data;
                break;

            case 'me':
                macros.me = data.json;
                console.log(macros.me);
                console.log(typeof macros.me);
                delete data;
                $('#avatar').attr("src", macros.me.profile_image_url_https);
                $('#go-to-twitter').attr("href", macros.me.screen_name);
                $('#my-screen-name').html(`<span class=\"w3-green\">${macros.me.screen_name}</span>`);
                break;

            default:
                break;
        }
    },
    logging: (data) => {
        let d = new Date();
        macros.logs.push(`[${d.toTimeString().split(' ')[0]}:${d.getMilliseconds()}] ${data}`);
        let buffer = [];
        for (let l of macros.logs){
            buffer.push([l])
        }
        window.updateLogsView(buffer)
    },
    alert: (data) => {
        window.notify(data)
    },
    ack: window.ackHandler
};