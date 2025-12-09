import os
import json
from dotenv import load_dotenv
import weather

# Load environment variables
load_dotenv()

def get_simple_weather(city="Lipa", days=4):
    """Get weather and print to console in simple format"""
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENWEATHER_API_KEY not set in .env file")
        return
    
    try:
        # Get weather data
        print(f"🔍 Fetching weather for {city}...\n")
        data = weather.get_weather_for_city_json(city, api_key=api_key, days_ahead=days)
        
        location = f"{data['city']}, {data['country']}"
        
        # Print today's weather
        today = data['current']
        print(f"📍 Location: {location}")
        print(f"📅 Date: {today['date']}, Day: {today['day']}, Weather: {today['simple']}, Temp: {today['temp']}°C")
        print()
        
        # Print forecast
        for day in data['forecast']:
            print(f"📍 Location: {location}")
            print(f"📅 Date: {day['date']}, Day: {day['day']}, Weather: {day['simple']}, Temp: {day['temp_day']}°C")
            print()
        
        # Also output as JSON for robot parsing
        simple_json = {
            "today": {
                "location": location,
                "date": today['date'],
                "day": today['day'],
                "weather": today['simple'],
                "temp": f"{today['temp']}°C"
            },
            "forecast": []
        }
        
        for day in data['forecast']:
            simple_json["forecast"].append({
                "location": location,
                "date": day['date'],
                "day": day['day'],
                "weather": day['simple'],
                "temp": f"{day['temp_day']}°C"
            })
        
        print("\n" + "="*50)
        print("JSON OUTPUT FOR ROBOT:")
        print("="*50)
        print(json.dumps(simple_json, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple weather console for Sekai robot")
    parser.add_argument("--city", "-c", default="Lipa", help="City name (default: Lipa)")
    parser.add_argument("--days", "-d", type=int, default=4, help="Number of forecast days (default: 4)")
    
    args = parser.parse_args()
    
    get_simple_weather(args.city, args.days)