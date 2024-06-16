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
pip install -e ".[dev]"
```

### Build Lumino
```
cd lumino
jlpm && jlpm build
```

### Build JupyterLab
```
cd jupyterlab
jlpm link ..\lumino --all
jlpm && jlpm run build
jupyter lab build
```

### Build ipydatagrid
```
cd ipydatagrid
jlpm link ..\lumino --all
jlpm && jlpm build
pip install -ve .
```
