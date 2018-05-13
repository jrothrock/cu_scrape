from emailer import Emailer
from scraper_faculty import ScraperFaculty
from scraper_students import ScraperStudent
import os.path

def main():
    students = False
    emails = getEmailsFaculty()

    if students:
        emails = getEmailsStudents()
    else:
        emails = getEmailsFaculty()
    
    with Emailer() as email:
        success = email.Send(emails)

    if success:
        file = './cu_students_remaining.txt' if students else './cu_research_faculty_remaining.txt'
        with open(file, 'w') as fout:
            fout.writelines(data[400:])

def getEmailsFaculty():
    if os.path.exists('./cu_research_faculty_remaining.txt'):
        return readEmails('./cu_research_faculty_remaining.txt')
    else:
        with ScraperFaculty() as sf:
            return sf.scrape()
        return readEmails('./cu_research_faculty_remaining.txt')

def getEmailsStudents():
    if os.path.exists('./cu_students_remaining.txt'):
        return readEmails('./cu_students_remaining.txt')
    else:
        cookie = None
        with ScraperStudent(cookie) as ss:
            ss.scrape()
        return readEmails('./cu_students_remaining.txt')

def readEmails(file):
    # I'm going to ignore memory efficiency. 
    with open(file, 'r') as fin:
        data = fin.read().splitlines(True)
    return ', '.join(data[:400]).replace('\n', '').replace('\r', '')


if __name__ == '__main__':
    main()