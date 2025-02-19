# **WildWareness**

**Canvas/Slack Group Number:** 03

**Project Name:** WildWareness

## Team Members:
- Milan Dhaduk
- Audrey Tan @akt2468
- Zakaria Sisalem
- Pooja Vasanthan

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


## Models:

### 1. Wildfire Incidents
**Attributes:**
- Fire Name
- Location
- Date/time
- Severity
- Cause

**Estimated Instances:** ~3,500  
**Connections:** Linked to Emergency Shelters and Community Reports  
**Media Types:**
- Satellite images of fires
- Interactive maps

### 2. Emergency Shelters
**Attributes:**
- Name
- Location
- Capacity
- Status (Open/Closed)
- Contact Info

**Estimated Instances:** ~1000  
**Connections:** Linked to Wildfire Incidents and Wildfire Incidents  
**Media Types:**
- Images of shelter locations
- Interactive shelter maps
- Live availability updates

### 3. Community Reports
**Attributes:**
- Title
- Source
- Date/time
- Link
- Content Blurb

**Estimated Instances:** ~5000+  
**Connections:** Linked to Wildfire Incidents  
**Media Types:**
- User-uploaded images of fire conditions
- Geo-tagged reports


## Questions the Site Will Answer
- Where are the current wildfires near me?
- In California, what emergency shelters are open for wildfire evacuees?
- Are there any community-reported updates on fire conditions in my area?

