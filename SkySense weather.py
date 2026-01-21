import tkinter as tk
import requests
from tkinter import messagebox

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    output.configure(state="normal")
    output.delete("1.0", tk.END)

    try:
        # --- Geocoding ---
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_data = requests.get(geo_url).json()

        if not geo_data.get("results"):
            output.insert(tk.END, "City not found ❌")
            output.configure(state="disabled")
            return

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        # --- Weather ---
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current_weather=true&hourly=precipitation_probability"
        )
        weather_data = requests.get(weather_url).json()

        current = weather_data.get("current_weather", {})
        temp = current.get("temperature", "N/A")
        wind = current.get("windspeed", "N/A")
        wind_dir = current.get("winddirection", "N/A")

        precip = weather_data.get("hourly", {}).get("precipitation_probability", [])
        precip_chance = f"{precip[0]}%" if precip else "N/A"

        # --- Output ---
        output.insert(tk.END, f"📍 City: {city}\n")
        output.insert(tk.END, f" Lattitude: {round(lat,3)} , longitude: {round(lon,3)}\n\n")
        output.insert(tk.END, f"🌡 Temperature: {temp} °C\n")
        output.insert(tk.END, f"💨 Wind Speed: {wind} km/h\n")
        output.insert(tk.END, f"🧭 Wind Direction: {wind_dir}°\n")
        output.insert(tk.END, f"🌧 Chance of Rain: {precip_chance}\n")

    except Exception as e:
        output.insert(tk.END, f"Error fetching data ❌\n{e}")

    output.configure(state="disabled")


# ---------------- GUI ----------------
root = tk.Tk()
root.state("zoomed")
root.title("SkySense Weather")

main_frame = tk.Frame(root, bg="#F2F4F8")
main_frame.pack(fill="both", expand=True)

tk.Label(
    main_frame,
    text="SkySense Weather",
    font=("Segoe UI Semibold", 52),
    fg="#1F2937",
    bg="#F2F4F8"
).pack(pady=30)

tk.Frame(main_frame, height=2, bg="black").pack(fill="x", pady=10)

# Input
input_frame = tk.Frame(main_frame, bg="#E5E7EB", padx=25, pady=20)
input_frame.pack(pady=20)

tk.Label(
    input_frame,
    text="Enter city name",
    font=("Segoe UI", 20),
    bg="#E5E7EB"
).pack(side=tk.LEFT, padx=(0, 15))

city_entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 20),
    width=24,
    bd=0
)
city_entry.pack(side=tk.LEFT)

# Button
tk.Button(
    main_frame,
    text="Get Current Weather",
    font=("Segoe UI Semibold", 18),
    bg="#3B82F6",
    fg="white",
    bd=0,
    padx=30,
    pady=12,
    cursor="hand2",
    command=get_weather
).pack(pady=30)

# Output box
prediction_frame = tk.Frame(main_frame, bg="white")
prediction_frame.pack(pady=30)

output = tk.Text(
    prediction_frame,
    height=10,
    width=100,
    font=("Segoe UI", 16),
    bg="white",
    bd=0
)
output.pack(pady=20)
output.configure(state="disabled")

root.mainloop()

