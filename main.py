import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def job_ads_by_title(title):
  max_results_per_city = 5
  city_set = ['Raleigh','Boston','Portland', 'San+Diego', 'Dallas', 'Denver', 'Hartford', 'Atlanta']
  columns = ["city", "job_title", "company_name", "location", "summary", "rating"]
  sample_df = pd.DataFrame(columns = columns)

  print('starting')
  for city in city_set:
    for start in range(0, max_results_per_city, 10):
      page = requests.get(f'https://www.indeed.com/jobs?q={title}&l=' + str(city) + '&start=' + str(start))
      soup = BeautifulSoup(page.text, "html.parser")
      time.sleep(5)  
      print(city)
      for div in soup.find_all(name="div",attrs={"class":"row"}):
        num = (len(sample_df) + 1) 
        job_post = [] 
        job_post.append(city) 
        print('getting job title')
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
          job_post.append(a["title"])
        print('getting company name')
        company = div.find_all(name="span", attrs={"class":"company"})
        if len(company) > 0:
          for b in company:
            job_post.append(b.text.strip())
        print('getting location')
        sjcl = div.find('div', attrs={'class': 'sjcl'})
        locations = sjcl.find_all('div', attrs={'class': 'location'}) 
        for location in locations: 
          job_post.append(location.text) 
        if len(locations) == 0:
          job_post.append("N/A")
        print('getting job description')
        try:
          job_post.append(div.find("summary").text)
        except:
          try:
            div_two = div.find(name="ul", attrs={"style":"list-style-type:circle;margin-top: 0px;margin-bottom: 0px;padding-left:20px;"})
            div_three = div_two.find("li")
            job_post.append(div_three.text.strip())
          except:
            job_post.append("Nothing_found")
        print('getting rating')
        rating = sjcl.find_all(name="span", attrs={"class": "ratingsContent"})
        for r in rating:
          job_post.append(r.text.strip())
        if len(rating) == 0:
          job_post.append("N/A")

        sample_df.loc[num] = job_post
        print(sample_df.loc[num])

  return sample_df


if __name__ == "__main__":
  data_engineer_df = job_ads_by_title("data+engineer") 
  big_data_df= job_ads_by_title("big+data+developer") 
  
  data_engineer_df.to_csv("data_engineer_jobs.csv", encoding='utf-8')
  big_data_df.to_csv("big_data_developer_jobs.csv", encoding='utf-8')
