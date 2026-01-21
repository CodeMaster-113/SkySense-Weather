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
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_data = requests.get(geo_url).json()

        if not geo_data.get("results"):
            output.insert(tk.END, "City not found ❌")
            output.configure(state="disabled")
            return

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

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

        output.insert(tk.END, f"📍 City: {city}\n")
        output.insert(tk.END, f"📌 Latitude: {round(lat,3)}, Longitude: {round(lon,3)}\n\n")
        output.insert(tk.END, f"🌡 Temperature: {temp} °C\n")
        output.insert(tk.END, f"💨 Wind Speed: {wind} km/h\n")
        output.insert(tk.END, f"🧭 Wind Direction: {wind_dir}°\n")
        output.insert(tk.END, f"🌧 Chance of Rain: {precip_chance}\n")

    except Exception as e:
        output.insert(tk.END, f"Error fetching data ❌\n{e}")

    output.configure(state="disabled")

def clear():
    output.configure(state="normal")
    output.delete("1.0", tk.END)
    output.configure(state="disabled")
    city_entry.delete(0, tk.END)


# ---------------- GUI ----------------
def main():
    global city_entry, output

    root = tk.Tk()
    root.title("SkySense Weather")
    root.state("zoomed")
    root.configure(bg="#F8FAFC")

    # OPTIONAL (if you add icon.ico)
    # root.iconbitmap("icon.ico")

    main_frame = tk.Frame(root, bg="#F8FAFC")
    main_frame.pack(fill="both", expand=True)

    tk.Label(
        main_frame,
        text="SkySense Weather",
        font=("Segoe UI Variable", 48, "bold"),
        fg="#0F172A",
        bg="#F8FAFC"
    ).pack(pady=(30, 10))

    tk.Frame(main_frame, height=2, bg="#CBD5E1").pack(fill="x", padx=200, pady=10)

    input_frame = tk.Frame(main_frame, bg="white", padx=30, pady=25)
    input_frame.pack(pady=25)

    tk.Label(
        input_frame,
        text="Enter city name",
        font=("Segoe UI Semibold", 18),
        bg="white",
        fg="#1E293B"
    ).pack(side=tk.LEFT, padx=(0, 15))

    city_entry = tk.Entry(
        input_frame,
        font=("Segoe UI", 18),
        width=26,
        bd=0,
        bg="#F1F5F9",
        fg="#0F172A",
        insertbackground="#0F172A"
    )
    city_entry.pack(side=tk.LEFT, ipady=8)

    button_frame = tk.Frame(main_frame, bg="#F8FAFC")
    button_frame.pack(pady=25)

    tk.Button(
        button_frame,
        text="🌤 Get Current Weather",
        font=("Segoe UI Semibold", 16),
        bg="#2563EB",
        fg="white",
        bd=0,
        padx=36,
        pady=12,
        cursor="hand2",
        activebackground="#1D4ED8",
        command=get_weather
    ).pack(side=tk.LEFT, padx=16)

    tk.Button(
        button_frame,
        text="🧹 Clear Forecast Box",
        font=("Segoe UI Semibold", 16),
        bg="#EF4444",
        fg="white",
        bd=0,
        padx=36,
        pady=12,
        cursor="hand2",
        activebackground="#DC2626",
        command=clear
    ).pack(side=tk.LEFT, padx=16)

    prediction_frame = tk.Frame(main_frame, bg="white", padx=40, pady=30)
    prediction_frame.pack(pady=30)

    output = tk.Text(
        prediction_frame,
        height=9,
        width=80,
        font=("Segoe UI", 16),
        bg="white",
        fg="#0F172A",
        bd=0,
        wrap="word"
    )
    output.pack()
    output.configure(state="disabled")

    root.mainloop()


# ✅ REQUIRED FOR APP BUILD
if __name__ == "__main__":
    main()
