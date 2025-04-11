import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title = 'Data sweper', layout="wide")

st.markdown(
    """
    <style>
    .stApp{
     background-color: black;
     color : white;
    }
    </style>
     """,
     unsafe_allow_html=True
   
)


st.title("Datasweper sterling Intergrator By Anmol Adeeba")
st.write("Transform your file between CSV and Excel Format with build-in data cleaning and visuallization creating the project of quater 3!")

uploaded_files = st.file_uploader("Upload your file (accepted CSV or Excel): ",type=["cvs","xlsx"] , accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue

        st.write ("Preview the head of Dataframe")
        st.dataframe(df.head()) 


        st.subheader("Data Cleaning Option")
        if st.checkbox(f"clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_col = df.select_dtypes(include=['number']).columns
                    df[numeric_col] = df[numeric_col].fillna(df[numeric_col].mean())
                    st.write("Missing value have been filled!")

        st.subheader("Select colums to keep")
        colums = st.multiselect(f"Choose Colums for {file.name}", df.columns, default = df.columns)
        df = df[colums]


        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        st.subheader('Conversion Option')
        conversion_type = st.radio(f"Convert{file.name} to:",["CVS","Excel"], key=file.name)
        if st.button(f"Convert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CVS":
                df.to.cvs(buffer, index=False)
                file_name = file.name.replace(file_ext, ".cvs")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext,".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
            
st.success("All files processed successfully!")                                            

          