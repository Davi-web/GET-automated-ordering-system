from selenium import webdriver
from selenium.webdriver import ActionChains
import time


restaurants = dict(
    EBI_Omelet="https://get.cbord.com/vanderbilt/full/food_merchant.php?ID=183c92ec-bf3f-421d-808c-73e93a071c09",
    Kissam_Taqueria="https://get.cbord.com/vanderbilt/full/food_merchant.php?ID=444ab8da-5aad-4f32-99ec-9252edb81411",
    EBI_Mongolian="https://get.cbord.com/vanderbilt/full/food_merchant.php?ID=74777669-5ad7-4626-a9ad-980fdf48f37e"
)

"""
EBI Omelet Menu: Egg Whites, Liquid Eggs, Vegan Liquid Eggs, Shell Eggs (Choose 1)

Pork Ground Sausage, Diced Turkey Ham, Pork Bacon Crumbles, Crumbled Vegan Sausage, No Protein (Choose 1)

Cheddar Mild Shredded, Vegan Cheddar Shredded, Pizza Blend Shredded, No Cheese (Choose 1)

Diced Onion, Diced Green Peppers, Diced Tomato, Sliced Mushrooms, Broccoli Florets, Baby Spinach, No Veggies, 
Salsa (Choose 4) 

Fresh Fruit Cup Breakfast Potato of the Day Yogurt Cup Oatmeal No Side (Choose 1)

Water Orange Juice Apple Juice Milk -Options? Bubly -Options? Coffee No Beverage (Choose 1)
"""

"""
Kissam Taqueria Menu: 
Base Choice Pick 1: Corn Tortillas, Corn Tortilla Chips, Spanish Rice, No Base

Protein Choice Pick 1: Pollo Asada, Coriander Lime Cod, Southwest Jackfruit, No Protein

Toppings Pick up to 6: Queso, Shredded Lettuce, Spinach, Diced Onion, Cheddar/Jack Cheese, Queso Fresco, Pico, 
Guacamole, Cilantro

Sauces Pick up to 1: Salsa Roja, Salsa Verde, Queso, No Sauce 

Sides Pick up to 2: Apple, Banana, Orange, Black Beans and Spanish Rice, Chips and Guacamole, Chips and Queso, 
Chips and Salsa 

Beverage Pick 1: Blackberry Bubly, Orange Bubly, Lime Bubly, Lemonade, Water, Yoo Hoo Chocolate Drink
"""

driver = webdriver.Chrome("/Users/davidha/Desktop/chromedriver")
# for key in all_cookies:
#     driver.add_cookie(key)
# driver.get_cookies(all_cookies)
driver.get("https://get.cbord.com/vanderbilt/full/food_home.php?showList=true")
print(driver.title)


# search = driver.find_element_by_name("s")
# search.send_keys("test")
# search.send_keys(Keys.RETURN)

def log_on(username, password):
    id = driver.find_element_by_id("identifierInput")
    id.send_keys(username)
    driver.find_element_by_id("postButton").click()
    checkbox = driver.find_element_by_id("myDevice")
    actions = ActionChains(driver)
    actions.move_to_element(checkbox).perform()
    driver.execute_script("arguments[0].click();", checkbox)
    driver.find_element_by_id("password").send_keys(password)
    l = driver.find_element_by_xpath("//a[@title='Sign On']")
    l.click()
    time.sleep(2)
    # driver.find_element_by_class_name("auth-button positive").click()
    time.sleep(10)


def choose_restaurant(restaurant):
    driver.get(restaurants[restaurant])


def choose_later_date():
    # select date
    actions = ActionChains(driver)
    driver.find_element_by_xpath("//*[@class='fa fa-calendar']").click()
    datepicker = driver.find_element_by_id("order_date")
    actions.move_to_element(datepicker).click().perform()

    # find the calendar, month and year picker and the current date
    calendar = driver.find_elements_by_xpath('//*[@id="ui-datepicker-div"]/table/tbody/tr/td')
    # click selected day
    for item in calendar:
        day = item.get_attribute("innerText")
        state = item.get_attribute("class")
        print(day, state)
        if "ui-datepicker-days-cell-over" in state:
            item.click()

    # driver.execute_script('$("timeFrom").val("10:45").change')
    # select = Select(driver.find_element_by_name("order_time"))
    # select.select_by_index(0)
    # print (select.options)
    # print (o.text for o in select.options) # these are string-s

    order_time = driver.find_element_by_id("order_time")

    actions.move_to_element(order_time).click().perform()

    pick_time = driver.find_elements_by_xpath(".//*")
    # pick_time.click()
    #
    for interval in pick_time:
        times = interval.get_attribute("value")
        print(times)
        if len(str(times)) == 8:
            interval.click()
            break

    driver.implicitly_wait(4)


def choose_menu(order, num):
    driver.find_element_by_class_name("accordMenuPrice").click()
    options = driver.find_elements_by_class_name("checkbox")
    for option in options:
        name = option.get_attribute("innerText")

        if name in order:
            option.click()
    options = driver.find_elements_by_class_name("radio")
    for option in options:
        name = option.get_attribute("innerText")

        if name in order:
            option.click()
    # Quantity
    actions = ActionChains(driver)
    quantity = driver.find_element_by_id("itemQuantity")
    actions.move_to_element(quantity).click().perform()
    pick_quantity = quantity.find_elements_by_xpath(".//*")
    for item in pick_quantity:
        count = item.get_attribute("innerText")
        if count == num:
            item.click()

    # Order it
    driver.find_element_by_xpath("//a[@title='Add to cart']").click()
    driver.implicitly_wait(4)
    # Check out
    element_to_hover_over = driver.find_element_by_id("navCart")

    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()
    driver.find_element_by_xpath('//a[@href="food_checkout.php"]').click()


def check_out(comments):
    # Now on Checkout Page
    # Add comments
    driver.find_element_by_id("additionalInstructions").send_keys(comments)
    # Pay
    driver.find_element_by_name("order_checkout").click()
    time.sleep(10)


if __name__ == "__main__":
    log_on("haj1", "David.21002333")
    choose_restaurant("Kissam_Taqueria")
    EBI_Omelet_Order = ["Shell Eggs", "Diced Turkey Ham", "Pork Bacon Crumbles", "Cheddar Mild Shredded",
                        "Sliced Mushrooms", "Diced Onion", "Baby Spinach", "Salsa", "Fresh Fruit Cup", "Apple Juice"]
    Kissam_Taqueria_Order = ["Corn Tortillas", "Pollo Asada", "Shredded Lettuce", "Cheddar/Jack Cheese", "Diced Onion",
                             "Cilantro", "Guacamole", "Pico", "Salsa Roja", "Chips and Queso", "Lemonade"]
    EBI_Mongolian_Order = ["Brown Rice", "Chicken Tempura", "Shredded Carrots", "Sliced Mushrooms", "Bean Sprouts",
                           "Julienne Red Cabbage", "Bok Choy", "Scallions", "Eggroll", "Sweet & Sour",
                           "Chocolate Chip Cookie", "Lemonade"]
    # choose_now()
    choose_later_date()
    order_quantity = 1
    choose_menu(Kissam_Taqueria_Order, order_quantity)
    additional_comments = ""
    time.sleep(10)
    check_out(additional_comments)
    driver.quit()
