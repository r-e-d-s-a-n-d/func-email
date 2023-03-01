## Testing

Install required libraries

```
  $ pip install -r requirements.txt
```

Update client_secret and add default value from keyvault. This is a temporary, only for testing. Located in src\email_alerts\send_mail.py

```
  client_secret = os.getenv("clientSecret", "***")
```

Run test

```
  $ python .\src\email_alerts\send_mail.py
```

## Requirements

- The [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) version 2.0.76 or later.
- [Azure Function Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=linux%2Ccsharp%2Cbash#v2) version 3.0 or later.
- The [conda package manager](https://docs.conda.io/en/latest/) for Python.  Recommend starting with the [Miniconda](https://docs.conda.io/en/latest/miniconda.html) distribution.
- VS Code - when combined with the Azure Tools extension, makes working with Azure functions easier.
- Docker - for building the function into a docker container
- Make [optional] - a utility for orchestrating shell commands (can be run manually instead if desired -- see the [`Makefile`](Makefile))
