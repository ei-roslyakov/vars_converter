# Vars converter

Converter ConfigMap values for Helm to Docker like vars file.

This converted will process file with format like:

```yaml
config:
  data:
    - key: BEENV
      value: "production"
    - key: CDN_HOST
      value: "example.com"
    - key: DATABASE_HOST
      value: ".db.example.com"
    - key: DATABASE_NAME
      value: "example"
    - key: DATABASE_PORT
      value: "5432"
```

and will generate output in formats:

```yaml
BEENV: production
CDN_HOST: example.com
DATABASE_HOST: .db.example.com
DATABASE_NAME: example
DATABASE_PORT: '5432'
```

or with prefix key

```yaml
my_entry:
  BEENV: production
  CDN_HOST: example.com
  DATABASE_HOST: .db.example.com
  DATABASE_NAME: example
  DATABASE_PORT: '5432'
```

loading data from key `config.data` from input file.

## Requirements

To run converter you need Python with version at least 3.6 (f-strings and typing required)

## Installation

To install all packages please run (you may use this in virtual environment):

```shell
pip install -r requirements.txt
```

On Linux you need to use `pip3` instead of `pip`

## Usage

To convert file `./data/input_helm_vars.yaml` and save results
into `./data/output_vars.yaml` please use command line like:

```shell
python converter.py --input ./data/input_helm_vars.yaml --output ./data/output_vars.yaml
```

On Linux OS you may want to use `python3` instead of just `python`

If you want to have output with prefix like:

```yaml
my_entry:
  BEENV: production
  CDN_HOST: example.com
  DATABASE_HOST: .db.example.com
```

you need to execute:

```
python converter.py --input ./data/input_helm_vars.yaml --output ./data/output_with_prefix.yaml --root-key my_entry
```

## Development

To install all required packages please run:

```shell
pip install -r requirements-dev.txt
```

To run linter `flake8` just execute command:

```shell
flake8
```

Enjoy!
