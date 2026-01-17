import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

def run_eda(df):
    st.header("🎯 Advanced Exploratory Discovery")
    
    # --- PERFORMANCE SETTINGS ---
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({'figure.max_open_warning': 0})
    
    # Identify Column Types
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()
    # Guardrail: Categories with < 15 unique values for better legends
    legend_cols = [c for c in cat_cols if df[c].nunique() < 15]

    tabs = st.tabs(["1. Univariate", "2. Bivariate", "3. Multivariate"])

    # --- TAB 1: UNIVARIATE  ---
    with tabs[0]:
        st.subheader("Distribution & Frequency")
        col = st.selectbox("Select Column:", df.columns, key="u_col")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        if pd.api.types.is_numeric_dtype(df[col]):
            u_chart = st.selectbox("Type:", ["Histogram", "Box Plot", "KDE"], key="u_num")
            if u_chart == "Histogram": 
                sns.histplot(df[col], kde=True, ax=ax, color='#4A90E2')
            elif u_chart == "Box Plot": 
                sns.boxplot(x=df[col], ax=ax, color='#F5A623')
            else: 
                sns.kdeplot(df[col], fill=True, ax=ax, color='#9013FE')
        else:
            u_chart = st.selectbox("Type:", ["Count Plot", "Pie Chart"], key="u_cat")
            counts = df[col].value_counts().nlargest(10)
            
            if u_chart == "Count Plot":
                sns.barplot(x=counts.index, y=counts.values, hue=counts.index, palette="viridis", legend=True, ax=ax)
                # Adding Data Labels (Numbers)
                for i, v in enumerate(counts.values):
                    ax.text(i, v + (max(counts.values)*0.01), str(v), ha='center', fontweight='bold')
                plt.xticks(rotation=45)
            elif u_chart == "Pie Chart":
                ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
            
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        st.pyplot(fig)
        

    # --- TAB 2: BIVARIATE ---
    with tabs[1]:
        st.subheader("Relationship & Custom Choice")
        c1, c2, c3 = st.columns(3)
        bx = c1.selectbox("X-Axis:", df.columns, key="bx")
        by = c2.selectbox("Y-Axis:", df.columns, key="by")
        bh = c3.selectbox("Group By (Hue):", [None] + legend_cols, key="bh")

        is_x_n = pd.api.types.is_numeric_dtype(df[bx])
        is_y_n = pd.api.types.is_numeric_dtype(df[by])

        # Smart Logic for available graphs
        if is_x_n and is_y_n: 
            b_opts = ["Scatter Plot", "Line Plot", "RegPlot", "Hexbin"]
        elif is_x_n or is_y_n: 
            b_opts = ["Box Plot", "Violin Plot", "Bar Plot (Mean)"]
        else: 
            b_opts = ["Grouped Count Plot", "Heatmap (Crosstab)"]

        b_chart = st.selectbox("🛠️ Select Graph Type:", b_opts)
        fig, ax = plt.subplots(figsize=(10, 6))

        try:
            if b_chart == "Scatter Plot": 
                sns.scatterplot(data=df, x=bx, y=by, hue=bh, alpha=0.6, ax=ax)
            elif b_chart == "Line Plot": 
                sns.lineplot(data=df, x=bx, y=by, hue=bh, marker='o', ax=ax)
            elif b_chart == "RegPlot":
                # Forced numeric conversion for trend calculation
                sns.regplot(data=df, x=pd.to_numeric(df[bx]), y=pd.to_numeric(df[by]), ax=ax, line_kws={'color':'red'})
            elif b_chart == "Hexbin":
                clean_df = df[[bx, by]].dropna()
                hb = ax.hexbin(clean_df[bx], clean_df[by], gridsize=30, cmap='Blues', mincnt=1)
                plt.colorbar(hb, ax=ax, label='Point Density')
            elif b_chart == "Box Plot": 
                sns.boxplot(data=df, x=bx, y=by, hue=bh if bh else bx, ax=ax)
            elif b_chart == "Bar Plot (Mean)":
                sns.barplot(data=df, x=bx, y=by, hue=bh if bh else bx, ax=ax)
                for container in ax.containers: ax.bar_label(container, fmt='%.1f', padding=3)
            elif b_chart == "Grouped Count Plot":
                sns.countplot(data=df, x=bx, hue=by if not bh else bh, ax=ax)
                for container in ax.containers: ax.bar_label(container, padding=3)
            elif b_chart == "Heatmap (Crosstab)":
                sns.heatmap(pd.crosstab(df[bx], df[by]), annot=True, fmt='d', cmap="YlGnBu", ax=ax)

            plt.xticks(rotation=45, ha='right')
            if bh or not is_x_n: ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            st.pyplot(fig)
        except Exception as e:
            st.error(f"⚠️ Error: {b_chart} failed. Check if X and Y columns are both numeric for this plot type.")

    # --- TAB 3: MULTIVARIATE (Pro Suite: 3D, Bubble, Treemaps, Facets) ---
    with tabs[2]:
        m_tech = st.radio("Technique:", ["Matrix & Matrix", "3D & Bubble", "Conditioning & Hierarchy"], horizontal=True)

        if m_tech == "Matrix & Matrix":
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Correlation Heatmap")
                if len(num_cols) >= 2:
                    fig, ax = plt.subplots()
                    sns.heatmap(df[num_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
                    st.pyplot(fig)
            with c2:
                st.subheader("Scatterplot Matrix (Pair Plot)")
                sel = st.multiselect("Select Variables:", num_cols, default=num_cols[:3])
                phue = st.selectbox("Color by:", [None] + legend_cols, key="m_phue")
                if len(sel) > 1:
                    g = sns.pairplot(df, vars=sel, hue=phue, plot_kws={'alpha':0.4, 's':20})
                    st.pyplot(g.fig)
            

        elif m_tech == "3D & Bubble":
            sub = st.radio("Type:", ["3D Scatter Plot", "4D Bubble Chart"], horizontal=True)
            if sub == "3D Scatter Plot":
                c1, c2, c3, c4 = st.columns(4)
                x3, y3, z3 = c1.selectbox("X:", num_cols), c2.selectbox("Y:", num_cols), c3.selectbox("Z:", num_cols)
                h3 = c4.selectbox("Color:", [None] + legend_cols, key="h3d")
                fig = px.scatter_3d(df, x=x3, y=y3, z=z3, color=h3, opacity=0.7, height=600)
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                c1, c2, c3, c4 = st.columns(4)
                xb, yb = c1.selectbox("X-Axis:", num_cols, key="xb"), c2.selectbox("Y-Axis:", num_cols, key="yb")
                sb = c3.selectbox("Size (3rd Num):", num_cols, key="sb")
                hb = c4.selectbox("Color (Hue):", [None] + legend_cols, key="hb")
                fig = px.scatter(df, x=xb, y=yb, size=sb, color=hb, size_max=40, hover_data=df.columns)
                st.plotly_chart(fig, use_container_width=True)
                

        elif m_tech == "Conditioning & Hierarchy":
            sub = st.radio("Strategy:", ["Facet Grid (Small Multiples)", "Treemap", "Sunburst"], horizontal=True)
            if sub == "Facet Grid (Small Multiples)":
                c1, c2, c3 = st.columns(3)
                fx, fy = c1.selectbox("X:", num_cols, key="fx"), c2.selectbox("Y:", num_cols, key="fy")
                fs = c3.selectbox("Facet by:", legend_cols, key="fs")
                g = sns.relplot(data=df, x=fx, y=fy, col=fs, col_wrap=3, height=4, kind="scatter", alpha=0.5)
                st.pyplot(g.fig)
                
            elif sub == "Treemap":
                path = st.multiselect("Hierarchy Path:", cat_cols, default=cat_cols[:2] if len(cat_cols)>1 else cat_cols)
                val = st.selectbox("Box Area (Numeric):", num_cols)
                if path:
                    fig = px.treemap(df, path=path, values=val, color=val, color_continuous_scale='RdYlGn')
                    st.plotly_chart(fig, use_container_width=True)
                
            else:
                path = st.multiselect("Hierarchy Path:", cat_cols, default=cat_cols[:2], key="sun_path")
                val = st.selectbox("Sector Size:", num_cols, key="sun_val")
                if path:
                    fig = px.sunburst(df, path=path, values=val, color=val)

                    st.plotly_chart(fig, use_container_width=True)

