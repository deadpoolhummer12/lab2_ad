import pandas as pd
import os
import re

folder_path = "csv_data_test"
province_ids = [22, 24, 23, 25, 3, 4, 8, 19, 20, 21, 9, 26, 10, 11, 12, 13, 14, 15, 16, 27, 17, 18, 6, 1, 2, 7, 5]

dfs = []

def get_file_number(filename):
    match = re.search(r"VHI(\d+)_", filename)
    if match:
        return int(match.group(1))
    else:
        return 0

for filename in sorted(os.listdir(folder_path), key=get_file_number):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and filename.endswith('.csv'):
        with open(file_path, 'r') as f:
            first_line = f.readline().strip()
            match = re.search('Province= (\d+): (.+),', first_line)
            if match:
                province_id = province_ids[int(match.group(1))-1]
                province_name = match.group(2)
                #print(f"File: {filename}, Province: {province_id}, Name: {province_name}")

                # adding indexes of province
                df = pd.read_csv(file_path, index_col=False, header=1)
                df["province"] = province_id

                #data clearing
                df = df.rename(columns={" VHI<br>": "VHI"})
                df = df.rename(columns={" SMN": "SMN"})
                df["year"].replace({"<tt><pre>1982": "1982"}, inplace=True) 
                df = df.drop(df.loc[df['VHI'] == -1].index)
                df = df.drop(2184)
                
                dfs.append(df)
            else:
                print(f"No province found in file {filename}")
    else:
        print(f"Ignoring non-csv file {filename}")

merged_df = pd.concat(dfs, ignore_index=True)
print(f"Увесь об'єднаний датафрейм: \n {merged_df}")
dnipro = merged_df[merged_df['province'] == 3]
print(f"\nДемонстрація, що все об'єднано правильно:\n---Зробимо вибірку тільки з Дніпропетровщини: \n{dnipro}")

# в нас була проблема у типі даних, тому виводився пустий датафрейм. 
# щоб це виправити - перевіремо тип даних
# print(f"\n Типи даних у стовпцях: \n {merged_df.dtypes}")
# переведемо дані у числа. тепер все працює

# merged_df['year'] = pd.to_numeric(merged_df['year'], errors='coerce')
# merged_df['week'] = pd.to_numeric(merged_df['week'], errors='coerce')
# merged_df['province'] = pd.to_numeric(merged_df['province'], errors='coerce')

columns_to_convert = ['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'province']

for column in columns_to_convert:
    merged_df[column] = pd.to_numeric(merged_df[column], errors='coerce')


selected_records = merged_df[(merged_df['year'] == 2000) & (merged_df['week'] == 19)]
print("\nЗапис за умовою: \n", selected_records)

# знаходженння екстремумів
import pandas as pd

def find_extrema(province_id, year):
    selected_records = merged_df[(merged_df['province'] == province_id) & (merged_df['year'] == year)]

    if selected_records.empty:
        raise ValueError(f"No records found for province {province_id} and year {year}")

    min_vhi = selected_records['VHI'].min()
    max_vhi = selected_records['VHI'].max()
    return min_vhi, max_vhi

def get_drought_years(province_id, percent):
    """Get years with extreme and mild droughts affecting more than the specified percentage of the province"""
    extreme_drought_years = []
    mild_drought_years = []

    for year in merged_df['year'].unique():
        province_records = merged_df[(merged_df['province'] == province_id) & (merged_df['year'] == year)]
        total_records = len(province_records)

        extreme_drought_records = province_records[province_records['VHI'] < 35]
        extreme_percentage = (len(extreme_drought_records) / total_records) * 100

        mild_drought_records = province_records[province_records['VHI'] > 60]
        mild_percentage = (len(mild_drought_records) / total_records) * 100

        if extreme_percentage >= percent:
            extreme_drought_years.append(year)

        if mild_percentage >= percent:
            mild_drought_years.append(year)

    return extreme_drought_years, mild_drought_years

def main():

    province_id = int(input("Enter province ID: "))
    year = int(input("Enter year: "))
    percent = float(input("Enter %: "))
    try:
        min_vhi, max_vhi = find_extrema(province_id, year)
        extreme_drought_years, mild_drought_years = get_drought_years(province_id, percent)
        print("Minimum VHI:", min_vhi)
        print("Maximum VHI:", max_vhi)
        print(f"Years with extreme droughts of province {province_id}:\n {extreme_drought_years} ")
        print(f"\nYears with mild droughts of province {province_id}:\n {mild_drought_years}")
    except ValueError as e:
        print(str(e))

if __name__ == "__main__":
    main()