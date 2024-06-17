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
jlpm && jlpm build
pip install -ve ".[dev]"
```

```
cd ipydatagrid
jlpm link ..\lumino --all
jlpm && jlpm build
pip install -ve .
```

### Build JupyterLab App
```
cd jupyterlab
jupyter lab clean --app-dir ..\app
jupyter lab build --app-dir ..\app
```

Delete ..\app\staging\node_modules\@lumino
```
mklink /j ..\app\staging\node_modules\@lumino ..\lumino
```

### Launch JupyterLab App
```
pip install jupytext
```

```
cd myTable
jupyter lab --app-dir ..\app
```
