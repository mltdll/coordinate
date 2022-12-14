# Coördinate

A simple app to help coordinate the work of employees in your company.

The project is deployed on render; [check it out](https://coordinate.onrender.com/). To access the website, use these credentials:

*Note that the hosting can be slow to respond initially*

```
login: test.subject
password: Lqlc3iUnfS2uf-K9olBi6g
```


## Installation

### Prerequisites
* Python 3.10+

### Steps to install

1. Clone the repository:
`
git clone https://github.com/mltdll/coordinate.git
`
2. Activate virtual environment: 
    * On Windows: `venv\Scripts\activate`
    * On Linux or MacOS: `source venv/bin/activate`
      * If you are using non-standard shell, you may have to source different file in `venv/bin/`, such as `venv/bin/activate.fish` for fish.
3. Install requirements: `pip install -r requirements.txt`
4. Apply migrations: `python manage.py migrate`
5. Run the server! `python manage.py runserver`

## Functionality
* Create profiles for your employees, change their positions, fire them!
* Create tasks, assign employees to them, update, mark them as completed or vice versa.
* Create unlimited number of positions for your employees. 

## Screenshots

Home page:
![](screenshots/homepage.png)

Task list:
![](screenshots/task_list.png)

Task detail:
![](screenshots/task_detail.png)

Employee detail:
![](screenshots/employee_detail.png)
