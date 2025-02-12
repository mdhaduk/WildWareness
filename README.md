# **WildWareness**

**Canvas/Slack Group Number:** 03

---

## Team Members:
- Milan Dhaduk
- Audrey Tan
- Zakaria Sisalem
- Pooja Vasanthan
**Project Name:** WildWareness
## **Proposed Project:**
is a web application designed to provide real-time wildfire information, emergency shelter locations, and community-reported fire updates.

The platform serves:
- People in wildfire-affected areas who need information on active fires and emergency shelters.
- Volunteers and first responders looking for ways to help communities impacted by wildfires.

Users can:
- Track active wildfires with real-time data.
- Find emergency shelters near affected areas.
- View and (eventually) submit community reports on wildfire conditions.

---

## **Data Sources** *(RESTful APIs and Web Scraping)*
- [NASA FIRMS API](https://firms.modaps.eosdis.nasa.gov/api/) – Provides near real-time wildfire detection from satellite imagery.
- [CAL FIRE](https://data.ca.gov/dataset/cal-fire) – Reports active and past wildfires with containment details.
- [OpenFEMA API](https://www.fema.gov/about/openfema/api) – Lists available emergency shelters.
- [Ushahidi API](https://docs.ushahidi.com/ushahidi-documentation)- Allows user-submitted community reports about wildfire conditions.

---

## **Models**
### **1. Wildfire Incidents**
**Attributes:**
- Fire Name
- Location
- Date/time
- Author
- Content Blurb

**Estimated Instances:** ~3,500  
**Connections:** Linked to **Emergency Shelters** and **Community Reports**
**Media Types:**
- Satellite images of fires
- Interactive maps

### **2. Emergency Shelters**
**Attributes:**
- Name
- Location
- Capacity
- Status (Open/Closed)
- Contact Info
**Estimated Instances:** ~1000  
**Connections:** Linked to **Wildfire Incidents**  
**Media Types:**
- Images of shelter locations
- Interactive shelter maps
- Live availability updates

### **3. Community Reports**
**Attributes:**
- Title
- Location
- Date/time
- Author
- Content Blurb


**Estimated Instances:** ~5000+  
**Connections:** Linked to **Wildfire Incidents**
**Media Types:**
- User-uploaded images of fire conditions
- Geo-tagged reports

---

## **Questions the Site Will Answer**

- Where are the current wildfires near me?
- What emergency shelters are open for wildfire evacuees?
- Are there any community-reported updates on fire conditions in my area?
