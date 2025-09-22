# Sugar-Quality-Assessment
This project aims to assess the quality of sugar using machine learning techniques. The system analyzes various features of sugar to predict its quality, leveraging a dataset of sugar quality metrics.
Project Structure and Steps

Data Preparation:

The data directory contains the sugar_quality_dataset.csv file, which holds the dataset used for training and testing the machine learning models.
Model Training:

The models directory includes pre-trained model files: decisiontree_model.pkl, linearregression_model.pkl, randomforest_model.pkl, and svr_model.pkl. These models are trained to predict sugar quality based on the dataset's features.
Exploratory Data Analysis (EDA):

The EDA section involves loading the dataset and visualizing the distribution of features using histograms. This helps in understanding the underlying patterns in the data.
Model Performance Evaluation:

Model performance is evaluated by comparing the R2 scores of different models. The performance of each model is visualized using a bar plot.
Prediction Visualization:

The system predicts sugar quality for the test set and visualizes the predicted values against the actual values to assess the model's accuracy. This is done using a line plot that shows both actual and predicted quality values.
Code Execution:

The main script loads the dataset, performs EDA, evaluates model performance, and visualizes predictions. It utilizes libraries such as pandas for data manipulation, matplotlib and seaborn for plotting, and joblib for loading pre-trained models.
Requirements:

The project requires the following Python libraries: pandas, matplotlib, seaborn, scikit-learn, and joblib. These can be installed using the requirements.txt file provided.
Running the Project:

To run the project, execute the main script. This will generate the visualizations for feature distribution, model performance, and predicted vs actual quality.
By following these steps, the project provides a comprehensive assessment of sugar quality using various machine learning models and visualization techniques.
