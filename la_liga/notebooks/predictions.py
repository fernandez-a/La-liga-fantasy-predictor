import pickle

# Load the pickled model
with open('random_forest.pkl', 'rb') as file:
    model = pickle.load(file)

# Prepare the new data
new_data = [[5.1, 3.5, 1.4, 0.2]]  # Replace this with your actual data

# Use the model to make a prediction
prediction = model.predict(new_data)

print(prediction)

'./data/Week1_Season2020Stats.xlsx'