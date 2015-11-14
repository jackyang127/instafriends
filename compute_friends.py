
from instagram.client import InstagramAPI

def find_self(access_token):

        client_secret = "22a6a272eeaa4b18aba7b242ade48cd3"

        api = InstagramAPI(access_token=access_token, client_secret=client_secret)
        self_info = api.user()
        return self_info

def find_friends(access_token):
        client_secret = "22a6a272eeaa4b18aba7b242ade48cd3"
        api = InstagramAPI(access_token=access_token, client_secret=client_secret)

        #sets recent_feed  media
        recent_feed, next_ = api.user_recent_media(100)

        """
        Finding users tagged in your photos, this should be the most important factor
        """
        users = []
        num_photos_in_feed = 0
        num_photos_tagged = 0
        for media in recent_feed:
                num_photos_in_feed += 1
                if media.users_in_photo:
                        for tagged_person in media.users_in_photo:
                                num_photos_tagged += 1
                                users.append(tagged_person.user)

        tagged_user = {}
        for user in users:
                if user.id in tagged_user.keys():
                        tagged_user[user.id] += 1
                else:
                        tagged_user[user.id] = 1

        #Done



        #likes - list of users that has liked each photo
        likes = []
        for media in recent_feed:
                a = api.media_likes(media.id)
                for i in a:
                        likes.append(i)

        # d_ids - dict key = user id and value is number of times they have liked a photo
        likes_ids = [user.id for user in likes]
        d_ids = {}
        for userid in likes_ids:
                d_ids[userid] = likes_ids.count(userid)

        #users is list of all users that you have liked a photo of theirs
        feed, next_ = api.user_liked_media(access_token=access_token, count = 100)
        users = []
        for media in feed:
                users.append(media.user)

        #d - pairs users and number of times you have liked their photo
        other_ids = [user.id for user in users]
        d = {}
        for user in other_ids:
                d[user] = other_ids.count(user)


        #all relevant users
        like_users = {}
        for user in likes:
                like_users[user.id] = user

        liked_users = {}
        for user in users:
                liked_users[user.id] = user

        like_users.update(liked_users)
        all_users = list(like_users.values())


        #give scores to each user
        scores = {}
        for user in all_users:
                score = 0
                if user.id in d_ids:  # d_ids - dict key = user id and value is number of times they have liked a photo
                        score += 5 *d_ids[user.id]
                if user.id in d:
                        score += 2 * d[user.id]  #d - pairs users and number of times you have liked their photo
                if user.id in tagged_user:
                        if (num_photos_tagged < 2) or ((num_photos_tagged/num_photos_in_feed) < .2):
                                score += 14 * tagged_user[user.id]
                        else:
                                score += 13 * tagged_user[user.id]
                scores[user] = score

        #print(d)
        #print(d_ids)

        #gives scores for like_me index
        scores_likeme = {}
        for user in all_users:
                score = 0
                if user.id in d_ids:
                        score += d_ids[user.id]
                scores_likeme[user] = score

        final_likeme = []
        for _ in range(5):
                v=list(scores_likeme.values())
                k=list(scores_likeme.keys())
                score = k[v.index(max(v))]
                final_likeme.append(score.full_name)
                scores_likeme.pop(score)

        final_likeme_str = str(final_likeme)

        #print(final_likeme, "diff")

        #gives scores for like_them index
        scores_likethem = {}
        for user in all_users:
                score = 0
                if user.id in d:
                        score += d[user.id]
                scores_likethem[user] = score

        final_likethem = []
        for _ in range(5):
                v=list(scores_likethem.values())
                k=list(scores_likethem.keys())
                score = k[v.index(max(v))]
                final_likethem.append(score.full_name)
                scores_likethem.pop(score)

        final_likethem_str = str(final_likethem)

        #print(final_likethem, 'more diff')

        #compute final list of 5 best users with highest scores
        final = []
        finalname = []
        finalscore = []
        for _ in range(5):
                v=list(scores.values())
                k=list(scores.keys())
                score = k[v.index(max(v))]
                final.append(score)
                finalname.append(score.full_name)
                finalscore.append(scores[score])
                scores.pop(score)


        final_str = str(final)
        finalname_str = str(finalname)
        finalscore_str = str(finalscore)

        return final
