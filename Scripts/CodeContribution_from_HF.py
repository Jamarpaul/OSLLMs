from huggingface_hub import HfApi
import pandas as pd

api = HfApi()

df = pd.read_csv("Datasets\HF_ByDownload_text-generation05032024.csv") #You can replace it with your own extracted files

with pd.ExcelWriter("you save path", engine='openpyxl') as writer:
	# extract the first 100 repo.
	for j in df['name'].head(100):

		# Commits are sorted by date (last commit first)
		commitlist = api.list_repo_commits(j)
		data = []
		for i in commitlist:
			#print(i.authors)
			#print(i.created_at)
			#print(i.title)
			#print(i.message)
			data.append({
				'contributor': i.authors, 
				'commit_time': str(i.created_at), 
				'title': i.title, 
				'message': i.message, 
			})
		df_temp = pd.DataFrame(data)
		
		project = j.replace('/', '_')

		df_temp.to_excel(writer, sheet_name=project, index=False)
	writer.close()