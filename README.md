# spejstore

Because there is not enough general inventory software invented here yet.
Please use Python3, for the love of `$deity`...

## Usage

### Quick start

1. Run:
   ```sh
   ln -s docker-compose.dev-override.yml docker-compose.override.yml
   docker-compose up --build
   ```
2. Run `docker-compose run --rm web python manage.py createsuperuser` -- now you can dev authenticate w/o SSO

### Build & run

```sh
docker-compose up --build

# if you need to reset built static files and/or postgres database:
docker-compose up --build --renew-anon-volumes
```

### Troubleshooting

- https://askubuntu.com/q/615394/413683

## New docs (WIP):

Spejstore is a simple inventory system made for Warsaw Hackerspace purposes. Includes some features very specific to hswaw requirements, which are:

- Label printing and label-system support (via `django-rest-api` api views and `SPEJSTORE_LABEL_API` env variable), using the [spejstore-labelmaker](https://code.hackerspace.pl/informatic/spejstore-labelmaker/) software
- Publically viewing all items and requiring users to sign in view oauth to manage inventory via `django-admin`
- Authorizing label printing via local network only, see `SPEJSTORE_LAN_ALLOWED_ADDRESS_SPACE` env variable

Currently inventory is deployed under `inventory.waw.hackerspace.pl`, with a [Beyondspace NGINX configuration](https://cs.hackerspace.pl/hscloud/-/blob/hswaw/machines/customs.hackerspace.pl/beyondspace.nix), which allows the inventory to be accessible from outside of the Warsaw Hackerspace network with a necessary oauth authorization, but does not allow printing of labels without physically being in the local network of HSWAW.
