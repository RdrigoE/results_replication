import streamlit as st
import base64


bins = st.sidebar.slider('Number of bins', 0.0, 1.0, 0.1)
max_freq_value = st.sidebar.slider('Max Freq', 0.0, 1.0,  value=1.0)
duration = st.sidebar.slider('duration (s)', 0.0, 10.0, value=1.0)


tab1, tab2, tab3 = st.tabs(
    ["Differences INSaFLU and Snakemake",
     "Build DAG and Rulegraph",
     "Rulegraph with bottlenecks"])

with tab1:
    st.title("Differences INSaFLU and Snakemake")
    st.markdown(
        """
|               | Snakemake   | Website |
|-----------    | ----------- |----------
|**coverage**   | ❌|❌|
|**consensus**  | ✓|✓|
|**validated variants**  | 341 ✓ |341 ✓|
|**minor variants**  | 165 ❌   |26 ❌|

# Coverage

Demo\_Sample are ont and the other illumina
|key                 |website|snakemake|Equal|
|---------------------|-------|---------|--|
|**Demo\_Sample\_076**|        99.2| 99.8|❌|
|**Demo\_Sample\_085**|        98.5| 99.1|❌|
|**Demo\_Sample\_094**|        99.2| 99.7|❌|
|**Portugal\_PT43285\_2022**|  99.7| 99.7|✓|
|**Portugal\_PT43287\_2022**|  99.1| 99.1|✓|
|**Portugal\_PT43286\_2022**|  99.7| 99.7|✓|

# Consensus

|key                 |website == snakemake|
|---------------------|----------------|
|**Demo\_Sample\_076**|        ❌ | N G @29867
|**Demo\_Sample\_085**|        ✓|
|**Demo\_Sample\_094**|        ✓|
|**Portugal\_PT43285\_2022**|  ✓|
|**Portugal\_PT43287\_2022**|  ✓|
|**Portugal\_PT43286\_2022**|  ✓   | 
            """
    )

    st.warning("Still needs some reviews! Scripts have changed since")

with tab2:
    st.title("Build DAG and Rulegraph")
    st.text("""Once the rule mergeCoverage is implemented, encompassing the
            computation of all coverage and providing details on the samples
            that surpass the minimum threshold, it becomes possible to
            generate the rulegraph or dag. This crucial information allows
            for a comprehensive analysis of the entire process, unveiling
            precise dependencies from the initial stage to the very last
            segment.""")
    st.text("Getting the rule graph")
    st.title("Rule graph colored")
    st.code(language="bash", body="snakemake --rulegraph | dot -Tpdf > rulegraph.pdf")

    st.image("./rule_graph.png")
    with open("./rule_graph.pdf", "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    st.title("DAG")
    st.text("Getting the dag")
    st.code(language="bash", body="snakemake --dag | dot -Tpdf > dag.pdf")
    st.image("./dag.png")
    with open("./dag.pdf", "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)


with tab3:
    st.title("Rulegraph with bottlenecks")
    st.markdown("""
# How to do dag by color?
```python 
python ./graph/get_rule_info.py graph/ workflow/rules rules.csv results/benchmark/ time.csv rule_graph rule_graph.png
```

# Getting the information from benchmarks

Each rule has a benchmark file that saves the following information:

- s
- h: m: s
- max_rss
- max_vms
- max_uss
- max_pss
- io_in
- io_out
- mean_load
- cpu_time

The intersting part is the second that the rule take from being called to being executed.

# Get every benchmark file pattern

The first step is to go to every rule file(workflow/rules/*.smk) and search for the terms "rule " or "checkpoint ". In this stage we will save the file where we are, the name of the rule and the name of the file where the benchamark will go.

Then we will save to a file and apply some changes.

First there is the need to replace "benchmark" with ".": $s/benchmark/./g
Second replace all entries with {[a-zA-z]} with "*": % s/[{[a-zA-z]*}]*/*/g

Then it is ready to feed to the crawler.py script.

# Crawling benchmark folder
1. Load in the rules and their patterns.
2. Compare each file inside benchmark folder to the pattern of each rule.
3. Save the file name in a dictionary where the key is the rule name and the values are a list of files.
4. Go thru the latter dictionary and for each rule check each file and save the value of the property in interest.
5. Find the max value of the list and save in a file with rule name and the value.

# Converting values into a range from red to green

1. Convert values from numeric to percentage
2. From percentage to rgb
3. From rbg to hex

# Get rulegraph from snakemake

```bash 
snakemake --rulegraph > rulegraph.txt
``` 

# Replace default colors with new colors


```bash 
python3 color_python.py results/benchmark/time.csv rulegraph.txt new_rulegraph.txt
```
# Generate png

```bash 
cat new_rulegraph.txt | dot - Tpng > rulegraph_new.png
```
""")
