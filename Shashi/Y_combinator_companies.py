import requests
from bs4 import BeautifulSoup
import json

####################################################
# Job IDs extraction
####################################################
search_url = 'https://www.ycombinator.com/jobs/role/product'
r = requests.get(search_url)
htmlContent = r.content
# print(htmlContent)
# Parse HTML
soup = BeautifulSoup(htmlContent, 'html.parser')
# print(soup.prettify)

job_href = []
jobs_list = soup.find("div", class_="jobs-list").find_all("a", class_="job-view-link job-detail job-name")
for job in jobs_list:
    print(job)
    job_parser = BeautifulSoup(str(job), "html.parser")
    # convert the string (job) to a html element (job_parser)
    print(job_parser)

    data_href_link = job_parser.a.attrs["href"]
    # get the href attribute of "a" section
    print(data_href_link)
    job_href.append(data_href_link)
    # append the list

print(len(jobs_list))

####################################################
# Detail extraction
####################################################

json = ''
company_list = []
count = 0
for href in job_href:

    count += 1

    r1 = requests.get(href)
    htmlContent1 = r1.content
    soup1 = BeautifulSoup(htmlContent1, 'html.parser')

    data = soup1.find("div", class_="main-column")
    # print(data)

    company_name = data.find("a", class_="font-bold color-inherit").contents[0]

    link = data.find("a", class_="font-bold color-inherit").attrs["href"]
    print(link)
    if link[0]=='/':
        company_url = 'https://www.ycombinator.com' + link
    # print(company_url)
    # print(company_name)

    company_list.append(company_url)

    title = data.find("h1").contents[0]
    print(title)

    json += '{"Company_Name":"' + company_name + '", '
    title1 = ""
    if " at" in title:
        for i in range (len(title)-2):
            if title[i+1]== 'a' and title[i+2] == 't' and title[i]==' ':
                break
            title1 += title[i]
    else:
        title1 = title



    top_bar = data.find("div", class_="highlight-box mb-20")
    # print(top_bar)

    strong_in_top_bar = top_bar.find_all("strong")
    span_in_top_bar = top_bar.find_all("span")
    # print(strong_in_top_bar)
    # print(span_in_top_bar)

    length = len(top_bar.find_all("strong"))
    isLocationPresent = False
    isExperiencePresent = False
    isJobPresent = False
    isSalaryPresent = False

    location = ""
    experience = ""
    job_type= ""
    salary = ""
    remote = 0
    remote_only = 0
    upper_salary = ""
    lower_salary = ""
    salary_exist = 1
    experience1 = ""
    experience2 = 0



    for i in range(1, length + 1):
        if strong_in_top_bar[-1 * i].contents[0] == 'Location':
            location += span_in_top_bar[-1 * i].contents[0]
            #json += '"Location":"' + span_in_top_bar[-1 * i].contents[0] + '", '
            isLocationPresent = True
        elif strong_in_top_bar[-1 * i].contents[0] == 'Experience':
            experience += span_in_top_bar[-1 * i].contents[0]
            #json += '"Experience":"' + span_in_top_bar[-1 * i].contents[0] + '", '
            isExperiencePresent = True

        elif strong_in_top_bar[-1 * i].contents[0] == 'Job Type':
            job_type += span_in_top_bar[-1 * i].contents[0]
            #json += '"Job_Type":"' + span_in_top_bar[-1 * i].contents[0] + '", '
            isJobPresent = True
        else:
            salary += strong_in_top_bar[-1 * i].contents[0]
            #json += '"Salary":"' + strong_in_top_bar[-1 * i].contents[0] + '", '
            isSalaryPresent = True

    if not isLocationPresent:
        location += "N/A"
    if not isExperiencePresent:
        experience +="N/A"
    if not isJobPresent:
        job_type += "N/A"
    if not isSalaryPresent:
        salary += "N/A"

    if "Remote" in location:
        remote = 1
    if location == "Remote":
        remote_only = 1
    if "-" in salary:
        lower_salary = salary.split("-")[0]
        upper_salary = salary.split("-")[1]
    elif salary == "N/A":
        lower_salary = "N/A"
        upper_salary = "N/A"
    else:
        upper_salary = lower_salary = salary
    if salary == "N/A":
        salary_exist = 0
    if "+ years" in experience:
        for i in range(len(experience)-7):
            if experience[i] == "+":
                break
            experience1 += experience[i]
    else:
        experience1 = "0"
    experience2 = int(experience1)
    if experience2 < 3:
        experience1 = "Entry Level"
    elif experience2 < 7:
        experience1 = "Mid Level"
    elif experience2 < 12:
        experience1 = "Senior Level"
    else:
        experience1 = "Executive Level"




    json += '"Job_Title":"' + title1 + '", '
    json += '"Location":"' + location + '", '
    json += '"Experience":' + str(experience2)+ ', '
    json += '"Experience_Level":"' + experience1 + '", '
    json += '"Job_Type":"' + job_type + '", '
    json += '"Salary":"' + salary + '", '
    json += '"Upper_Salary":"' + upper_salary + '", '
    json += '"Lower_Salary":"' + lower_salary + '", '
    json += '"Salary_Exist":' + str(salary_exist) + ', '
    json += '"Remote":' + str(remote) + ', '
    json += '"Remote_only":' + str(remote_only) + ', '




    # Description

    description = data.find_all("div", class_="readable show-more-less")[0].stripped_strings
    description_str = ''

    # for para in description:
    #    description_str += para
    # print('\n')
    # print(description_str)

    for element in data.find_all("div", class_="readable show-more-less")[0].contents:
        description_str += str(element)

    temporary_description_str = ''
    for i in range(0, len(description_str)):
        if description_str[i] == '\n':
            continue
        temporary_description_str += description_str[i]

    final_description_str = ''
    for char in temporary_description_str:
        if char == '"':
            continue
        final_description_str += char

    json += '"Description":"' + final_description_str + '", '

    # About Us

    why_to_join = data.find_all("div", class_="readable show-more-less")[1].stripped_strings
    why_to_join_str = ''

    for element in data.find_all("div", class_="readable show-more-less")[1].contents:
        why_to_join_str += str(element)

    temporary_why_to_join_str = ''
    for i in range(0, len(why_to_join_str)):
        if why_to_join_str[i] == '\n':
            continue
        temporary_why_to_join_str += why_to_join_str[i]

    final_why_to_join_str = ''
    for char in temporary_why_to_join_str:
        if char == '"':
            continue
        final_why_to_join_str += char

    json += '"About_Us":"' + final_why_to_join_str + '"'

    json += '}, '
    #print(json)

    output = ""
    for char in json:
        if char == '\n':
            output += ". "
        else:
            output += char

    #  comment the print for printing the company details
    #print(output)



company_detail_json = ''

for company_url in company_list:
    r1 = requests.get(company_url)
    htmlContent1 = r1.content
    soup1 = BeautifulSoup(htmlContent1, 'html.parser')

    data = soup1.find("div", class_="main-column")
    # print(data)

    logo_img = data.find("div", class_="round-logo-wrapper").find("img")

    if logo_img != None:
        logo=logo_img.attrs['src']
    else:
        logo='N/A'
    print(logo)



    pill = data.find_all("span", class_="pill")
    industry_type = ''

    if len(pill) == 3:
        industry_type += pill[1].contents[0]
    else:
        industry_type += 'N/A'
    #print(industry_type)

    name = data.find("h1").contents[0]
    #print(name)

    tag_line = data.find("h3").contents[0]
    #print(tag_line)

    description = data.find("p", class_="pre-line").contents
    #print(description)
    description_str = ''

    for element in description:
        description_str += str(element)

    temporary_description_str = ''
    for i in range(0, len(description_str)):
        if description_str[i] == '\r':
            continue
        if description_str[i] == '\n':
            continue
        temporary_description_str += description_str[i]

    final_description_str = ''
    for char in temporary_description_str:
        if char == '"':
            continue
        final_description_str += char

    #print(temporary_description_str)
    #print(final_description_str)

    link = data.find("div", class_="links").find("a").attrs["href"]
    #print(link)

    data = soup1.find("div", class_="sidebar-column")
    facts = data.find("div", class_="facts").find_all("span")

    founded = ''
    if len(facts[0].contents) > 0:
        founded += facts[0].contents[0]
    else:
        founded += 'N/A'
    #print(founded)

    team_size = ''
    if len(facts[1].contents) > 0:
        if '-' not in facts[1].contents[0]:
            team_size_num = int(facts[1].contents[0])
            if team_size_num <= 15:
                team_size += "1-15"
            elif team_size_num <= 30:
                team_size += "16-30"
            elif team_size_num <= 100:
                team_size += "31-100"
            elif team_size_num <= 500:
                team_size += "101-500"
            elif team_size_num <=1000:
                team_size += "501-1,000"
            elif team_size_num <= 5000:
                team_size += "1,001-5,000"
            elif team_size_num <= 10000:
                team_size += "5,001-10,000"
            else:
                team_size += "10,000"
        else:
            team_size += facts[1].contents[0]
    else:
        team_size += 'N/A'
    #print(team_size)

    state = ""
    city = ""
    headquarter = ''
    if len(facts[2].contents) > 0:
        headquarter += facts[2].contents[0]
        #print(headquarter)
        headquarter_split = headquarter.split(",")
        print(len(headquarter_split))
        if len(headquarter_split)>1:
            city = headquarter.split(",")[0]
            state = headquarter.split(",")[1]
        else:
            city = headquarter
            state = ""
    else:
        headquarter += 'N/A'


    company_detail_json += '{"Company_Name":"' + name + '", '
    company_detail_json += '"Tagline":"' + tag_line + '", '
    company_detail_json += '"logo":"' + logo + '", '
    company_detail_json += '"Industry_type":"' + industry_type + '", '
    company_detail_json += '"About_Company":"' + final_description_str + '", '
    company_detail_json += '"Founded":"' + founded + '", '
    company_detail_json += '"Team_size":"' + team_size + '", '
    company_detail_json += '"Headquarter":"' + headquarter + '",'
    company_detail_json += '"City":"' + city + '",'
    company_detail_json += '"State_Code":"' + state + '",'
    company_detail_json += '"link":"' + link + '"'
    company_detail_json += '}, '
    # comment this print when printing the job details
    print(company_detail_json)



