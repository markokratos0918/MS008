import numpy as np

temperatures_C = np.array([18.5, 19, 20, 25.0, 2, 30, 13.9])


avg_temp = np.mean(temperatures_C)
print(f"Average Temperature (°C): {avg_temp:.2f}")

max_temp = np.max(temperatures_C)
print(f"Highest Temperature (°C): {max_temp}")

min_temp = np.min(temperatures_C)
print(f"Lowest Temperature (°C): {min_temp}")

temperatures_f = (temperatures_c * 9/5) + 32
print("\nTemperatures in Fahrenheit:")
print(temperatures_f)

days = [0]
indices_above_20 = np.where(temperatures_c > 20)[days]
print("\nIndices of days with temperature > 20°C:")
print(indices_above_20)