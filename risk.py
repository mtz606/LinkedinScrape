from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import csv
import os

from selenium.webdriver.common.keys import Keys

def linkedin_login(driver, username, password):
    login_url = "https://www.linkedin.com/login"
    driver.get(login_url)
    
    # Find the username field and fill in the username
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)
    
    # Find the password field and fill in the password
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    
    # Submit the login
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

def validate_url(url):
    #ensure that the url is a linkedin post
    return "linkedin.com" in url and "/posts/" in url

def load_full_page(driver):
    # Scroll to load comments
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  
        new_height = driver.execute_script("return document.body.scrollHeight")
        # scroll until the end of the page
        if new_height == last_height:
            break
        last_height = new_height

def extract_comments(driver):
    comments = []
    
    # retrieve all elements in comment section
    comment_elements = driver.find_elements(By.CSS_SELECTOR, "article.comments-comment-item")
    for comment in comment_elements:
    
        # Extract name for each comment
        name = comment.find_element(By.CSS_SELECTOR, ".comments-post-meta__name-text").text.strip()

        # Extract profile link for each comment
        profile_link_element = comment.find_element(By.CSS_SELECTOR, ".comments-post-meta__actor-link")
        profile_link = profile_link_element.get_attribute('href').strip()

        # Extract comment text for each comment
        comment_text_element = comment.find_element(By.CSS_SELECTOR, ".comments-comment-item-content-body")
        comment_text = comment_text_element.text.strip()
        
        #Extract profile position for each commment
        profile_position_element = comment.find_element(By.CSS_SELECTOR, ".comments-post-meta__headline")
        profile_position_text = profile_position_element.text.strip()
        
        

        # Append comment information to the list
        comments.append({
            "name": name,
            "profile_link": profile_link,
            "comment": comment_text,
            "position": profile_position_text
        })
    
    return comments


def save_to_csv(comments, filepath):
    if not comments:
        print("There are no comments")
        return
    try:
        keys = comments[0].keys()
        with open(filepath, 'w', newline='', encoding='utf-8') as output_file:
            # write into the csv file
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(comments)
        print(f"Data successfully saved to {filepath}")
    except Exception as e:
        print(f"Failed to save data to CSV: {e}")

def main():
    driver = webdriver.Chrome()  # set the webdriver
    # Log in to LinkedIn
    linkedin_login(driver, "Give Linkedin username here", "give Linkedin password here")
    
    # After login, navigate to the specific post
    post_url = "https://www.linkedin.com/posts/ivanrichmond_opentowork-activity-7194762244520353792-Utak?utm_source=share&utm_medium=member_desktop"
    driver.get(post_url)
    load_full_page(driver)
    comments = extract_comments(driver)
    print(comments)
    
    # Save to CSV if comments were extracted
    if comments:
        directory = "give local directory to save csv file in here"
        filename = "comments.csv"
        filepath = os.path.join(directory, filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        save_to_csv(comments, filepath)


main()