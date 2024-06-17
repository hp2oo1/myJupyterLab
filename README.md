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

### ReBuild JupyterLab
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
cd jupyterlab
jupyter lab clean --app-dir .
mkdir staging
mklink /j staging\node_modules node_modules
jupyter lab build --app-dir .
```

### Launch JupyterLab App
```
pip install jupytext
```

```
cd myTable
jupyter lab --app-dir ..\jupyterlab
```
