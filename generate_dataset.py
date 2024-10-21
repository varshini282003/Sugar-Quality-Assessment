import numpy as np
import pandas as pd

# Define factors and their ranges
factors = {
    'Sweetness': (0, 10),
    'Moisture_content': (0, 10),
    'Impurities': (0, 5),
    'Acidity': (0, 14),
    'Color': (0, 10),
    'Particle_size': (0, 500),
    'Crystallinity': (0, 100),
    'Granulation': (0, 10),
    'Solubility': (0, 100),
    'Density': (0, 2),
    'Reducing_sugars': (0, 10),
    'Total_sugar_content': (0, 100),
    'Quality': (0, 100)  # Target variable
}

# Function to generate random dataset
def generate_random_values(num_samples=1):
    np.random.seed(0)  # For reproducibility
    data = {factor: np.random.uniform(low, high, num_samples) for factor, (low, high) in factors.items()}
    df = pd.DataFrame(data)
    return df.iloc[0].tolist()  # Return a single row as a list of values

if __name__ == "__main__":
    num_samples = 1700
    dataset = generate_random_values(num_samples)
    dataset.to_csv('sugar_quality_dataset.csv', index=False)
    print(f"Dataset saved successfully with {num_samples} samples.")
