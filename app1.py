import argparse
import os
import streamlit as st
import pandas as pd
import time
import asyncio
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
l1=[]
l2=[]
Name = ""
Address = ""
Website = ""
Phone_Number = ""
Reviews_Count = 0
Reviews_Average = 0
Store_Shopping = ""
In_Store_Pickup = ""
Store_Delivery = ""
Place_Type = ""
Opens_At = ""
Introduction = ""
names_list=[]
address_list=[]
website_list=[]
phones_list=[]
reviews_c_list=[]
reviews_a_list=[]
store_s_list=[]
in_store_list=[]
store_del_list=[]
place_t_list=[]
open_list=[]
intro_list=[]
# Function to search for Architect in a district
async def search_Architect_factories_in_district(Keyword, district, State):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        # Replace this URL with the appropriate search URL for Architect in the district
        search_url = f"https://www.google.com/maps/@32.9817464,70.1930781,3.67z?"
        search = f"{Keyword} in {district}, {State}"
        await page.goto(search_url, timeout=60000)
        await page.wait_for_timeout(2000)
        await page.locator('//input[@id="searchboxinput"]').fill(search)
        await page.wait_for_timeout(1000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(1000)
        await page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')
        previously_counted = 0
        while True:
            await page.mouse.wheel(0, 10000)
            await page.wait_for_timeout(3000)
            if (await page.locator( '//a[contains(@href, "https://www.google.com/maps/place")]').count() >= total):
                listings = await page.locator( '//a[contains(@href, "https://www.google.com/maps/place")]').all()[:total]
                listings = [listing.locator("xpath=..") for listing in listings]
                print(f"Total Found: {len(listings)}")
                break
            else: #The loop should not run infinitely
                if (await page.locator( '//a[contains(@href, "https://www.google.com/maps/place")]' ).count() == previously_counted ):
                    listings = await page.locator( '//a[contains(@href, "https://www.google.com/maps/place")]' ).all()
                    print(f"Arrived at all available\nTotal Found: {len(listings)}")
                    break
                else:
                    previously_counted = await page.locator( '//a[contains(@href, "https://www.google.com/maps/place")]' ).count()
                    print( f"Currently Found: ", await page.locator( '//a[contains(@href, "https://www.google.com/maps/place")]' ).count(), )
        # scraping
        for listing in listings:
            await listing.click()
            await page.wait_for_timeout(5000)
            name_xpath = '//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            reviews_count_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span//span//span[@aria-label]'
            reviews_average_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span[@aria-hidden]'
            info1='//div[@class="LTs0Rc"][1]'#store
            info2='//div[@class="LTs0Rc"][2]'#pickup
            info3='//div[@class="LTs0Rc"][3]'#delivery
            opens_at_xpath='//button[contains(@data-item-id, "oh")]//div[contains(@class, "fontBodyMedium")]'#time
            opens_at_xpath2='//div[@class="MkV9"]//span[@class="ZDu9vd"]//span[2]'
            place_type_xpath='//div[@class="LBgpqf"]//button[@class="DkEaL "]'#type of place
            intro_xpath='//div[@class="WeS02d fontBodyMedium"]//div[@class="PYvSYb "]'
            if await page.locator(intro_xpath).count() > 0:
                Introduction = await page.locator(intro_xpath).inner_text()
                intro_list.append(Introduction)
            else:
                Introduction = ""
                intro_list.append("None Found")
            if await page.locator(reviews_count_xpath).count() > 0:
                temp = await page.locator(reviews_count_xpath).inner_text()
                temp=temp.replace('(','').replace(')','').replace(',','')
                Reviews_Count=int(temp)
                reviews_c_list.append(Reviews_Count)
            else:
                Reviews_Count = ""
                reviews_c_list.append(Reviews_Count)
            if await page.locator(reviews_average_xpath).count() > 0:
                temp = await page.locator(reviews_average_xpath).inner_text()
                temp=temp.replace(' ','')
                Reviews_Average=float(temp)
                reviews_a_list.append(Reviews_Average)
            else:
                Reviews_Average = ""
                reviews_a_list.append(Reviews_Average)
            if await page.locator(info1).count() > 0:
                temp = await page.locator(info1).inner_text()
                temp=temp.split('·')
                check=temp[1]
                check=check.replace("\n","")
                if 'shop' in check:
                    Store_Shopping=check
                    store_s_list.append("Yes")
                elif 'pickup' in check:
                    In_Store_Pickup=check
                    in_store_list.append("Yes")
                elif 'delivery' in check:
                    Store_Delivery=check
                    store_del_list.append("Yes")
            else:
                Store_Shopping = ""
                store_s_list.append("No")
            if await page.locator(info2).count() > 0:
                temp = await page.locator(info2).inner_text()
                temp=temp.split('·')
                check=temp[1]
                check=check.replace("\n","")
                if 'pickup' in check:
                    In_Store_Pickup=check
                    in_store_list.append("Yes")
                elif 'shop' in check:
                    Store_Shopping=check
                    store_s_list.append("Yes")
                elif 'delivery' in check:
                    Store_Delivery=check
                    store_del_list.append("Yes")
            else:
                In_Store_Pickup = ""
                in_store_list.append("No")
            if await page.locator(info3).count() > 0:
                temp = await page.locator(info3).inner_text()
                temp=temp.split('·')
                check=temp[1]
                check=check.replace("\n","")
                # l1.append(check)
                if 'Delivery' in check:
                    Store_Delivery=check
                    store_del_list.append("Yes")
                elif 'pickup' in check:
                    In_Store_Pickup=check
                    in_store_list.append("Yes")
                elif 'shop' in check:
                    Store_Shopping=check
                    store_s_list.append("Yes")
            else:
                # l1.append("")
                Store_Delivery = ""
                store_del_list.append("No")
            if await page.locator(opens_at_xpath).count() > 0:
                opens = await page.locator(opens_at_xpath).inner_text()
                opens=opens.split('⋅')
                if len(opens)!=1:
                    opens=opens[1]
                else:
                    opens = await page.locator(opens_at_xpath).inner_text()
                    # print(opens)
                opens=opens.replace("\u202f","")
                Opens_At=opens
                open_list.append(Opens_At)
            else:
                Opens_At = ""
                open_list.append(Opens_At)
            if await page.locator(opens_at_xpath2).count() > 0:
                opens = await page.locator(opens_at_xpath2).inner_text()
                opens=opens.split('⋅')
                opens=opens[1]
                opens=opens.replace("\u202f","")
                Opens_At=opens
                open_list.append(Opens_At)
            if await page.locator(name_xpath).count() > 0:
                Name = await page.locator(name_xpath).inner_text()
                names_list.append(Name)
                #l1.append(page.locator(name_xpath).inner_text())
            else:
                Name = ""
                names_list.append(Name)
            if await page.locator(address_xpath).count() > 0:
                Address = await page.locator(address_xpath).inner_text()
                address_list.append(Address)
            else:
                Address = ""
                address_list.append(Address)
            if await page.locator(website_xpath).count() > 0:
                Website = await page.locator(website_xpath).inner_text()
                website_list.append(Website)
            else:
                Website = ""
                website_list.append(Website)
            if await page.locator(phone_number_xpath).count() > 0:
                Phone_Number = await page.locator(phone_number_xpath).inner_text()
                phones_list.append(Phone_Number)
            else:
                Phone_Number = ""
                phones_list.append(Phone_Number)
            if await page.locator(place_type_xpath).count() > 0:
                Place_Type = await page.locator(place_type_xpath).inner_text()
                place_t_list.append(Place_Type)
            else:
                Place_Type = ""
                place_t_list.append(Place_Type)
        # df = pd.DataFrame(list(zip(names_list, website_list,intro_list,phones_list,address_list,reviews_c_list,reviews_a_list,store_s_list,in_store_list,store_del_list,place_t_list,open_list)), columns =['Names','Website','Introduction','Phone Number','Address','Review Count','Average Review Count','Store Shopping','In Store Pickup','Delivery','Type','Opens At'])
        # for column in df.columns:
        #     if df[column].nunique() == 1:
        #         df.drop(column, inplace=False)
        # df.to_csv(r'result.csv', index = False)
        # browser.close()
        # print(df.head())
        if os.path.exists('result.csv'):
    # Load existing data from result.csv
            existing_data = pd.read_csv('result.csv')
    # Append new data to the existing DataFrame
            new_data = pd.DataFrame(list(zip(names_list, website_list, intro_list, phones_list, address_list, reviews_c_list, reviews_a_list, store_s_list, in_store_list, store_del_list, place_t_list, open_list)), columns=['Names', 'Website', 'Introduction', 'Phone Number', 'Address', 'Review Count', 'Average Review Count', 'Store Shopping', 'In Store Pickup', 'Delivery', 'Type', 'Opens At'])
            combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    # Drop columns with the same value in all rows
            for column in combined_data.columns:
                if combined_data[column].nunique() == 1:
                    combined_data.drop(column, axis=1, inplace=True)
    # Write the updated data back to result.csv
            combined_data.to_csv('result.csv', index=False)
            print(combined_data.head())
            await browser.close()
        else:
    # If the file doesn't exist, write the initial data
            df = pd.DataFrame(list(zip(names_list, website_list, intro_list, phones_list, address_list, reviews_c_list, reviews_a_list, store_s_list, in_store_list, store_del_list, place_t_list, open_list)), columns=['Names', 'Website', 'Introduction', 'Phone Number', 'Address', 'Review Count', 'Average Review Count', 'Store Shopping', 'In Store Pickup', 'Delivery', 'Type', 'Opens At'])
            df.to_csv('result.csv', index=False)
            print(df.head())
            await browser.close()
        await browser.close()
# Your main function to handle the logic
# def main():
#     districts_list = ["Almora", "Bageshwar", "Chamoli", "Champawat", "Dehradun", "Haridwar", "Nainital", "Pauri Garhwal", "Pithoragarh", "Rudraprayag", "Tehri Garhwal", "Udham Singh Nagar", "Uttarkashi"]
#     for district in districts_list:
#         search_Architect_factories_in_district(district)
#         # Add a delay to avoid overwhelming the server (simulate scraping)
#         print("Scraping completed for",district)
#         time.sleep(5)  # Adjust this delay as needed
#     print("Scraping completed for all districts.")
async def main():
    st.title("Google Maps Scraper")
    scraping_completed = False
    keyword = st.text_input("Enter Keyword to Search")
    # districts_list = ["Almora", "Bageshwar", "Chamoli", "Champawat", "Dehradun", "Haridwar", "Nainital", "Pauri Garhwal", "Pithoragarh", "Rudraprayag", "Tehri Garhwal", "Udham Singh Nagar", "Uttarkashi"]
    districts_input = st.text_input("Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore", "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kanchipuram", "Kanyakumari", "Karur", "Krishnagiri", "Madurai", "Mayiladuthurai", "Nagapattinam", "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai", "Ramanathapuram", "Ranipet", "Salem", "Sivaganga", "Tenkasi", "Thanjavur", "Theni", "Thiruvallur", "Thoothukudi (Tuticorin)", "Tiruchirappalli", "Tirunelveli", "Tirupathur", "Tiruppur", "Tiruvannamalai", "Tiruvarur", "Vellore", "Viluppuram", "Virudhunagar")
    districts_list = [district.strip() for district in districts_input.split(",")]
    State=st.text_input("Enter state name", value="Tamil Nadu")
    if st.button("Scrape for Architect"):
        for district in districts_list:
            await search_Architect_factories_in_district(keyword, district, State)
        scraping_completed = True
        st.success(f"Scraping completed for all district")
    if scraping_completed and os.path.exists("result.csv"):
        st.download_button(
            label="Download result.csv",
            data=open("result.csv", "rb"),
            file_name="result.csv",
            mime="text/csv",
        )
    os.remove("result.csv")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()
    if args.search:
        search_for = args.search
    if args.total:
        total = args.total
    else:
        total = 200
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
















