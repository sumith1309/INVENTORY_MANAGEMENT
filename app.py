import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from scipy.stats import norm
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Inventory Management & Optimization Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for corporate professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
        background-color: #f5f7fa;
    }
    
    .stApp {
        background-color: #f5f7fa;
    }
    
    .main .block-container {
        background: #ffffff;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-top: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e1e8ed;
    }
    
    h1 {
        color: #1a2332;
        font-weight: 600;
        margin-bottom: 1.5rem;
        font-size: 2rem;
        border-bottom: 3px solid #2563eb;
        padding-bottom: 0.5rem;
    }
    
    h2 {
        color: #1a2332;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    h3 {
        color: #374151;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
        font-size: 1.25rem;
    }
    
    .stMetric {
        background: #ffffff;
        padding: 1.25rem;
        border-radius: 6px;
        border-left: 4px solid #2563eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .stMetric:hover {
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    
    .stMetric label {
        color: #6b7280;
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #1a2332;
        font-weight: 700;
        font-size: 1.75rem;
    }
    
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.625rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        background-color: #1d4ed8;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3);
        transform: translateY(-1px);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    .stSelectbox label, .stNumberInput label, .stSlider label, .stMultiselect label {
        font-weight: 600;
        color: #374151;
        font-size: 0.875rem;
    }
    
    .stSlider label {
        color: #374151;
    }
    
    .sidebar .sidebar-content {
        background-color: #ffffff;
        border-right: 1px solid #e1e8ed;
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #374151;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f9fafb;
        padding: 8px;
        border-radius: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: #6b7280;
        border: 1px solid #e1e8ed;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2563eb;
        color: #ffffff;
        border-color: #2563eb;
    }
    
    .stDataFrame {
        border: 1px solid #e1e8ed;
        border-radius: 6px;
    }
    
    .stDataEditor {
        border: 1px solid #e1e8ed;
        border-radius: 6px;
    }
    
    .stSuccess {
        background-color: #d1fae5;
        color: #065f46;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 6px;
    }
    
    .stWarning {
        background-color: #fef3c7;
        color: #92400e;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 6px;
    }
    
    .stInfo {
        background-color: #dbeafe;
        color: #1e40af;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 6px;
    }
    
    /* Improve readability */
    p, div, span {
        color: #374151;
        line-height: 1.6;
    }
    
    /* Chart containers */
    [data-testid="stPlotlyChart"] {
        background-color: #ffffff;
        border: 1px solid #e1e8ed;
        border-radius: 6px;
        padding: 1rem;
    }
    
    /* Sidebar headers */
    .sidebar .element-container h3 {
        color: #1a2332;
        font-weight: 600;
        font-size: 1rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.75rem;
    }
    
    /* Input fields */
    .stNumberInput>div>div>input {
        border: 1px solid #d1d5db;
        border-radius: 6px;
    }
    
    .stNumberInput>div>div>input:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* Sliders */
    .stSlider>div>div>div {
        background-color: #e5e7eb;
    }
    
    .stSlider>div>div>div>div {
        background-color: #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'model' not in st.session_state:
    st.session_state.model = None
if 'reg_model' not in st.session_state:
    st.session_state.reg_model = None

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

def process_all_calculations(df, service_level, holding_cost_rate):
    """Process all calculations automatically: ABC Analysis, AI Classification, Demand Forecasting, Safety Stock"""
    df = df.copy()
    
    # Step 1: ABC Analysis
    # Calculate Annual Value = Annual Usage × Unit Cost
    df['Annual_Value'] = df['Annual_Usage'] * df['Unit_Cost']
    
    # Sort by Annual Value (descending)
    df = df.sort_values(by='Annual_Value', ascending=False).reset_index(drop=True)
    
    # Calculate Cumulative Percentage
    df['Cumulative%'] = df['Annual_Value'].cumsum() / df['Annual_Value'].sum() * 100
    
    # Classify ABC: Top 70% → A, Next 20% → B, Remaining → C
    df['ABC_Category'] = df.apply(classify_abc, axis=1)
    
    # Step 2: Train Decision Tree for ABC Prediction
    if len(df) >= 3:  # Need at least 3 samples
        features = df[['Annual_Usage', 'Unit_Cost', 'Lead_Time', 'Past_Demand']]
        labels = df['ABC_Category']
        
        model = DecisionTreeClassifier(random_state=42)
        model.fit(features, labels)
        df['Predicted_ABC'] = model.predict(features)
    else:
        df['Predicted_ABC'] = df['ABC_Category']
        model = None
    
    # Step 3: Demand Forecasting using Linear Regression
    if len(df) >= 2:  # Need at least 2 samples for regression
        X = np.array(df['Past_Demand']).reshape(-1, 1)
        y = np.array(df['Annual_Usage'])
        
        reg = LinearRegression()
        reg.fit(X, y)
        df['Predicted_Demand'] = reg.predict(X).round()
    else:
        df['Predicted_Demand'] = df['Annual_Usage']
        reg = None
    
    # Step 4: Safety Stock Calculation
    # Formula: Safety stock = Z.σ√Lead Time where σ = 10% of predicted demand
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
    
    return df, model, reg

# Main title
st.title("📊 Inventory Management & Optimization Dashboard")
st.markdown("---")

# Sidebar for data input
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("### Data Input")
    
    num_items = st.number_input("Number of Items", min_value=3, max_value=20, value=7, step=1)
    
    st.markdown("### Service Level Settings")
    service_level = st.slider("Service Level (%)", min_value=80, max_value=99, value=95, step=1) / 100
    holding_cost_rate = st.slider("Holding Cost Rate (%)", min_value=10, max_value=50, value=20, step=1) / 100
    
    st.markdown("### Visualization Settings")
    show_abc_chart = st.checkbox("Show ABC Category Distribution", value=True)
    show_safety_stock_chart = st.checkbox("Show Safety Stock by Item", value=True)
    show_tradeoff_chart = st.checkbox("Show Service Level Trade-offs", value=True)

# Main Dashboard - Single Page Layout
# Data Input Section
st.header("📝 Data Input & Configuration")
col_input1, col_input2 = st.columns([2, 1])

with col_input1:
    st.subheader("Enter Inventory Data")
    
    # Create editable dataframe
    if st.session_state.df is None:
        # Default sample data
        default_data = {
            'Item': [f'A{i+1}' for i in range(min(3, num_items))] + 
                    [f'B{i+1}' for i in range(min(2, max(0, num_items-3)))] + 
                    [f'C{i+1}' for i in range(max(0, num_items-5))],
            'Annual_Usage': [1000, 800, 600, 400, 300, 100, 50][:num_items],
            'Unit_Cost': [10, 12, 8, 5, 6, 2, 1][:num_items],
            'Lead_Time': [2, 2, 2, 3, 3, 4, 4][:num_items],
            'Past_Demand': [950, 820, 610, 390, 310, 120, 60][:num_items]
        }
        st.session_state.df = pd.DataFrame(default_data)
    
    # Editable dataframe - only show input columns
    input_cols = ['Item', 'Annual_Usage', 'Unit_Cost', 'Lead_Time', 'Past_Demand']
    if st.session_state.df is not None:
        df_to_edit = st.session_state.df[input_cols].copy() if all(col in st.session_state.df.columns for col in input_cols) else st.session_state.df.copy()
    else:
        df_to_edit = pd.DataFrame(columns=input_cols)
    
    edited_df = st.data_editor(
        df_to_edit,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Item": st.column_config.TextColumn("Item", required=True),
            "Annual_Usage": st.column_config.NumberColumn("Annual Usage", min_value=1, required=True),
            "Unit_Cost": st.column_config.NumberColumn("Unit Cost", min_value=0.01, format="%.2f", required=True),
            "Lead_Time": st.column_config.NumberColumn("Lead Time", min_value=1, required=True),
            "Past_Demand": st.column_config.NumberColumn("Past Demand", min_value=1, required=True)
        }
    )

with col_input2:
    st.subheader("Service Level Settings")
    service_level_display = st.slider("Service Level (%)", min_value=80, max_value=99, value=int(service_level*100), step=1)
    service_level = service_level_display / 100
    holding_cost_rate_display = st.slider("Holding Cost Rate (%)", min_value=10, max_value=50, value=int(holding_cost_rate*100), step=1)
    holding_cost_rate = holding_cost_rate_display / 100
    
    st.markdown("---")
    st.markdown("**Service Level Trade-offs Settings**")
    service_level_min = st.slider("Min Service Level (%)", min_value=80, max_value=95, value=80, step=1)
    service_level_max = st.slider("Max Service Level (%)", min_value=85, max_value=99, value=99, step=1)
    
    st.markdown("---")
    st.markdown("**Product Selection**")
    if st.session_state.df is not None and len(st.session_state.df) > 0:
        selected_products = st.multiselect(
            "Select Products for Trade-off Analysis",
            options=st.session_state.df['Item'].tolist(),
            default=st.session_state.df['Item'].head(min(3, len(st.session_state.df))).tolist()
        )
    else:
        selected_products = []

# Automatically process all calculations when data changes
if len(edited_df) > 0:
    # Always recalculate to ensure everything is up to date with current service level and holding cost rate
    processed_df, model, reg = process_all_calculations(edited_df, service_level, holding_cost_rate)
    st.session_state.df = processed_df
    st.session_state.model = model
    st.session_state.reg_model = reg

# Key Metrics Section
if st.session_state.df is not None and 'ABC_Category' in st.session_state.df.columns:
    st.markdown("---")
    st.header("📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Total Items", len(st.session_state.df))
    with col2:
        st.metric("Category A", len(st.session_state.df[st.session_state.df['ABC_Category'] == 'A']))
    with col3:
        st.metric("Category B", len(st.session_state.df[st.session_state.df['ABC_Category'] == 'B']))
    with col4:
        st.metric("Category C", len(st.session_state.df[st.session_state.df['ABC_Category'] == 'C']))
    with col5:
        if 'Predicted_Demand' in st.session_state.df.columns:
            st.metric("Avg Predicted Demand", f"{st.session_state.df['Predicted_Demand'].mean():.0f}")
        else:
            st.metric("Avg Predicted Demand", "N/A")
    with col6:
        if 'Safety_Stock' in st.session_state.df.columns:
            st.metric("Total Safety Stock", f"{st.session_state.df['Safety_Stock'].sum():.0f}")
        else:
            st.metric("Total Safety Stock", "N/A")

# Visualization Section
if st.session_state.df is not None and 'ABC_Category' in st.session_state.df.columns:
    df = st.session_state.df.copy()
    
    st.markdown("---")
    st.header("📈 Model Predictions & Analysis")
    
    # Row 1: ABC Analysis Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("ABC Category Distribution")
        abc_counts = df['ABC_Category'].value_counts().sort_index()
        fig_abc = px.bar(
            x=abc_counts.index,
            y=abc_counts.values,
            color=abc_counts.index,
            color_discrete_map={'A': '#2563eb', 'B': '#64748b', 'C': '#94a3b8'},
            labels={'x': 'Category', 'y': 'Number of Items'},
            title="ABC Category Distribution"
        )
        fig_abc.update_layout(
            showlegend=False,
            height=350,
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            font=dict(family='Inter', size=12, color='#374151'),
            title_font=dict(size=16, color='#1a2332'),
            xaxis=dict(gridcolor='#e5e7eb', linecolor='#d1d5db'),
            yaxis=dict(gridcolor='#e5e7eb', linecolor='#d1d5db')
        )
        st.plotly_chart(fig_abc, use_container_width=True)
    
    with col_chart2:
        st.subheader("ABC vs Predicted ABC Comparison")
        if 'Predicted_ABC' in df.columns:
            comparison_data = pd.DataFrame({
                'Item': df['Item'],
                'Actual': df['ABC_Category'],
                'Predicted': df['Predicted_ABC']
            })
            
            # Create comparison chart
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(
                name='Actual ABC',
                x=comparison_data['Item'],
                y=[1 if cat == 'A' else (2 if cat == 'B' else 3) for cat in comparison_data['Actual']],
                marker_color='#2563eb',
                text=comparison_data['Actual'],
                textposition='outside'
            ))
            fig_comp.add_trace(go.Bar(
                name='Predicted ABC',
                x=comparison_data['Item'],
                y=[1 if cat == 'A' else (2 if cat == 'B' else 3) for cat in comparison_data['Predicted']],
                marker_color='#10b981',
                text=comparison_data['Predicted'],
                textposition='outside'
            ))
            fig_comp.update_layout(
                height=350,
                plot_bgcolor='#ffffff',
                paper_bgcolor='#ffffff',
                font=dict(family='Inter', size=12, color='#374151'),
                title="Actual vs Predicted ABC Categories",
                title_font=dict(size=16, color='#1a2332'),
                xaxis=dict(gridcolor='#e5e7eb', linecolor='#d1d5db'),
                yaxis=dict(
                    gridcolor='#e5e7eb',
                    linecolor='#d1d5db',
                    tickmode='array',
                    tickvals=[1, 2, 3],
                    ticktext=['A', 'B', 'C'],
                    title='Category'
                ),
                barmode='group'
            )
            st.plotly_chart(fig_comp, use_container_width=True)
            
            # Show accuracy
            accuracy = (df['ABC_Category'] == df['Predicted_ABC']).mean() * 100
            st.metric("Model Accuracy", f"{accuracy:.2f}%")
        else:
            st.info("Predicted ABC categories will appear after calculations")
    
    # Row 2: Demand Forecasting Charts
    if 'Predicted_Demand' in df.columns:
        col_chart3, col_chart4 = st.columns(2)
        
        with col_chart3:
            st.subheader("Demand Forecasting: Actual vs Predicted")
            fig_demand = go.Figure()
            fig_demand.add_trace(go.Scatter(
                x=df['Item'],
                y=df['Annual_Usage'],
                mode='lines+markers',
                name='Actual Annual Usage',
                line=dict(color='#2563eb', width=3),
                marker=dict(size=8)
            ))
            fig_demand.add_trace(go.Scatter(
                x=df['Item'],
                y=df['Predicted_Demand'],
                mode='lines+markers',
                name='Predicted Demand',
                line=dict(color='#10b981', width=3, dash='dash'),
                marker=dict(size=8)
            ))
            fig_demand.update_layout(
                height=350,
                plot_bgcolor='#ffffff',
                paper_bgcolor='#ffffff',
                font=dict(family='Inter', size=12, color='#374151'),
                title="Demand Forecasting Comparison",
                title_font=dict(size=16, color='#1a2332'),
                xaxis=dict(gridcolor='#e5e7eb', linecolor='#d1d5db', title='Item'),
                yaxis=dict(gridcolor='#e5e7eb', linecolor='#d1d5db', title='Demand'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_demand, use_container_width=True)
        
        with col_chart4:
            st.subheader("Past Demand vs Predicted Demand Scatter")
            fig_scatter = px.scatter(
                df,
                x='Past_Demand',
                y='Predicted_Demand',
                color='ABC_Category',
                size='Annual_Usage',
                hover_data=['Item'],
                labels={'Past_Demand': 'Past Demand', 'Predicted_Demand': 'Predicted Demand'},
                title="Demand Prediction Scatter Plot",
                color_discrete_map={'A': '#2563eb', 'B': '#64748b', 'C': '#94a3b8'}
            )
            # Add diagonal line
            max_val = max(df['Past_Demand'].max(), df['Predicted_Demand'].max())
            fig_scatter.add_trace(go.Scatter(
                x=[0, max_val],
                y=[0, max_val],
                mode='lines',
                name='Perfect Prediction',
                line=dict(color='#dc2626', width=2, dash='dot'),
                showlegend=True
            ))
            fig_scatter.update_layout(
                height=350,
                plot_bgcolor='#ffffff',
                paper_bgcolor='#ffffff',
                font=dict(family='Inter', size=12, color='#374151'),
                title_font=dict(size=16, color='#1a2332'),
                xaxis=dict(gridcolor='#e5e7eb', linecolor='#d1d5db'),
                yaxis=dict(gridcolor='#e5e7eb', linecolor='#d1d5db')
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Row 3: Safety Stock Analysis
    if 'Safety_Stock' in df.columns:
        col_chart5, col_chart6 = st.columns(2)
        
        with col_chart5:
            st.subheader("Safety Stock by Item")
            fig_safety = px.bar(
                x=df['Item'],
                y=df['Safety_Stock'],
                color=df['Safety_Stock'],
                color_continuous_scale='Blues',
                labels={'x': 'Item', 'y': 'Safety Stock Units'},
                title="Safety Stock Levels (AI-Predicted)"
            )
            fig_safety.update_layout(
                showlegend=False,
                height=350,
                plot_bgcolor='#ffffff',
                paper_bgcolor='#ffffff',
                font=dict(family='Inter', size=12, color='#374151'),
                title_font=dict(size=16, color='#1a2332'),
                xaxis=dict(gridcolor='#e5e7eb', linecolor='#d1d5db'),
                yaxis=dict(gridcolor='#e5e7eb', linecolor='#d1d5db')
            )
            st.plotly_chart(fig_safety, use_container_width=True)
        
        with col_chart6:
            st.subheader("Holding Cost Analysis")
            fig_cost = px.bar(
                x=df['Item'],
                y=df['Holding_Cost'],
                color=df['ABC_Category'],
                color_discrete_map={'A': '#2563eb', 'B': '#64748b', 'C': '#94a3b8'},
                labels={'x': 'Item', 'y': 'Holding Cost ($)'},
                title="Holding Cost by Item and Category"
            )
            fig_cost.update_layout(
                height=350,
                plot_bgcolor='#ffffff',
                paper_bgcolor='#ffffff',
                font=dict(family='Inter', size=12, color='#374151'),
                title_font=dict(size=16, color='#1a2332'),
                xaxis=dict(gridcolor='#e5e7eb', linecolor='#d1d5db'),
                yaxis=dict(gridcolor='#e5e7eb', linecolor='#d1d5db')
            )
            st.plotly_chart(fig_cost, use_container_width=True)
    
    # Main Feature: Service Level Trade-offs (Full Width)
    st.markdown("---")
    st.header("🎯 Service Level Trade-offs Analysis")
    
    if len(selected_products) > 0 and 'Predicted_Demand' in df.columns:
        # Create service level range
        service_levels = np.arange(service_level_min / 100, (service_level_max + 1) / 100, 0.01)
        
        # Create subplots
        num_products = len(selected_products)
        fig_tradeoff = make_subplots(
            rows=1, cols=num_products,
            subplot_titles=selected_products,
            shared_yaxes=True,
            horizontal_spacing=0.1
        )
        
        # Calculate for each product
        for idx, product in enumerate(selected_products):
            product_data = df[df['Item'] == product].iloc[0]
            predicted_demand = product_data['Predicted_Demand']
            lead_time = product_data['Lead_Time']
            unit_cost = product_data['Unit_Cost']
            
            safety_stocks = []
            holding_costs = []
            
            for sl in service_levels:
                ss = calculate_safety_stock(predicted_demand, lead_time, sl)
                hc = calculate_holding_cost(ss, unit_cost, holding_cost_rate)
                safety_stocks.append(ss)
                holding_costs.append(hc)
            
            # Add safety stock line (blue)
            fig_tradeoff.add_trace(
                go.Scatter(
                    x=service_levels * 100,
                    y=safety_stocks,
                    mode='lines',
                    name='Safety Stock',
                    line=dict(color='#2563eb', width=3),
                    showlegend=(idx == 0)
                ),
                row=1, col=idx+1
            )
            
            # Add holding cost line (red)
            fig_tradeoff.add_trace(
                go.Scatter(
                    x=service_levels * 100,
                    y=holding_costs,
                    mode='lines',
                    name='Holding Cost',
                    line=dict(color='#dc2626', width=3),
                    showlegend=(idx == 0)
                ),
                row=1, col=idx+1
            )
        
        # Update layout
        fig_tradeoff.update_layout(
            title={
                'text': "Service Level Trade-offs in Inventory Optimization",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1a2332', 'family': 'Inter'}
            },
            height=500,
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            font=dict(family='Inter', size=12, color='#374151'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#e1e8ed',
                borderwidth=1
            )
        )
        
        # Update axes
        for i in range(1, num_products + 1):
            fig_tradeoff.update_xaxes(
                title_text="Service Level (%)",
                range=[service_level_min, service_level_max],
                row=1, col=i,
                gridcolor='#e5e7eb',
                linecolor='#d1d5db',
                title_font=dict(size=13, color='#374151', family='Inter'),
                tickfont=dict(size=11, color='#6b7280', family='Inter')
            )
            fig_tradeoff.update_yaxes(
                title_text="Units / Cost",
                row=1, col=i,
                gridcolor='#e5e7eb',
                linecolor='#d1d5db',
                title_font=dict(size=13, color='#374151', family='Inter'),
                tickfont=dict(size=11, color='#6b7280', family='Inter')
            )
        
        st.plotly_chart(fig_tradeoff, use_container_width=True)
        
        # Interpretation
        st.markdown("""
        ### 📝 Interpretation
        - **Blue Line (Safety Stock)**: Shows how safety stock increases non-linearly as service level increases
        - **Red Line (Holding Cost)**: Shows the associated holding cost for maintaining safety stock
        - **Trade-off**: Higher service levels require more safety stock and incur higher holding costs
        - **Product Differences**: Each product responds differently based on demand variability and lead time
        - **Interactive**: Adjust the service level range, holding cost rate, and product selection above to see real-time updates
        """)
    else:
        st.info("👆 Please select at least one product from the configuration panel to see trade-off analysis")
    
    # Summary Table
    st.markdown("---")
    st.header("📋 Complete Results Summary")
    summary_cols = ['Item', 'ABC_Category', 'Predicted_ABC', 'Annual_Usage', 'Past_Demand', 'Predicted_Demand', 'Lead_Time', 'Safety_Stock', 'Holding_Cost']
    summary_cols = [col for col in summary_cols if col in df.columns]
    st.dataframe(df[summary_cols], use_container_width=True)

else:
    st.info("👆 Please enter inventory data above to see analysis results")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 1.5rem; font-size: 0.875rem;'>
    <p style='margin: 0; font-weight: 500;'>Inventory Management & Optimization Dashboard | AI-Powered Analytics</p>
</div>
""", unsafe_allow_html=True)

