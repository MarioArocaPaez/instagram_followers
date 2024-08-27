# InstaBackTrack

**InstaBackTrack** is a web application that helps Instagram users identify which accounts they follow but are not followed back by. This is done by comparing the user's following and followers lists from their Instagram data. The application displays the results in a user-friendly manner, showing the username, a link to their Instagram profile, and the date the user started following them.

## Purpose

The purpose of InstaBackTrack is to provide a simple and efficient way for Instagram users to manage their follower relationships. By identifying users who do not follow back, it allows users to make informed decisions about their social media connections.

## How InstaBackTrack is Different

Unlike typical apps that require your Instagram credentials to tell you who doesn't follow you back, **InstaBackTrack** respects your privacy:

- **No Instagram Credentials Required**: InstaBackTrack does not ask for your Instagram username or password. You only need to provide the JSON files that contain your following and followers data.
- **No Access to Your Instagram Account**: We do not perform any actions on your Instagram account. The app only compares the data you upload.
- **No Data Storage**: The data you upload is not stored anywhere on our servers. Once the comparison is done and results are displayed, the data is discarded.

## Technologies Used

- **Django**: A high-level Python web framework that promotes rapid development and clean, pragmatic design.
- **Bootstrap**: A popular CSS framework for building responsive and mobile-first websites, used to enhance the aesthetic and responsiveness of the web application.
- **HTML/CSS**: For structuring and styling the web pages.
- **JavaScript**: To handle the dynamic parts of the web app.
- **Python**: The main programming language used to build the backend logic.
- **JSON**: The format used to handle Instagram data for followers and following lists.

## How It Works

1. **File Upload**: Users upload their Instagram `following.json` and `followers_1.json` files.
2. **Data Processing**: The application reads and parses the JSON data from these files.
3. **Comparison Logic**: It extracts the usernames and compares the `following` list with the `followers` list.
4. **Display Results**: The results are displayed on the web page in a tabular format, showing:
   - The username of the account not following back.
   - A clickable link to the Instagram profile.
   - The date when the user started following the account.
5. **Error Handling**: If the uploaded files are not in the expected JSON format or structure, a friendly error message is displayed without crashing the application.

## Features

- **User-Friendly Interface**: Uses Bootstrap for a clean and responsive design.
- **Error Handling**: Handles incorrect file uploads gracefully, providing user feedback without app crashes.
- **Mobile Responsiveness**: Designed to be accessible and usable on mobile devices.
- **Clickable Links**: Provides direct links to Instagram profiles for quick access.
- **Date Information**: Displays when each account was followed, providing more context.

## How to Use It

1. **Clone the Repository**: Clone the InstaBackTrack repository from GitHub to your local machine.
    ```bash
    git clone https://github.com/MarioArocaPaez/instagram_followers.git
    cd InstaBackTrack
    ```

2. **Install Requirements**: Install the necessary dependencies using `pip`.
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Django Server**: Start the Django development server.
    ```bash
    python manage.py runserver
    ```

4. **Access the Web App**: Open a web browser and navigate to `http://127.0.0.1:8000/`.

5. **Upload Files**: On the homepage, use the form to upload your `following.json` and `followers_1.json` files.

6. **View Results**: The application will process the files and display a table with accounts that do not follow you back, along with links to their Instagram profiles and the date you started following them.

## Contributing

If you would like to contribute to the project, please fork the repository and create a pull request. Any improvements or suggestions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact

For any questions or support, please contact the project maintainer: [marioap2002@gmail.com](mailto:marioap2002@gmail.com)
