# Addy Halos | Analytics Engineering Portfolio

Analytics engineer with experience building end-to-end data workflows, from ETL pipelines to dashboards used for business reporting and decision-making. My work focuses on data infrastructure design, data workflow automation, BI dashboards, and turning raw data into usable business outputs.

## What This Portfolio Shows

- End-to-end ETL workflows using Python and SQL
- API data extraction and reporting automation
- Dashboard development in Looker Studio, Tableau, and Google Sheets
- Business-focused analytics for operations, marketing, and financial data

## Featured Project

### Financial Market Data ETL Pipeline

End-to-end ETL pipeline that extracts company financial metrics from the Financial Modeling Prep API, loads them into a local database, transforms the data with SQL, and publishes reporting outputs to Google Sheets, Looker Studio, and Tableau.

**Pipeline Flow:**  
FMP API → Python extraction → SQLite staging tables → SQL transformations → reporting tables → Google Sheets → Looker Studio / Tableau

**Tech Stack:** Python, SQL, SQLite, Google Sheets, Looker Studio, Tableau, FMP API  
**Focus Areas:** API extraction, ETL, data modeling, reporting automation, dashboarding

**Project Links**
- ETL Documentation: [FMP ETL Pipeline](data_engineering/fmp_etl_documentation.ipynb)
- Looker Studio Dashboard: [View Dashboard](https://lookerstudio.google.com/reporting/9896e31d-efa0-4ff6-8493-f52110496c3c)
- Tableau Dashboard Page 1: [Company Profile](https://public.tableau.com/views/FMPTableauDashboard/CompanyProfile?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
- Tableau Dashboard Page 2: [Market Comparison](https://public.tableau.com/views/FMPTableauDashboard/MarketComparison?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
- Google Sheets Dashboard: [View Sheet](https://docs.google.com/spreadsheets/d/1VzRRUCt46Upqxm7HiJiGPE4Y2lIH9EnHo2swDhYeM1U/edit?usp=sharing)

## Other Projects

### Leads Generated Workflow Automation

Workflow automation using Tally, Zapier, and Airtable to clean lead submissions, check duplicate emails, and create validated lead records.

**Project Link:** [View Project](#leads-generated-workflow-automation)  
**Form Demo:** [Tally Form](https://tally.so/r/5B9276)  
**Tech Stack:** Zapier, Airtable, Tally  
**Focus Areas:** Workflow automation, data validation, lead management, no-code operations

### FPA Monthly Registered Biofertilizers Report

Automated reporting workflow that scrapes registered product data from the Fertilizer and Pesticide Authority, filters relevant biofertilizer products, and emails the output to recipients.

**Project Link:** [View Notebook](data_engineering/FPA_Monthly_Registered_Biofertilizer_Process.ipynb)  
**Data Source:** [FPA Registered Products](https://fpa.da.gov.ph/resources/reports/registered-products/)  
**Tech Stack:** Google Apps Script, JavaScript, Spreadsheet automation  
**Focus Areas:** Web scraping, automation, recurring reports

### Netflix Dashboard

Dashboard built in Looker Studio to analyze user profiles, subscription types, preferred devices, and customer segments from a public dataset.

**Project Link:** [View Dashboard](https://lookerstudio.google.com/u/0/reporting/9a6ae993-fbbc-46e3-bca9-bc8e11692ad5/page/uP4YD)  
**Tech Stack:** Looker Studio  
**Focus Areas:** Dashboard design, customer segmentation, data visualization

### New York Vehicular Accidents Dashboard

Dashboard built in Looker Studio to analyze accident patterns by vehicle type, cause, location, and severity using public crash data.

**Project Link:** [View Dashboard](https://lookerstudio.google.com/reporting/8740bf9f-dbc6-4b88-ab55-8bf69f714c7f)  
**Data Source:** [Motor Vehicle Collisions - Crashes](https://catalog.data.gov/dataset/motor-vehicle-collisions-crashes)  
**Tech Stack:** Looker Studio  
**Focus Areas:** Public data analysis, dashboarding, geographic and categorical analysis

## Skills

**Data Engineering:** ETL, API extraction, data pipelines, workflow automation  
**Analytics:** SQL, business reporting, dashboarding, data visualization  
**Tools:** Python, SQL, Google Sheets, Looker Studio, Tableau, Zapier, Airtable  
**Cloud and Databases:** SQLite, Google Cloud Platform, Azure, AWS

## Background

I have worked across ecommerce, logistics, food delivery, and B2B operations, including roles at Shopee Philippines, Lalafood, and Zoom2u. My experience includes owning reporting workflows, building dashboards, automating recurring reports, and supporting business teams with analytics.

## Contact

- Email: adrieldphalos@gmail.com
- LinkedIn: https://www.linkedin.com/in/addy-halos/
- CV: [View CV](CV_ADPH.pdf)

---

# Project Details

## Leads Generated Workflow Automation

### Overview

This project demonstrates a no-code workflow automation process for capturing, cleaning, validating, and storing lead submissions.

The workflow starts with a Tally form submission, standardizes the email address, checks whether the lead already exists in Airtable, and creates a new record only when the email is not a duplicate.

### Workflow

Tally Form → Formatter by Zapier → Airtable Duplicate Check → Filter by Zapier → Airtable Create Record

### Tools Used

- Tally
- Zapier
- Airtable

### Process

1. A user submits a lead form through Tally.
2. Zapier receives the form submission.
3. The email address is converted to lowercase for standardization.
4. Airtable is checked for an existing record with the same email.
5. If the email already exists, no new record is created.
6. If the email does not exist, a new lead record is added to Airtable.

### Airtable Fields

- Email
- First name
- Last name
- Phone number
- Company name
- Additional details
- Status
- Source
- Created at

### What This Demonstrates

- Workflow automation
- Data validation
- Duplicate checking
- Lead capture process design
- No-code operational tooling
