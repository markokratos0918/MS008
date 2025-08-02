import numpy as np

temperatures_C = np.array([18.5, 19, 20, 25.0, 2, 30, 13.9])
avg_temp = np.mean(temperatures_C)
max_temp = np.max(temperatures_C)
min_temp = np.min(temperatures_C)
temperatures_f = (temperatures_C * 9/5) + 32
indices_above_20 = np.where(temperatures_C > 20)[0]
if __name__ == "__main__":
    print(f"Average Temperature (°C): {avg_temp:.2f}")
    print(f"Highest Temperature (°C): {max_temp}")
    print(f"Lowest Temperature (°C): {min_temp}")
    print("\nTemperatures in Fahrenheit:")
    print(temperatures_f)
    print("\nIndices of days with temperature > 20°C:")
    print(indices_above_20)