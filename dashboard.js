// Dashboard JavaScript - Standalone Version (No Backend Required)
// All calculations done client-side using JavaScript

// Sample data
let currentData = [
    { Item: 'A1', Annual_Usage: 1000, Unit_Cost: 10, Lead_Time: 2, Past_Demand: 950 },
    { Item: 'A2', Annual_Usage: 800, Unit_Cost: 12, Lead_Time: 2, Past_Demand: 820 },
    { Item: 'A3', Annual_Usage: 600, Unit_Cost: 8, Lead_Time: 2, Past_Demand: 610 },
    { Item: 'B1', Annual_Usage: 400, Unit_Cost: 5, Lead_Time: 3, Past_Demand: 390 },
    { Item: 'B2', Annual_Usage: 300, Unit_Cost: 6, Lead_Time: 3, Past_Demand: 310 },
    { Item: 'C1', Annual_Usage: 100, Unit_Cost: 2, Lead_Time: 4, Past_Demand: 120 },
    { Item: 'C2', Annual_Usage: 50, Unit_Cost: 1, Lead_Time: 4, Past_Demand: 60 }
];

let calculatedData = [];
let tradeoffData = {};

// Normal distribution Z-scores for common service levels
const Z_SCORES = {
    0.80: 0.8416,
    0.81: 0.8779,
    0.82: 0.9154,
    0.83: 0.9542,
    0.84: 0.9945,
    0.85: 1.0364,
    0.86: 1.0803,
    0.87: 1.1264,
    0.88: 1.1750,
    0.89: 1.2265,
    0.90: 1.2816,
    0.91: 1.3408,
    0.92: 1.4051,
    0.93: 1.4758,
    0.94: 1.5548,
    0.95: 1.6449,
    0.96: 1.7507,
    0.97: 1.8808,
    0.98: 2.0537,
    0.99: 2.3263
};

// Helper function to get Z-score
function getZScore(serviceLevel) {
    const level = Math.round(serviceLevel * 100) / 100;
    return Z_SCORES[level] || 1.6449; // Default to 95% if not found
}

// Classify ABC category
function classifyABC(cumulativePercent) {
    if (cumulativePercent <= 70) return 'A';
    if (cumulativePercent <= 90) return 'B';
    return 'C';
}

// Calculate safety stock
function calculateSafetyStock(predictedDemand, leadTime, serviceLevel) {
    const z = getZScore(serviceLevel);
    const stdDev = predictedDemand * 0.1; // 10% of predicted demand
    return z * stdDev * Math.sqrt(leadTime);
}

// Calculate holding cost
function calculateHoldingCost(safetyStock, unitCost, holdingCostRate) {
    return safetyStock * unitCost * holdingCostRate;
}

// Simple linear regression
function linearRegression(x, y) {
    const n = x.length;
    const sumX = x.reduce((a, b) => a + b, 0);
    const sumY = y.reduce((a, b) => a + b, 0);
    const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0);
    const sumXX = x.reduce((sum, xi) => sum + xi * xi, 0);
    
    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;
    
    return { slope, intercept };
}

// Predict using linear regression
function predictDemand(pastDemand, slope, intercept) {
    return Math.round(slope * pastDemand + intercept);
}

// Decision Tree-like prediction (rule-based approximation)
// This mimics a Decision Tree classifier based on multiple features
function predictABC(annualUsage, unitCost, leadTime, pastDemand) {
    const annualValue = annualUsage * unitCost;
    
    // Decision tree-like rules based on feature combinations
    // Rule 1: High value items are typically A
    if (annualValue >= 8000) return 'A';
    
    // Rule 2: Medium-high value with high usage
    if (annualValue >= 4000 && annualUsage >= 500) return 'A';
    
    // Rule 3: Medium value items
    if (annualValue >= 2000 && annualValue < 8000) {
        // Check additional features
        if (unitCost >= 8 && annualUsage >= 300) return 'A';
        return 'B';
    }
    
    // Rule 4: Lower value items
    if (annualValue >= 500 && annualValue < 2000) {
        if (annualUsage >= 200 && unitCost >= 5) return 'B';
        return 'C';
    }
    
    // Rule 5: Very low value items are C
    return 'C';
}

// Process all calculations
function processAllCalculations(data, serviceLevel, holdingCostRate) {
    // Step 1: Calculate Annual Value and sort
    let processed = data.map(item => ({
        ...item,
        Annual_Value: item.Annual_Usage * item.Unit_Cost
    }));
    
    processed.sort((a, b) => b.Annual_Value - a.Annual_Value);
    
    // Step 2: Calculate Cumulative Percentage and ABC Category
    const totalValue = processed.reduce((sum, item) => sum + item.Annual_Value, 0);
    let cumulativeSum = 0;
    
    processed = processed.map(item => {
        cumulativeSum += item.Annual_Value;
        const cumulativePercent = (cumulativeSum / totalValue) * 100;
        return {
            ...item,
            Cumulative: cumulativePercent,
            ABC_Category: classifyABC(cumulativePercent)
        };
    });
    
    // Step 3: Predict ABC using simple rules
    processed = processed.map(item => ({
        ...item,
        Predicted_ABC: predictABC(item.Annual_Usage, item.Unit_Cost, item.Lead_Time, item.Past_Demand)
    }));
    
    // Step 4: Demand Forecasting using Linear Regression
    const pastDemands = processed.map(item => item.Past_Demand);
    const annualUsages = processed.map(item => item.Annual_Usage);
    
    let predictedDemands;
    if (pastDemands.length >= 2) {
        const { slope, intercept } = linearRegression(pastDemands, annualUsages);
        predictedDemands = pastDemands.map(pd => predictDemand(pd, slope, intercept));
    } else {
        predictedDemands = annualUsages;
    }
    
    processed = processed.map((item, index) => ({
        ...item,
        Predicted_Demand: predictedDemands[index]
    }));
    
    // Step 5: Calculate Safety Stock and Holding Cost
    processed = processed.map(item => {
        const safetyStock = calculateSafetyStock(item.Predicted_Demand, item.Lead_Time, serviceLevel);
        const holdingCost = calculateHoldingCost(safetyStock, item.Unit_Cost, holdingCostRate);
        
        return {
            ...item,
            Safety_Stock: Math.round(safetyStock * 100) / 100,
            Holding_Cost: Math.round(holdingCost * 100) / 100
        };
    });
    
    return processed;
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeTable();
    initializeSliders();
    initializeProductSelect();
    attachEventListeners();
    
    // Auto-calculate on load
    setTimeout(() => {
        calculate();
    }, 500);
});

function initializeTable() {
    const tbody = document.getElementById('dataTableBody');
    tbody.innerHTML = '';
    
    currentData.forEach((row, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><input type="text" value="${row.Item}" data-field="Item" data-index="${index}"></td>
            <td><input type="number" value="${row.Annual_Usage}" data-field="Annual_Usage" data-index="${index}"></td>
            <td><input type="number" step="0.01" value="${row.Unit_Cost}" data-field="Unit_Cost" data-index="${index}"></td>
            <td><input type="number" value="${row.Lead_Time}" data-field="Lead_Time" data-index="${index}"></td>
            <td><input type="number" value="${row.Past_Demand}" data-field="Past_Demand" data-index="${index}"></td>
            <td><button class="btn-icon" onclick="deleteRow(${index})"><i class="fas fa-trash"></i></button></td>
        `;
        tbody.appendChild(tr);
    });
    
    // Add event listeners to inputs
    tbody.querySelectorAll('input').forEach(input => {
        input.addEventListener('change', updateData);
        input.addEventListener('input', updateData);
    });
}

function initializeSliders() {
    const sliders = ['serviceLevel', 'holdingCostRate', 'serviceLevelMin', 'serviceLevelMax'];
    
    sliders.forEach(sliderId => {
        const slider = document.getElementById(sliderId);
        const valueDisplay = document.getElementById(sliderId + 'Value');
        
        if (slider && valueDisplay) {
            valueDisplay.textContent = slider.value + '%';
            
            slider.addEventListener('input', function() {
                valueDisplay.textContent = this.value + '%';
                if (calculatedData.length > 0) {
                    if (sliderId === 'serviceLevel' || sliderId === 'holdingCostRate') {
                        calculate();
                    } else if (sliderId === 'serviceLevelMin' || sliderId === 'serviceLevelMax') {
                        updateTradeoffChart();
                    }
                }
            });
        }
    });
}

function initializeProductSelect() {
    updateProductSelect();
}

function updateProductSelect() {
    const container = document.getElementById('productSelect');
    container.innerHTML = '';
    
    currentData.forEach(item => {
        const checkbox = document.createElement('div');
        checkbox.className = 'product-checkbox';
        checkbox.innerHTML = `
            <input type="checkbox" id="product-${item.Item}" value="${item.Item}" checked>
            <label for="product-${item.Item}">${item.Item}</label>
        `;
        container.appendChild(checkbox);
    });
}

function attachEventListeners() {
    document.getElementById('addRowBtn').addEventListener('click', addRow);
    document.getElementById('calculateBtn').addEventListener('click', calculate);
    document.getElementById('refreshBtn').addEventListener('click', () => location.reload());
    
    // Product selection change
    document.addEventListener('change', function(e) {
        if (e.target.type === 'checkbox' && e.target.closest('#productSelect')) {
            if (calculatedData.length > 0) {
                updateTradeoffChart();
            }
        }
    });
}

function updateData() {
    const tbody = document.getElementById('dataTableBody');
    const rows = tbody.querySelectorAll('tr');
    
    currentData = [];
    rows.forEach((row, index) => {
        const inputs = row.querySelectorAll('input[type="text"], input[type="number"]');
        if (inputs.length >= 5) {
            currentData.push({
                Item: inputs[0].value,
                Annual_Usage: parseFloat(inputs[1].value) || 0,
                Unit_Cost: parseFloat(inputs[2].value) || 0,
                Lead_Time: parseFloat(inputs[3].value) || 0,
                Past_Demand: parseFloat(inputs[4].value) || 0
            });
        }
    });
    
    updateProductSelect();
}

function addRow() {
    const newItem = {
        Item: `Item${currentData.length + 1}`,
        Annual_Usage: 100,
        Unit_Cost: 5,
        Lead_Time: 2,
        Past_Demand: 95
    };
    
    currentData.push(newItem);
    initializeTable();
    updateProductSelect();
}

function deleteRow(index) {
    currentData.splice(index, 1);
    initializeTable();
    updateProductSelect();
}

function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function calculate() {
    showLoading();
    
    setTimeout(() => {
        try {
            const serviceLevel = document.getElementById('serviceLevel').value / 100;
            const holdingCostRate = document.getElementById('holdingCostRate').value / 100;
            
            calculatedData = processAllCalculations(currentData, serviceLevel, holdingCostRate);
            
            updateMetrics();
            updateCharts();
            updateResultsTable();
            updateTradeoffChart();
            
            // Show sections
            document.getElementById('metricsSection').style.display = 'block';
            document.getElementById('chartsSection').style.display = 'block';
            document.getElementById('tradeoffSection').style.display = 'block';
            document.getElementById('resultsSection').style.display = 'block';
            
            hideLoading();
        } catch (error) {
            console.error('Error:', error);
            alert('Error calculating: ' + error.message);
            hideLoading();
        }
    }, 100);
}

function updateMetrics() {
    if (calculatedData.length === 0) return;
    
    document.getElementById('totalItems').textContent = calculatedData.length;
    
    const categoryA = calculatedData.filter(item => item.ABC_Category === 'A').length;
    const categoryB = calculatedData.filter(item => item.ABC_Category === 'B').length;
    const categoryC = calculatedData.filter(item => item.ABC_Category === 'C').length;
    
    document.getElementById('categoryA').textContent = categoryA;
    document.getElementById('categoryB').textContent = categoryB;
    document.getElementById('categoryC').textContent = categoryC;
    
    const avgPredicted = calculatedData.reduce((sum, item) => sum + (item.Predicted_Demand || 0), 0) / calculatedData.length;
    document.getElementById('avgPredictedDemand').textContent = Math.round(avgPredicted);
    
    const totalSafetyStock = calculatedData.reduce((sum, item) => sum + (item.Safety_Stock || 0), 0);
    document.getElementById('totalSafetyStock').textContent = Math.round(totalSafetyStock);
}

function updateCharts() {
    if (calculatedData.length === 0) return;
    
    updateABCChart();
    updateABCComparisonChart();
    updateDemandChart();
    updateScatterChart();
    updateSafetyStockChart();
    updateHoldingCostChart();
}

function updateABCChart() {
    const abcCounts = {};
    calculatedData.forEach(item => {
        abcCounts[item.ABC_Category] = (abcCounts[item.ABC_Category] || 0) + 1;
    });
    
    const trace = {
        x: Object.keys(abcCounts),
        y: Object.values(abcCounts),
        type: 'bar',
        marker: {
            color: ['#2563eb', '#64748b', '#94a3b8']
        }
    };
    
    const layout = {
        title: 'ABC Category Distribution',
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        font: { family: 'Inter', size: 12, color: '#374151' },
        xaxis: { title: 'Category' },
        yaxis: { title: 'Number of Items' }
    };
    
    Plotly.newPlot('abcChart', [trace], layout, {responsive: true});
}

function updateABCComparisonChart() {
    const items = calculatedData.map(item => item.Item);
    const actual = calculatedData.map(item => item.ABC_Category === 'A' ? 1 : (item.ABC_Category === 'B' ? 2 : 3));
    const predicted = calculatedData.map(item => item.Predicted_ABC === 'A' ? 1 : (item.Predicted_ABC === 'B' ? 2 : 3));
    
    const trace1 = {
        x: items,
        y: actual,
        name: 'Actual ABC',
        type: 'bar',
        marker: { color: '#2563eb' }
    };
    
    const trace2 = {
        x: items,
        y: predicted,
        name: 'Predicted ABC',
        type: 'bar',
        marker: { color: '#10b981' }
    };
    
    const layout = {
        title: 'Actual vs Predicted ABC Categories',
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        font: { family: 'Inter', size: 12, color: '#374151' },
        yaxis: {
            tickmode: 'array',
            tickvals: [1, 2, 3],
            ticktext: ['A', 'B', 'C'],
            title: 'Category'
        },
        barmode: 'group'
    };
    
    Plotly.newPlot('abcComparisonChart', [trace1, trace2], layout, {responsive: true});
}

function updateDemandChart() {
    const items = calculatedData.map(item => item.Item);
    const actual = calculatedData.map(item => item.Annual_Usage);
    const predicted = calculatedData.map(item => item.Predicted_Demand);
    
    const trace1 = {
        x: items,
        y: actual,
        name: 'Actual Annual Usage',
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#2563eb', width: 3 },
        marker: { size: 8 }
    };
    
    const trace2 = {
        x: items,
        y: predicted,
        name: 'Predicted Demand',
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#10b981', width: 3, dash: 'dash' },
        marker: { size: 8 }
    };
    
    const layout = {
        title: 'Demand Forecasting Comparison',
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        font: { family: 'Inter', size: 12, color: '#374151' },
        xaxis: { title: 'Item' },
        yaxis: { title: 'Demand' }
    };
    
    Plotly.newPlot('demandChart', [trace1, trace2], layout, {responsive: true});
}

function updateScatterChart() {
    const pastDemand = calculatedData.map(item => item.Past_Demand);
    const predictedDemand = calculatedData.map(item => item.Predicted_Demand);
    const items = calculatedData.map(item => item.Item);
    const categories = calculatedData.map(item => item.ABC_Category);
    
    const colors = {
        'A': '#2563eb',
        'B': '#64748b',
        'C': '#94a3b8'
    };
    
    const traces = ['A', 'B', 'C'].map(cat => {
        const indices = categories.map((c, i) => c === cat ? i : -1).filter(i => i !== -1);
        return {
            x: indices.map(i => pastDemand[i]),
            y: indices.map(i => predictedDemand[i]),
            text: indices.map(i => items[i]),
            name: `Category ${cat}`,
            mode: 'markers',
            type: 'scatter',
            marker: {
                size: 10,
                color: colors[cat]
            }
        };
    });
    
    const maxVal = Math.max(...pastDemand, ...predictedDemand);
    traces.push({
        x: [0, maxVal],
        y: [0, maxVal],
        name: 'Perfect Prediction',
        mode: 'lines',
        type: 'scatter',
        line: { color: '#dc2626', width: 2, dash: 'dot' }
    });
    
    const layout = {
        title: 'Past Demand vs Predicted Demand',
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        font: { family: 'Inter', size: 12, color: '#374151' },
        xaxis: { title: 'Past Demand' },
        yaxis: { title: 'Predicted Demand' }
    };
    
    Plotly.newPlot('scatterChart', traces, layout, {responsive: true});
}

function updateSafetyStockChart() {
    const items = calculatedData.map(item => item.Item);
    const safetyStock = calculatedData.map(item => item.Safety_Stock);
    
    const trace = {
        x: items,
        y: safetyStock,
        type: 'bar',
        marker: {
            color: safetyStock,
            colorscale: 'Blues'
        }
    };
    
    const layout = {
        title: 'Safety Stock Levels (AI-Predicted)',
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        font: { family: 'Inter', size: 12, color: '#374151' },
        xaxis: { title: 'Item' },
        yaxis: { title: 'Safety Stock Units' }
    };
    
    Plotly.newPlot('safetyStockChart', [trace], layout, {responsive: true});
}

function updateHoldingCostChart() {
    const items = calculatedData.map(item => item.Item);
    const holdingCost = calculatedData.map(item => item.Holding_Cost);
    const categories = calculatedData.map(item => item.ABC_Category);
    
    const colors = {
        'A': '#2563eb',
        'B': '#64748b',
        'C': '#94a3b8'
    };
    
    const trace = {
        x: items,
        y: holdingCost,
        type: 'bar',
        marker: {
            color: categories.map(cat => colors[cat])
        }
    };
    
    const layout = {
        title: 'Holding Cost by Item and Category',
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        font: { family: 'Inter', size: 12, color: '#374151' },
        xaxis: { title: 'Item' },
        yaxis: { title: 'Holding Cost ($)' }
    };
    
    Plotly.newPlot('holdingCostChart', [trace], layout, {responsive: true});
}

function updateTradeoffChart() {
    if (calculatedData.length === 0) return;
    
    const selectedProducts = Array.from(document.querySelectorAll('#productSelect input[type="checkbox"]:checked'))
        .map(cb => cb.value);
    
    if (selectedProducts.length === 0) return;
    
    const serviceLevelMin = parseFloat(document.getElementById('serviceLevelMin').value) / 100;
    const serviceLevelMax = parseFloat(document.getElementById('serviceLevelMax').value) / 100;
    const holdingCostRate = parseFloat(document.getElementById('holdingCostRate').value) / 100;
    
    const serviceLevels = [];
    for (let sl = serviceLevelMin; sl <= serviceLevelMax; sl += 0.01) {
        serviceLevels.push(Math.round(sl * 100) / 100);
    }
    
    const traces = [];
    const subplotTitles = selectedProducts;
    
    selectedProducts.forEach((product, idx) => {
        const item = calculatedData.find(d => d.Item === product);
        if (!item) return;
        
        const safetyStocks = [];
        const holdingCosts = [];
        
        serviceLevels.forEach(sl => {
            const ss = calculateSafetyStock(item.Predicted_Demand, item.Lead_Time, sl);
            const hc = calculateHoldingCost(ss, item.Unit_Cost, holdingCostRate);
            safetyStocks.push(ss);
            holdingCosts.push(hc);
        });
        
        const xValues = serviceLevels.map(sl => sl * 100);
        
        const xaxisName = idx === 0 ? 'x' : `x${idx + 1}`;
        const yaxisName = idx === 0 ? 'y' : `y${idx + 1}`;
        
        traces.push({
            x: xValues,
            y: safetyStocks,
            name: 'Safety Stock',
            type: 'scatter',
            mode: 'lines',
            line: { color: '#2563eb', width: 3 },
            xaxis: xaxisName,
            yaxis: yaxisName,
            showlegend: idx === 0
        });
        
        traces.push({
            x: xValues,
            y: holdingCosts,
            name: 'Holding Cost',
            type: 'scatter',
            mode: 'lines',
            line: { color: '#dc2626', width: 3 },
            xaxis: xaxisName,
            yaxis: yaxisName,
            showlegend: idx === 0
        });
    });
    
    const numProducts = selectedProducts.length;
    
    // Use Plotly's subplot function for proper layout
    const fig = {
        data: traces,
        layout: {
            title: {
                text: 'Service Level Trade-offs in Inventory Optimization',
                x: 0.5,
                font: { size: 20, color: '#1a2332', family: 'Inter' }
            },
            plot_bgcolor: 'white',
            paper_bgcolor: 'white',
            font: { family: 'Inter', size: 12, color: '#374151' },
            showlegend: true,
            legend: {
                orientation: 'h',
                yanchor: 'bottom',
                y: 1.02,
                xanchor: 'right',
                x: 1
            }
        }
    };
    
    // Create subplot layout
    const subplotLayout = {};
    selectedProducts.forEach((product, idx) => {
        const domainStart = idx / numProducts;
        const domainEnd = (idx + 1) / numProducts;
        
        if (idx === 0) {
            subplotLayout.xaxis = {
                title: 'Service Level (%)',
                domain: [domainStart, domainEnd],
                anchor: 'y',
                range: [serviceLevelMin * 100, serviceLevelMax * 100]
            };
            subplotLayout.yaxis = {
                title: 'Units / Cost',
                anchor: 'x'
            };
        } else {
            subplotLayout[`xaxis${idx + 1}`] = {
                title: '',
                domain: [domainStart, domainEnd],
                anchor: `y${idx + 1}`,
                range: [serviceLevelMin * 100, serviceLevelMax * 100]
            };
            subplotLayout[`yaxis${idx + 1}`] = {
                title: '',
                anchor: `x${idx + 1}`
            };
        }
    });
    
    // Merge layouts
    Object.assign(fig.layout, subplotLayout);
    
    // Add annotations for subplot titles
    fig.layout.annotations = selectedProducts.map((product, idx) => ({
        text: product,
        x: (idx + 0.5) / numProducts,
        y: 1.05,
        xref: 'paper',
        yref: 'paper',
        xanchor: 'center',
        showarrow: false,
        font: { size: 14, color: '#1a2332' }
    }));
    
    Plotly.newPlot('tradeoffChart', fig.data, fig.layout, {responsive: true});
}

function updateResultsTable() {
    const tbody = document.getElementById('resultsTableBody');
    tbody.innerHTML = '';
    
    calculatedData.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.Item}</td>
            <td>${item.ABC_Category}</td>
            <td>${item.Predicted_ABC}</td>
            <td>${item.Annual_Usage}</td>
            <td>${item.Past_Demand}</td>
            <td>${item.Predicted_Demand}</td>
            <td>${item.Lead_Time}</td>
            <td>${Math.round(item.Safety_Stock)}</td>
            <td>$${item.Holding_Cost.toFixed(2)}</td>
        `;
        tbody.appendChild(tr);
    });
}
