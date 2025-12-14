# Transportation & Assignment Problems - Optimization Project

## 📋 Project Overview
This project provides comprehensive solutions to various Transportation and Assignment problems using Python. It implements optimization techniques to solve both balanced and unbalanced transportation problems, with detailed analysis and visualizations. The project was developed as part of the MATH F212 Optimization course at BITS Pilani.

## 🚀 Key Features
- **Balanced Transportation Problem Solution**: Solves standard transportation problems where total supply equals total demand
- **Unbalanced Problems Handling**:
  - Supply > Demand: Implements dummy destination approach
  - Demand > Supply: Implements dummy source with penalty costs
- **Interactive Visualization**: Generates heatmaps for optimal allocations
- **Comprehensive Reporting**: Detailed step-by-step solution process
- **Multiple Solution Methods**: Implements various algorithms including:
  - North-West Corner Method
  - Least Cost Method
  - Vogel's Approximation Method (VAM)
  - MODI (Modified Distribution) Method

## 📁 Project Structure

### 📄 Main Python Files
- **`TP_Python.py`**: Main Python script containing the implementation of all transportation problem solutions
  - Implements three main problems:
    1. Balanced Transportation Problem
    2. Unbalanced Problem with Supply > Demand
    3. Unbalanced Problem with Demand > Supply (Premium Network)
  - Generates visualizations and detailed solution reports

### 📊 Visualization Files
- **`Problem_1_Balanced_TP_allocation.png`**: Heatmap showing optimal allocation for the balanced transportation problem
- **`Problem_2_Supply_Excess_allocation.png`**: Heatmap showing allocation with dummy destination for excess supply
- **`Problem_3_Demand_Excess_allocation.png`**: Heatmap showing allocation with dummy source for unmet demand
- **`TP_Solution_Flowchart.png`**: Flowchart illustrating the solution methodology

### 📚 Documentation Files
- **`Software_Based_Assignment.pdf`**: Assignment problem statement and requirements

### 📝 Other Files
- **`final.txt`**: Additional notes or final report
- **`LICENSE`**: MIT License file

## 🛠️ Implementation Details

### Problem 1: Balanced Transportation
- **Description**: Standard transportation problem where total supply equals total demand
- **Key Features**:
  - Implements basic transportation algorithm
  - Verifies supply-demand balance
  - Provides detailed allocation plan
  - Includes cost analysis and verification

### Problem 2: Unbalanced (Supply > Demand)
- **Description**: Handles cases where total supply exceeds total demand
- **Key Features**:
  - Automatically adds dummy destination
  - Calculates excess inventory
  - Provides recommendations for surplus management

### Problem 3: Unbalanced (Demand > Supply)
- **Description**: Addresses scenarios where demand exceeds supply
- **Key Features**:
  - Implements premium network with penalty costs
  - Calculates shortage costs
  - Provides cost breakdown and recommendations

## 📊 Visualizations
The project generates the following visualizations:

1. **Allocation Heatmaps**
   - Color-coded heatmaps showing optimal allocation from sources to destinations
   - Visual representation of dummy allocations for unbalanced problems

2. **Solution Flowchart**
   - Step-by-step visualization of the solution methodology
   - Decision points and algorithm flow

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Required Python packages:
  ```
  pip install pulp numpy pandas matplotlib seaborn
  ```

### Running the Project
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the main script:
   ```
   python TP_Python.py
   ```
4. View generated visualizations in the project directory

## 📝 Analysis and Results

### Key Findings
1. **Balanced Problems**: Achieved optimal allocation with minimum transportation cost
2. **Supply > Demand**: Successfully handled excess supply through dummy destinations
3. **Demand > Supply**: Effectively managed shortages using premium network with penalty costs

### Performance
- The implementation efficiently handles problems of various sizes
- Visualizations provide clear insights into allocation patterns
- Detailed output helps in understanding the solution process

## 📚 References
1. Operations Research: An Introduction by Hamdy A. Taha
2. Introduction to Operations Research by Hillier and Lieberman
3. BITS Pilani Optimization Course Materials (MATH F212)

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ✨ Contributors
- Aaryan Gupta - Initial work

## 🙏 Acknowledgments
- BITS Pilani Faculty for guidance
- Open-source community for valuable libraries and tools
