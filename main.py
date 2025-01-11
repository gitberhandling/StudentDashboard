import dash
from dash import dcc, html, dash_table, Input, Output, State
import pandas as pd

# Load the dataset
file_path = 'dataset1.csv'
df = pd.read_csv(file_path)

# Clean column names to remove leading/trailing spaces
df.columns = df.columns.str.strip()

# Define the questions (ensure these match the actual column names in your dataset)
questions = [
    "Question1: When considering enrolling in a new course or program, what is your primary motivation?",
    "Question2: How do you view opportunities for exposure to new ideas and experiences?",
    "Question3: How much time are you willing to dedicate weekly to a course that prepares you for internships?",
    "Question4: How do you handle a situation when a lot of people discourage you around a project that you are doing with a lot of interest",
    "Question5: Do you wish to standout from your peers?"
]

# Verify that these columns exist in the dataframe
missing_columns = [col for col in questions if col not in df.columns]
if missing_columns:
    raise ValueError(f"The following columns are missing: {missing_columns}")

# Define the XLOOKUP table for mapping responses to scores
lookup_table = {
    "Option A": 10,
    "Option B": 20,
    "Option C": 30,
    "Option D": 40
}

# Map responses to scores for each question
for col in questions:
    df[f"Score_{col}"] = df[col].map(lookup_table).fillna(0)

# Compute total score, rank, and percentile
df['Total Score'] = df[[f"Score_{col}" for col in questions]].sum(axis=1)
df['Rank'] = df['Total Score'].rank(ascending=False, method='min').astype(int)
df['Percentile'] = (df['Rank'] / len(df) * 100).round(2)

# Apply color coding
def categorize_score(score):
    if score >= 80:
        return "Green"
    elif score >= 50:
        return "Yellow"
    else:
        return "Red"

df['Category'] = df['Total Score'].apply(categorize_score)

# Dash app setup
app = dash.Dash(__name__)
app.title = "Student Dashboard"

# Layout
app.layout = html.Div([
    html.H1("Student Leaderboard Dashboard", style={"textAlign": "center"}),

    # Leaderboard table
    dash_table.DataTable(
        id='leaderboard-table',
        columns=[
            {"name": "Name", "id": "Name"},
            {"name": "Total Score", "id": "Total Score"},
            {"name": "Rank", "id": "Rank"},
            {"name": "Percentile", "id": "Percentile"},
            {"name": "Category", "id": "Category"}
        ],
        data=df.to_dict('records'),
        style_data_conditional=[
            {
                'if': {'filter_query': '{Category} = "Green"', 'column_id': 'Category'},
                'backgroundColor': 'lightgreen',
                'color': 'black'
            },
            {
                'if': {'filter_query': '{Category} = "Yellow"', 'column_id': 'Category'},
                'backgroundColor': 'yellow',
                'color': 'black'
            },
            {
                'if': {'filter_query': '{Category} = "Red"', 'column_id': 'Category'},
                'backgroundColor': 'lightcoral',
                'color': 'black'
            }
        ],
        style_table={'overflowX': 'auto'},
        sort_action="native",
        page_size=10
    ),

    # Visualizations
    html.Div([
        dcc.Graph(
            id='category-distribution',
            figure={
                "data": [
                    {
                        "x": df['Category'].value_counts().index,
                        "y": df['Category'].value_counts().values,
                        "type": "bar",
                        "marker": {"color": ["lightgreen", "yellow", "lightcoral"]},
                    }
                ],
                "layout": {
                    "title": "Category Distribution",
                    "xaxis": {"title": "Category"},
                    "yaxis": {"title": "Count"}
                }
            }
        )
    ]),

    html.Div([
        dcc.Graph(
            id='percentile-distribution',
            figure={
                "data": [
                    {
                        "x": df['Name'] if not df.empty else [],
                        "y": df['Percentile'] if not df.empty else [],
                        "type": "line",
                        "marker": {"color": "blue"}
                    }
                ],
                "layout": {
                    "title": "Percentile Distribution",
                    "xaxis": {"title": "Student"},
                    "yaxis": {"title": "Percentile"}
                }
            }
        )
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
