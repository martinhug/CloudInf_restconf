# CloudInf Restconf Lab
This python script provides the functionality to automatically configure a network router. 
The script configures the Interfaces, OSPF settings and BGP settings.

## Prerequirements & installation
- Python > 3.6
- pip
- any text editor or IDE
- Jinja2
- we recommend to use virtual environments [Documentation](https://docs.python.org/3/library/venv.html)
- Install the required libraries by running the command `pip install -r requirements.txt`

## Usage
Start the program:
`python restconf_configurator.py`

## Jinja & YAML
To configure the router, we use Yaml files to provide the individual parameters for the config. The script creates XML templates with jinja, which are used to upload to the router.

## File responsibility

