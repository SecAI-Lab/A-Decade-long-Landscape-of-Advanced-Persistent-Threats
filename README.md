# A Decade-long Landscape of Advanced Persistent Threats: Longitudinal Analysis and Global Trends

This repository accompanies the paper **"A Decade-long Landscape of Advanced Persistent Threats: Longitudinal Analysis and Global Trends"**, published in the *Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security (CCS '25)*.

It provides:
- Curated datasets from the longitudinal study of Advanced Persistent Threat (APT) campaigns across the last decade 
- Visual representations of APT campaigns, including an interactive map and a flow diagram showing relationships between threat actors and target countries   
- Python code to generate the figures included in the paper for full reproducibility  

---
## Dataset Overview
The repository contains the following collections:

### [Threat Actor Collection](Threat_Actor_Collection.csv)
Aggregates APT threat actor (TA) information from three curated open-source repositories (TA#1–TA#3):
- TA#1  **[MISP Galaxy](https://github.com/MISP/misp-galaxy)**
- TA#2: **[EternalLiberty](https://github.com/StrangerealIntel/EternalLiberty)**
- TA#3: **[APTmap](https://github.com/andreacristaldi/APTmap/)**

Each record provides:
  - "Threat Actor": Unique identifier  
  - "Other Names": Known aliases  
  - "Country": Attributed country of origin  
  - "Sponsor": Sponsoring entity
  - Motivation
  - "First seen": First recorded year of activity

### [Technical Report Collection](Technical_Report_Collection.csv)
Consolidates metadata on APT technical reports from three open-source repositories (TR#1–TR#3):
- TR#1: **[APT & Cybercriminals Campaign Collection](https://github.com/CyberMonitor/APT_CyberCriminal_Campagin_Collections)**
- TR#2: **[APTnotes](https://github.com/aptnotes/data)**
- TR#3: **[Malpedia](https://malpedia.caad.fkie.fraunhofer.de/library)**

Metadata fields include:
  - "Date": Publication date  
  - Filename  
  - Title  
  - "Download Url": Source download link

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

## Visual Representations

This repository provides interactive visualizations that complement the findings in the paper:
- **[Interactive APT Map](https://lngt-apt-study-map.vercel.app/)** 
  - A map enabling exploration of APT campaigns by selecting either an attacking or victim country. It presents decade-long historical data including threat actor(s), CVEs, attack vector(s), malware, target sector(s), and estimated duration. Data is dynamically updated using LLM-based retrieval from **[TR#1](https://github.com/CyberMonitor/APT_CyberCriminal_Campagin_Collections)**. It also integrates a timeline chart linking campaigns to relevant news articles for additional context.
- **[Threat Actor - Victim Country Flow Diagram](https://public.tableau.com/app/profile/anonymouseauthor/viz/TopMentionedCountries/Top30Countries)** 
  - An interactive Sankey-style diagram visualizing the relationships between the top 10 threat actors and the 30 most frequently targeted countries over the past decade.

## Global Trends

The [`Global Trends`](Global%20Trends/) directory contains Python scripts for generating the figures presented in the paper.  
Each script reads from the curated datasets in this repository and outputs a figure in **PDF format** using the same visual style and parameters as in the published paper.

### Usage
All figure-generation scripts require require **Python 3.8+** and the following Python packages:
```bash
pip install pandas numpy altair vl-convert-python seaborn matplotlib
```
After installing the dependencies, you can run a script with:
```bash
cd "Global Trends"
python {desiredCode}.py
```
Running a script will produce a **PDF file** in the current directory.

### Font Configuration
The figures in the paper use specific fonts.  
If they are missing, Matplotlib will show `findfont` warnings and fall back to its default fonts. The scripts will still run correctly, and figures will be generated. 

To suppress the warnings and use the intended fonts on Linux systems, run:
```bash
sudo apt install msttcorefonts -qq
rm -rf ~/.cache/matplotlib
```

On Windows and macOS, installing these fonts can be more complex, and is optional.
