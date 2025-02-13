# Testing Plan for ScrollToDo Application

## 1. Testing Strategy
The application was tested using:
- **Manual Testing** (Core functionality validation)
- **Automated Unit Tests** (Using Django’s built-in testing framework)

## 2. Test Execution Plan
| Test Case ID | Component         | Description                                    | Expected Result                                                                 | Status  |
|--------------|-------------------|------------------------------------------------|---------------------------------------------------------------------------------|---------|
| TC01         | User Registration | Verify user can register                       | Redirect to dashboard                                                           | ✅ Passed |
| TC02         | User Login        | Verify login with valid credentials            | Redirect to dashboard                                                           | ✅ Passed |
| TC03         | User Login        | Verify that an unregistered user can use the login form to create a new account | Redirect to dashboard | ✅ Passed |
| TC04         | Change Password   | Verify password change functionality           | Show success message                                                            | ❌ Failed |
| TC05         | Create Item List  | Verify that a logged-in user can create a new item list | Item list should be created and displayed on the dashboard              | ✅ Passed |
| TC06         | Add Item          | Verify that a logged-in user can add a new item to an item list | Item should be added to the item list and displayed                     | ✅ Passed |
| TC07         | Logout            | Verify that a logged-in user can log out successfully | User should be redirected to the index page and session should be terminated | ✅ Passed |
| TC08         | Delete Item       | Verify that a logged-in user can delete an item from an item list | Item should be removed from the item list                               | ✅ Passed |
| TC09         | Access Control    | Verify that an unauthenticated user cannot access the dashboard | User should be redirected to the index page for login                         | ✅ Passed |

## 3. Bugs & Issues Found
- **TC04: Change Password** → No confirmation message displayed after update, password not updated after form submition.

## 4. Future Improvements
- Implement better test coverage for edge cases.
- Improve UI notifications system.