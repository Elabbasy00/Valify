# Secret Sharing

TDLR;

I assumed that the volume of data to be encrypted would be larger than what asymmetric encryption technology could accommodate, so I decided to work on double encryption. However, asymmetric encryption is rather slow. You decide to encrypt the data with symmetric encryption, and then encrypt this key with asymmetric encryption.
Gains in performance and freedom in the size of data to be encrypted.

When you sign up, this API sends you your private key, which decrypts the encrypted data using the public key saved in the database. It's like creating a certificate, huh?

It also creates a record in the database containing the symmetric encryption key encrypted with its public key for each person you decide to share your data with. Sorry to the dry Python community.

## Folder Structure

```curl
── business_logic
│   ├── adapter # repository layer
│   ├── exceptions # exceptions & validation
│   └── services # services layer
├── manage.py
├── requirements.txt
├── secret
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── serializers.py
│   ├── test # unit & e2e
│   ├── urls.py
│   └── views.py
├── server
│   ├── asgi.py
│   ├── settings
│   ├── urls.py
│   └── wsgi.py
├── users
│   ├── admin.py
│   ├── apps.py
│   ├── logic.py # only user logic
│   ├── managers.py
│   ├── migrations
│   ├── models.py
│   ├── serializers.py
│   ├── test # unit & e2e
│   ├── urls.py
│   └── views.py
```

## Installation

```bash
python3 venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```python
# backend/manage.py
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings.dev') # dev | prod
...

# backend/server/wsgi.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings.dev') # dev | prod
```

# or

```bash
export DJANGO_SETTINGS_MODULE=server.settings.dev | prod
```

```bash
python manage.py migrate
python manage.py runserver
```

# Request & Response

postman

```
Valify.postman_collection.json
```
