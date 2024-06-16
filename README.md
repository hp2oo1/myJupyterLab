### MyJupyterLab
```
git clone --recursive https://github.com/hp2oo1/my
cd myJupyterLab
conda install -c conda-forge nodejs
```

### Install Development Version
```
git clone https://github.com/hp2oo1/jupyterlab.git
cd jupyterlab
pip install -ve ".[dev]"
```

```
cd ipydatagrid
pip install -ve .
```

### Build Lumino
```
cd lumino
jlpm && jlpm build
```

### Rebuild JupyterLab
```
cd jupyterlab
jlpm link ..\lumino --all
jlpm && jlpm build
jupyter lab build
```

### ReBuild ipydatagrid
```
cd ipydatagrid
jlpm link ..\lumino --all
jlpm && jlpm build
```
