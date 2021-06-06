# archinstall-aur
An [archinstall](https://github.com/archlinux/archinstall) plugin that makes it possible to install AUR packages.

## EXPERIMENTAL
Plugin support is currently only available in archinstalls master branch. It is not part of the official release yet, and the plugin API is experimental, which means this plugin could break at any time.
Please wait until archinstall Plugin support is officially released, and this plugin ships a stable release before you use it.

Other than that, have fun experimenting with this!

## Usage
Archinstall currently can load a plugin via the `plugin` argument. This argument can be provided on the cli, or in a json configuration.

Additionally, this plugin requires the `packages_aur` argument, which is an array of the AUR packages you want installed.

### Using CLI
You can directly provide the plugin path or url, and the `packages_aur` argument to the archinstall command:

```sh
archinstall --packages_aur "package1 package2 package3" --plugin "https://github.com/phisch/archinstall-aur/raw/master/archinstall-aur.py"
```

### Using config.json
Add the following 2 properties to your configuration:

```json
{
    ...
    "packages_aur": ["giph", "ttf-material-design-icons-git"],
    "plugin": "http://10.0.2.2:8000/plugins/archinstall-aur.py",
    ...
}
```

And load that configuration using archinstalls `config` argument:

```sh
archinstall --config https://path/or/url/to/your/config.json
```

For more detail, read [Running from a declarative configuration file or URL](https://github.com/archlinux/archinstall#running-from-a-declarative-configuration-file-or-url) over in the archinstall repository.