import numpy as np

if __name__ == "__main__":

    rainfall = [0.0, 5.2, 3.1, 0.0, 12.4, 0.0, 7.5]

    rainfall_array = np.array(rainfall)
    print("Rainfall Data:", rainfall_array)

    total_rainfall = np.sum(rainfall_array)
    print(f"Total rainfall for the week: {total_rainfall:.2f} mm")

    
    avg_rainfall = np.mean(rainfall_array)
    print(f"Average rainfall for the week: {avg_rainfall:.2f} mm")

  
    no_rain_days = np.sum(rainfall_array == 0)  
    print("Number of days with no rain:", no_rain_days)

    # Print the days (by index) where the rainfall was more than 5 mm
    days_more_than_5mm = np.where(rainfall_array > 5)[0]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_names = [days[i] for i in days_more_than_5mm]
    print("Days with rainfall > 5 mm (indices):", day_names)