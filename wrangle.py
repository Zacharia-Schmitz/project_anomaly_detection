import pandas as pd
import matplotlib.pyplot as plt


def check_columns(DataFrame, reports=False, graphs=False, dates=False):
    """
    This function takes a pandas dataframe as input and returns
    a dataframe with information about each column in the dataframe.
    """

    dataframeinfo = []

    # Check information about the index
    index_dtype = DataFrame.index.dtype
    index_unique_vals = DataFrame.index.unique()
    index_num_unique = DataFrame.index.nunique()
    index_num_null = DataFrame.index.isna().sum()
    index_pct_null = index_num_null / len(DataFrame.index)

    if pd.api.types.is_numeric_dtype(index_dtype) and not isinstance(
        DataFrame.index, pd.RangeIndex
    ):
        index_min_val = DataFrame.index.min()
        index_max_val = DataFrame.index.max()
        index_range_vals = (index_min_val, index_max_val)
    elif pd.api.types.is_datetime64_any_dtype(index_dtype):
        index_min_val = DataFrame.index.min()
        index_max_val = DataFrame.index.max()
        index_range_vals = (
            index_min_val.strftime("%Y-%m-%d"),
            index_max_val.strftime("%Y-%m-%d"),
        )

        # Check for missing dates in the index if dates kwarg is True
        if dates:
            full_date_range = pd.date_range(
                start=index_min_val, end=index_max_val, freq="D"
            )
            missing_dates = full_date_range.difference(DataFrame.index)
            if not missing_dates.empty:
                print(
                    f"Missing dates in index: ({len(missing_dates)} Total) {missing_dates.tolist()}"
                )
    else:
        index_range_vals = None

    dataframeinfo.append(
        [
            "index",
            index_dtype,
            index_num_unique,
            index_num_null,
            index_pct_null,
            index_unique_vals,
            index_range_vals,
        ]
    )

    print(f"Total rows: {DataFrame.shape[0]}")
    print(f"Total columns: {DataFrame.shape[1]}")

    if reports:
        describe = DataFrame.describe().round(2)
        print(describe)

    if graphs:
        DataFrame.hist(figsize=(10, 10))
        plt.subplots_adjust(hspace=0.5)
        plt.show()

    for column in DataFrame.columns:
        dtype = DataFrame[column].dtype
        unique_vals = DataFrame[column].unique()
        num_unique = DataFrame[column].nunique()
        num_null = DataFrame[column].isna().sum()
        pct_null = DataFrame[column].isna().mean().round(5)

        if pd.api.types.is_numeric_dtype(dtype):
            min_val = DataFrame[column].min()
            max_val = DataFrame[column].max()
            mean_val = DataFrame[column].mean()
            range_vals = (min_val, max_val, mean_val)
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            min_val = DataFrame[column].min()
            max_val = DataFrame[column].max()
            range_vals = (min_val.strftime("%Y-%m-%d"), max_val.strftime("%Y-%m-%d"))

            if dates:
                full_date_range_col = pd.date_range(
                    start=min_val, end=max_val, freq="D"
                )
                missing_dates_col = full_date_range_col.difference(DataFrame[column])
                if not missing_dates_col.empty:
                    print(
                        f"Missing dates in column '{column}': ({len(missing_dates_col)} Total) {missing_dates_col.tolist()}"
                    )
                else:
                    print(f"No missing dates in column '{column}'")

        else:
            range_vals = None

        dataframeinfo.append(
            [column, dtype, num_unique, num_null, pct_null, unique_vals, range_vals]
        )

    return pd.DataFrame(
        dataframeinfo,
        columns=[
            "col_name",
            "dtype",
            "num_unique",
            "num_null",
            "pct_null",
            "unique_values",
            "range (min, max, mean)",
        ],
    )


def plot_web_top_paths(webjava_df, topx=10):
    """
    Plots the top X paths for each cohort in the webjava_df DataFrame alongside the overall top X paths.

    Args:
    - webjava_df: pandas DataFrame containing webjava cohort data
    - topx: integer representing the number of top paths to plot (default is 10)

    Returns:
    - None
    """

    # Cut webjava cohorts to only after 2020
    recentjava = webjava_df[webjava_df["class_start"] > "2021-01-01"]

    # Get the counts for the overall top X paths for 'web'
    overall_top_counts = recentjava["path"].value_counts(normalize=True).head(topx)

    # For each cohort, plot their top X paths alongside the overall top X
    for cohort, group in recentjava.groupby("cohort_id"):
        cohort_top_10 = group["path"].value_counts(normalize=True).head(topx)

        # Create a combined dataframe for plotting
        df2 = pd.DataFrame(
            {"Overall Web": overall_top_counts, f"Cohort {cohort}": cohort_top_10}
        )

        # Sort the dataframe by the cohort top X
        df2 = df2.sort_values(by=f"Cohort {cohort}", ascending=False)

        # Plot
        ax = df2.plot(kind="barh", figsize=(12, 8), width=0.8)
        ax.set_title(
            f"Web Dev (Java) Cohort {cohort} Top {topx} Paths vs. Overall Top {topx}"
        )
        ax.set_xlabel("Ratio of Accesses")
        ax.set_ylabel("Paths")
        plt.tight_layout()
        plt.show()


def plot_data_top_paths(data_df, topx=10):
    """
    Plots the top X paths for each cohort in the data_df DataFrame alongside the overall top X paths.

    Args:
    - data_df: pandas DataFrame containing data cohort data
    - topx: integer representing the number of top paths to plot (default is 10)

    Returns:
    - None
    """

    # Cut data cohorts to only after 2020
    recentdata = data_df[data_df["class_start"] > "2020-01-01"]

    # Get the counts for the overall top X paths for 'data'
    overall_top_counts = recentdata["path"].value_counts(normalize=True).head(topx)

    # For each cohort, plot their top X paths alongside the overall top X paths
    for cohort, group in recentdata.groupby("cohort_id"):
        cohort_top_10 = group["path"].value_counts(normalize=True).head(topx)

        # Create a combined dataframe for plotting
        df3 = pd.DataFrame(
            {"Overall Data": overall_top_counts, f"Cohort {cohort}": cohort_top_10}
        )

        # Sort the dataframe by the cohort top X
        df3 = df3.sort_values(by=f"Cohort {cohort}", ascending=False)

        # Plot
        ax = df3.plot(kind="barh", figsize=(12, 8), width=0.8)
        ax.set_title(f"Cohort {cohort} Top {topx} Paths vs. Overall Top {topx}")
        ax.set_xlabel("Ratio of Accesses")
        ax.set_ylabel("Paths")
        plt.tight_layout()
        plt.show()


def plot_active_selection(df):
    """
    Plots various metrics related to active selection in the given DataFrame.

    Args:
    - df: pandas DataFrame containing data

    Returns:
    - None
    """

    # Users Accessing Outside of Cohort Duration
    outside_access = df[
        ~df.apply(lambda x: x["class_start"] <= x["datetime"] <= x["class_end"], axis=1)
    ]
    outside_users = outside_access["user_id"].value_counts()

    # High Request Volume
    ip_request_counts = df["source_ip"].value_counts()
    high_request_ips = ip_request_counts[
        ip_request_counts > ip_request_counts.quantile(0.99)
    ]  # IPs with requests in the top 1%

    # Access Patterns and Unique Page Access
    ip_unique_pages = df.groupby("source_ip")["path"].nunique()
    high_unique_page_ips = ip_unique_pages[
        ip_unique_pages > ip_unique_pages.quantile(0.99)
    ]  # IPs accessing unique pages in the top 1%

    # Frequent Access to the Same Page
    ip_same_page_counts = df.groupby(["source_ip", "path"]).size()
    high_same_page_ips = ip_same_page_counts[
        ip_same_page_counts > ip_same_page_counts.quantile(0.99)
    ]

    # Suspicious IP Addresses
    known_ips = df[df["cohort_id"].notna()]["source_ip"].unique()
    suspicious_ips = set(df["source_ip"].unique()) - set(known_ips)

    # Set up the figure and axes
    fig, axs = plt.subplots(4, 1, figsize=(14, 20))

    # 1. Users Accessing Outside of Cohort Duration
    outside_users.head(10).sort_values().plot(
        kind="barh", ax=axs[0], color="cornflowerblue"
    )
    axs[0].set_title("Top 10 Users Accessing Outside of Cohort Duration")
    axs[0].set_xlabel("Number of Accesses")
    axs[0].set_ylabel("User ID")

    # 2. High Request Volume
    high_request_ips_new = high_request_ips[
        ~high_request_ips.index.str.startswith("97.105")
    ]
    high_request_ips_new.head(10).sort_values().plot(
        kind="barh", ax=axs[1], color="lightcoral"
    )
    axs[1].set_title("IPs with High Request Volume (excluding 97.105 IPs)")
    axs[1].set_xlabel("Number of Requests")
    axs[1].set_ylabel("IP Address")

    # 3. Unique Page Access
    high_unique_page_ips_new = high_unique_page_ips[
        ~high_unique_page_ips.index.str.startswith("97.105")
    ]
    high_unique_page_ips_new.sort_values().head(20).plot(
        kind="barh", ax=axs[2], color="mediumseagreen"
    )
    axs[2].set_title("Top 20 IPs Accessing Most Unique Pages (excluding 97.105 IPs)")
    axs[2].set_xlabel("Number of Unique Pages Accessed")
    axs[2].set_ylabel("IP Address")

    # 4. Frequent Access to the Same Page
    high_same_page_ips_new = ip_same_page_counts[
        ip_same_page_counts > ip_same_page_counts.quantile(0.99)
    ]
    high_same_page_ips_new = high_same_page_ips_new[
        ~high_same_page_ips_new.index.get_level_values("source_ip").str.startswith(
            "97.105"
        )
    ]
    high_same_page_ips_new.reset_index().groupby("source_ip").sum().sort_values(
        by=0, ascending=False
    ).head(10)[0].sort_values().plot(kind="barh", ax=axs[3], color="orchid")
    axs[3].set_title(
        "Top 10 IPs Frequently Accessing the Same Page (excluding 97.105 IPs)"
    )
    axs[3].set_xlabel("Number of Accesses")
    axs[3].set_ylabel("IP Address")

    plt.tight_layout()
    plt.show()


def plot_program_cross_access(df):
    """
    Plots the monthly accesses for data program users accessing web paths and web program users accessing data paths.

    Args:
    - df: pandas DataFrame containing data

    Returns:
    - None
    """

    # Identify unique paths for web_php, web_java, web_front program
    web_paths = df[df["program"].isin(["web_php", "web_java", "web_front"])][
        "path"
    ].unique()

    # Drop homepage from web_paths path
    web_paths = web_paths[web_paths != "homepage"]

    # Identify unique paths for "data" program
    data_paths = df[df["program"] == "data"]["path"].unique()
    # Drop homepage from data_paths path
    data_paths = data_paths[data_paths != "homepage"]

    # Check if any users from the "data" program accessed "web" paths in the entire dataframe
    all_data_users_accessing_web = df[
        (df["program"] == "data") & (df["path"].isin(web_paths))
    ]

    # Check if any users from the "web" program accessed "data" paths in the entire dataframe
    all_web_users_accessing_data = df[
        (df["program"].isin(["web_php", "web_java", "web_front"]))
        & (df["path"].isin(data_paths))
    ]
    # Group by month and year and count accesses for data users accessing web paths
    all_monthly_data_accessing_web = all_data_users_accessing_web.groupby(
        [
            all_data_users_accessing_web["datetime"].dt.year,
            all_data_users_accessing_web["datetime"].dt.month,
        ]
    ).size()

    # Group by month and year and count accesses for web users accessing data paths
    all_monthly_web_accessing_data = all_web_users_accessing_data.groupby(
        [
            all_web_users_accessing_data["datetime"].dt.year,
            all_web_users_accessing_data["datetime"].dt.month,
        ]
    ).size()

    # Plotting the results
    fig, axs = plt.subplots(2, 1, figsize=(14, 12))

    all_monthly_data_accessing_web.plot(
        ax=axs[0], marker="o", color="mediumseagreen", linestyle="-"
    )
    axs[0].set_title(
        "Monthly Accesses: Data Program Users Accessing Web Paths (Full Data)"
    )
    axs[0].set_xlabel("Year, Month")
    axs[0].set_ylabel("Number of Accesses")
    axs[0].grid(True, which="both", linestyle="--", linewidth=0.5)

    all_monthly_web_accessing_data.plot(
        ax=axs[1], marker="o", color="cornflowerblue", linestyle="-"
    )
    axs[1].set_title(
        "Monthly Accesses: Web Program Users Accessing Data Paths (Full Data)"
    )
    axs[1].set_xlabel("Year, Month")
    axs[1].set_ylabel("Number of Accesses")
    axs[1].grid(True, which="both", linestyle="--", linewidth=0.5)

    plt.tight_layout()
    plt.show()


def plot_top_post_grad_paths(df):
    """
    Plots the top 10 accessed paths after graduation for each program.

    Args:
    - df: pandas DataFrame containing data

    Returns:
    - None
    """

    # Filter the dataset to only include records accessed after the class_end date
    post_grad_data = df[df["datetime"] > df["class_end"]]

    # Group by program and path to count accesses
    post_grad_access_counts = post_grad_data.groupby("program")["path"].value_counts()

    # Identify the top 10 most accessed paths for each program
    top_paths_per_program = post_grad_access_counts.groupby("program").head(10)

    # Set up the figure and axes
    fig, axs = plt.subplots(4, 1, figsize=(12, 14))

    # Plotting top 10 post-graduation paths for "web" program
    top_paths_per_program["web_php"].sort_values().plot(
        kind="barh", ax=axs[0], color="gold"
    )
    axs[0].set_title("Top 10 Accessed Paths After Graduation for Web PHP Program")
    axs[0].set_xlabel("Number of Accesses")
    axs[0].set_ylabel("Paths")

    # Plotting top 10 post-graduation paths for "web" program
    top_paths_per_program["web_java"].sort_values().plot(
        kind="barh", ax=axs[1], color="crimson"
    )
    axs[1].set_title("Top 10 Accessed Paths After Graduation for Web Java Program")
    axs[1].set_xlabel("Number of Accesses")
    axs[1].set_ylabel("Paths")

    # Plotting top 10 post-graduation paths for "web" program
    top_paths_per_program["web_front"].sort_values().plot(
        kind="barh", ax=axs[2], color="cornflowerblue"
    )
    axs[2].set_title("Top 10 Accessed Paths After Graduation for Web Front End Program")
    axs[2].set_xlabel("Number of Accesses")
    axs[2].set_ylabel("Paths")

    # Plotting top 10 post-graduation paths for "data" program
    top_paths_per_program["data"].sort_values().plot(
        kind="barh", ax=axs[3], color="mediumseagreen"
    )
    axs[3].set_title("Top 10 Accessed Paths After Graduation for Data Science Program")
    axs[3].set_xlabel("Number of Accesses")
    axs[3].set_ylabel("Paths")

    plt.tight_layout()
    plt.show()
