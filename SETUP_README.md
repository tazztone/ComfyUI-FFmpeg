# Jules Environment Setup Script

This `environment_setup.sh` script is a functional tool for setting up your Jules environment. It performs two main tasks:

1.  **Verification:** It checks for the presence and versions of key pre-installed software (like Python, Node.js, and Docker) as documented in the Jules environment.
2.  **Customization:** It provides a clearly marked section for you to add your own project-specific dependency installations.

## How to Use the Script

1.  **Make the script executable (if it isn't already):**
    ```bash
    chmod +x environment_setup.sh
    ```

2.  **Customize for your project:**
    Open the `environment_setup.sh` file and navigate to the "Project-Specific Dependency Installation" section. Here, you can add the commands needed for your project.

    For example, if your project uses Python dependencies, you can uncomment the `pip install` section:
    ```bash
    # Before
    # if [ -f "requirements.txt" ]; then
    #   ...
    # fi

    # After
    if [ -f "requirements.txt" ]; then
      echo "Installing Python dependencies from requirements.txt..."
      pip install -r requirements.txt
      echo "Python dependencies installed."
    else
      echo "No requirements.txt found. Skipping pip installation."
    fi
    ```

3.  **Run the script:**
    Execute the script from your terminal:
    ```bash
    ./environment_setup.sh
    ```

The script will first verify the base environment and then install your custom dependencies.
