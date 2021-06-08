import os 
import pandas as pd
import numpy as np

#the melt() function reshapes the time series models to more appriopate format
def read_and_melt(filename, covid_type):
    #read in the csv 
    covid_cases = pd.read_csv(filename)
    covid_cases = pd.melt(covid_cases, id_vars=covid_cases.columns[:4], 
                    value_vars = covid_cases.columns[4:], 
                    var_name = 'date', 
                    value_name = covid_type)
    return covid_cases


#sums all the values for a specifed column based on a certain column values. 
def summarise_country_by_date(covid_cases, column, row_value, column_grouped, column_name):
    return covid_cases[covid_cases[column] == row_value].groupby(column_grouped).sum()[[column_name]]

#extracts the entire dataframe except the last column 
def extract_tables(covid_cases, column, row_value):
    recoveries = covid_cases[covid_cases[column] == row_value]
    return recoveries[recoveries.columns[:-1]].reset_index(drop=True)

#merge two dataframes together based on a certain column, row values. 
def merge_columns(covid_case_from, covid_case_to, method, matching_with, index):
    return covid_case_from.merge(covid_case_to, how=method, left_on=matching_with, right_index=index)

#mergeing two dataframes togther 
def merge_cases(covid_case_from, covid_case_to, how, on = []):
    return covid_case_from.merge(right = covid_case_to, how = how, on = on)

def covid_template(confirmed, deaths, recovered):
    #extracts canada's covid cases from each .csv file, skips all other countries and returns the total 
    #number of covid cases for each date. 
    confirmed_canada = summarise_country_by_date(confirmed, 'Country/Region', 'Canada', 'date', 'confirmed')
    deaths_canada = summarise_country_by_date(deaths, 'Country/Region', 'Canada', 'date', 'deaths')
    
    #Returns all the columns expect the confirmed cases column - this is used as a template
    reovered_canada = extract_tables(recovered, 'Country/Region', 'Canada')
    
    #The template created in merges with the confirmed cases, and deaths cases. 
    canada = merge_columns(reovered_canada, confirmed_canada, 'inner', 'date', True)
    deaths_canada = merge_columns(reovered_canada, deaths_canada, 'inner', 'date', True)
    
    #remove the original data from the dataset, and append the new Canada's data
    confirmed = confirmed[confirmed['Country/Region'] != 'Canada'].append(canada)
    deaths = deaths[deaths['Country/Region'] != 'Canada'].append(deaths_canada)
    
    #merge together all three cases types into one dataframe.
    on = ['Province/State','Country/Region','Lat','Long','date']
    data = merge_cases(confirmed, deaths, 'left', on)
    data = merge_cases(data, recovered, 'left', on)

    return data

#replace the name of the row with the name you want 
def covid_data(dataset, columnName, replace_from = [], replace_to = []):
    return dataset[columnName].replace(replace_from, replace_to)

#drops entiers rows based on a certain index value
def drop_index(ds, cn, conm=[]):
    for i in conm:
        country_region_index = ds[ds[cn] == i].index
        ds = ds.drop(country_region_index)
    return ds 
    

#drop the entire column in the dataframe ecoli 
def drop_column(dataset, column_name):
    return dataset.drop(column_name, axis = 'columns')

#eliminate the entire row based on a certain value
def drop_row(covid_cases, column, target=[]):
    #looping through the list and skipping all the rows based on a certain row value in column
    for x in target:
        covid_cases = covid_cases[covid_cases[column] != x]
    return covid_cases

#creates the dimension table for Countries. The following code basically merges together the three dataframes to combiine the region, continent and country. 
def dimWorld(world_data_df, country_region):
    #selects the columns 'location' and 'continent' and assigns it to world_data_contienent
    world_data_continent = world_data_df[['location','continent']]
    #removes any duplicates, only require unique values
    world_data_continent = world_data_continent.drop_duplicates()
    #merges the world_data_continent with the country_region. 
    world_data_continent = pd.merge(world_data_continent, country_region, left_on=['location'], right_on = ['COUNTRY'],how = 'left')
    world_data_continent = drop_column(world_data_continent, 'COUNTRY')
    #assigns unique id for each row
    world_data_continent['Id']= world_data_continent.groupby('location').ngroup()+1
    #rearrange the columns - the unique id should be the first colimn 
    cols = world_data_continent.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    world_data_continent = world_data_continent[cols]
    #drops any duplicates in the dataframe with the same name/ 
    world_data_continent = world_data_continent.drop_duplicates(subset = ['location'])
    return  world_data_continent 
    
    #creates the dimension table for the time. 
    '''
        The algorithm converts the date into a datetime, then seperates out the date into four seperate columns:
        day, month, quarter and year. The dataframe only stores: month, quarter and year into the dimTime. 
    '''
def dimTime(cases_combined):
    cases_combined['date']= pd.to_datetime(cases_combined['date'])
    cases_combined['day'] = cases_combined['date'].dt.day
    cases_combined['month'] = cases_combined['date'].dt.month_name().str.slice(stop = 3)
    cases_combined['quarter'] = cases_combined['date'].dt.quarter
    cases_combined['quarter'] = 'Q' + cases_combined['quarter'].astype(str)
    cases_combined['year'] = cases_combined['date'].dt.year
    #drop all the columns except month, quarter and year, and return all the unique values for the group.  
    date_time=cases_combined.drop(cases_combined.columns[0:9], axis = 1).drop_duplicates()
    date_time_dataframe = pd.DataFrame(date_time)
    #Add a unique id for each row
    date_time_dataframe.insert(0, 'Id', range(1, 1 + len(date_time_dataframe)))
    return date_time_dataframe



#dimension table for lifeexpectancy 
def dimExpectancy():
    data_exp = {
    'expID':[1,2],
    'expectancy': ['<=75','>75' ]}
    exp_df = pd.DataFrame(data_exp, columns = ['expID','expectancy'])
    return exp_df

#dimension table for the size of the country. 
def dimSize():
    data_size = {
    'sizeID':[1,2,3],
    'size': ['small','medium','large' ]}
    size_df = pd.DataFrame(data_size , columns = ['sizeID','size'])
    return size_df 


'''
    the covid cases stores in the dataset are accumulative. We extract the data for last day of each month for the available data. 

'''

#dataframe for the facts table 
def factTable(world_data_continent, cases_combined, world_data_df, date_time):

    #drops all the columns we do not require as it will not aint us for further computation
    cases_combined =drop_column(cases_combined, 'Province/State')
    cases_combined = drop_column(cases_combined, 'Lat')
    cases_combined = drop_column(cases_combined, 'Long')
    cases_combined = drop_column(cases_combined, 'date')
    #extract the data based on the last day of each month in both 2020 and 2021
    new_cases_df = cases_combined[cases_combined['day'] ==  31]
    feb_date = cases_combined[(cases_combined['day'] ==  29) &(cases_combined['month'] ==  'Feb') &(cases_combined['year'] ==  2020)]
    feb_date_2021 = cases_combined[(cases_combined['day'] ==  28) &(cases_combined['month'] ==  'Feb') &(cases_combined['year'] ==  2021)]
    april_2020 = cases_combined[(cases_combined['day'] ==  30) &(cases_combined['month'] ==  'Apr')]
    june_2020 = cases_combined[(cases_combined['day'] ==  30) &(cases_combined['month'] ==  'Jun')]
    sep_2020 = cases_combined[(cases_combined['day'] ==  30) &(cases_combined['month'] ==  'Sep')]
    nov_2020 = cases_combined[(cases_combined['day'] ==  30) &(cases_combined['month'] ==  'Nov')]

    #append the data into the dataframe 
    facttable_time = pd.DataFrame(new_cases_df)
    facttable_time = facttable_time.append(feb_date)
    facttable_time = facttable_time.append(feb_date_2021)
    facttable_time = facttable_time.append(april_2020)
    facttable_time = facttable_time.append(june_2020)
    facttable_time = facttable_time.append(sep_2020)
    facttable_time = facttable_time.append(nov_2020)

    #returns the required columns
    world_data_expectancy = world_data_df[['location','population','life_expectancy']]
    #drops any duplicate in the country colimn
    world_data_expectancy = world_data_expectancy.drop_duplicates(subset = 'location')
    #rename 
    world_data_expectancy =world_data_expectancy.rename({"location":"Country/Region"}, axis=1)
    #merge data with the time dimension, this will assign the unique id for each available row in the time dim to the releven
    fact_table = facttable_time.merge(date_time, on =['month','quarter','year'])
    #drop the unwanted rows
    fact_table = drop_column(fact_table, 'day')
    fact_table = drop_column(fact_table, 'month')
    fact_table = drop_column(fact_table, 'quarter')
    fact_table = drop_column(fact_table, 'year')
    fact_table = fact_table.rename({"Id":"timeID"}, axis=1)
    #sum up the total number of confirmed, deaths and recovered based on a specific country/region and timeid
    fact_table =fact_table.groupby(['Country/Region','timeID']).sum(['confirmed','deaths','recovered']).reset_index()
    #rearrange the index for the timeID 
    cols = fact_table.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    fact_table= fact_table[cols]
    
    #merge the expectancy table 
    fact_table = world_data_expectancy.merge(fact_table, on = 'Country/Region')

    country_id = world_data_continent[['Id','location']]
    country_id = country_id .rename({"Id":"countryID","location":"Country/Region"}, axis=1)
    #merge the country table with the fact table
    fact_table = country_id.merge(fact_table, on='Country/Region')
    #select only the relevant feaures and leaving out columns such as Country/Region as we have stored it as a unique int in the fact table 
    fact_table = fact_table[['countryID','timeID','population','life_expectancy','confirmed','deaths','recovered']]
    return fact_table


def main():
    #read and melths the csv files
    confirmed = read_and_melt('time_series_covid19_confirmed_global.csv','confirmed')
    deaths = read_and_melt('time_series_covid19_deaths_global.csv','deaths')
    recovered = read_and_melt('time_series_covid19_recovered_global.csv','recovered')
    
    #template for covid cases with all three types
    cases_combined = covid_template(confirmed, deaths, recovered)

    #reads in the excel sheet, and returns the following columns: 'COUNTRY', 'REGION'
    world_data_df = pd.read_csv(f'owid-covid-data.csv')
    excel_data_df = pd.read_excel('acaps_covid19_government_measures_dataset.xlsx', sheet_name='Dataset', usecols = ['COUNTRY','REGION'])
    country_region = pd.DataFrame(excel_data_df).drop_duplicates()
    #rename the values in the columns to an appriopiate naming convention
    world_data_df['location'] = world_data_df['location'].replace(['Democratic Republic of Congo','Timor'],['Congo','Timor-Leste'])
    cases_combined['Country/Region'] =  cases_combined['Country/Region'].replace(['US','Burma','Korea, South', 'Holy See', 'West Bank and Gaza', 'Taiwan*', 'Congo (Brazzaville)', 'Congo (Kinshasa)','Cabo Verde'],
                                  ['United States','Myanmar','South Korea', 'Vatican', 'Israel','Taiwan', 'Congo', 'Congo','Cape Verde'])
    replace_from = ['Korea, Republic of','St. Vincent and the Grenadines','CAR','St. Lucia','St. Kitts and Nevis','DPRK','DRC', 'Czech Republic','Macedonia','Timor Leste','Palau','Nauru',"CÃ´te d'Ivoire"]
    replace_to = ['South Korea','Saint Vincent and the Grenadines','Central African Republic','Saint Lucia','Saint Kitts and Nevis','North Korea','Congo','Czechia','North Macedonia','Timor-Leste','Micronesia','Micronesia',"Cote d'Ivoire"]
    country_region['COUNTRY'] = country_region['COUNTRY'].replace(replace_from,replace_to)

    #remove the following countries from the dataset. 
    target_list = ['Tongo', 'Tuvalu','Kiribati', 'North Koreea']
    country_region  = drop_index(country_region,  'COUNTRY', target_list)
    #the gov dataset
    target_list_country_region = ['Tongo', 'Tuvalu','Palestine','Hong Kong','North Korea','Micronesia','Kiribati','Tonga','Kiribati', 'Turkmenistan']
    country_region = drop_row(country_region , 'COUNTRY', target_list_country_region)
    #world data 
    world_df_country_list = ['Taiwan','Vatican','Kosovo','Monaco','Andorra','World','International','Hong Kong','Palestine']
    world_data_df = drop_row(world_data_df , 'location', world_df_country_list)
    #covid template
    cases_combined_list_country = ['Diamond Princess','MS Zaandam','Taiwan','Kosovo','Vatican','Monaco','Andorra','MS Zaandam','Micronesia']
    cases_combined = drop_row(cases_combined , 'Country/Region', cases_combined_list_country)
    cases_combined_list_state = ['Diamond Princess']
    cases_combined = drop_row(cases_combined , 'Province/State', cases_combined_list_state)
    
    #creates the .csv file for country
    world_data_continent = dimWorld(world_data_df, country_region)
    #creates the .csv file for time
    date_time_dataframe = dimTime(cases_combined)
    #creates the .csv file for expectancy
    expectancy = dimExpectancy()
    #creates the .csv file for size
    size_df = dimSize()
    #builts the facts table model 
    fact_table = factTable(world_data_continent, cases_combined, world_data_df, date_time_dataframe)
    fact_table = fact_table.sort_values(by =['countryID', 'timeID'], ascending=[True, True])

    #Output the dataframes to the respective files 
    world_data_continent.to_csv('./dimCountry.csv', index = False, header = False)
    size_df.to_csv('./dimSize.csv', index = False, header = False)
    expectancy.to_csv('./dimExpectancy.csv', index = False, header = False)
    date_time_dataframe .to_csv('./dimTime.csv', index = False, header = False)
    fact_table.to_csv('./FactTable.csv', index = False, header = False)

main()