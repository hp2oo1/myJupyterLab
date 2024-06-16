### MyJupyterLab
```
git clone --recursive https://github.com/hp2oo1/myJupyterLab
```

Create and activate conda environment

```
cd myJupyterLab
conda install -c conda-forge nodejs=20 yarn -y
```

### Build Lumino (modified)
```
cd lumino
yarn && yarn build
```

### Install Development Version
```
git clone https://github.com/hp2oo1/jupyterlab.git
cd jupyterlab
yarn link ..\lumino
pip install -ve ".[dev]"
```

```
cd ipydatagrid
yarn link ..\lumino
pip install -ve .
```

### Rebuild JupyterLab
```
cd jupyterlab
jlpm && jlpm build
jupyter lab build
```

### ReBuild ipydatagrid (modified)
```
cd ipydatagrid
jlpm && jlpm build
```

### Before Launch JupyterLab
```
cd jupyterLab
jupyter lab build
```

```
rm -rf ..\.conda\share\jupyter\lab\staging\node_modules\@lumino
mklink /J ..\.conda\share\jupyter\lab\staging\node_modules\@lumino ..\lumino\packages
```

```
jupyter lab build
```

### Launch JupyterLab
```
jupyter lab
```
