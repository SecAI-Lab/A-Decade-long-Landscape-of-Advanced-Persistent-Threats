# A Decade-long Landscape of Advanced Persistent Threats: Longitudinal Analysis and Global Trends

This repository accompanies the paper **"A Decade-long Landscape of Advanced Persistent Threats: Longitudinal Analysis and Global Trends"**, published in the *Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security (CCS '25)*.

It provides:
- Visual representations of APT campaigns, including an interactive map and a flow diagram showing relationships between threat actors and target countries  
- Curated datasets from the longitudinal study of Advanced Persistent Threat (APT) campaigns across the last decade  
- Python code to generate the figures included in the paper for full reproducibility  

---

## Visual Representation

This repository provides interactive visualizations that complement the findings in the paper:
- **[Interactive APT Map](https://lngt-apt-study-map.vercel.app/)** 
  - A map enabling exploration of APT campaigns by selecting either an attacking or victim country. It presents decade-long historical data including threat actor(s), CVEs, attack vector(s), malware, target sector(s), and estimated duration. Data is dynamically updated using LLM-based retrieval from **[technical reports source](https://github.com/CyberMonitor/APT_CyberCriminal_Campagin_Collections)**. It also integrates a timeline chart linking campaigns to relevant news articles for additional context.
- **[Threat Actor - Victim Country Flow Diagram](https://public.tableau.com/app/profile/anonymouseauthor/viz/TopMentionedCountries/Top30Countries)** 
  - An interactive Sankey-style diagram visualizing the relationships between the top 10 threat actors and the 30 most frequently targeted countries over the past decade.

## Dataset Overview
The repository contains the following collections:

### [Threat Actor Collection](Threat_Actor_Collection.csv)
A comprehensive list of APT groups, each annotated with:
  - Unique identifier  
  - Known aliases  
  - Country of origin (attributed)  
  - Sponsoring entity
  - Motivation
  - First known activity year

### [Technical Report Collection](Technical_Report_Collection.csv)
Metadata of technical reports used for analysis, including:
  - Publication date  
  - Report filename  
  - Title  
  - Source download link

### [Information Retrieval Collection](Information_Retrieved_Collection.csv)
Refined dataset resulting from the extraction and validation of structured information from the reports. 
Information was obtained through a combination of rule-based, LLM-based, and manual methods:

The final dataset after information retrieval and refinement of generated answers.
The information was retrieved using rule-based (i.e. IoCParser), LLM-based (i.e. GPT-4-Turbo), and manual retrievals.

#### `Rule-based Retrieval`
IoCParser, a tool designed for processing IoCs from various data sources, was chosen. 
It focuses on extracting:
  - CVE identifiers  
  - MITRE ATT&CK technique IDs  
  - YARA rules

#### `LLM-based Retrieval`
After comparative evaluation, **GPT-4-Turbo** was selected for its highest performance across precision, recall, and F1 score metrics. The model was used to extract:
  - Threat actor attribution  
  - Victim country  
  - Use of zero-day exploits  
  - Initial attack vectors  
  - Malware names  
  - Targeted sectors  
  - Campaign duration

#### `Manual Verification`
Due to the persistent and stealthy nature of APT campaigns, LLM-derived information on attack durations was manually reviewed and validated for accuracy.

## Figure Drawing Code

The [`Figure Drawing Code`](Figure%20Drawing%20Code/) directory contains Python scripts for generating the figures presented in the paper.  
Each script reads from the curated datasets in this repository and outputs a figure in **PDF format** using the same visual style and parameters as in the published paper.

### Usage
All figure drawing scripts require **Python 3.8+** and the following Python packages:
```bash
pip install pandas numpy altair vl-convert-python seaborn matplotlib
```
### Font Configuration
The figures in the paper use specific fonts.

On Debian/Ubuntu (including WSL), run:
```bash
sudo apt install msttcorefonts -qq
rm -rf ~/.cache/matplotlib
```

### Example Usage
Navigate to the [`Figure Drawing Code`](Figure%20Drawing%20Code/) directory and run a script:
```bash
python draw_Figure4a.py
```
The generated PDF will be saved in the current working directory.