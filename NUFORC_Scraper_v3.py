# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:53:35 2023

@author: aidan
"""

# get requests to interact with html and beautifulsoup to parse responses
import requests
from bs4 import BeautifulSoup
import pandas as pd

# get response from main webpage and parse
response = requests.get('https://nuforc.org/webreports/ndxevent.html')
soup = BeautifulSoup(response.content, 'html.parser')

# get all links from parsed response using the <a> character
time_links = soup.find_all("a") # Find all elements with the tag <a>

# counter to ignore certain useless links
count = 0

# url to append to the start of each link discovered in the page
time_pre_url = 'https://nuforc.org/webreports/'
event_pre_url = ''

# loop over all time-based links provided by response
for time_link in time_links:
    
    # ignore first and final links
    if count > 0 and count < len(time_links)-1:
   
        # print current time-based link
        print("Time link:", time_link.get("href"))
        
        # assign URL to variable
        this_time_link = time_link.get('href')
        
        # get html response from this time-based link
        time_link_response = requests.get(time_pre_url+this_time_link)
        time_link_soup = BeautifulSoup(time_link_response.content, 'html.parser')
        
        # find all event-based links associated with this time-based link
        event_links = time_link_soup.find_all("a")
        
        # iterate over event-based links to extract useful data
        count2 = 0 # counter used to ignore first link
        
        # title of this dataset to be saved
        dataset_title = time_link_soup.find('title').text + '.csv'
        dataset_title = dataset_title.replace('/','-')
        
        #populate dataframe
        if count2 == 0:
            # create new dataframe to be populated
            df = pd.DataFrame(columns=['Date','Location','Shape','Characteristics'],index=[0])
            
        for event_link in event_links:
            
            # ignore first link
            if count2 > 0:
                
                try: 
                            
                    # print current event-based link
                    print("Event link:", event_link.get("href"))
                    
                    # get html response and parse it
                    event_link_response = requests.get(time_pre_url+event_link.get('href'))
                    event_link_soup = BeautifulSoup(event_link_response.content, 'html.parser')
                    
                    # extract the sighting characteristics for this event
                    event_table = event_link_soup.find_all('table')[0]
                    
                    # get occurance date
                    date_filtered = event_link_soup.find('body').text.split('Entered as : ')[1]
                    event_date = date_filtered.split(')Reported:')[0]
                
                    print(event_date)
                    
                    # get location of event
                    event_location = event_link_soup.find('body').text.split('Location: ')[1]
                    event_location = event_location.split('Shape')[0]
                    
                    print(event_location)
                    
                    # get shape of sighted craft
                    event_shape = event_link_soup.find('body').text.split('Shape: ')[1]
                    event_shape.split('Du')[0]
                    print(event_shape)
                    
                    # get characteristics
                    row = event_table.find_all("tr")[-1]
                    event_characteristics = [cell.get_text(strip=True) for cell in row.find_all("td")][0]
                    
                    print(event_characteristics)
                    print('\n')
                    
                    if count2 > 1:
                        df.loc[df.index.max() + 1] = [event_date,event_location,event_shape,event_characteristics]

                except:
                #    break
                    continue
                
            # increment counter
            count2 += 1
            
        # save this dataframe after dropping any rows with empty values and using date as index
        # also correct some issues in the 'shape' category
        df['Shape']=df['Shape'].str.replace('Duration', '')
        df['Shape']=df['Shape'].str.replace('Duratio', '')
        df['Shape']=df['Shape'].str.replace('Durati', '')
        df['Shape']=df['Shape'].str.replace('Durat', '')
        df['Shape']=df['Shape'].str.replace('Dura', '')
        df['Shape']=df['Shape'].str.replace('Dur', '')
        df['Shape']=df['Shape'].str.replace('Du', '')
        df['Shape']=df['Shape'].str.split(':').str[0]
        df.set_index('Date',inplace=True,drop=True)
        df.dropna(how='any',inplace=True)
        df.to_csv('.\\Scraped Data\\'+dataset_title)

    # increment counter
    print(count)
    count += 1


















