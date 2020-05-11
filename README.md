# spejstore

Because there is not enough general inventory software invented here yet.
Please use Python3, for the love of `$deity`...

## Usage

### Quick start

1. Open `docker-compose.yml` and make changes as comments indicate (TODO: Please someone make this not awful)
2. Run:
    ```sh
    docker-compose up --build
    ```
3. Open `spejstore/urls.py` and comment out `url(r'^admin/login/.*', auth_redirect),`
4. Run `docker-compose run --rm web python manage.py createsuperuser` -- now you can dev authenticate w/o SSO

### Build & run

```sh
docker-compose up
```

### Rebuild

```sh
docker-compose build
```

### Troubleshooting

- https://askubuntu.com/q/615394/413683
