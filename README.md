# **WildWareness**

**Canvas/Slack Group Number:** 03

**Project Name:** WildWareness

## Link to Website
https://wildwareness.net/

## **Git SHA**
- 

## **API Documentation**
- [API Design - Postman](https://documenter.getpostman.com/view/31322139/2sAYdZvEUy)

## **API Endpoint**
- [https://api.wildwareness.net/](https://api.wildwareness.net/)

## Team Members:
- Milan Dhaduk @mdhaduk
- Audrey Tan @akt2468
- Zakaria Sisalem @sisalemz
- Pooja Vasanthan @PoojaVasanthan10


Phase 1 

Phase leader: Milan Dhaduk                                                   
Responsibilites: Determine meeting times, assign tasks, ensure progress being made.

**Estimated Time to Completion:**
- Milan Dhaduk - 11 hours
- Audrey Tan - 10 hours
- Zakaria Sisalem - 10 hours
- Pooja Vasanthan - 10 hours

**Actual Time to Completion:**
- Milan Dhaduk - 16 hours
- Audrey Tan - 13 hours
- Zakaria Sisalem - 12 hours
- Pooja Vasanthan - 13 hours




Phase 2

Phase leader: Pooja Vasanthan                                               
Responsibilites: Determine meeting times, assign tasks, ensure progress being made.

**Estimated Time to Completion:**
- Milan Dhaduk - 17 hours
- Audrey Tan - 16 hours
- Zakaria Sisalem - 15 hours
- Pooja Vasanthan - 16 hours

**Actual Time to Completion:**
- Milan Dhaduk - 35 hours
- Audrey Tan - 30 hours
- Zakaria Sisalem - 30 hours
- Pooja Vasanthan - 32 hours


Phase 3 leader: Audrey Tan                                                     
Responsibilites: Determine meeting times, assign tasks, ensure progress being made.

Phase 4 leader: Zakaria Sisalem                                                 
Responsibilites: Determine meeting times, assign tasks, ensure progress being made.



## **Proposed Project:**
WildWareness is a web application designed to provide real-time wildfire information, emergency shelter locations, and community-reported fire updates in the state of California.

The platform serves:
- People in wildfire-affected areas who need information on active fires and emergency shelters.
- Volunteers and first responders looking for ways to help communities impacted by wildfires.

Users can:
- Track active wildfires with real-time data.
- Find emergency shelters near affected areas.
- View and (eventually) submit community reports on wildfire conditions.

## **Data Sources** *(RESTful APIs and Web Scraping)*
- [CAL FIRE](https://www.fire.ca.gov/incidents/2025) – Reports active and past wildfires with containment details (2025)
- [TheNewsAPI](https://www.thenewsapi.com/documentation)- Information about news/local reports and headlines fetched from TheNewsAPI.
- [Google Maps API](https://mapsplatform.google.com/pricing/?utm_source=google&utm_medium=cpc&utm_campaign=gmp25_us_search_api&gad_source=1&gclid=CjwKCAjwp8--BhBREiwAj7og1_8QWnO-NMYt295SA5xAZgVTAEWjR5t_f_M6DDBTlr6awfqMmf4eRRoC5IAQAvD_BwE&gclsrc=aw.ds)-  Google's API is used for fetching information about a location.
- [Leaflet](https://leafletjs.com/) – an API used for map rendering given details of a location.
- [Google Maps Geocoding API](https://console.cloud.google.com/marketplace/product/google/geocoding-backend.googleapis.com?q=search&referrer=search&project=hardy-position-450923-v1) - a service that allows you to convert addresses into geographic coordinates (latitude & longitude) and vice versa (reverse geocoding).
- [Google Custom Search API](https://developers.google.com/custom-search/v1/overview) - Google’s API allows data to be retrieved from custom search results.


## Models:

### 1. Wildfire Incidents
**Attributes:**
- Fire Name
- County
- Location
- Year
- Acres Burned

**Estimated Instances:** 310  
**Connections:** Linked to Emergency Shelters and Community Reports  
**Media Types:**
- Images
- Interactive maps
- Text

### 2. Emergency Shelters
**Attributes:**
- Name
- Address
- Phone
- Website
- Rating


**Estimated Instances:** 207  
**Connections:** Linked to Wildfire Incidents and Community Reports  
**Media Types:**
- Images of shelter
- Interactive Maps of Shelter
- Text and Links

### 3. Community Reports
**Attributes:**
- Title
- Source
- Date
- Author
- Categories

**Estimated Instances:** 115  
**Connections:** Linked to Wildfire Incidents and Emergency Shelters
**Media Types:**
- Images of Relevant to Articles
- Interactive Maps
- Text and Links

## Questions the Site Will Answer
- Where are the current wildfires near me?
- In California, what emergency shelters are open for wildfire evacuees?
- Are there any community-reported updates on fire conditions in my area?

## Comments
- It's important to note that we referenced last year's HomelessAid in developing 
our HTML/CSS for Phase I and in the code development of Phase 2.
