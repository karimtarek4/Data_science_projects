"""
Glassdoor Web Scraping Script for Job Listings

This script uses Selenium to scrape job listings from Glassdoor based on a given job title.
It extracts relevant job details, including job title, location, salary estimate, employer name,
job description, rating, and company information. The extracted data is then saved to a CSV file.

Author: Kareem Tarek
Date: Sat Aug 19 15:01:36 2023
"""

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd

# Function to click the "Show More" button to expand job details
def click_show_more(driver):
    try:
        show_more_less = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-t3xrds.e856ufb4")))
    except:
        show_more_less = None
    
    if show_more_less:
        # Scroll the element into view
        driver.execute_script("arguments[0].scrollIntoView();", show_more_less)
        driver.execute_script("arguments[0].click();", show_more_less)
        return True
    else:
        return False

# Function to click the "Next" button for pagination
def click_next_button(driver):
    try:
        time.sleep(2)
        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@data-test="pagination-next"]')))
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(3)
    except NoSuchElementException:
        print("Reached the last page or unable to find the 'Next' button")
        return False
    return True

# Function to extract job details from a listing
def extract_job_details(listing, driver):
    job_details = {}
    
    # Extract job title
    try:         
         job_title = listing.find_element(By.CLASS_NAME, "job-title").text
    except NoSuchElementException:
         job_title = "N/A"
    
    # Extract location
    try:         
          location = listing.find_element(By.CLASS_NAME, "location").text
    except NoSuchElementException:
          location = "N/A"

    # Extract salary estimate
    try:
         salary_estimate_element = listing.find_element(By.CSS_SELECTOR, 'div.salary-estimate[data-test="detailSalary"]')
         salary_estimate = salary_estimate_element.text
    except NoSuchElementException:
         salary_estimate = "N/A"
         
    # Extract employer name
    try:
         employer_name_element = driver.find_element(By.XPATH, './/div[@data-test="employerName"]')
         employer_name = employer_name_element.text.strip().split('\n')[0]
    except NoSuchElementException:        
        employer_name = "N/A"
    
    # Extract job description
    job_description = ""
    try:
         job_description_element = driver.find_element(By.CLASS_NAME, "jobDescriptionContent")
         elements = job_description_element.find_elements(By.XPATH, ".//*")
         job_description = "\n".join([element.text for element in elements if element.text])
         job_description = job_description.replace('\n', ' ')  # Remove newlines within job description
    except NoSuchElementException:
         job_description = "N/A"
         
         
     
    # Extract rating
    try:
         rating = driver.find_element(By.CSS_SELECTOR, '[data-test="detailRating"]').text
    except NoSuchElementException:
         rating = "N/A"
    
    # Create the job details dictionary
    job_details["Location"] = location
    job_details["Job Title"] = job_title
    job_details["Salary Estimate"] = salary_estimate
    job_details["Employer Name"] =  employer_name    
    job_details["Job Description"] = job_description.replace('\n', ' ')
    job_details["Rating"] = rating
    
    # Extract company info  
    try:
        company_container = driver.find_element(By.ID, "CompanyContainer")
    
        # Extract company size
        try:
            size_element = company_container.find_element(By.XPATH, './/span[text()="Size"]/following-sibling::span')
            size = size_element.text
        except NoSuchElementException:
            size = "N/A"
    
        # Extract founded year
        try:
            founded_element = company_container.find_element(By.XPATH, './/span[text()="Founded"]/following-sibling::span')
            founded = founded_element.text
        except NoSuchElementException:
            founded = "N/A"
    
        # Extract company type
        try:
            company_type_element = company_container.find_element(By.XPATH, './/span[text()="Type"]/following-sibling::span')
            company_type = company_type_element.text
        except NoSuchElementException:
            company_type = "N/A"
    
        # Extract industry
        try:
            industry_element = company_container.find_element(By.XPATH, './/span[text()="Industry"]/following-sibling::span')
            industry = industry_element.text
        except NoSuchElementException:
            industry = "N/A"
    
        # Extract sector
        try:
            sector_element = company_container.find_element(By.XPATH, './/span[text()="Sector"]/following-sibling::span')
            sector = sector_element.text
        except NoSuchElementException:
            sector = "N/A"
    
        # Extract revenue
        try:
            revenue_element = company_container.find_element(By.XPATH, './/span[text()="Revenue"]/following-sibling::span')
            revenue = revenue_element.text
        except NoSuchElementException:
            revenue = "N/A"
        
        # Add company info to job details dictionary
        job_details["Company Size"] = size
        job_details["Founded"] = founded
        job_details["Type"] = company_type
        job_details["Industry"] = industry
        job_details["Sector"] = sector
        job_details["Revenue"] = revenue
    
    except NoSuchElementException:
        print("Company info not found.")
         
    return job_details

# Main function to initiate scraping
def main(job_title, number_of_jobs):
    print("="*50)
    print("Fetching for: ", job_title)
    # Set up WebDriver
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(options=options)
    driver.set_window_size(1120, 1000)

    # Construct the URL for the Glassdoor job search
    url = f"https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={job_title}&sc.keyword={job_title}&locT=&locId=&jobType="
    driver.get(url)

    # Extract total number of pages for pagination
    pagination_footer = driver.find_element(By.CLASS_NAME, "paginationFooter").text
    page_numbers = pagination_footer.split()[-1]

    jobs = []

    # Iterate over page_numbers or reach maximum number of jobs
    for _ in range(int(5)):
        #if len(jobs) >= number_of_jobs:bvbvbvbbbvb
           #break  # Stop if the desired number of jobs is reached
        
        # Find job listings on the current page
        job_listings = driver.find_elements(By.CLASS_NAME, "react-job-listing")
        
        # Iterate over job listings
        for listing in job_listings:  # Process only the first 3 job in each page 
            # Click on the job listing
            driver.execute_script("arguments[0].click();", listing)
    
            # Sleep until page loads
            time.sleep(3)
    
            # Click "Show More" to expand job details
            click_show_more(driver)
    
            # Sleep until page loads
            time.sleep(2)
    
            # Extract job details using the function
            job_details = extract_job_details(listing, driver)
            # Check for duplicates before appending
            if job_details not in jobs:
                print(job_details)
                print("*"*50)
                jobs.append(job_details)
    
        # Click the "Next" button and check if there are more pages
        if not click_next_button(driver):
            break
    
    return jobs

# Existing job listings for 'data scientist'
# jobs = main('data scientist', 0)
# data_scientist_df = pd.DataFrame(jobs)
# print("="*20, "date scientist complete", "="*20)

# Existing job listings for 'data scientist'
jobs = main('data_scientist', 0)
data_scientist_df = pd.DataFrame(jobs)
print("="*20, "scientist complete", "="*20)




#  Additional job listings for 'data analyst', 'machine learning', and 'data engineer'
data_analyst_jobs = main('data analyst', 500)
data_analyst_jobs_df = pd.DataFrame(data_analyst_jobs)
print("="*20, "date analyst complete", "="*20)


machine_learning_jobs = main('machine learning', 500)
machine_learning_jobs_df = pd.DataFrame(machine_learning_jobs)
print("="*20, "achine learning", "="*20)


data_engineer_jobs = main('data engineer', 500)
data_engineer_jobs_df = pd.DataFrame(data_engineer_jobs)
print("="*20, "data engineer complete", "="*20)



business_intelligence_analyst = main('business intelligence analyst', 500)
business_intelligence_analyst_df = pd.DataFrame(business_intelligence_analyst)
print("="*20, "business intelligence analyst complete", "="*20)



business_intelligence_developer = main('business intelligence developer', 500)
business_intelligence_developer_df = pd.DataFrame(business_intelligence_developer)
print("="*20, "business intelligence developer complete", "="*20)



# Append the additional job listings to the 'jobs' list
jobs.extend(data_analyst_jobs)
jobs.extend(machine_learning_jobs)
jobs.extend(data_engineer_jobs)
jobs.extend(business_intelligence_analyst)
jobs.extend(business_intelligence_developer)


# Convert the jobs list to a DataFrame
jobs_df = pd.DataFrame(jobs)
print("="*20, "Data Frame Ready", "="*20)


# Display the DataFrame
print(jobs_df)

# Save the DataFrame to a CSV file
jobs_df.to_csv('machine_learning.csv', index=False, encoding='utf-8-sig')


print("Jobs data saved to 'jobs.csv'")
