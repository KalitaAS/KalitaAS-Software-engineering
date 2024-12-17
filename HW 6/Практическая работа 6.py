import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

data_path = '/kaggle/input/transactions-fraud-datasets/cards_data.csv'
data = pd.read_csv(data_path)

# 2. Анализ объема памяти
# a. Объем памяти файла на диске
file_size = os.path.getsize(data_path) / (1024 ** 2) 
print(f"Объем памяти файла на диске: {file_size:.2f} МБ")

# b. Объем памяти набора данных в оперативной памяти
memory_usage = data.memory_usage(deep=True).sum() / (1024 ** 2)  # В МБ
print(f"Объем памяти набора данных в оперативной памяти до оптимизации: {memory_usage:.2f} МБ")

# c. Информация по колонкам
columns_stats = []
for col in data.columns:
    col_mem = data[col].memory_usage(deep=True)
    col_percentage = (col_mem / memory_usage * (1024 ** 2)) * 100
    col_dtype = data[col].dtype
    columns_stats.append({
        'column': col,
        'memory_usage_bytes': col_mem,
        'memory_percentage': col_percentage,
        'dtype': str(col_dtype)
    })

# 3. Сортировка по занимаемому объему памяти
columns_stats_sorted = sorted(columns_stats, key=lambda x: x['memory_usage_bytes'], reverse=True)

with open('columns_stats_no_optimization.json', 'w') as f:
    json.dump(columns_stats_sorted, f, indent=4)

# 4. Преобразование колонок "object" в категориальные
for col in data.select_dtypes(include=['object']).columns:
    unique_count = data[col].nunique()
    total_count = len(data[col])
    if unique_count / total_count < 0.5:
        data[col] = data[col].astype('category')

# 5. Понижающее преобразование типов "int"
int_cols = data.select_dtypes(include=['int']).columns
for col in int_cols:
    data[col] = pd.to_numeric(data[col], downcast='integer')

# 6. Понижающее преобразование типов "float"
float_cols = data.select_dtypes(include=['float']).columns
for col in float_cols:
    data[col] = pd.to_numeric(data[col], downcast='float')

# 7. 
memory_usage_optimized = data.memory_usage(deep=True).sum() / (1024 ** 2)
print(f"Объем памяти набора данных в оперативной памяти после оптимизации: {memory_usage_optimized:.2f} МБ\n")
columns_stats_optimized = []
for col in data.columns:
    col_mem = data[col].memory_usage(deep=True)
    col_percentage = (col_mem / memory_usage_optimized * (1024 ** 2)) * 100
    col_dtype = data[col].dtype
    columns_stats_optimized.append({
        'column': col,
        'memory_usage_bytes': col_mem,
        'memory_percentage': col_percentage,
        'dtype': str(col_dtype)
    })

with open('columns_stats_optimized.json', 'w') as f:
    json.dump(columns_stats_optimized, f, indent=4)


# 8. 
selected_columns = ['id', 'client_id', 'card_brand', 'card_type', 'has_chip',
                    'num_cards_issued', 'credit_limit', 'acct_open_date', 'year_pin_last_changed', 'card_on_dark_web']
data_chunks = pd.read_csv(data_path, usecols=selected_columns, chunksize=1000)

output_file = 'optimized_subset.csv'
with open(output_file, 'w') as f:
    for chunk in data_chunks:
        chunk.to_csv(f, index=False, header=f.tell()==0)

# 9. 
optimized_data = pd.read_csv(output_file)

# Линейный график
plt.figure(figsize=(10, 5))
optimized_data['num_cards_issued'].value_counts().sort_index().plot(kind='line')
plt.title('Number of Cards Issued Over Time')
plt.xlabel('Number of Cards Issued')
plt.ylabel('Count')
plt.show()

# Столбчатый график
plt.figure(figsize=(10, 5))
optimized_data['card_brand'].value_counts().plot(kind='bar')
plt.title('Distribution of Card Brands')
plt.xlabel('Card Brand')
plt.ylabel('Count')
plt.show()

# Круговая диаграмма
plt.figure(figsize=(8, 8))
optimized_data['card_type'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Card Type Distribution')
plt.ylabel('')
plt.show()

# Корреляция
correlation_matrix = optimized_data.corr(numeric_only=True)
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Точечный график
plt.figure(figsize=(10, 6))
plt.scatter(optimized_data.index, 
            optimized_data['credit_limit'].str.replace('$', '').str.replace(',', '').astype(float),
            alpha=0.6, color='purple')
plt.title('Credit Limits Scatter Plot')
plt.xlabel('Index')
plt.ylabel('Credit Limit')
plt.show()
