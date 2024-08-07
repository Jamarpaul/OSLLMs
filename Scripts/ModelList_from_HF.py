import pandas as pd
from huggingface_hub import HfApi

api = HfApi(token = "token")

models = api.list_models(
    sort="likes",
    direction=-1, 
    filter="text-generation",
    expand=["author",
            "cardData", 
            "config", 
            "createdAt", 
            "disabled", 
            "downloads", 
            "downloadsAllTime", 
            "gated", 
            "gitalyUid", 
            "inference", 
            "lastModified", 
            "library_name", 
            "likes",
            "mask_token", 
            "model-index", 
            "pipeline_tag", 
            "private", 
            "safetensors", 
            "sha", 
            "siblings", 
            "spaces", 
            "tags", 
            "transformersInfo", 
            "widgetData"]
    
)


data = []

for i in models:
    
    arxiv_items = [item for item in i.tags if 'arxiv' in item]
    repourl = "https://huggingface.co/" + i.id

    
    
    if i.card_data is None:
        lic = "missing"
        datasets = "missing"
        eval_results = "missing"
    else:
        lic = str(i.card_data.license)
        datasets = str(i.card_data.datasets)
        eval_results = str(i.card_data.eval_results)
    
    data.append({
        'name': i.id, 
        'author': i.author, 
        'release_time': i.created_at, 
        'last_modified': i.last_modified,
        'downloads_last_30days': i.downloads, 
        'downloads_all_time': i.downloads_all_time,
        'likes': i.likes,
        'datasets' : datasets,
        'eval_results' : eval_results,
        'license':lic, 
        'arXiv': arxiv_items,
        'HuggingFace_repo':repourl,
        
    })


df = pd.DataFrame(data)

df