# Addy Halos - Data Science Portfolio

## About

Hello, it's great to find you here! I am Addy, and it is very nice to meet you.

Before anything else, I'd like to thank you for your interest in looking at my page.

Now, I'd like to give you an introduction to my background in data science. 

I have an extensive background in the ecommerce industry. I was a pioneer business intelligence team member in Shopee Philippines, now an ecommerce industry giant in our country today. I eventually moved on to Lalafood, a food delivery sister company of the well-known on-demand logistics company Lalamove. My last full time job was with Zoom2u, an ASX-listed on-demand B2B logistics provider based in Sydney, Australia.

Today, I am freelancing, continually expanding my knowledge in all aspects of data science.

During my time in these companies, I've developed my skills deeply in data analytics and engineering. I had front line experience in each company, working and learning largely on my own. I was given an opportunity to work in a special project that eventually grew into a fintech company known as SeaMoney, I established strategic plans to smoothen driver onboarding and optimize order matching with drivers in Lalafood, and held my own as the only data professional handling all regular reporting, analytics, and engineering at my last company. In my career, I've never backed down from a challenge, given that I'm always pushed to my boundaries in areas where my past companies have never been before.

Moreover, I would like to introduce the fact that I am a graduate of BS Agribusiness Management while finding success in data science. I believe that this should say a lot about how fast I can rise to the challenge of learning new skills as demanded by any task given to me.

I made this repository to give you a taste of what I can do. Feel free to  browse, and reach out if you have any clarifications!

You may access my CV [here](CV_ADPH.pdf).

### Core Skills
 * Analytics and Strategy
 * Data Visualization
 * Data Engineering
 * Automation
 * SQL
 * Python
 * Javascript
 * ETL
 * Cloud Platform (AWS, Azure, GCP, etc.)

### Contact Details

- adrieldphalos@gmail.com
- [LinkedIn](https://www.linkedin.com/in/addy-halos/)

   
## Table of Contents

* [About](#about)
* [Contact Details](#contact-details)
* Portfolio Projects
   * [Data Engineering](data_engineering)
     - [Leads Generated Workflow Automation](#i-leads-generated-workflow-automation) (Zapier, Airtable, Tally, automation)
     - [Emailed Report - FPA Monthly Registered Biofertilizers](data_engineering/FPA_Monthly_Registered_Biofertilizer_Process.ipynb) (javascript, automation, scraping)
     - [FMP ETL Pipeline - Scheduled Data Extraction of Company Financial Metrics](data_engineering/fmp_etl_documentation.ipynb) (end-to-end ETL pipeline, python, automation)
   * [Data Analytics](data_analytics)
      + [Netflix Dashboard](https://lookerstudio.google.com/u/0/reporting/9a6ae993-fbbc-46e3-bca9-bc8e11692ad5/page/uP4YD) (data visualization, Looker Studio)
      + [New York Vehicular Accidents](https://lookerstudio.google.com/reporting/8740bf9f-dbc6-4b88-ab55-8bf69f714c7f) (data visualization, Looker Studio)
      + FMP Dashboard (data visualization, Looker Studio, Tableau, end-to-end ETL pipeline)
          + [Looker Studio](https://lookerstudio.google.com/reporting/9896e31d-efa0-4ff6-8493-f52110496c3c)
          + Tableau [[Page 1](https://public.tableau.com/views/FMPTableauDashboard/CompanyProfile?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)][[Page 2](https://public.tableau.com/views/FMPTableauDashboard/MarketComparison?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)]
          + [Google Sheets Dashboard](https://docs.google.com/spreadsheets/d/1VzRRUCt46Upqxm7HiJiGPE4Y2lIH9EnHo2swDhYeM1U/edit?usp=sharing)


## Portfolio Projects

### Data Engineering
#### I. [Leads Generated Workflow Automation](#i-leads-generated-workflow-automation)
##### A. Tools and Skills 
Zapier, Airtable, Tally, automation

##### B. Description
This is a simple project that is automated through Zapier. It takes an entry from the Tally form, makes sure the email is in lowercase, checks for duplicates, and finally after successful checks, adds the entry as a new record.

##### C. Project Design
**Automation Tool**: Zapier
**Database**: Airtable
**Form**: Tally

**Step 1**: A response is submitted in Tally

**Step 2**: Zapier starts running 

**Step 3**: Email turned to lowercase if not yet in this form

**Step 4**: Fixed email is checked among existing records

**Step 5**:
**If it already exists**: The record is not created in Airtable
**Else**: response is recorded with the corrected email

#### II. [Emailed Report - FPA Monthly Registered Biofertilizers](data_engineering/FPA_Monthly_Registered_Biofertilizer_Process.ipynb) 
##### A. Skills 
javascript, etl, scraping, automation

##### B. Description
This project takes the list of all registered products under the Fertilizer and Pesticide Authority from their [website]() and filters the biofertilizer products that are based on the bacteria azospirillum. The Excel file is exported, contents are processed as a dataframe, azospirillum-based products are filtered, and finally sent as an email to specific recipients.
   
#### III. [FMP ETL Pipeline - Scheduled Data Extraction of Company Financial Metrics](data_engineering/fmp_etl_documentation.ipynb) 
##### A. Skills
end-to-end ETL pipeline, python, automation

##### B. Description
This project is part of an entire end-to-end ETL project starting from data extraction via [FMP API](https://site.financialmodelingprep.com/developer/docs) up to a fully-functioning dashboard. From data extraction, the data is loaded into staging tables in the [nyse_financials.db](data_engineering/data/nyse_financials.db) file in this repo. After data cleaning, it is loaded into the main tables in the same database. SQL queries built into the script are ran to summarize the data, and finally loaded into tabs in Google sheets. This sheet is used as data sources for both [Looker Studio](######links) and [Tableau](######links) dashboards.

### Data Analytics
#### I. [Netflix Dashboard](https://lookerstudio.google.com/u/0/reporting/9a6ae993-fbbc-46e3-bca9-bc8e11692ad5/page/uP4YD) 
##### A. Skills
data visualization, Looker Studio

##### B. Description
This is a dashboard based on an old dataset from Kaggle. It visualizes customer profile, such as gender, preferred gadget, subscription type, etc.

#### II. [New York Vehicular Accidents](https://lookerstudio.google.com/reporting/8740bf9f-dbc6-4b88-ab55-8bf69f714c7f) 
##### A. Skills
data visualization, Looker Studio

##### B. Description
The dataset came from [data.gov](https://catalog.data.gov/dataset/motor-vehicle-collisions-crashes). It gives a broken down view in order to analyze vehicular accidents in New York. Accidents are broken down into vehicle type, accident reason, death reason, etc.

#### III. FMP Dashboard
##### A. Links
- [Looker Studio](https://lookerstudio.google.com/reporting/9896e31d-efa0-4ff6-8493-f52110496c3c)
- Tableau [[Page 1](https://public.tableau.com/views/FMPTableauDashboard/CompanyProfile?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)][[Page 2](https://public.tableau.com/views/FMPTableauDashboard/MarketComparison?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)]
- [Google Sheets Dashboard](https://docs.google.com/spreadsheets/d/1VzRRUCt46Upqxm7HiJiGPE4Y2lIH9EnHo2swDhYeM1U/edit?usp=sharing)

##### B. Skills
data visualization, Looker Studio, end-to-end ETL pipeline

##### C. Description
These two dashboards on different platforms creates a visualization of the data extracted from the financial modeling prep API. The dashboards focus on the stock performance of five well-known companies in the USA.
