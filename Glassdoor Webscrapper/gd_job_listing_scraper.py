from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import socket
import time
    
import pandas as pd

# Function to check network connectivity
def check_network_connection():
    while True:
        try:
            # Try to establish a socket connection to a known website (like Google)
            socket.create_connection(("www.google.com", 80))
            print("Network connection is active.")
            return True
        except OSError:
            print("Network connection is not active. Waiting...")
            time.sleep(30)  # Wait for 10 seconds before checking again



# Function to click the "Show More" button to expand job details
def click_show_more(driver):
    # Verify network connection first 
    check_network_connection()
    
    try:
        show_more_less = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-t3xrds.e856ufb4")))
    except:
        show_more_less = None
    
    if show_more_less:
        # Scroll the element into view
        driver.execute_script("arguments[0].scrollIntoView();", show_more_less)
        driver.execute_script("arguments[0].click();", show_more_less)
        time.sleep(10)
        return True
    else:
        return False

# Function to click the "Next" button for pagination
def click_next_button(driver):
    # Verify network connection first 
    check_network_connection()
    
    # Execute code
    try:
        next_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//button[@data-test="pagination-next"]')))
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(10)
      
        
    except NoSuchElementException:
        print("Reached the last page or unable to find the 'Next' button")
        return False
    return True

# Function to extract job details from a listing
def extract_job_details(listing, driver):
    # Verify network connection first 
    check_network_connection()
    
    #Execude code 
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
        job_description = " ".join([element.text for element in elements if element.text])
        job_description = job_description.replace('\n', ' ')  # Remove newlines within job description
    except NoSuchElementException:
        job_description = "N/A"
    
    # Split job description into three parts
    num_parts = 3
    job_description_parts = [job_description[i:i+len(job_description)//num_parts] for i in range(0, len(job_description), len(job_description)//num_parts)]
    
    # Extract rating
    try:
         rating = driver.find_element(By.CSS_SELECTOR, '[data-test="detailRating"]').text
    except NoSuchElementException:
         rating = "N/A"
    
    # Create the job details dictionary
    job_details["Location"] = location
    job_details["Job Title"] = job_title
    job_details["Salary Estimate"] = salary_estimate
    job_details["Employer Name"] = employer_name
    job_details["Job Description Part 1"] = job_description_parts[0] if len(job_description_parts) > 0 else "N/A"
    job_details["Job Description Part 2"] = job_description_parts[1] if len(job_description_parts) > 1 else "N/A"
    job_details["Job Description Part 3"] = job_description_parts[2] if len(job_description_parts) > 2 else "N/A"
    job_details["Rating"] = rating
    job_details["Company Size"] = job_details.get("Company Size", "N/A")
    job_details["Founded"] = job_details.get("Founded", "N/A")
    job_details["Type"] = job_details.get("Type", "N/A")
    job_details["Industry"] = job_details.get("Industry", "N/A")
    job_details["Sector"] = job_details.get("Sector", "N/A")
    job_details["Revenue"] = job_details.get("Revenue", "N/A")
    
    # Add job description parts to job details dictionary
    for i, part in enumerate(job_description_parts, start=1):
        job_details[f"Job Description Part {i}"] = part
    
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
        print("Company info not fetched******.")
    
    return job_details


# Function to initiate the WebDriver with retries
def initiate_webdriver():
    # Verify network connection first 
    check_network_connection()
    
    max_attempts = 5  # Maximum number of attempts to establish WebDriver
    
    for attempt in range(1, max_attempts + 1):
        try:
            options = webdriver.EdgeOptions()
            driver = webdriver.Edge(options=options)
            driver.set_window_size(1120, 1000)
            return driver
        except WebDriverException:
            print(f"Attempt {attempt}/{max_attempts}: WebDriver initiation failed. Retrying...")
            time.sleep(60)  # Wait before retrying
    
    print(f"Failed to initiate WebDriver after {max_attempts} attempts.")
    return None

# Function to export job listings to CSV
def export_csv(jobs, page_num, job_title):
    job_df = pd.DataFrame(jobs)
    csv_filename = f'{job_title}_page_{page_num}.csv'
    job_df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"Exported job listings to '{csv_filename}'")
    
    
# Function to print extracted job details in consol (tracing)
def print_job_details(job_index, page_num, job_details):
    print(f"Job {job_index} (Page {page_num}):")
    print("/" * 10)
    print("Location:", job_details.get("Location", "N/A"))
    print("Job Title:", job_details.get("Job Title", "N/A"))
    print("Salary Estimate:", job_details.get("Salary Estimate", "N/A"))
    print("Employer Name:", job_details.get("Employer Name", "N/A"))
    
    # Print job description parts
    for part_num in range(1, 4):
        description_part_key = f"Job Description Part {part_num}"
        description_part = job_details.get(description_part_key, "N/A")
        print(f"Job Description Part {part_num}:", description_part)
    
    print("Rating:", job_details.get("Rating", "N/A"))
    print("Company Size:", job_details.get("Company Size", "N/A"))
    print("Founded:", job_details.get("Founded", "N/A"))
    print("Type:", job_details.get("Type", "N/A"))
    print("Industry:", job_details.get("Industry", "N/A"))
    print("Sector:", job_details.get("Sector", "N/A"))
    print("Revenue:", job_details.get("Revenue", "N/A"))


    

# Main function to initiate scraping
# Export_interval= export every 2 pages
def main(job_title, export_interval=1):
    # Verify network connection first 
    check_network_connection()
    
    print("-"*30)
    print("Fetching for: ", job_title)
    
    driver = initiate_webdriver()
    if driver is None:
        print("Exiting due to WebDriver initiation failure.")
        return []

    # Construct the URL for the Glassdoor job search
    url = f"https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={job_title}&sc.keyword={job_title}&locT=&locId=&jobType="
    driver.get(url)

    # Extract total number of pages for pagination
    pagination_footer = driver.find_element(By.CLASS_NAME, "paginationFooter").text
    page_numbers = pagination_footer.split()[-1] # Total page numbers in the page
    page_start = 1 # Start page (mark checkpoint if the algorithm haulted for connection reason)
    page_end = 30
    # jobs_per_page = 10  # Number of jobs to fetch per page


    jobs = []
    
    # Click next until reaching start page
    # for _ in range(page_start - 1):
    #     if not click_next_button(driver):
    #         print("Reached the desired starting page.")
    #         break
    
    
    for page_num in range(page_start, int(page_end) + 1):
        
        print("="*50)    
        print(f"Accessing page {page_num}")
        
        job_listings = driver.find_elements(By.CLASS_NAME, "react-job-listing")
            
        # Iterate over job listings
        for listing in job_listings:
            driver.execute_script("arguments[0].click();", listing)
            time.sleep(15)
            click_show_more(driver)
            job_details = extract_job_details(listing, driver)
            if job_details not in jobs:
                job_index = len(jobs) + 1  # Get the current index of the job in the jobs list
                print_job_details(job_index, page_num, job_details)
                jobs.append(job_details)
            else: 
                # If already inserted in the array wait to give website time to load
                print("Job listing already present")
                time.sleep(5)
        if not click_next_button(driver):
            break
            
        if page_num % export_interval == 0:
            export_csv(jobs, page_num, job_title)  # Export every n pages 
        
    driver.quit()  # Close the WebDriver

    return jobs

## Main function call
# job_titles = ['data_scientist', 'data analyst', 'machine learning', 'data engineer', 'business intelligence analyst', 'business intelligence developer']

job_titles = ['data_analyst']

jobs = []

# Verify network connection first 
check_network_connection()

# Scraping job listings and creating DataFrames
for title in job_titles:
    job_listings = main(title)
    job_df = pd.DataFrame(job_listings)
    
    # Check for duplicate job listings before appending
    for _, row in job_df.iterrows():
        if row.to_dict() not in jobs:
            jobs.append(row.to_dict())
    export_csv(jobs, title, 'all') 
    

# Create a DataFrame from the combined job listings
jobs_df = pd.DataFrame(jobs)

# Save all job title in one csv
jobs_df.to_csv('combined_data_jobs.csv', index=False, encoding='utf-8-sig')

print("Jobs data saved to 'combined_data_jobs.csv'")