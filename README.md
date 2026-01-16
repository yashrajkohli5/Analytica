# 🧼 Analytica: Modular Data Analysis & AI Reporting Suite

**Analytica** is a professional-grade, end-to-end data processing platform. It bridges the gap between raw data ingestion and automated statistical intelligence, providing a guided 8-step workflow for data cleaning, structural transformation, and high-dimensional visualization.

---

## 🛠️ Modular Architecture

This project follows the **Separation of Concerns** principle. By splitting logic into dedicated Python modules, the application remains scalable, maintainable, and highly performant.

| Module | Primary Functions | Responsibility |
| :--- | :--- | :--- |
| **`app.py`** | `main()`, `update_df()` | **Orchestrator**: Central controller for navigation, session state, and the Undo/Reset engine. |
| **`data_loader.py`** | `upload_file()` | **Ingestion**: Manages CSV uploads and initializes the dataframe into memory. |
| **`data_info.py`** | `show_basic_info()`, `get_null_report()` | **Diagnostics**: Provides structural metadata and detailed reports on missing values. |
| **`data_cleaner.py`** | `apply_cleaning()` | **Remediation**: Executes strategies for null handling (imputation/deletion) and duplicate removal. |
| **`data_transformer.py`**| `change_datatypes()` | **Type Engineering**: Ensures columns are correctly cast (e.g., strings to DateTime or Numeric). |
| **`data_reshaper.py`** | `reshape_logic()` | **Structural Engineering**: Handles complex table restructuring like melting or merging. |
| **`data_pivot_table.py`** | `create_pivot_table()` | **Summarization**: Interactive engine for generating multidimensional pivot tables. |
| **`data_viz.py`** | `run_eda()` | **Visual Artist**: Generates Bivariate and Multivariate visualizations (3D, Bubble, Heatmaps). |
| **`data_discovery.py`** | `filter_data()`, `group_data()`, `run_automated_discovery()` | **Intelligence**: Combines manual dynamic filtering with the AI-powered `ydata-profiling` report. |

---

## 🌟 Key Features

### 1. Guided Engineering Workflow
The app guides users through a logical data pipeline: starting with a basic **Overview**, moving through **Cleaning** and **Transformation**, and concluding with a deep **AI Report**.

### 2. State Management & Undo System
Never lose progress. The application tracks dataset versions in `st.session_state`, allowing for **instant Undos** if a transformation or cleaning step yields unexpected results.

### 3. AI-Powered Automated Audit
The final step integrates the **YData-Profiling** engine. It performs a deep-dive scan of variables, automatically surfacing correlations, missing data patterns, and high-cardinality alerts.

### 4. Multivariate Visualization
Go beyond simple bar charts. Analytica features Plotly-powered **3D scatter plots** and **4D bubble charts**, enabling the visualization of four distinct data dimensions simultaneously.


