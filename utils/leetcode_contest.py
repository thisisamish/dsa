import argparse
import requests
from bs4 import BeautifulSoup
import os

def get_contest_url(contest_type, contest_number):
    return f"https://leetcode.com/contest/{contest_type}-contest-{contest_number}/"

def scrape_problems(contest_url):
    response = requests.get(contest_url)
    if response.status_code != 200:
        print("Failed to retrieve contest page.")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    problems = []
    
    table = soup.find('table')
    if not table:
        print("Could not find problems table.")
        return []
    
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) >= 2:
            problem_number = cols[0].text.strip()
            link_tag = cols[1].find('a')
            if link_tag:
                problem_name = link_tag.text.strip()
                problem_link = "https://leetcode.com" + link_tag['href']
                problems.append((problem_number, problem_name, problem_link))
    
    return problems

def generate_markdown(contest_type, contest_number, problems):
    filename = f"{contest_type.capitalize()}_Contest_{contest_number}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# [{contest_type.capitalize()} Contest {contest_number}]({get_contest_url(contest_type, contest_number)})\n\n")
        f.write("## Problems\n\n")
        f.write("| Number    | Name                              | Link  |\n")
        f.write("| --------- | --------------------------------- | ----- |\n")
        for num, name, link in problems:
            f.write(f"|  {num}     | {name} | {link} |\n")
    print(f"Markdown file '{filename}' generated.")

def create_code_files(problems, language):
    ext_map = {"py": "py", "go": "go", "cpp": "cpp", "java": "java"}
    ext = ext_map.get(language, "txt")
    
    for num, _, _ in problems:
        filename = f"{num}.{ext}"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"// Solution for problem {num}\n")
        print(f"Created file: {filename}")

def main():
    parser = argparse.ArgumentParser(description="LeetCode Contest Scraper")
    parser.add_argument("contest_type", choices=["weekly", "biweekly"], help="Contest type: weekly or biweekly")
    parser.add_argument("contest_number", type=int, help="Contest number")
    parser.add_argument("language", choices=["py", "go", "cpp", "java"], help="Language for code files")
    
    args = parser.parse_args()
    
    contest_url = get_contest_url(args.contest_type, args.contest_number)
    problems = scrape_problems(contest_url)
    
    if problems:
        generate_markdown(args.contest_type, args.contest_number, problems)
        create_code_files(problems, args.language)
    else:
        print("No problems found.")

if __name__ == "__main__":
    main()
