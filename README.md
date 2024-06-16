```
git clone --recursive https://github.com/hp2oo1/myJupyterLab.git
```

```
cd myJupyterLab
conda install -c conda-forge jupyterlab nodejs
```

```
cd lumino
jlpm && jlpm build
```

```
pip install hatchling
```

```
cd jupyterlab
jlpm link ..\lumino --all
jlpm && jlpm run build
pip install -ve .
```

```
cd jupyterlab
juypter lab build
```

```
cd ipydatagrid
jlpm link ..\lumino --all
jlpm && jlpm build
pip install -ve .
```

```
pip install jupytext
```
