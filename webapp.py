import streamlit as st 
import pandas as pd 

from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

from pathlib import Path
import os, time

st.title('Web App -  Data Explorer')


uploaded = False
dataset = pd.DataFrame()
@st.cache
def load_df(path,nrows=None):
	if nrows is not None:
		df = pd.read_csv(path).sample(nrows)
	else:
		df = pd.read_csv(path)
	return df

@st.cache    
def get_columns(df):
	return df.columns.to_list()

@st.cache
def generate_profile_report(df):
	pr = ProfileReport(df, explorative=True, minimal = True)
	return pr

def SwitchExample(argument):
	from vega_datasets import data
	switcher = {
	"Airports": data.airports(),
	"Cars" : data.cars()
	}
	return switcher.get(argument, "Not found!")


placeholder = st.empty()

if not uploaded:
	st.subheader("Choose a dataset or upload it")
	placeholder.text("Upload a dataset via .csv file or choose one from the predefined datasets list!")
	option_select = st.selectbox("Select a data source", options=['Upload .csv file','Choose a predefined dataset'])
	if option_select == 'Upload .csv file':
		try:
			uploaded_file = st.file_uploader("Choose a CSV file", type="csv", encoding = 'auto')
			if uploaded_file is not None:
				dataset = load_df(uploaded_file)
				uploaded = True
		except Exception as e:
			placeholder.error(e)
			uploaded = True
	if option_select == 'Choose a predefined dataset':
		option_select_data = st.selectbox("Select a dataset", options=['Airports','Cars'])
		dataset = SwitchExample(option_select_data)

		

	#dataset = load_df()
if not dataset.empty :
	options = get_columns(dataset)
	columns = options
	uploaded = True

if uploaded and not dataset.empty:
	check_select = st.sidebar.checkbox('Do you want to select columns?')
	if check_select:
		columns = st.sidebar.multiselect("Select Columns", options=options, default=options)

	check_pr = st.sidebar.checkbox('Show Profile Report')
	if check_pr:
		pr = generate_profile_report(dataset[columns])
		st_profile_report(pr)
	else:
		dataset[columns]

	if st.button(label='Download data'):
		path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))
		download_data = dataset[columns]
		download_data.to_csv(path_to_download_folder+"/data-download.csv")
		with st.spinner('Downloading Data ...'):
			time.sleep(5)
		st.success("File downloaded!\nYou should find it in " + path_to_download_folder)
#	if st.button("Clear file list"):
#		static_store.clear()
#if uploaded:
#	if st.button(label='Upload new data'):
#		uploaded = False
#		dataset = pd.DataFrame()