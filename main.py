import utils.config_util as config_util
import utils.df_util as df_util
import utils.helper as hp

import utils.playwright_manager as pm
import utils.requests_manager as rm

import time
import json

def start(main_dir, start_with_page=1):
    print("Starting cvParser...")

    url, xlsx_file_name, xlsx_sheet_name, save_file_interval = config_util.get_all("cv", main_dir)
    save_file_interval = int(save_file_interval)

    browser = pm.launch_playwright(main_dir)

    columns = ["Vacancy Name", "Company Name", "Salary", "Location", "Published Date", "End Date", "Type of job", "EMail", "Phone"]
    df = df_util.create_df(columns)

    pm.goto_page(browser, url)

    pm.wait_for(browser, "ul.vacancies-list")

    page = pm.get_current_page(browser)

    number_of_results_text = rm.get_text(page, ".search-results-heading__value", "0")
    number_of_results = hp.get_number(number_of_results_text)

    page_size = int(hp.get_url_param(url, "limit", 20))
    start_with_element = (start_with_page - 1) * page_size
    url = hp.update_url_param(url, "offset", start_with_element)

    progress_counter = start_with_element
    while True:
        pm.goto_page(browser, url)

        pm.wait_for(browser, "ul.vacancies-list", default=None)

        page = pm.get_current_page(browser)

        results = rm.get_elements(page, "li.vacancies-list__item")

        for result in results:
            start_time = time.time()

            vacancy_name = rm.get_text(result, "a.vacancy-item__title")
            company_name = rm.get_text(result, ".vacancy-item__column a")
            salary = rm.get_text(result, ".salary-label")
            location = rm.get_text(result, ".vacancy-item__column.vacancy-item__locations")

            info_box = rm.get_element(result, ".vacancy-item__info-secondary > div:first-child")
            try:
                published_date = str(info_box.contents[0]).strip()
                end_date = rm.get_text(info_box, ".vacancy-item__expiry")
            except:
                published_date = ""
                end_date = ""

            vacancy_url = rm.get_attribute(result, "href", "a.vacancy-item__title", "")

            vacancy_page = rm.get_page("https://cv.ee" + vacancy_url)

            try:
                script_tag = vacancy_page.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
                if script_tag:
                    data = script_tag.string
                    data = json.loads(data)

                    value = list(data["props"]["pageProps"]["initialReduxState"]["publicVacancies"].values())[0]

                    type_of_job = ", ".join(value["highlights"]["workTimes"])
                    type_of_job = type_of_job.replace("_", " ").capitalize()

                    email = value["contacts"]["email"]
                    phone = value["contacts"]["phone"]

                    if email == None:
                        email = ""
                    if phone == None:
                        phone = ""
            except:
                type_of_job = ""
                email = ""
                phone = ""

            row = {
                "Vacancy Name": vacancy_name,
                "Company Name": company_name,
                "Salary": salary,
                "Location": location,
                "Published Date": published_date,
                "End Date": end_date,
                "Type of job": type_of_job,
                "EMail": email,
                "Phone": phone
            }
            df = df_util.add_row(df, row)

            progress_counter += 1
            if progress_counter % save_file_interval == 0:
                df_util.save_df(df, main_dir, xlsx_file_name, xlsx_sheet_name)

            end_time = time.time()
            elapsed_time = end_time - start_time
            if elapsed_time < 1:
                time.sleep(1 - elapsed_time)
                elapsed_time = 1
            print(f"{company_name} data parsed in {(elapsed_time):.2f} seconds. [{progress_counter}/{number_of_results}]")

            vacancy_name = ""
            company_name = ""
            salary = ""
            location = ""
            published_date = ""
            end_date = ""
            type_of_job = ""
            email = ""
            phone = ""

        start_with_element += page_size
        url = hp.update_url_param(url, "offset", start_with_element)
        if start_with_element >= number_of_results:
            break

    df_util.save_df(df, main_dir, xlsx_file_name, xlsx_sheet_name)

    pm.close_playwright(browser)

    print(f"Data parsing completed. {progress_counter} companies parsed.")

if __name__ == "__main__":
    import os

    current_dir = os.path.dirname(os.path.realpath(__file__))

    start(current_dir)