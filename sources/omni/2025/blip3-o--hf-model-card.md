---
language:
- en
license: apache-2.0
---
This is BLIP3o-8B checkpoint trained on the **open source** data.


| Model               | Pretrain Data                                             | GenEval | DBP    | WISE |
|---------------------|-----------------------------------------------------------|---------|--------|------|
| 4B (open source)    | 30 million open-source data                           | 0.81    | 79.36  | 0.50 |
| 8B (open source)    | 30 million open-source data                           | 0.83    | 80.73  | 0.52 |
| 8B (paper reported) | 30 million open-source + 30 million proprietary data  | 0.84    | 81.60  | 0.62 |



Here is the category results for WISE.

|       Model      |        Pretrain Data        | Cultural | Time | Space | Biology | Physics | Chemistry | Overall |
| :--------------: | :-------------------------: | :------: | :--: | :---: | :-----: | :-----: | :-------: | :-----: |
| 8B (open source) | 30 million open-source data |   0.49   | 0.51 |  0.63 |   0.54  |   0.63  |    0.37   |   0.52  |
| 8B (paper reported)  | 30 million open-source + 30 million proprietary data|  0.63  | 0.57 | 0.70 |  0.62 |  0.66 |   0.51  |  0.62   |











### Download

```
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="BLIP3o/BLIP3o-Model-8B",
    repo_type="model"
)
```

Clone the repo (if you haven’t already) and install the environment:

```
git clone https://github.com/JiuhaiChen/BLIP3o.git
```

Change to the demo folder:

```
cd gradio
```

Launch with your model path:

```
python app.py /path/to/your/model
```
