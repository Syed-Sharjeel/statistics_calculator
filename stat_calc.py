import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter
from scipy.stats import skew

st.set_page_config(page_title="Statistics Calculator", layout="centered")
st.title("📊 Statistics Calculator (Grouped & Ungrouped)")

# ============================================
# CREATE TABS
# ============================================
tab1, tab2 = st.tabs(["Ungrouped Data", "Grouped Data"])

# ============================================================
# ===================== UNGROUPED DATA =======================
# ============================================================
with tab1:

    st.header("Ungrouped Data")

    data_input = st.text_area(
        "Enter dataset (comma separated):",
        placeholder="2, 4, 6, 8, 10"
    )

    st.subheader("Select computations")

    col1, col2 = st.columns(2)

    with col1:
        five_num = st.toggle("Five Number Summary", key="u1")
        mean_t = st.toggle("Mean (Average)", key="u2")
        median_t = st.toggle("Median", key="u3")
        mode_t = st.toggle("Mode", key="u4")
        variance_t = st.toggle("Variance (σ²)", key="u5")
        std_t = st.toggle("Standard Deviation (σ)", key="u6")

    with col2:
        boxplot_t = st.toggle("Boxplot + Skewness", key="u7")
        fences_t = st.toggle("Inner & Outer Fences", key="u8")
        freq_t = st.toggle("Frequency Table", key="u9")
        stemleaf_t = st.toggle("Stem & Leaf Plot", key="u10")
        hist_t = st.toggle("Histogram + Class Table", key="u11")

    if st.button("Calculate (Ungrouped)"):

        try:
            data = np.array([float(x.strip()) for x in data_input.split(",")])
            data.sort()
            N = len(data)

            mean = np.mean(data)
            variance = np.var(data)        # Population
            std = np.std(data)             # Population

            Q1 = np.percentile(data, 25)
            Q2 = np.percentile(data, 50)
            Q3 = np.percentile(data, 75)

            # ---------------------------
            if mean_t:
                st.write("**Mean:**", mean)

            if median_t:
                st.write("**Median:**", Q2)

            if mode_t:
                counts = Counter(data)
                max_freq = max(counts.values())
                modes = [k for k, v in counts.items() if v == max_freq]
                st.write("**Mode:**", modes)

            if variance_t:
                st.write("**Variance (σ²):**", variance)

            if std_t:
                st.write("**Standard Deviation (σ):**", std)

            if five_num:
                st.write("**Minimum:**", np.min(data))
                st.write("**Q1:**", Q1)
                st.write("**Median:**", Q2)
                st.write("**Q3:**", Q3)
                st.write("**Maximum:**", np.max(data))

            if fences_t:
                IQR = Q3 - Q1
                st.write("**Inner Lower Fence:**", Q1 - 1.5*IQR)
                st.write("**Inner Upper Fence:**", Q3 + 1.5*IQR)
                st.write("**Outer Lower Fence:**", Q1 - 3*IQR)
                st.write("**Outer Upper Fence:**", Q3 + 3*IQR)

            if boxplot_t:
                fig, ax = plt.subplots()
                ax.boxplot(data, vert=False)
                st.pyplot(fig)

                skewness = skew(data)
                if abs(skewness) < 0.5:
                    shape = "Symmetrical"
                elif skewness > 0:
                    shape = "Right Skewed"
                else:
                    shape = "Left Skewed"

                st.write("**Skewness:**", shape)

            if freq_t:
                df = pd.DataFrame(
                    Counter(data).items(),
                    columns=["Value", "Frequency"]
                ).sort_values("Value")
                st.dataframe(df)

            if stemleaf_t:
                stems = {}
                for num in data:
                    stem = int(num // 10)
                    leaf = int(num % 10)
                    stems.setdefault(stem, []).append(leaf)

                text = ""
                for stem, leaves in stems.items():
                    text += f"{stem} | {' '.join(map(str, leaves))}\n"

                st.text(text)

            if hist_t:
                bins = int(np.sqrt(N))
                fig, ax = plt.subplots()
                ax.hist(data, bins=bins)
                st.pyplot(fig)

        except:
            st.error("Invalid input.")

# ============================================================
# ======================= GROUPED DATA =======================
# ============================================================
with tab2:

    st.header("Grouped Data")

    grouped_input = st.text_area(
        "Paste grouped data (Range Frequency):",
        placeholder="11.5 – 11.9 6\n12.0 – 12.4 14"
    )

    st.subheader("Select computations")

    col1, col2 = st.columns(2)

    with col1:
        g_five = st.toggle("Five Number Summary", key="g1")
        g_mean = st.toggle("Mean (Average)", key="g2")
        g_median = st.toggle("Median", key="g3")
        g_mode = st.toggle("Mode", key="g4")
        g_var = st.toggle("Variance (σ²)", key="g5")
        g_std = st.toggle("Standard Deviation (σ)", key="g6")

    with col2:
        g_box = st.toggle("Boxplot + Skewness", key="g7")
        g_fence = st.toggle("Inner & Outer Fences", key="g8")
        g_freq = st.toggle("Frequency Table", key="g9")
        g_stem = st.toggle("Stem & Leaf Plot", key="g10")
        g_hist = st.toggle("Histogram + Class Table", key="g11")

    if st.button("Calculate (Grouped)"):

        try:
            lines = grouped_input.strip().split("\n")
            lower, upper, freq = [], [], []

            for line in lines:
                nums = re.findall(r"\d+\.?\d*", line)
                if len(nums) == 3:
                    lower.append(float(nums[0]))
                    upper.append(float(nums[1]))
                    freq.append(int(nums[2]))

            lower = np.array(lower)
            upper = np.array(upper)
            freq = np.array(freq)

            mid = (lower + upper) / 2
            width = upper[0] - lower[0]
            N = np.sum(freq)
            cf = np.cumsum(freq)

            mean = np.sum(freq * mid) / N
            variance = np.sum(freq * (mid - mean)**2) / N
            std = np.sqrt(variance)

            expanded = np.repeat(mid, freq)

            if g_mean:
                st.write("**Mean:**", mean)

            if g_var:
                st.write("**Variance (σ²):**", variance)

            if g_std:
                st.write("**Standard Deviation (σ):**", std)

            if g_mode:
                modal = np.argmax(freq)
                L = lower[modal]
                f1 = freq[modal]
                f0 = freq[modal-1] if modal > 0 else 0
                f2 = freq[modal+1] if modal < len(freq)-1 else 0
                mode = L + ((f1-f0)/(2*f1-f0-f2))*width
                st.write("**Mode:**", mode)

            if g_box:
                fig, ax = plt.subplots()
                ax.boxplot(expanded, vert=False)
                st.pyplot(fig)

            if g_stem:
                st.warning("Stem & Leaf not valid for grouped data.")

            if g_freq:
                df = pd.DataFrame({
                    "Class": [f"{l}-{u}" for l, u in zip(lower, upper)],
                    "Midpoint": mid,
                    "Frequency": freq,
                    "Cumulative Frequency": cf
                })
                st.dataframe(df)

            if g_hist:
                fig, ax = plt.subplots()
                ax.bar(mid, freq, width=width)
                st.pyplot(fig)

        except:
            st.error("Invalid grouped format.")
