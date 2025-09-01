import pandas as pd
import openpyxl
class DataFrameUtils:

    @staticmethod
    def dropna_rows_by_column(dataframe,header_name):
        return dataframe[dataframe[header_name].notna()]

    @staticmethod 
    def get_rows_have_nulls(dataframe,header_name):
        return dataframe[dataframe[header_name].isnull()]

    @staticmethod 
    def drop_rows_have_nulls(dataframe,header_name):
        return dataframe[dataframe[header_name].notnull()].reset_index(drop=True)

    @staticmethod
    def append_series_in_dataframe(dataframe,new_column,content):
        dataframe[new_column] = content
        return dataframe
    
    @staticmethod   
    def delete_series(dataframe,column_to_delete):
        return dataframe.drop(column_to_delete,axis = 1)
    
    @staticmethod
    def filter_content_by_column(dataframe,value_filter,header_name):
        return dataframe.loc[dataframe[header_name] == value_filter]
    
    @staticmethod
    def verify_if_have_nulls(df_series):
        return df_series.isnull().any()
    
    @staticmethod
    def replace_series(dataframe,header_name,original_value,new_value):
        dataframe[header_name] = dataframe[header_name].astype(str).str.replace(original_value,new_value) 
        return dataframe
            
    @staticmethod
    def concat_dataframes(dataframe_top,dataframe_down):
        return pd.concat([dataframe_top,dataframe_down],ignore_index=True)
    
    @staticmethod
    def xlookup(df_base,df_search,lookup_value,lookup_array,return_array,name_column):
        df_no_dups = df_search.drop_duplicates(subset = lookup_array)
        lookup_search = df_no_dups.set_index(lookup_array)[return_array].to_dict()
        df_base[name_column] = df_base[lookup_value].map(lookup_search) 
        return df_base
    
    @staticmethod
    def concat_series_with_separator(list_of_series,separator = None):
        quantity = len(list_of_series)
        if quantity == 2 and separator is not None:
            concat = list_of_series[0].astype(str).str.replace(r"\.0$", "", regex=True) + separator + list_of_series[1].astype(str).str.replace(r"\.0$", "", regex=True)
        else:
            concat = list_of_series[0].astype(str)
            for i in range(1,quantity):
                concat += list_of_series[i].astype(str)
        return concat
    
    @staticmethod
    def remove_duplicates_by_columns(dataframe,header_name):
        return dataframe.drop_duplicates(subset= header_name)
    
    @staticmethod
    def get_duplicates_by_column(dataframe,header_name):
        return dataframe[dataframe.duplicated(subset=header_name, keep=False)] 
    
    @staticmethod
    def get_duplicates_and_position(dataframe,column_name):
        duplicates =  dataframe[dataframe.duplicated(subset=column_name,keep = False)]
        duplicates_index = duplicates.index.tolist()
        return duplicates,duplicates_index
    
    @staticmethod
    def textjoin_unique(serie, separator = ","):
        return separator.join(serie.dropna().astype(str).unique())
    
    @staticmethod
    def remove_values_from_column(dataframe,column_search,series_to_remove):
        dataframe = dataframe[~dataframe[column_search].isin(series_to_remove)]
        return dataframe
    
    @staticmethod
    def find_and_replace(dataframe,condition_column,value_condition,destiny_column,destiny_value):
        dataframe.loc[dataframe[condition_column] == value_condition,destiny_column] = destiny_value
        return dataframe
    
    @staticmethod
    def get_rows_by_index(dataframe,interval_rows):
        return dataframe.iloc[interval_rows]
    
    @staticmethod
    def drop_rows(dataframe,interval_rows):
        dataframe = dataframe.reset_index(drop = True)
        return dataframe.drop(interval_rows)
    
    @staticmethod
    def save_dataframe(dataframe,full_path,sheet_name):
        app_version = "SOE - v1.2.0"
        if app_version not in dataframe.columns:
            dataframe.insert(0,"SOE - v1.2.0","")
        with pd.ExcelWriter(full_path,engine='xlsxwriter') as writer:
            dataframe.to_excel(writer,sheet_name =sheet_name, index= False)

    @staticmethod
    def save_multiple_dataframes(dataframes,full_path,sheet_names):
        app_version = "SOE - v1.2.0"
        with pd.ExcelWriter(full_path,engine='xlsxwriter') as writer:
            for df,sheet in zip(dataframes,sheet_names):
                if app_version not in df.columns:
                    df.insert(0,"SOE - v1.2.0","")
                df.to_excel(writer,sheet_name =sheet, index= False)
        