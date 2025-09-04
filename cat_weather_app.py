from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import requests
import geocoder

# ========== CONFIG ==========
API_KEY = "f353e03c3bff34d83b7f879e2d286bf4"  # replace with your API key
UNIT = "metric"               # "metric" = Celsius, "imperial" = Fahrenheit
# ============================

class WeatherApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.label = Label(text=" Press button to get weather!", font_size=20)
        self.button = Button(text="Get Weather", size_hint=(1, 0.2))
        self.button.bind(on_press=self.get_weather)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)

        return self.layout

    def get_weather(self, instance):
        # Get current location
        g = geocoder.ip('me')
        lat, lng = g.latlng

        # Reverse geocode to get city/state
        g_rev = geocoder.osm([lat, lng], method='reverse', headers={'User-Agent': 'CatWeatherApp/1.0'})
        print(f"datag={(g_rev)}")

        city = g_rev.city
        state = g_rev.state
        country = g_rev.country

        # print(f"datag={repr(g)}")

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={API_KEY}&units={UNIT}"
        try:
            response = requests.get(url)
            data = response.json()

            print(f"data: {data}");

            if data["cod"] != 200:
                self.label.text = f" Hey Meow! I couldn't fetch the weather for {city} {state} {country}"

            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]

            # Cat-style formatted message
            self.label.text = f" Hey Meow! Today in {city}, it's {temp}°C with {description}. Purr~"

        except Exception as e:
             self.label.text = f" Oops! Something went wrong: {e}"

if __name__ == "__main__":
    WeatherApp().run()