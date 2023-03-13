# Generating docs

## Generating `rst` files

```cmd
sphinx-apidoc -f -o docs_src\source src */migrations/*
```

## Starting the doc server locally

```cmd
sphinx-autobuild -b html --watch src\ docs_src\source docs_src\build\
```

> Note: Running the `sphinx-autobuild` command also generates the `html` files inside the build folder.

If your documentation is not getting updated properly, delete the `docs_src/build` folder and run the `sphinx-autobuild` command again.
