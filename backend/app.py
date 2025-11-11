from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from scipy.stats import norm
import pickle
import os

app = Flask(__name__)
CORS(app)

# Global variables to store models
decision_tree_model = None
regression_model = None

def classify_abc(row):
    """Classify items into ABC categories based on cumulative percentage"""
    if row['Cumulative%'] <= 70:
        return 'A'
    elif row['Cumulative%'] <= 90:
        return 'B'
    else:
        return 'C'

def calculate_safety_stock(predicted_demand, lead_time, service_level):
    """Calculate safety stock using Z-score and lead time
    Formula: Safety stock = Z.σ√Lead Time where σ is 10% of predicted demand
    """
    z = norm.ppf(service_level)
    std_dev = predicted_demand * 0.1  # σ is 10% of predicted demand
    safety_stock = z * std_dev * np.sqrt(lead_time)
    return safety_stock

def calculate_holding_cost(safety_stock, unit_cost, holding_cost_rate=0.2):
    """Calculate holding cost for safety stock
    Formula: Holding Cost = Safety Stock × Unit Cost × Holding Cost Rate
    """
    return safety_stock * unit_cost * holding_cost_rate

def process_all_calculations(data, service_level=0.95, holding_cost_rate=0.2):
    """Process all calculations: ABC Analysis, AI Classification, Demand Forecasting, Safety Stock"""
    df = pd.DataFrame(data)
    
    # Step 1: ABC Analysis
    df['Annual_Value'] = df['Annual_Usage'] * df['Unit_Cost']
    df = df.sort_values(by='Annual_Value', ascending=False).reset_index(drop=True)
    df['Cumulative%'] = df['Annual_Value'].cumsum() / df['Annual_Value'].sum() * 100
    df['ABC_Category'] = df.apply(classify_abc, axis=1)
    
    # Step 2: Train Decision Tree for ABC Prediction
    if len(df) >= 3:
        features = df[['Annual_Usage', 'Unit_Cost', 'Lead_Time', 'Past_Demand']]
        labels = df['ABC_Category']
        
        global decision_tree_model
        decision_tree_model = DecisionTreeClassifier(random_state=42)
        decision_tree_model.fit(features, labels)
        df['Predicted_ABC'] = decision_tree_model.predict(features)
    else:
        df['Predicted_ABC'] = df['ABC_Category']
    
    # Step 3: Demand Forecasting using Linear Regression
    if len(df) >= 2:
        X = np.array(df['Past_Demand']).reshape(-1, 1)
        y = np.array(df['Annual_Usage'])
        
        global regression_model
        regression_model = LinearRegression()
        regression_model.fit(X, y)
        df['Predicted_Demand'] = regression_model.predict(X).round()
    else:
        df['Predicted_Demand'] = df['Annual_Usage']
    
    # Step 4: Safety Stock Calculation
    df['Safety_Stock'] = df.apply(
        lambda row: calculate_safety_stock(
            row['Predicted_Demand'],
            row['Lead_Time'],
            service_level
        ), axis=1
    ).round()
    
    # Calculate Holding Cost
    df['Holding_Cost'] = df.apply(
        lambda row: calculate_holding_cost(
            row['Safety_Stock'],
            row['Unit_Cost'],
            holding_cost_rate
        ), axis=1
    ).round(2)
    
    return df.to_dict('records')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Main endpoint for processing inventory data"""
    try:
        data = request.json
        items = data.get('items', [])
        service_level = data.get('service_level', 0.95)
        holding_cost_rate = data.get('holding_cost_rate', 0.2)
        
        if not items:
            return jsonify({'error': 'No items provided'}), 400
        
        results = process_all_calculations(items, service_level, holding_cost_rate)
        
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tradeoff', methods=['POST'])
def tradeoff():
    """Calculate service level trade-offs for selected products"""
    try:
        data = request.json
        items = data.get('items', [])
        selected_items = data.get('selected_items', [])
        service_level_min = data.get('service_level_min', 80) / 100
        service_level_max = data.get('service_level_max', 99) / 100
        holding_cost_rate = data.get('holding_cost_rate', 0.2)
        
        if not items or not selected_items:
            return jsonify({'error': 'Missing required data'}), 400
        
        df = pd.DataFrame(items)
        service_levels = np.arange(service_level_min, service_level_max + 0.01, 0.01)
        
        results = {}
        for item_name in selected_items:
            item_data = df[df['Item'] == item_name].iloc[0]
            predicted_demand = item_data['Predicted_Demand']
            lead_time = item_data['Lead_Time']
            unit_cost = item_data['Unit_Cost']
            
            safety_stocks = []
            holding_costs = []
            
            for sl in service_levels:
                ss = calculate_safety_stock(predicted_demand, lead_time, sl)
                hc = calculate_holding_cost(ss, unit_cost, holding_cost_rate)
                safety_stocks.append(float(ss))
                holding_costs.append(float(hc))
            
            results[item_name] = {
                'service_levels': [float(sl * 100) for sl in service_levels],
                'safety_stocks': safety_stocks,
                'holding_costs': holding_costs
            }
        
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

