import pandas as pd
import time
from huggingface_hub import get_repo_discussions
from huggingface_hub import get_discussion_details

start_time = time.time()

df = pd.read_csv("your model list").head(100)



reply = []
post = []
post_reply_count = []
for index, row in df.iterrows():
    repo = row['name']
    try:
        for discussion in get_repo_discussions(repo):
            comment = get_discussion_details(repo, discussion.num)
            #print(comment.num, comment.title)
            #print(comment.author)
            #print(comment.created_at)
            count = 0
            rep_count = 0
            poster = ''
            for e in comment.events:
                if e.type == 'comment':
                    rep_count = rep_count + 1
                if count == 0 :
                    poster = e.author
                    post.append({
                        'poster': e.author,
                        'title': comment.title,
                        'post_time': e.created_at,
                        'type': e.type,
                        'repo': repo
                    })
                    
                else:
                    reply.append({
                        'replier': e.author,
                        'post_time': e.created_at,
                        'type': e.type,
                        'repo': repo
                    })
                        
                count = count + 1

            #print(rep_count)
            post_reply_count.append({
                            'poster': comment.author,
                            'title': comment.title,
                            'repo': repo, 
                            'recevied_replies': rep_count
                        })
                
    except:
        print("Discussions are disabled for this repo " + repo)
        continue
end_time = time.time()
elapsed_time = end_time - start_time
print(f"excution time: {elapsed_time:.2f} s")
df_post = pd.DataFrame(post)
df_reply = pd.DataFrame(reply)
df_prc = pd.DataFrame(post_reply_count)
