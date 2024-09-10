## Bitcoin Monte Carlo Simulations
Install [uv](https://docs.astral.sh/uv/). 

Initialize venv and activate: 
```
uv venv
```

```
source .venv/bin/activate
```

Install packages:
```
uv pip sync requirements.lock
```

Run `main.py` to generate simulations graph. Run `update_data.py` to update bitcoin price data.
