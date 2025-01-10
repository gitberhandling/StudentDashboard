# Student Dashboard

A web-based dashboard to visualize and analyze student survey responses, including scores, ranks, percentiles, and category distributions. Built using **Dash** and **Pandas**, this project offers a leaderboard and graphical representations of student performance.

## Features

- Displays a leaderboard with total scores, ranks, percentiles, and categories.
- Color-coded categories based on scores:
  - **Green**: Excellent (Score ≥ 80)
  - **Yellow**: Good (50 ≤ Score < 80)
  - **Red**: Needs Improvement (Score < 50)
- Bar chart to visualize the distribution of categories.
- Line graph to illustrate percentile distribution among students.
- Dynamic and interactive table with sorting and pagination.

## Prerequisites

- Python 3.7+
- Required Python libraries:
  - Dash
  - Pandas
  - Plotly

Install the dependencies using:

    ```bash
    pip install dash pandas plotly

1.Clone this repository:

    ```bash
    git clone https://github.com/your-username/StudentDashboard.git
    cd StudentDashboard

#Place your dataset file (dataset1.csv) in the project directory.

Run the app:

    ```bash
    python app.py

    
Open your web browser and go to http://127.0.0.1:8050/ to view the dashboard.
