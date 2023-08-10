import streamlit as st
import pandas as pd

# Streamlit layout
st.sidebar.title("Extract Matching data")
page_select = st.sidebar.selectbox("Go to", ["Based on Column and Unique Rows",
                                             "Based on Column only"])


if page_select == "Based on Column and Unique Rows":
    st.title("Extract Matching data by Column and Unique Rows")
    st.write("Note:\n"
             "1) Please ensure that the column names match between the two files.\n"
             "2) The first column contain unique IDs or names that are not repeated.\n"
             "2) Columns from either file that are not available in the other file will be skipped.")
    uploaded_file = st.sidebar.file_uploader("Upload Main file containing all data")
    uploaded_file2 = st.sidebar.file_uploader("Upload second file to match and extract")

    if uploaded_file is not None and uploaded_file2 is not None:
        # Load the data from uploaded CSV files
        df = pd.read_csv(uploaded_file)
        df2 = pd.read_csv(uploaded_file2)

        # Create df3 to store matched data
        df3 = df2.copy()

        # Get the column name for matching
        matching_column = df2.columns[0]

        # Check for columns from second file that are not available in main file
        missing_columns_second = [col for col in df2.columns if col not in df.columns]
        if missing_columns_second:
            st.warning(
                f"The following columns from the second file are not available in the main file and will be skipped:"
                f" {', '.join(missing_columns_second)}")

        # Iterate through df2 and fill matching values from df
        for index, row in df3.iterrows():
            if matching_column in df.columns:
                value_to_match = row[matching_column]
                matching_row = df[df[matching_column] == value_to_match]
                if not matching_row.empty:
                    matching_index = matching_row.index[0]
                    for column in df2.columns:
                        if column != matching_column and column in df.columns:
                            df3.at[index, column] = matching_row[column].values[0]
            else:
                st.warning(f"Column '{matching_column}' not found in the main data DataFrame.")

        # Display matched data in Streamlit
        st.dataframe(df3)

        # Add a button to download df3 as a CSV file
        filename = st.text_input("Enter the filename (e.g., matching_data.csv):")
        file_path = st.text_input("Enter the file path (e.g., /path/to/directory/):")

        if st.button("Download Matching Data as CSV"):
            if filename and file_path:
                full_path = f"{file_path}/{filename}"
                df3.to_csv(full_path, index=False)
                st.success(f"Matching data saved at {full_path}")


if page_select == "Based on Column only":
    st.title("Extract Matching data by Column only")
    st.write("Note:\n"
             "1) Please ensure that the column names match between the two files.\n"
             "2) Columns from either file that are not available in the other file will be skipped.")
    uploaded_file = st.sidebar.file_uploader("Upload Main file containing all data")
    uploaded_file2 = st.sidebar.file_uploader("Upload second file to extract")

    if uploaded_file is not None and uploaded_file2 is not None:
        # Load the data from uploaded CSV files
        df = pd.read_csv(uploaded_file)
        df2 = pd.read_csv(uploaded_file2)

        # Create df3 to store matched data
        # Create df3 with columns from df2 that match column names of df
        matching_columns = [col for col in df2.columns if col in df.columns]

        # Check for columns from second file that are not available in main file
        missing_columns_second = [col for col in df2.columns if col not in df.columns]
        if missing_columns_second:
            st.warning(
                f"The following columns from the second file are not available in the main file and will be skipped: "
                f"{', '.join(missing_columns_second)}")

        df3 = df[matching_columns].copy()

        # Display matched data in Streamlit
        st.dataframe(df3)

        # Add a button to download df3 as a CSV file
        filename = st.text_input("Enter the filename (e.g., matching_data.csv):")
        file_path = st.text_input("Enter the file path (e.g., /path/to/directory/):")

        if st.button("Download Matching Data as CSV"):
            if filename and file_path:
                full_path = f"{file_path}/{filename}"
                df3.to_csv(full_path, index=False)
                st.success(f"Matching data saved at {full_path}")

# Run the Streamlit app
if __name__ == "__main__":
    st.set_page_config(page_title="Matching Data App")
    st.sidebar.header("Matching Data App")
