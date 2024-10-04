#!/usr/bin/env python
# coding: utf-8

# In[4]:


from bs4 import BeautifulSoup
import requests
import pandas as pd


# In[5]:


headers = {
    "User-Agent" : "Mozilla/5.0 (Linux; Android 7.0; Nexus 8 Build/NPD90G) AppleWebKit/600.18 (KHTML, like Gecko)  Chrome/52.0.2311.359 Mobile Safari/534.2"
}

l = []

url = 'https://www.albumoftheyear.org/album/940786-eminem-the-death-of-slim-shady-coup-de-grace/user-reviews/?sort=recent&type=ratings'
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "html")

artist = soup.find('div', class_='artist').text.strip()
album = soup.find('div', class_='albumTitle').text.strip()
review_count = soup.find('div', class_='userReviewCounter').text.strip()
review_count_text = review_count.split()

page_cap = int(review_count_text[5])/(int(review_count_text[3]) - int(review_count_text[1]) + 1) # Denominator is inclusive
print(review_count_text)


# In[6]:


for x in range(1, int(page_cap)+2): # +1 to account for the few extra reviews on pg. page_cap+1 and another +1 for the loop
    url = f'https://www.albumoftheyear.org/album/940786-eminem-the-death-of-slim-shady-coup-de-grace/user-reviews/?p={x}&sort=recent&type=ratings'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html")
    
    users = soup.find_all('div', class_='userRatingBlock')
    for user in users:
        username = user.find('div', class_='userName').text.strip()
        date = user.find('div', class_='date')['title']
        rating = user.find('div', class_='ratingBlock').text.strip()

        individual_user_data = {
            'Username' : username,
            'Date' : date,
            'Rating' : rating
        }
        
        l.append(individual_user_data)
        
        if len(l) == review_count_text[5]:
            break

print("almost done. please hold...")
df = pd.DataFrame(l)
file_title = f"{artist} - {album} Ratings"
df.to_csv(f'{file_title}.csv', index=False)
print("process complete")


# In[ ]:




