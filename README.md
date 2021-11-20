# rapidmail-api 
## Python Module for the Newsletter Tool Rapidmail
-----

**rapidmail-api** is a Python library for dealing with the [Rapidmail](https://www.rapidmail.de) Newsletter Tool API.  

***Disclaimer***:  
This project is in no way affiliated with Rapidmail despite myself being a user of the tool.     

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install rapidmail-api.

```bash
pip install rapidmail-api
```

## Configuration

rapidmail-api expects an .env file with two variables, and uses dotenv to read the file:
- RAPIDMAIL_USERNAME
- RAPIDMAIL_PASSWORD

You need to sign-up for Rapidmail and generate an API user to access the API. 
Website: [https://www.rapidmail.de/](https://www.rapidmail.de/)

## Usage

```python
import rapidmail

# returns infos on all recipientlists
print(rapidmail.Recipientlists())
```

## API Documentation
The Rapidmail API documentation can be found on their developers website:
[https://developer.rapidmail.wiki](https://developer.rapidmail.wiki)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

