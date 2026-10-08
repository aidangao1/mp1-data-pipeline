# MP1 Data Pipeline

A configurable command-line pipeline that loads a data file, validates it, cleans it,
and saves the result as a CSV.

## How data moves through it

The pipeline runs in five stages. First it validates that the input and config file
paths exist. It then loads the data file into a pandas DataFrame and the YAML config
into a dictionary. Next it validates the DataFrame, dropping rows whose numeric columns
contain invalid values and converting those columns to a numeric type. The validated
data is then processed: duplicates removed, rows or columns with missing values dropped,
and outliers removed from the configured numeric columns. Finally the cleaned DataFrame
is saved to the output path.

## Project organization

`pipeline.py` sits at the root and coordinates the workflow. The modules live in `src/`:

- `utils.py` — configures logging and checks that a given file path exists
- `data_loaders.py` — loads a file into a Python object based on its extension: CSV into
  a pandas DataFrame, JSON and YAML into dictionaries
- `data_validator.py` — checks that all required columns are present, drops rows with
  invalid values in numeric columns, and converts those columns to a numeric type
- `data_processor.py` — removes duplicates, handles missing values, and removes outliers,
  in that order, according to the settings in the config
- `data_output.py` — creates the output directory if it does not exist and writes the
  DataFrame to CSV without the index

Column names and processing settings live in `config/config.yaml` rather than in the
modules, so the pipeline can be run against a different dataset by editing the config
instead of the code.

## Example

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:

```text
12:20:26 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv, config=config/config.yaml
12:20:26 INFO     src.utils — Input file validated: fixtures/sample_data.csv
12:20:26 INFO     src.utils — Input file validated: config/config.yaml
12:20:26 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
12:20:26 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
12:20:26 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
12:20:26 DEBUG    src.data_validator — Validation: 100 -> 98 rows
12:20:26 INFO     __main__ — Validation complete: 100 -> 98 rows
12:20:26 DEBUG    src.data_processor — remove_duplicates: 98 → 96 rows
12:20:26 DEBUG    src.data_processor — handle_missing: 96 → 94 rows
12:20:26 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, lower=43.625, upper=106.625, removed=2
12:20:26 INFO     __main__ — Processing complete: 98 → 92 rows
12:20:26 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
12:20:26 INFO     __main__ — Saved cleaned data to output/clean.csv
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}

```