# Synthetic Data Generator

The **Synthetic Data Generator** is a lightweight tool that creates realistic, customizable datasets for training, testing, and demonstration purposes—without exposing sensitive information. By simulating real-world data structures, the tool helps researchers, trainers, and developers practice analysis workflows, prototype dashboards, or showcase tools while protecting respondent confidentiality.

This project reduces risks around handling personal data while increasing efficiency in research support, training, and capacity-building activities.

---

## Features

- **Customizable Data Generation:** Control the number of rows and columns
- **Statistical Control:** Choose distributions (Normal, Uniform, Exponential, Lognormal) for numeric variables
- **Correlation Management:** Enable and control correlation between numeric variables
- **Missing Data:** Adjust missing data percentage for realistic datasets
- **Personal Information:** Include realistic fake data (names, emails, addresses, phone numbers, etc.)
- **Multiple Export Formats:** Download data as CSV, Excel, or Stata DTA files
- **Data Preview:** Visualize correlations and data quality metrics

---

## Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd Synthetic-Data-Generator
```

Install required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run fake_data_generator.py
```

---

## Requirements

The application requires the following Python packages:

- `streamlit` – Web application framework
- `faker` – Fake data generation
- `pandas` – Data manipulation and analysis
- `numpy` – Numerical computing
- `scipy` – Scientific computing
- `openpyxl` – Excel file support
- `matplotlib` – Data visualization

---

## Usage

1. **Configure Parameters:** Use the sidebar to set:
	- Number of rows and columns
	- Personal information fields to include
	- Missing data percentage
	- Variable distributions and correlations
2. **Generate Data:** Click the "Generate Data" button
3. **Preview:** Review the data in the "Preview Data" tab
4. **Export:** Download your dataset in CSV, Excel, or Stata format

---

## Project Structure

```
Synthetic-Data-Generator/
├── fake_data_generator.py   # Main application file
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── run.bat                  # Windows batch file for easy execution
```

---

## Batch File Execution

For easy execution on Windows, use the provided `run.bat` file:

- Double-click `run.bat` to start the application
- The application will open in your default web browser

---

## Customization

You can easily modify the application to:

- Add new distribution types
- Include additional personal information fields
- Change correlation methods
- Add new export formats

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

This project is open source and available under the MIT License.

---

## Support

If you encounter any issues:

- Check that all dependencies are installed
- Ensure your Python environment is properly configured
- Verify that the required directories are in your system PATH

---

## Acknowledgments

- Built with Streamlit
- Uses Faker for realistic fake data generation
- Pandas for data manipulation and export capabilities

> **Note:** This tool generates synthetic data for testing and development purposes only. Always ensure compliance with data protection regulations when working with personal information.