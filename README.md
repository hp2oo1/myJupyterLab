### MyJupyterLab
```
git clone --recursive https://github.com/hp2oo1/myJupyterLab
```

Create and activate conda environment

```
cd myJupyterLab
conda install -c conda-forge jupyterlab nodejs=20 -y
```

### Build Lumino (modified)
```
cd lumino
jlpm && jlpm build
```

### Install Development Version
```
git clone https://github.com/hp2oo1/jupyterlab.git
```

```
cd jupyterlab
jlpm link ..\lumino --all
pip install -ve ".[dev]"
```

```
cd ipydatagrid
jlpm link ..\lumino --all
pip install -ve .
```

### Rebuild JupyterLab
```
cd jupyterlab
jlpm && jlpm build
```

### ReBuild ipydatagrid (modified)
```
cd ipydatagrid
jlpm && jlpm build
```

### Build JupyterLab App
```
cd jupyterLab
jupyter lab clean --app-dir .
mkdir /p staging
mklink /j staging\node_modules node_modules
jupyter lab build --app-dir .
```

### Launch JupyterLab
```
jupyter lab --app-dir .
```
