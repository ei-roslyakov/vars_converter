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

and will generate output in different formats:

- YAML
- INI (configuration file)
- plain text key value

Command line arguments supported:

```
$ python converter.py --help
2020-09-14 15:16:30,581 [root @ PID:4456 (main:157)] - DEBUG - Application started
usage: converter.py [-h] --input INPUT --output OUTPUT [--root-key ROOT_KEY]
                    [--output-format {yaml,config,txt}]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Input file path
  --output OUTPUT       Output file path
  --root-key ROOT_KEY   Root key in output file
  --output-format {yaml,config,txt}
                        Output format
```

## Requirements

To run converter you need Python with version at least 3.6 (f-strings and typing required)

## Installation

To install all packages please run (you may use this in virtual environment):

```shell
pip install -r requirements.txt
```

On Linux you need to use `pip3` instead of `pip`

## Usage and supported output formats

### YAML format support

To use this format please specify `--output-format yaml` in command line

Supports output in formats like:

```yaml
BEENV: production
CDN_HOST: example.com
DATABASE_HOST: .db.example.com
DATABASE_NAME: example
DATABASE_PORT: '5432'
```

or with prefix key (can be specified using `--root-key my_entry`)

```yaml
my_entry:
  BEENV: production
  CDN_HOST: example.com
  DATABASE_HOST: .db.example.com
  DATABASE_NAME: example
  DATABASE_PORT: '5432'
```

loading data from key `config.data` from input file.

Command line example:

```
python converter.py --input ./data/input_helm_vars.yaml --output ./data/output_with_prefix.yaml --root-key my_entry --output-format yaml
```

Or:

```
python converter.py --input ./data/input_helm_vars.yaml --output ./data/output_flat_yaml.yaml --output-format yaml
```

### Ini file (configuration file with sections)

To use this format please specify ` --output-format config` in command line.

**Warning:** to use this format you need to specify section
name using `--root-key my_entry`.

As output converter will generate data like:

```ini
[my_entry]
beenv = production
cdn_host = example.com
database_host = .db.example.com
database_name = example
database_port = 5432
```

Command line example:

```shell
python converter.py --input ./data/input_helm_vars.yaml --output ./data/output_as_ini.ini --root-key my_entry --output-format config
```

### Plain text format

To use this format please specify ` --output-format kv` in command line.

**Warning:** this output format will not support root key.

Using this format converter will generate output like:

```
BEENV=production
CDN_HOST=example.com
DATABASE_HOST=.db.example.com
DATABASE_NAME=example
DATABASE_PORT=5432
```

Command line example:

```
python converter.py --input ./data/input_helm_vars.yaml --output ./data/output_as_raw_kv.txt --output-format kv
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
