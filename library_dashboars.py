from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Required Columns
required_columns = [
    "Transaction ID",
    "Date",
    "User ID",
    "Book Title",
    "Genre",
    "Borrowing Duration (Days)"
]


class LibraryDashboard:

    def __init__(self):
        self.data = pd.DataFrame()

    # Load Data
    def load_data(self, file_name):

        self.data = pd.read_csv(file_name)

        self.data = self.data[required_columns]

        self.data["Date"] = pd.to_datetime(
            self.data["Date"]
        )

        self.data.drop_duplicates(
            subset=["Transaction ID"],
            inplace=True
        )

        print("Data Loaded Successfully")
        return self.data

    # Statistics
    def calculate_statistics(self):

        print("\n===== Statistics =====")

        print(
            "Total Transactions :",
            len(self.data)
        )

        print(
            "Unique Users :",
            self.data["User ID"].nunique()
        )

        most_book = (
            self.data["Book Title"]
            .value_counts()
            .idxmax()
        )

        print(
            "Most Borrowed Book :",
            most_book
        )

        avg_days = (
            self.data["Borrowing Duration (Days)"]
            .mean()
        )

        print(
            "Average Duration :",
            avg_days
        )

    # Filter by Genre
    def filter_by_genre(self, genre):

        filtered = self.data[
            self.data["Genre"] == genre
        ]

        return filtered

    # Generate Report
    def generate_report(self):

        total = len(self.data)

        users = (
            self.data["User ID"]
            .nunique()
        )

        report = f"""
=========================
      E-LIBRARY REPORT
=========================

Total Transactions : {total}
Unique Users       : {users}

=========================
"""

        return report

    # Visualizations
    def create_visualizations(self):

        fig, ax = plt.subplots(
            2,
            2,
            figsize=(15, 10)
        )

        # BAR CHART
        books = (
            self.data["Book Title"]
            .value_counts()
            .head(5)
        )

        books.plot(
            kind="bar",
            color="skyblue",
            ax=ax[0, 0]
        )

        ax[0, 0].set_title(
            "Top 5 Borrowed Books"
        )

        ax[0, 0].set_xlabel(
            "Book Title"
        )

        ax[0, 0].set_ylabel(
            "Count"
        )

        # LINE CHART
        transactions = (
            self.data
            .groupby("Date")
            .size()
        )

        transactions.plot(
            kind="line",
            marker="o",
            color="green",
            ax=ax[0, 1]
        )

        ax[0, 1].set_title(
            "Transactions Over Time"
        )

        ax[0, 1].set_xlabel(
            "Date"
        )

        ax[0, 1].set_ylabel(
            "Transactions"
        )

        # PIE CHART
        genre_counts = (
            self.data["Genre"]
            .value_counts()
        )

        ax[1, 0].pie(
            genre_counts,
            labels=genre_counts.index,
            autopct="%1.1f%%"
        )

        ax[1, 0].set_title(
            "Genre Distribution"
        )

        # HEATMAP
        heatmap_data = pd.crosstab(
            self.data["Genre"],
            self.data["Book Title"]
        )

        sns.heatmap(
            heatmap_data,
            annot=True,
            cmap="YlGnBu",
            fmt="d",
            ax=ax[1, 1]
        )

        ax[1, 1].set_title(
            "Genre vs Book Title Heatmap"
        )

        plt.tight_layout()
        plt.show()


# ==========================
# MAIN PROGRAM
# ==========================

dashboard = LibraryDashboard()

dashboard.load_data(
    "library_transcation.csv"
)

print(
    dashboard.generate_report()
)

dashboard.calculate_statistics()

dashboard.create_visualizations()