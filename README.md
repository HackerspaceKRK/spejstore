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
docker-compose up
```

### Rebuild

```sh
docker-compose build
```

### Troubleshooting

- https://askubuntu.com/q/615394/413683
