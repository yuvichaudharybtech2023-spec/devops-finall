# Student Feedback Form - Jenkins CI Guide

This guide explains how to fulfill Sub Task 5 (Use of Jenkins) to automate the execution of your Selenium test cases.

## Prerequisites
1. Ensure you have Java installed (`java -version`). Jenkins requires Java.
2. Ensure you have Python and `pip` installed (`python --version`).
3. You should have downloaded the `Jenkins.war` file or installed Jenkins via the Windows installer from the official Jenkins website.

## Step 1: Install Jenkins
1. Run the Jenkins installer or start it via command line:
   ```cmd
   java -jar jenkins.war --httpPort=8080
   ```
2. Open your browser and navigate to `http://localhost:8080`.
3. Follow the initial setup instructions by providing the initial admin password found in your secrets directory.
4. Install the "Suggested Plugins."

## Step 2: Create a simple Jenkins job
1. Once logged in, click on **New Item** on the left menu.
2. Enter a name (e.g., `Student-Feedback-Tests`).
3. Choose **Freestyle project** (or **Pipeline** if you want to use the included `Jenkinsfile`) and click **OK**.

## Step 3: Connect the project folder or GitHub repository
If you are using a Freestyle project and running this locally from your desktop:
1. In the **General** tab, click **Advanced** and check **Use custom workspace**.
2. Enter the path to your project folder: `C:\Users\Lenovo\OneDrive\Desktop\devops project`

*(Alternatively, if you pushed this to GitHub: Go to the **Source Code Management** section, select **Git**, and provide your repository URL.)*

## Step 4: Configure the job to run Selenium test scripts
1. Scroll down to the **Build Steps** section.
2. Click **Add build step** -> **Execute Windows batch command**.
3. Enter the necessary commands to set up the environment and run pytest:
   ```bat
   echo "Setting up virtual environment..."
   python -m venv venv
   call venv\Scripts\activate.bat
   pip install -r requirements.txt
   echo "Running Selenium tests..."
   pytest test_form.py -v
   ```

## Step 5: Execute the job
1. Click **Save** to finish configuring your job.
2. On the job dashboard, click **Build Now** on the left menu.
3. You should see a new build appear under **Build History** (e.g., #1).

## Step 6: Observe whether the build is successful or failed
1. Click on the build number (e.g., `#1`) in the **Build History**.
2. Click on **Console Output** to see the logs.
3. You should see pytest initializing, running the 7 tests, and showing `7 passed` at the bottom.
4. The build dot will be **Green/Blue** if successful, or **Red** if it failed.
