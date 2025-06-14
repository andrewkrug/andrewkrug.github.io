# YAML Data & Where's Andrew Page Update

## ✅ Completed Updates

### 1. **Converted Data to YAML Format**
- **Removed**: `src/_data/site.json`
- **Added**: `src/_data/site.yaml` - Clean YAML format for all site configuration
- **Added**: `src/_data/events.yaml` - Comprehensive event and location data

### 2. **Created "Where's Andrew" Page**
- **File**: `src/wheres-andrew.njk`
- **URL**: `/wheres-andrew/`
- **Features**:
  - Interactive event map placeholder (ready for real mapping API)
  - Event filtering by type (upcoming, recent, security, cloud)
  - Upcoming events with full details
  - Recent appearances timeline
  - Regular locations (home/office)
  - Mobile-responsive design

### 3. **Updated Navigation**
- Added "Where's Andrew" to main navigation menu
- Navigation now includes: Home, About, Speaking, Writing, **Where's Andrew**, Contact

### 4. **Event Data Structure**
The new YAML data includes:

**Upcoming Events:**
- DevLeadership Summit 2024 (Austin, TX)
- CloudNative Conference (San Francisco, CA)
- BSides Las Vegas (Las Vegas, NV)

**Recent Events:**
- BlackHat USA 2024
- AWS re:Invent 2023
- BSides San Francisco 2024
- Wild West Hackin' Fest 2023

**Regular Locations:**
- Datadog HQ (New York, NY)
- Home Base (Medford, OR)

### 5. **Interactive Features**
- **Event Filtering**: Filter events by type or time period
- **Map Integration**: Placeholder for interactive map with coordinates
- **Show on Map**: Buttons to focus map on specific locations
- **Responsive Design**: Mobile-optimized layout and controls

## 🗂️ File Structure Changes

```
src/
├── _data/
│   ├── site.yaml          ✅ NEW - YAML site configuration
│   └── events.yaml        ✅ NEW - Event and location data
├── wheres-andrew.njk       ✅ NEW - Interactive event page
└── _includes/
    └── nav.njk            ✅ UPDATED - Added Where's Andrew link
```

## 🚀 Technical Implementation

**YAML Benefits:**
- More readable and maintainable than JSON
- Supports comments and multi-line strings
- Native support in 11ty for YAML data files

**Page Features:**
- Semantic HTML structure
- CSS Grid and Flexbox layouts
- JavaScript for filtering and map interactions
- Coordinate data ready for real mapping APIs (Mapbox, Google Maps, etc.)

**Mobile Responsive:**
- Smaller map on mobile devices
- Wrapped navigation menu
- Condensed filter buttons
- Optimized card layouts

## 🔄 Data Migration
All existing site data successfully migrated from JSON to YAML:
- Site metadata (name, description, URLs)
- Social media handles (including Instagram: @therealandrewkrug)
- Author information
- Contact details

## ✅ Build Status
- **Site builds successfully**: All pages render correctly
- **Navigation works**: New page accessible from main menu
- **Data loads**: YAML files processed correctly by 11ty
- **Responsive**: Mobile-friendly across all devices

The "Where's Andrew" page provides a comprehensive view of Andrew's conference schedule and travel, making it easy for attendees to connect at events!