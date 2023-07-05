from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from folium.plugins import MarkerCluster
from bs4 import BeautifulSoup
import requests,datetime,random
import folium,requests
from .models import Job,LastRefreash
from datetime import datetime, timedelta
def getLoc(address):    
    """
    Get longitude and latitude coordinates for a given address using a geocoding API.

    Args:
        address (str): The address to geocode.

    Returns:
        tuple: A tuple containing the longitude and latitude coordinates.
               If the coordinates cannot be obtained, returns (None, None).
    """
    try:
        addres=address.replace(' ','+')
        
        print("req loc of ", addres)
        response = requests.get(f"https://geocode.search.hereapi.com/v1/geocode?q={addres}&apiKey=rllzMKVvoddnP-NF_-BOhPf97Xi7iIU_Wd15Ge7Y-CI")
        
        if response.status_code == 200 and response.json():
            print("loc found")
            location = response.json()['items'][0]['position']
            return location['lng'], location['lat']
        else:
            return None,None
    except:
            return None,None

def plotMap():
    """
    Plot the job locations on a map and save it as HTML.

    Returns:
        JsonResponse: A JSON response indicating the status of the operation.
    """
    map = folium.Map(min_zoom=4, max_zoom=19,location=[ 32.871172,70.954883], zoom_start = 5.3,tiles='Cartodbdark_matter',
            attr='My Data Attribution')
    print("plotingg")
    coordinates=[]
    for job in list(Job.objects.all()):
        long,lat=getLoc(job.location)
        if (long or lat):
            print("add marker")
            coordinates.append([job.title, [lat,long],job.id])
    offset = 0.001
    coordinates = [[coord[0],[coord[1][0]+offset*i-random.random()/100, coord[1][1]+offset*i+random.random()/100],coord[2]] for i, coord in enumerate(coordinates)]
    print(coordinates)
    marker_cluster = MarkerCluster().add_to(map)

    for coord in coordinates:
        marker_html = f'''<div id="jobID-{coord[2]}" onClick="discription({coord[2]});">
        {coord[0].upper()}\nclick for more details
        </div>'''
        folium.Marker(location=coord[1],popup=marker_html,icon=folium.Icon(icon='briefcase', color='red')).add_to(marker_cluster)
    map.save("jobmap/templates/JobMap/map.html")
    HttpResponseRedirect(reverse('index'))
    return JsonResponse({'status':'sucess'},status=201)

def scrapeJobs(request):
    
    """
    Scrape job listings from a website and save them to the database.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the status of the operation.
    """
    if LastRefreash.objects.count()==0:
        LastRefreash.objects.create(date='starting')
        
    if LastRefreash.objects.last().date not in [(datetime.today().date()-timedelta(days=i)).strftime("%Y-%m-%d") for i in range(34)]:
        LastRefreash.objects.all().delete()
        Job.objects.all().order_by('-id').delete()
        LastRefreash.objects.create(date=str(datetime.today().date()))
        print('started')
        html_txt=requests.get("https://pk.linkedin.com/jobs/search?keywords=Software%20Development&location=Pakistan&locationId=&geoId=101022442&f_TPR=r604800&position=1&pageNum=0").text
        Mainsoup=BeautifulSoup(html_txt,'lxml')
        jobs=Mainsoup.find_all("div",class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")
        print("scraping fresh")
        for job in jobs:
            apply='';apply_ln=''
            try:
                apply=BeautifulSoup(requests.get(job.a.get('href')).text,'lxml').find('a',class_="sign-up-modal__company_webiste").get('href')
            except:
                apply_ln=job.a.get('href')
            try:
                discription=BeautifulSoup(requests.get(job.a.get('href')).text,'lxml').find('div',class_="show-more-less-html__markup show-more-less-html__markup--clamp-after-5").text.replace('\n','<br>')
            except:
                discription=""
            for punc in ['(','\'',')','.']:
                if punc in discription:
                    discription.replace(punc,'<br>')
            a=Job(title=job.a.span.text.strip(),
            apply=apply,apply_linkedIn=apply_ln,discription=discription,
            company=job.find('div',class_='base-search-card__info').a.text.strip(),
            location=job.find('div',class_='base-search-card__info').div.find('span',class_='job-search-card__location').text.strip(),
            time=job.find('div',class_='base-search-card__info').div.time.text.strip(),
            company_linkedIn=job.find('div',class_='base-search-card__info').a.get('href')
            )
            if a not in Job.objects.all():
                a.save()
        return plotMap()
    else:
        return JsonResponse({'status':'sucess'},status=201)
def main():
    """
    Main entry point of the script.
    """
    scrapeJobs('')
if __name__=='__main__':
    main()