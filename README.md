# **WildWareness**

**Canvas/Slack Group Number:** 03

**Project Name:** WildWareness

## Team Members:
- Milan Dhaduk @mdhaduk
- Audrey Tan @akt2468
- Zakaria Sisalem @sisalemz
- Pooja Vasanthan @PoojaVasanthan10


Phase 1 leader: Milan Dhaduk
Responsibilites: Coordinates meet times and designates tasks.

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
- [NewsData.io API](https://newsdata.io/)- Community/local reports and headlinges fetched from NewsData.io
- [Google Places API](https://console.cloud.google.com/apis/library/places-backend.googleapis.com?project=hardy-position-450923-v1)- Google's API used for fetching information about a location on Google Maps.
- [Google Maps Geocoding API](https://console.cloud.google.com/marketplace/product/google/geocoding-backend.googleapis.com?q=search&referrer=search&project=hardy-position-450923-v1) - a service that allows you to convert addresses into geographic coordinates (latitude & longitude) and vice versa (reverse geocoding).
- [List of Emergency Shelters Website](https://www.californiawildfirelawyer.com/fire-damage-list-of-shelters/) - a website containing a list of emergency shelters by county and city in the form of text.


## Models:

### 1. Wildfire Incidents
**Attributes:**
- Fire Name
- County
- Location
- Date/time
- Acres Burned

**Estimated Instances:** ~3,500  
**Connections:** Linked to Emergency Shelters and Community Reports  
**Media Types:**
- Satellite images of fires
- Interactive maps
- Embedded Videos
- Text

### 2. Emergency Shelters
**Attributes:**
- Name
- Address
- City
- Contact Info
- Status (Open/Closed)


**Estimated Instances:** ~1000  
**Connections:** Linked to Wildfire Incidents and Community Reports  
**Media Types:**
- Images of shelter locations
- Interactive Maps of Shelter
- Other Embedded Media (such as forms from shelter's website)
- Text and Links

### 3. Community Reports
**Attributes:**
- Source
- Date/time
- Category
- Region
- Reporter

**Estimated Instances:** ~5000+  
**Connections:** Linked to Wildfire Incidents and Community Reports 
**Media Types:**
- Images of Fires, Emergency Response, etc
- Interactive Maps
- Embedded Videos
- Text and Links

## Questions the Site Will Answer
- Where are the current wildfires near me?
- In California, what emergency shelters are open for wildfire evacuees?
- Are there any community-reported updates on fire conditions in my area?

## Link to Website
https://wildwareness.net/