# FUR — Fear User Repository

FUR is the public module catalog for [Fear](https://github.com/Fear-Selfbot/fear). Fear reads `registry.json` from this repository's `main` branch. Packages are ZIP archives referenced by a module ID, version, repository-relative archive path, and SHA-256 digest.

## Install and manage modules

Run these commands in a message sent from the account running Fear:

| Command | Action |
| --- | --- |
| `.flist` | List modules available in FUR and show which are installed |
| `.fins <module-id>` | Install and activate a module |
| `.fremove <module-id>` | Remove an installed FUR module and deactivate it |
| `.fupdate [module-id|all]` | Update one installed module or all installed FUR modules |

Installation downloads and validates the package, stages its files under Fear's `modules/` directory and installs optional Python requirements from a hash-pinned `requirements.lock` into `.data/module-deps/<module-id>/`. Fear then loads the new module in the running process; it does not restart either Telegram client. Installation failures during activation roll back the package files and installed-module record.

Modules are Python code running inside Fear with the same operating-system permissions as Fear. The repository digest detects a package that differs from the catalog, but it does not sandbox code or establish an independent publisher signature. Only install modules you trust. Python dependencies share the host process and `sys.modules`; modules requiring incompatible versions of the same library may conflict. Keep requirements pinned with hashes and avoid changing a library already imported by Fear or another module.

## Add a module

1. Create a unique lowercase ID and a module folder under `examples/` (or your own source tree).
2. Add `fear-module.json`, `main.py`, and optionally a hash-pinned `requirements.lock` (generate one with `uv pip compile --generate-hashes`).
3. Build a ZIP whose root contains those files. The root `main.py` must define a `FearModule` subclass. For the included example:

   ```sh
   zip -j packages/hello-1.0.0.zip examples/hello/fear-module.json examples/hello/main.py examples/hello/requirements.lock
   sha256sum packages/hello-1.0.0.zip
   ```

   Copy the resulting digest into the matching `registry.json` entry before publishing.
4. Put the archive under `packages/` and calculate its SHA-256 digest.
5. Add its ID, version, archive path and digest to `registry.json`, then submit the change.

The complete example is in [`examples/hello`](examples/hello). Fear currently accepts IDs matching `[a-z0-9][a-z0-9_-]{0,63}` and expects the manifest ID and version to match the registry.

Example package layout:

```text
packages/hello-1.0.0.zip
├── fear-module.json
├── main.py
└── requirements.lock   # optional, hash-pinned wheel requirements
```

The archive limit is 20 MiB and the expanded package limit is 50 MiB. Archives containing traversal paths or symbolic links are rejected.

## Compatibility

- Fear: Python 3.14+
- Fear Module SDK: install against the SDK API used by the current Fear release (the `fear` and `sdk` manifest fields are descriptive today; Fear does not yet enforce version ranges)
- Entrypoint: `main.py` at the package root
- Required class: a locally defined subclass of `fear_module.FearModule`

Use `.reload` after manual changes made directly in `modules/`. FUR commands load and activate changes automatically.
