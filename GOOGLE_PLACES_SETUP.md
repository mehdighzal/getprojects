# Google Places API Setup Guide

## ✅ Integration Complete!

The application is now configured to use **Google Places API** for real business data instead of AI-generated examples.

## 🔑 Get Your API Key

To get real business data, you need a Google Places API key with billing enabled:

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Note your project name/ID

### Step 2: Enable Required APIs

1. Go to **APIs & Services** → **Library**
2. Search and enable:
   - ✅ **Places API** (New)
   - ✅ **Geocoding API**
   
### Step 3: Enable Billing

⚠️ **Important:** Google Places API requires billing enabled

1. Go to **Billing** in Cloud Console
2. Link a billing account (credit card required)
3. **Free Tier:** Google provides **$200/month free credit** for Maps Platform
4. After free credit, pricing is:
   - Text Search: $32 per 1000 requests
   - Place Details: $17 per 1000 requests
   - Geocoding: $5 per 1000 requests

**Note:** For development/testing, $200 free credit is more than enough!

### Step 4: Create API Key

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **API Key**
3. Copy your API key (e.g., `AIza...`)

### Step 5: Secure Your API Key (Recommended)

1. Click **Edit API Key** (pencil icon)
2. Under **Application restrictions**:
   - Choose "HTTP referrers" for web app
   - Add: `http://localhost:3001/*` and your production domain
3. Under **API restrictions**:
   - Choose "Restrict key"
   - Select: Places API, Geocoding API
4. Save

### Step 6: Update Your .env

Add to your `.env` file:

```bash
GOOGLE_PLACES_API_KEY=your_actual_api_key_here
```

### Step 7: Restart Server

```bash
# Stop the server (Ctrl+C)
# Restart
python manage.py runserver
```

## 🧪 Testing

### Method 1: Using Test Script

```bash
python test_places_api.py
```

Expected output:
```
SUCCESS! Found 10 real businesses:
--------------------------------------------------

1. Osteria dei Cavalieri
   Address: Via San Frediano, 16, 56127 Pisa PI, Italy
   Phone: +39 050 580858
   Website: http://www.osteriacavalieri.pisa.it/
   Rating: 4.5 stars (1234 reviews)
...
```

### Method 2: Using Frontend

1. Go to http://localhost:3001
2. Login
3. Search: Country=Italy, City=Pisa, Category=Restaurant
4. See real businesses with verified data!

## 📊 What You Get

With Google Places API, each business includes:

- ✅ **Real business name**
- ✅ **Verified address** (formatted for the country)
- ✅ **Phone number** (if publicly available)
- ✅ **Website** (if available)
- ✅ **Google rating** & review count
- ✅ **Google Place ID** (for additional details)
- ✅ **Business types/categories**

## 🚨 Troubleshooting

### "No businesses found"
- ✅ Check API key is correct in `.env`
- ✅ Verify Places API is enabled in Cloud Console
- ✅ Confirm billing is enabled
- ✅ Check API key restrictions (should allow Places API)
- ✅ Try broader search (just city, no category)

### "API key not configured"
- ✅ Make sure `GOOGLE_PLACES_API_KEY` is in `.env`
- ✅ Restart Django server after updating `.env`

### "Billing not enabled" error
- ✅ Go to Cloud Console → Billing
- ✅ Link a billing account
- ✅ Wait 5-10 minutes for activation

### Rate limits / Quota exceeded
- ✅ Check usage in Cloud Console → APIs & Services → Dashboard
- ✅ Adjust quotas or upgrade billing

## 💰 Cost Estimation

### Development/Testing (with $200 free credit):
- ~6,200 searches per month (FREE)
- Perfect for development!

### Production (after free credit):
- Low traffic (1000 searches/month): ~$32
- Medium traffic (10,000 searches/month): ~$320
- Consider caching results to reduce costs

## 🔄 Alternative: Use Database

If you don't want to use Google Places API:

1. Manually add businesses to database:
   ```python
   python manage.py shell
   from businesses.models import Business
   Business.objects.create(
       name="Restaurant Name",
       email="info@restaurant.com",
       ...
   )
   ```

2. Or import from CSV/Excel

3. Or integrate with other APIs (Yelp, Foursquare)

## ✅ You're All Set!

Once you have a valid API key with billing enabled, you'll get real, verified business data from Google Maps! 🎉

