# Testing

- Manual testing was carried out throughout the development of the website and bugs fixed as they arose.

## Manual testing
- Manual testing was carried out on the local and deployed sites.

| Location           | Feature                 | Expected Outcome                                                                                                                                                                                                                                          | Pass/Fail | Notes                                                                                                                                      |
| ------------------ | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Header             | Home button             | Takes user to home page on click                                                                                                                                                                                                                          | PASS      |                                                                                                                                            |
| Header             | Log-in button           | Takes user to log-in page on click                                                                                                                                                                                                                        | PASS      | If user is not logged in, the register and log-in buttons will be displayed but if they are logged in, only the log-out button will appear |
| Header             | Register button         | Takes user to registration page on click                                                                                                                                                                                                                  | PASS      |
| Header             | Logout button           | Logs the user out on click                                                                                                                                                                                                                                | PASS      |
| Log-in page        | Log-in function         | When user enters an unknown username, the user will not be logged in                                                                                                                                                                                      | PASS      |                                                                                                                                            |
| Log-in page        | Log-in function         | When user enters an unknown password, the user will not be logged in                                                                                                                                                                                      | PASS      |                                                                                                                                            |
| Log-in page        | Log-in function         | When user enters a known username AND password, the user will be logged in                                                                                                                                                                                | PASS      |                                                                                                                                            |
| Register page      | Register function       | If user does not enter information into any of the fields, they will be prompted to fill in the field                                                                                                                                                     | PASS      |                                                                                                                                            |
| Register page      | Register function       | If user does not enter a password which fits the criteria, they will not be registered                                                                                                                                                                    | PASS      |                                                                                                                                            |
| Register page      | Register function       | If user does not enter a matching password into the password (again) box, they will not be registered                                                                                                                                                     | PASS      |                                                                                                                                            |
| Register page      | Register function       | If user enters appropriate details, they will be registered                                                                                                                                                                                               | PASS      |                                                                                                                                            |
| Logout page        | Sign out button         | Signs user out on click                                                                                                                                                                                                                                   | PASS      |                                                                                                                                            |
| Home page          | Task creation           | User can create a new task by entering a title and clicking the add button                                                                                                                                                                                | PASS      |                                                                                                                                            |
| Home page          | Task prioritization     | User can drag and drop tasks to prioritize them                                                                                                                                                                                                           | PASS      |                                                                                                                                            |
| Home page          | Task completion         | User can mark tasks as completed by checking the checkbox                                                                                                                                                                                                 | PASS      |                                                                                                                                            |
| Home page          | Task editing            | User can edit tasks by clicking the edit button and updating the task details                                                                                                                                                                             | PASS      |                                                                                                                                            |
| Home page          | Task deletion           | User can delete tasks by clicking the delete button                                                                                                                                                                                                       | PASS      |                                                                                                                                            |
| Task prioritization| Drag and drop           | User can drag and drop tasks into different quadrants in the priority matrix                                                                                                                                                                              | PASS      |                                                                                                                                            |
| Task prioritization| Quadrant assignment     | Tasks are correctly assigned to the selected quadrant and the button classes update accordingly                                                                                                                                                           | PASS      |                                                                                                                                            |
| Task prioritization| Quadrant reassignment   | Tasks can be reassigned to different quadrants by dragging and dropping, and the button classes update accordingly                                                                                                                                        | PASS      |                                                                                                                                            |

## Code validators
### HTML
- The [W3C Validator](https://validator.w3.org/) was used to validate the HTML.
#### Home
- ![Home page validator screenshot](static/images/html-vali-home.png)

#### Login page
- ![Login page validator screenshot](static/images/html-vali-login.png)

#### Register page
- ![Register page validator screenshot](static/images/html-val-register.png)

### CSS custom code
- The [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) was used to validate the CSS.
- ![CSS validator screenshot](static/images/css-vali.png)

<p>
    <a href="http://jigsaw.w3.org/css-validator/check/referer">
        <img style="border:0;width:88px;height:31px"
            src="http://jigsaw.w3.org/css-validator/images/vcss"
            alt="Valid CSS!" />
    </a>
</p>
<p>
<a href="http://jigsaw.w3.org/css-validator/check/referer">
    <img style="border:0;width:88px;height:31px"
        src="http://jigsaw.w3.org/css-validator/images/vcss-blue"
        alt="Valid CSS!" />
    </a>
</p>

### Python
- The [CI Python Linter](https://pep8ci.herokuapp.com/) was used to validate the Python files.
- admin.py
- ![PEP8 screenshot](static/images/pep8-admin.png)
- apps.py
- ![PEP8 screenshot](static/images/pep8-apps.png)
- forms.py
- ![PEP8 screenshot](static/images/pep8-forms.png)
- models.py
- ![PEP8 screenshot](static/images/pep8-models.png)
- settings.py
- ![PEP8 screenshot](static/images/pep8-settings.png)
- urls.py
- ![PEP8 screenshot](static/images/pep8-urls.png)
- views.py
- ![PEP8 screenshot](static/images/pep8-views.png)

### Lighthouse
#### Home
- ![Lighthouse screenshot for home page](static/images/lighthouse-home.png)

#### Register
- ![Lighthouse screenshot for register page](static/images/lighthouse-register.png)

#### Login
- ![Lighthouse screenshot for login page](static/images/lighthouse-login.png)

#### Task prioritization
- ![Lighthouse screenshot for task prioritization page](static/images/lighthouse-task-prioritization.png)

#### Future improvements based on Lighthouse
- The biggest performance issue was the detailed logo. This was already converted to WEBP so perhaps a less detailed image would be used if this site was to be carried forward.
- Accessibility would be a priority moving forward. The colour palette was chosen based upon the central image and maintained throughout the site for design purposes. Moving forward, more high contrast colours would be chosen.

## Responsiveness
#### Mobile (iPhone 14 Pro)
- ![mobile responsiveness screenshot- home](static/images/iphone-14-pro-home.png)
- ![mobile responsiveness screenshot- register](static/images/iphone-14-pro-register.png)
- ![mobile responsiveness screenshot- task prioritization](static/images/iphone-14-pro-task-prioritization.png)

#### Tablet (iPad Air 5)
- ![tablet responsiveness screenshot- home](static/images/ipad-air-5-home.png)
- ![tablet responsiveness screenshot- register](static/images/ipad-air-5-register.png)
- ![tablet responsiveness screenshot- task prioritization](static/images/ipad-air-5-task-prioritization.png)

#### Desktop (Macbook Air)
- ![laptop responsiveness screenshot- home](static/images/macbook-air-home.png)
- ![laptop responsiveness screenshot- register](static/images/macbook-air-register.png)
- ![laptop responsiveness screenshot- task prioritization](static/images/macbook-air-task-prioritization.png)

## Browsers
- I use Google Chrome as my browser so all screenshots above are from Google Chrome.
- The site was tested on Microsoft Edge:
- ![Microsoft Edge screenshot](static/images/edge.png)
- The site was tested on Opera:
- ![Opera screenshot](static/images/opera.png)

## Bugs
- When users want to Edit their tasks, I wanted to pre-populate the Edit box with their original task details. I tried this in many different ways, using views and JavaScript, searching the internet for many different solutions but could not solve this issue. Instead, when the user clicks Edit, they are taken to a new tab so that they can still read their initial task details and copy it if they want. The Edit functionality still works and users are able to Edit their tasks. Editing can also easily be achieved by the superuser in the admin panel.
- Initially there were going to be multiple tasks for one project and I based the slug off of the project name. I later realised that this would mean that there could be identical slugs which would cause major problems. I changed the concept so that there was one central project that the slug could be based on and then multiple tasks could be added to this central project. At first I thought to fix this by having a 'task tagline' which the slug would be based on but further developed this idea.
- When adding Summernote to the task function, initially the task description box was not showing up at all. After changing the Debug setting it then worked.