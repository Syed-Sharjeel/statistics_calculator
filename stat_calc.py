import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(page_title="Statistics Calculator", layout="centered")

st.title("📊 Statistics Calculator")

# =============================
# DATA INPUT
# =============================
data_input = st.text_area(
    "Enter dataset (comma separated values):",
    placeholder="Example: 2, 4, 6, 8, 10, 12"
)

# =============================
# OPTIONS
# =============================
st.subheader("Select computations")

col1, col2 = st.columns(2)

with col1:
    five_num = st.toggle("Five Number Summary")
    mean_t = st.toggle("Mean (Average)")
    median_t = st.toggle("Median")
    mode_t = st.toggle("Mode")
    variance_t = st.toggle("Variance")
    std_t = st.toggle("Standard Deviation")

with col2:
    boxplot_t = st.toggle("Boxplot + Skewness")
    fences_t = st.toggle("Inner & Outer Fences")
    freq_t = st.toggle("Frequency Table")
    stemleaf_t = st.toggle("Stem & Leaf Plot")
    hist_t = st.toggle("Histogram + Class Table")

# =============================
# CALCULATE BUTTON
# =============================
if st.button("Calculate"):
    try:
        # Convert input to numeric list
        data = np.array([float(x.strip()) for x in data_input.split(",")])
        data.sort()

        st.success("Data processed successfully")

        # =============================
        # FIVE NUMBER SUMMARY
        # =============================
        if five_num:
            st.subheader("Five Number Summary")
            q1 = np.percentile(data, 25)
            q2 = np.percentile(data, 50)
            q3 = np.percentile(data, 75)

            summary = {
                "Minimum": np.min(data),
                "Q1": q1,
                "Median": q2,
                "Q3": q3,
                "Maximum": np.max(data)
            }
            st.json(summary)

        # =============================
        # MEAN, MEDIAN, MODE
        # =============================
        if mean_t:
            st.write("**Mean:**", np.mean(data))

        if median_t:
            st.write("**Median:**", np.median(data))

        if mode_t:
            counts = Counter(data)
            max_freq = max(counts.values())
            modes = [k for k, v in counts.items() if v == max_freq]
            st.write("**Mode:**", modes)

        # =============================
        # VARIANCE & STD
        # =============================
        if variance_t:
            st.write("**Variance:**", np.var(data, ddof=1))

        if std_t:
            st.write("**Standard Deviation:**", np.std(data, ddof=1))

        # =============================
        # FENCES
        # =============================
        if fences_t:
            IQR = q3 - q1
            inner_lower = q1 - 1.5 * IQR
            inner_upper = q3 + 1.5 * IQR
            outer_lower = q1 - 3 * IQR
            outer_upper = q3 + 3 * IQR

            st.subheader("Inner & Outer Fences")
            st.json({
                "Inner Lower Fence": inner_lower,
                "Inner Upper Fence": inner_upper,
                "Outer Lower Fence": outer_lower,
                "Outer Upper Fence": outer_upper
            })

        # =============================
        # BOXPLOT + SKEWNESS
        # =============================
        if boxplot_t:
            st.subheader("Boxplot")

            fig, ax = plt.subplots()
            ax.boxplot(data, vert=False)
            ax.set_xlabel("Values")
            st.pyplot(fig)

            # Skewness (simple interpretation)
            mean = np.mean(data)
            median = np.median(data)

            if abs(mean - median) < 0.01:
                skew = "Symmetrical"
            elif mean > median:
                skew = "Right Skewed"
            else:
                skew = "Left Skewed"

            st.write("**Skewness:**", skew)

        # =============================
        # FREQUENCY TABLE
        # =============================
        if freq_t:
            st.subheader("Frequency Table")
            freq_df = pd.DataFrame(
                Counter(data).items(),
                columns=["Value", "Frequency"]
            ).sort_values("Value")
            st.dataframe(freq_df)

        # =============================
        # STEM & LEAF
        # =============================
        if stemleaf_t:
            st.subheader("Stem & Leaf Plot")

            stems = {}
            for num in data:
                stem = int(num // 10)
                leaf = int(num % 10)
                stems.setdefault(stem, []).append(leaf)

            stem_leaf_text = ""
            for stem, leaves in stems.items():
                stem_leaf_text += f"{stem} | {' '.join(map(str, leaves))}\n"

            st.text(stem_leaf_text)

        # =============================
        # HISTOGRAM + CLASS TABLE
        # =============================
        if hist_t:
            st.subheader("Histogram")

            bins = int(np.sqrt(len(data)))  # simple rule
            freq, edges = np.histogram(data, bins=bins)

            fig, ax = plt.subplots()
            ax.hist(data, bins=bins)
            ax.set_xlabel("Class Interval")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

            # Class table
            class_table = []
            total = sum(freq)

            for i in range(len(freq)):
                class_table.append([
                    f"{edges[i]:.2f} – {edges[i+1]:.2f}",
                    freq[i],
                    freq[i] / total
                ])

            df_class = pd.DataFrame(
                class_table,
                columns=["Class Boundary", "Frequency", "Relative Frequency"]
            )

            st.subheader("Histogram Class Table")
            st.dataframe(df_class)

    except Exception as e:
        st.error("Invalid input. Please enter numbers separated by commas.")