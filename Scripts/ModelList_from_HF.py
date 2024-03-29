import pandas as pd
from huggingface_hub import HfApi
from huggingface_hub import ModelFilter

api = HfApi()
models = api.list_models(
    sort="downloads",
    direction=-1, 
    cardData = 1,
    filter=ModelFilter(
        task="text-generation",
    )
)


data = []

for i in models:
    
    arxiv_items = [item for item in i.tags if 'arxiv' in item]
    repourl = "https://huggingface.co/" + i.id
    if i.card_data is None:
        lic = None
    else:
        lic = str(i.card_data.license)
    data.append({
        'name': i.id, 
        'author': i.author, 
        'release_time': i.created_at, 
        'downloads': i.downloads, 
        'likes': i.likes,
        'license':lic, 
        'arXiv': arxiv_items,
        'HuggingFace_repo':repourl,
        'HuggingFace_forum':repourl + "/discussions" 
    })


df = pd.DataFrame(data)

#df.to_csv('HF_ByDownload_text-generation05032024.csv')