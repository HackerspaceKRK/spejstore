# spejstore (AKA inventory)

The general HSWAW (and other polish hackerspaces) inventory system.

Because there is not enough general inventory software invented here yet.

## Usage

### Quick start (VSCode)

1. Copy `.env.example` as `.env`
2. Have `docker compose` 2.0. You can identify it by having `docker compose` command instead of `docker-compose`.
3. Customize your `.env` for your specific usecase.

#### VSCode

0. Setup environment variables
1. Get VSCode from [here](https://code.visualstudio.com/download), *CAN NOT* be VSCodium, as the extension is a microsoft binary which does not work with VSCodium.
2. Install [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
3. Clone the repository and open it with VSCode.
4. You should get a toast like this when re-opening directory with the cloned repository. ![Toast example](readme/toast-example.png 'Toast example')
   1. If you don't get a toast, then use (CMD|Ctrl)+Shift+P to open actions menu and choose option **Rebuild Without Cache and Reopen in Container**. ![Command example](readme/command-example.png 'Command example')
5. Reopen the directory in container either via command or popup button.
6. Wait for the application and container to properly build.
   1. Devcontainer's VSCode instance will be automatically configured with extensions to help your development process.
   2. You might get a Toast telling you to re-open the directory due to Black not working properly. Do so for proper autoformatting support.
7. `manage.py migrate` will be run automatically after container creation, to make sure you have the latest migrations done on the development database without any need for interaction.
8. Run debug session with either command of "Start Debugging" (default hotkey F5), or with the Debug sidebar. ![Debug sidebar instructions](readme/debug-example.png 'Debug sidebar')
9. You should have automatically forwarded ports, so the only thing remaining is opening browser window with the url provided in terminal.

#### Everything else (docker)

1. Run `docker compose up`. This will create a production-ready setup with gunicorn. out of the box.

### Everything else (python)

1. Get python3
2. `pip install -r requirements.txt`
3. `python3 manage.py migrate`
4. `python3 manage.py collecstatic`
5. `python3 manage.py runserver 0.0.0.0:8000`

## New docs (WIP)

Spejstore is a simple inventory system made for Warsaw Hackerspace purposes. Includes some features very specific to hswaw requirements, which are:

- Label printing and label-system support (via `django-rest-api` api views and `SPEJSTORE_LABEL_API` env variable), using the [spejstore-labelmaker](https://code.hackerspace.pl/informatic/spejstore-labelmaker/) software
- Publically viewing all items and requiring users to sign in view oauth to manage inventory via `django-admin`
- Authorizing label printing via local network only, see `SPEJSTORE_LAN_ALLOWED_ADDRESS_SPACE` env variable

Currently inventory is deployed under `inventory.waw.hackerspace.pl`, with a [Beyondspace NGINX configuration](https://cs.hackerspace.pl/hscloud/-/blob/hswaw/machines/customs.hackerspace.pl/beyondspace.nix), which allows the inventory to be accessible from outside of the Warsaw Hackerspace network with a necessary oauth authorization, but does not allow printing of labels without physically being in the local network of HSWAW.
