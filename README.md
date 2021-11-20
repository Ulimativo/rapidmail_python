# rapidmail-api 
## Python Module for the Newsletter Tool
-----

Rapidmail Api is a Python library for dealing with the [Rapidmail](https://www.rapidmail.de) Newsletter Tool API.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install rapidmail-api.

```bash
pip install rapidmail-api
```

## Configuration

rapidmail-api expects an .env file with two variables, and uses dotenv to read the file:
- RAPIDMAIL_USERNAME
- RAPIDMAIL_PASSWORD

## Usage

```python
import rapidmail

# returns infos on all recipientlists
print(rapidmail.Recipientlists())
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

