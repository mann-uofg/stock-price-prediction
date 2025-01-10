# Stock Price Prediction

This repository contains a comprehensive project for predicting stock prices using historical data and machine learning techniques. The project includes data fetching, feature engineering, model training, evaluation, and visualization of predictions.

## Table of Contents

- [Installation](#installation)
- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [File Structure](#file-structure)
- [Usage](#usage)
- [Logic and Implementation](#logic-and-implementation)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mann-uofg/stock-price-prediction.git
   cd stock-price-prediction
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Overview

This project aims to predict stock prices based on historical data using machine learning models such as LSTM and Random Forest. It includes a visualization component to display historical and predicted prices along with trade volumes.

## Features

- Fetch historical stock data using the Yahoo Finance API.
- Implement feature engineering techniques like moving averages and technical indicators.
- Train machine learning models for stock price prediction.
- Evaluate models using metrics such as RMSE, MAE, and directional accuracy.
- Visualize historical prices, future predictions, and feature importance.

## Tech Stack

- **Programming Language:** Python
- **Libraries:** 
  - Data Handling: `pandas`, `numpy`
  - Machine Learning: `scikit-learn`, `tensorflow`
  - Visualization: `matplotlib`, `mplcursors`
  - Data Fetching: `yfinance`

## File Structure

```plaintext
src/
├── data/
│   ├── stock_data.py           # Fetch stock data
│   ├── data_loader.py          # Data loading logic
├── features/
│   ├── feature_engineering.py  # Create features
│   ├── technical_indicators.py # Add technical indicators
├── models/
│   ├── lstm_model.py           # LSTM model logic
│   ├── random_forest_model.py  # Random Forest logic
├── visualization/
│   ├── plotter.py              # Plot historical and predicted prices
│   ├── hover_annotations.py    # Add hover annotations
└── main.py                     # Entry point for the project
```

## Usage (Step 1 & 2 are automatic, don't need to run)

1. Fetch stock data:
   ```bash
   python src/data/stock_data.py
   ```

2. Train models:
   ```bash
   python src/models/train_model.py
   ```

3. Visualize predictions:
   ```bash
   python3 predict.py
   ```

## Logic and Implementation

- **Data Fetching:** Stock data is fetched from Yahoo Finance using the `yfinance` library.
- **Feature Engineering:** Create new features to enhance predictive performance, such as moving averages and momentum indicators.
- **Model Training:** Train models like LSTM for time-series forecasting and Random Forest for feature-based predictions.
- **Evaluation:** Use evaluation metrics like RMSE and MAE to compare model performance.
- **Visualization:** Plot historical stock prices, predicted values, and trade volumes using `matplotlib`.

## Contributing

Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Add feature'`.
4. Push the changes: `git push origin feature-name`.
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
