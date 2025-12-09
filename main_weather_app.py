from flask import Flask, request, jsonify
import os
import traceback
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import directly from weather.py in the same folder
try:
    import weather
    print("✅ Successfully imported weather module")
    print(f"✅ Found function: {hasattr(weather, 'get_weather_for_city_json')}")
except Exception as e:
    print(f"❌ Failed to import weather module: {e}")
    traceback.print_exc()

app = Flask(__name__)

@app.get("/weather")
def weather_endpoint():
    city = request.args.get("city", "Lipa City")
    days = int(request.args.get("days", 4))
    api_key = request.args.get("api_key") or os.getenv("OPENWEATHER_API_KEY")
    
    print(f"\n🔍 Request received:")
    print(f"   City: {city}")
    print(f"   Days: {days}")
    print(f"   API Key set: {bool(api_key)}")
    
    try:
        data = weather.get_weather_for_city_json(
            city, 
            api_key=api_key, 
            days_ahead=days
        )
        print(f"✅ Weather data retrieved successfully")
        return jsonify(data)
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error: {error_msg}")
        traceback.print_exc()
        return jsonify({
            "error": error_msg,
            "city": city,
            "days": days,
            "api_key_set": bool(api_key)
        }), 400

@app.get("/simple")
def simple_weather():
    """Simplified endpoint - only essential data for Sekai robot"""
    city = request.args.get("city", "Lipa City")
    days = int(request.args.get("days", 4))
    api_key = request.args.get("api_key") or os.getenv("OPENWEATHER_API_KEY")
    
    print(f"\n🔍 Simple weather request:")
    print(f"   City: {city}")
    print(f"   Days: {days}")
    
    try:
        data = weather.get_weather_for_city_json(
            city, 
            api_key=api_key, 
            days_ahead=days
        )
        
        location = f"{data['city']}, {data['country']}"
        
        # Build simplified response - Location in every entry
        simple = {
            "today": {
                "location": location,
                "date": data['current']['date'],
                "day": data['current']['day'],
                "weather": data['current']['simple'],
                "temp": f"{data['current']['temp']}°C"
            },
            "forecast": []
        }
        
        for day in data['forecast']:
            simple["forecast"].append({
                "location": location,
                "date": day['date'],
                "day": day['day'],
                "weather": day['simple'],
                "temp": f"{day['temp_day']}°C"
            })
        
        # Print to console for robot debugging
        print(f"\n📅 Today - Location: {location}, Date: {simple['today']['date']}, Day: {simple['today']['day']}, Weather: {simple['today']['weather']}, Temp: {simple['today']['temp']}")
        for f in simple["forecast"]:
            print(f"📅 Location: {f['location']}, Date: {f['date']}, Day: {f['day']}, Weather: {f['weather']}, Temp: {f['temp']}")
        print()
        
        return jsonify(simple)
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error: {error_msg}")
        return jsonify({"error": error_msg}), 400

@app.get("/")
def home():
    return jsonify({
        "message": "Weather API is running!",
        "endpoints": {
            "/weather": "Full weather data (params: city, days)",
            "/simple": "Simplified data for Sekai robot (params: city, days)"
        },
        "examples": {
            "full": "/weather?city=Lipa&days=4",
            "simple": "/simple?city=Lipa&days=4"
        }
    })

if __name__ == "__main__":
    print("🌤️  Weather API Server Starting...")
    print("📍 Default city: Lipa City, Philippines")
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if api_key:
        print(f"✅ API Key is set (starts with: {api_key[:8]}...)")
    else:
        print("⚠️  WARNING: OPENWEATHER_API_KEY not set!")
    
    print("\n🌐 Server running at: http://127.0.0.1:5000")
    print("\n📝 Test URLs:")
    print("   Full data:   http://127.0.0.1:5000/weather?city=Lipa&days=4")
    print("   Simple data: http://127.0.0.1:5000/simple?city=Lipa&days=4")
    print("   (For Sekai robot, use /simple endpoint)\n")
    app.run(host="0.0.0.0", port=5000, debug=True)