# A Decade-long Landscape of Advanced Persistent Threats: Longitudinal Analysis and Global Trends

This repository accompanies the paper **"A Decade-long Landscape of Advanced Persistent Threats: Longitudinal Analysis and Global Trends"**, published in the *Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security (CCS '25)*.

It provides curated datasets used in the longitudinal study of Advanced Persistent Threat (APT) campaigns across the last decade.

---

## Dataset Overview
The repository contains the following collections:

### 1. Threat Actor Collection
A comprehensive list of APT groups, each annotated with:
  - Unique identifier  
  - Known aliases  
  - Country of origin (attributed)  
  - Sponsoring entity
  - Motivation
  - First known activity year

### 2. Technical Report Collection
Metadata of technical reports used for analysis, including:
  - Publication date  
  - Report filename  
  - Title  
  - Source download link

### 3. Information Retrieval Collection
Refined dataset resulting from the extraction and validation of structured information from the reports. 
Information was obtained through a combination of rule-based, LLM-based, and manual methods:

The final dataset after information retrieval and refinement of generated answers.
The information was retrieved using rule-based (i.e. IoCParser), LLM-based (i.e. GPT-4-Turbo), and manual retrievals.

#### `Rule-based Retrieval`
IoCParser, tool designed for processing IoCs from various data sources, was chosen. 
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
  - Malware and tool names  
  - Targeted industry sectors  
  - Campaign duration or timeline

#### `Manual Verification`
Due to the persistent and stealthy nature of APT campaigns, LLM-derived information—particularly attack durations—was manually reviewed and validated for consistency and accuracy.
