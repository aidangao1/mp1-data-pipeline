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
(paste your terminal output here)
```