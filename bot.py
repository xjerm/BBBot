from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import info

# ===============================
# Put your information here
PATH = "" #Path is the path of your chromedriver.exe
TARGET = "" #Target is the target URL of the Best Buy Product to buy
waitTime = 7 #Change this to however long you want the webDriver to wait before exception (7 recommended)
testingMode = 0

#Testing mode 0 means that you will actually checkout the item
#Testing mode 1 will print to console as if it was to checkout, but won't check out.


#=============
#Version 4
#=============

driver = webdriver.Chrome(PATH)
driver.get(TARGET)

isComplete = False

while not isComplete:
    # We are trying to find the add to cart button
    try:
        atcBtn = WebDriverWait(driver, waitTime).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-button"))
        )
    except:
        driver.refresh()
        continue

    print("SUCCESS: Add to cart button found")

    try:
        # Add to cart here
        atcBtn.click()
        
        gtcButton = WebDriverWait(driver, waitTime).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".go-to-cart-button"))
        )

        # Go to cart and checkout as guest assuming no sign in the first time
        driver.get("https://www.bestbuy.com/cart")

        checkoutBtn = WebDriverWait(driver, waitTime).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-lg.btn-block.btn-primary"))
        )
        checkoutBtn.click()
        print("SUCCESS: Successfully added to cart - beginning check out")
    except:
        print("ERROR: Something wrong with adding to cart and checking out - resetting")
        driver.get(TARGET)
        continue
    
    try:
        # Signing in process starts here
        emailField = WebDriverWait(driver, waitTime).until(
            EC.presence_of_element_located((By.ID, "fld-e"))
        )
        emailField.send_keys(info.email)

        pwField = WebDriverWait(driver, waitTime).until(
            EC.presence_of_element_located((By.ID, "fld-p1"))
        )
        pwField.send_keys(info.password)

        # We're clicking the sign in button, but if it's not found we just assume that we're signed in already
        signInBtn = WebDriverWait(driver, waitTime).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-secondary.btn-lg.btn-block.c-button-icon.c-button-icon-leading.cia-form__controls__submit"))
        )
        signInBtn.click()
        print("SUCCESS: Signing in")
    except:
        print("EXCEPTION: Sign in process failed, could be because we're signed in already, continuing on")

    try:
        # fill in card cvv
        cvvField = WebDriverWait(driver, waitTime).until(
            EC.presence_of_element_located((By.ID, "credit-card-cvv"))
        )
        cvvField.send_keys(info.cvv)
        print("SUCESS: CVV Inserted")
    except:
        print("EXCEPTION: Can't put down CVV, maybe BB didn't ask for it this time, continuing on")
    
    try:
        # place order
        placeOrderBtn = WebDriverWait(driver, waitTime).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-lg.btn-block.btn-primary.button__fast-track"))
        )
        
        if testingMode == 0:
            placeOrderBtn.click()
        elif testingMode == 1:
            print("Checkout simulated")
        else:
            print("Testing Mode not set correctly")

        isComplete = True
    except:
        # make sure this link is the same as the link passed to driver.get() before looping
        driver.get(TARGET)
        print("ERROR: Final Checkout process not working")
        continue

print("SUCCESS: Order successfully placed")
