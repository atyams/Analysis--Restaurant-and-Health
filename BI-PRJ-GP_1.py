# Import the requireds python Libraries
import json
import pandas as pd
import numpy as np

#File read from system path

path = '/Users/atyam/Desktop/Business Intelligence/BI-Project/'

#variables needed for ease of file access
file1 = 'business.json'
file2 = 'business.csv'
file3 = '500_Cities__Local_Data_for_Better_Health__2018_release.csv'
file4 = '500_Cities__City-level_Data__GIS_Friendly_Format___2018_release.csv'
file5 = 'bi_proj_grp1.csv'


                                                ###############################################################################
                                                #                                Business file                                #
                                                ###############################################################################





###############################################################################
#          Data Frame & Data Preparation Process - Business file             #
###############################################################################

#Open the file and read each line in the json document and using map function right strip each word in the line and convert to string.
#Use pd.read_json to convert to dataframe.
with open(path + file1, 'r', encoding="utf8") as f:
    data_bus = f.readlines()
data_bus = map(lambda x: x.rstrip(), data_bus)
data_bus_json_str = "[" + ','.join(data_bus)+ "]"
data_bus = pd.read_json(data_bus_json_str)

#Load the dataframe to csv file.
data_bus.to_csv(path + file2)

#Read the pulled data as dataframe using read_csv of the file 2 for data cleaning and analysis
df_bus = pd.read_csv(path + file2)
#Find number of columns
df_bus.columns
#Identify the number of rows in each column to identify the missing values. It is understood that few columns has NUll values.
df_bus.count()

###############################################################################
#          Data Cleaning Process - Business file                             #
###############################################################################

#Filter the rows of the city which are not NULL for our analysis.
df_bus = df_bus[pd.notnull(df_bus['city'])]

#Now perform match string for the categories to filter the data for restaurants specific for data analysis.
df_bus = df_bus[df_bus['categories'].str.match('Restaurants', na = False)]

# Use count to identify no.of available data rows in each column
df_bus.count()

#Since we found some NULL values in the attributes column fill it with others, it is a Character
df_bus = df_bus.fillna({ 'attributes':'others'})

###############################################################################
#          Data Frame Created - Business File                                     #
###############################################################################

# Now Create the final dataframe of the business file with required columns and sort the values by State and City in ascending order
df_bus = df_bus[['attributes','categories','name','is_open','city', 'state', 'latitude','longitude','review_count', 'stars']].sort_values(by = ['state','city'], ascending = True)



                                        ###############################################################################
                                        #                                500_Health file                              #
                                        ###############################################################################




##############################################################################
#    Data Frame & Data Preparation Process - 500_Cities-Health file           #
###############################################################################

#Read the csv file and create the dataframe
df_health = pd.read_csv(path + file3)

#Similarly to the previous process, filter the NULL data by City Column. Because this will be one of the key for merging different files.
df_health = df_health[pd.notnull(df_health['CityName'])]

#Preview few rows of the dataframe.
df_health.head()

# Use count to identify no.of available data rows in each column
df_health.count()

#Now sort the values in ascending order based on CityName and other columns. Similarly to the previous file
df_health = df_health.sort_values(by = ['StateAbbr','CityName','MeasureId'], ascending = True)

###############################################################################
#          Data Cleaning Process - 500_Cities-Health file                     #
###############################################################################

#Now find the duplicates in the data and use keep = first argument, to keep one original row and remove other repeated rows of the original one. Found duplicates
df_health = df_health[df_health.duplicated(['StateAbbr','CityName','MeasureId'], keep = 'first')]

#Remove the duplicate values from the dataframe.
df_health.drop_duplicates(subset = ['StateAbbr','CityName', 'MeasureId'], keep = 'first', inplace = True)

#Analyze the whole dataframe for miss match values
df_health

#Geogrpahiclevel coulmn has missmatch data. Clean the data by assigning the City for all the rows.
df_health = df_health[df_health['GeographicLevel'] == 'City']

# Use count to identify no.of available data rows in each column
df_health.count()

#Drop the unecessary columns in the dataframe.
df_health = df_health.drop(['Data_Value_Footnote_Symbol', 'Data_Value_Footnote','TractFIPS'], axis=1)

# Use count to identify no.of available data rows in each column
df_health.count()

#Now the second file dataframe is ready for further analysis.




                                                    ###############################################################################
                                                    #                                500_City Level file                          #
                                                    ###############################################################################



##############################################################################
#    Data Frame & Data Preparation Process - 500_City Level file           #
###############################################################################

#Read the csv file and create the dataframe
df_gis = pd.read_csv(path + file4)

#Identify number of columns
df_gis.columns

# Use count to identify no.of available data rows in each columns
df_gis.count()

#Further data cleaning process will be performed after merging three files.


                                                    ##############################################################################
                                                    #    Data Integration process- Business- Health- City Level files           #
                                                    ###############################################################################

#FIRST MERGE
# Perform Inner Join with Health dataframe and City Level dataframe(gis) using FIPS key.
df_fst = df_health.merge(df_gis, how='inner', left_on=['CityFIPS'], right_on=['PlaceFIPS'])

#Preview the few rows of the merged file.
df_fst.head()

# Use count to identify no.of available data rows in each colums
df_fst.count()


#SECOND MERGE

# Perform Inner Join with business dataframe and first merged dataframe using State and City key.
df_rest = df_bus.merge(df_fst, how='inner', left_on=['state','city'], right_on=['StateAbbr_y','CityName'])

#Preview the few rows of the merged file.
#df_rest.head(1)

# Use count to identify no.of available data rows in each colums
df_rest.count()


###############################################################################
#          Data Cleaning Process - Restaurant Merged file                    #
###############################################################################

#Check what columns to be removed: verify MeasureId column
df_rest['MeasureId'].unique()
df_rest.columns

#Drop the uncessary columns from the datatframe.
df_rest = df_rest.drop(columns=['StateAbbr_x','Low_Confidence_Limit','High_Confidence_Limit','ACCESS2_CrudePrev','ACCESS2_Crude95CI',
                                'ACCESS2_AdjPrev','ACCESS2_Adj95CI','ARTHRITIS_Crude95CI','ARTHRITIS_AdjPrev','ARTHRITIS_Adj95CI','BINGE_CrudePrev',
                                'BINGE_Crude95CI','BINGE_AdjPrev','BINGE_Adj95CI','BPHIGH_Crude95CI','BPHIGH_AdjPrev',
                                'BPHIGH_Adj95CI','BPMED_Crude95CI','BPMED_AdjPrev','BPMED_Adj95CI','CANCER_Crude95CI',
                                'CANCER_AdjPrev','CANCER_Adj95CI','CASTHMA_Crude95CI','CASTHMA_AdjPrev','CASTHMA_Adj95CI',
                                'CHD_CrudePrev','CHD_Crude95CI','CHD_AdjPrev','CHD_Adj95CI','CHECKUP_CrudePrev','CHECKUP_Crude95CI',
                                'CHECKUP_AdjPrev','CHECKUP_Adj95CI','CHOLSCREEN_CrudePrev','CHOLSCREEN_Crude95CI','CHOLSCREEN_AdjPrev',
                                'CHOLSCREEN_Adj95CI','COLON_SCREEN_CrudePrev','COLON_SCREEN_Crude95CI','COLON_SCREEN_AdjPrev',
                                'COLON_SCREEN_Adj95CI','COPD_CrudePrev','COPD_Crude95CI','COPD_AdjPrev','COPD_Adj95CI',
                                'COREM_CrudePrev','COREM_Crude95CI','COREM_AdjPrev','COREM_Adj95CI','COREW_CrudePrev','COREW_Crude95CI',
                                'COREW_AdjPrev','COREW_Adj95CI','CSMOKING_CrudePrev','CSMOKING_Crude95CI','CSMOKING_AdjPrev',
                                'CSMOKING_Adj95CI','DENTAL_CrudePrev','DENTAL_Crude95CI','DENTAL_AdjPrev','DENTAL_Adj95CI',
                                'DIABETES_Crude95CI','DIABETES_AdjPrev','DIABETES_Adj95CI','HIGHCHOL_Crude95CI','HIGHCHOL_AdjPrev',
                                'HIGHCHOL_Adj95CI','KIDNEY_CrudePrev','KIDNEY_Crude95CI','KIDNEY_AdjPrev','KIDNEY_Adj95CI','LPA_CrudePrev',
                                'LPA_Crude95CI','LPA_AdjPrev','LPA_Adj95CI','MAMMOUSE_CrudePrev','MAMMOUSE_Crude95CI','MAMMOUSE_AdjPrev',
                                'MAMMOUSE_Adj95CI','MHLTH_CrudePrev','MHLTH_Crude95CI','MHLTH_AdjPrev','MHLTH_Adj95CI','OBESITY_Crude95CI',
                                'OBESITY_AdjPrev','OBESITY_Adj95CI','PAPTEST_CrudePrev','PAPTEST_Crude95CI','PAPTEST_AdjPrev',
                                'PAPTEST_Adj95CI','PHLTH_CrudePrev','PHLTH_Crude95CI','PHLTH_AdjPrev','PHLTH_Adj95CI','SLEEP_CrudePrev',
                                'SLEEP_Crude95CI','SLEEP_AdjPrev','SLEEP_Adj95CI','STROKE_CrudePrev','STROKE_Crude95CI','STROKE_AdjPrev',
                                'STROKE_Adj95CI','TEETHLOST_CrudePrev','TEETHLOST_Crude95CI','TEETHLOST_AdjPrev','TEETHLOST_Adj95CI','Geolocation'])

#Drop the unnamed column from the dataframe, because index is already created.
df_rest = df_rest.drop(df_rest.columns[0], axis=1)

#Perform to count the number of rows in each columns
df_rest.count()

#Found one column less count. Find it
df_rest['Data_Value'].isna().values.any()

#find the datatype
df_rest.dtypes

#Fill the missing values with median
df_rest['Data_Value'] = df_rest['Data_Value'].fillna(df_rest.groupby('Data_Value_Type')['Data_Value'].transform('median'))

#Perform to count the number of rows in each columns
df_rest.count()

#Check whether there are any null values.
df_rest['Data_Value'].isna().values.any()

#Load the file to CSV for analysis in Tableau.
df_rest.to_csv(path + file5)
