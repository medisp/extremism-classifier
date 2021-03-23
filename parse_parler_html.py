# Import Modules
import glob 
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import timeit

start = timeit.timeit()
print("hello")
# Initialize file loader

files = glob.glob('data/*')
end = timeit.timeit()
print("[INFO]... File Load timing")
print(end - start)
data = []

for idx, file in enumerate(tqdm(files)):
	doc_data = {}
	with open(file, 'r') as html_doc:
		soup = BeautifulSoup(html_doc, 'html.parser')
	try:
	    author_name = soup.find('span', {'class': 'author--name'}).text
	except AttributeError:
		author_name = ""
		
	try:
		author_username = soup.find('span', {'class': 'author--username'}).text
	except AttributeError:
		author_username = ""
		
	try: 
		author_profile_picture = soup.find('img', {'alt': 'Post Author Profile Pic'}).get('src', '')
	except AttributeError:
		author_profile_picture = ""
		
	try:
		post_text = soup.find('div', {'class': 'card--body'}).find('p').text
	except AttributeError:
		post_text = ""
		
	try:
		post_image = soup.find('img', {'class': "mc-image--modal--element"}).get('src', '')
	except AttributeError:
		post_image = ""
		
	try:
		post_timestamp = soup.find('span', {'class': 'post--timestamp'}).text
	except AttributeError:
		post_timestamp = ""
		
	try:
		post_impressions = soup.find('span', {'class': 'impressions--count'}).text
	except AttributeError:
		post_impressions = ""
		
	data.append({
        "author_name": author_name,
        "author_username": author_username,
        "author_profile_photo": author_profile_picture,
        "post_text": post_text,
        "post_image": post_image,
        "post_timestamp": post_timestamp,
        "post_impressions": post_impressions})
	
end = timeit.timeit()
print("[INFO]... BeautifulSoup HTML Processing Time: ")
print(end - start)

df = pd.DataFrame(data)

pd.set_option('expand_frame_repr', False)
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 1000)

print(df.head())
print(df['author_username'].nunique())
compression_opts = dict(method='zip', archive_name='out.csv')

df.to_csv('out.zip', index=False, compression=compression_opts)

start = timeit.timeit()
print("second df read from zipped file")
df2 = pd.read_csv('out.zip', compression='zip', header=0, sep=',', quotechar='"')

print(df2.sample())
print(df2['author_username'].nunique())

end = timeit.timeit()
print("[INFO]... Loading Zipped csv Time:")
print(end - start)