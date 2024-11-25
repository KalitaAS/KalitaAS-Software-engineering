import pandas as pd
import json
import os
import msgpack

movies = pd.read_csv("./HW2 V8/movies_small_df.csv")

selected_columns = ["Movie", "Year", "Ratings", "Gross", "Budget", "Screens", "Likes"]
data = movies[selected_columns]

numeric_columns = ["Year", "Ratings", "Gross", "Budget", "Screens", "Likes"]
statistics = {}
for column in numeric_columns:
    stats = {
        "max": float(data[column].max()),
        "min": float(data[column].min()),
        "mean": float(data[column].mean()),
        "sum": float(data[column].sum()),
        "std_dev": float(data[column].std())
    }
    statistics[column] = stats

text_frequencies = data["Movie"].value_counts().to_dict()

with open("fifth_task.json", "w") as f:
    json.dump({"numeric_statistics": statistics, "text_frequencies": text_frequencies}, f, indent=4)

output_formats = {
    "csv": "movies_selected.csv",
    "json": "movies_selected.json",
    "msgpack": "movies_selected.msgpack",
    "pkl": "movies_selected.pkl"
}

data.to_csv(output_formats["csv"], index=False)
data.to_json(output_formats["json"], orient="records", lines=True)
data.to_pickle(output_formats["pkl"])

with open(output_formats["msgpack"], "wb") as f:
       f.write(msgpack.packb(data.to_dict(orient="records")))

file_sizes = {}
for fmt, filename in output_formats.items():
    file_sizes[fmt] = os.path.getsize(filename)

print("File sizes (in bytes):")
for fmt, size in file_sizes.items():
    print(f"{fmt}: {size}")

