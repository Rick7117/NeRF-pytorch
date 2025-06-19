# NeRF-pytorch


[NeRF](http://www.matthewtancik.com/nerf) (Neural Radiance Fields) is a method that achieves state-of-the-art results for synthesizing novel views of complex scenes. 

This project is a faithful PyTorch implementation of [NeRF](http://www.matthewtancik.com/nerf) that **reproduces** the results while running **1.3 times faster**. The code is based on authors' Tensorflow implementation [here](https://github.com/bmild/nerf), and has been tested to match it numerically. 

## Installation

```
git clone https://github.com/yenchenlin/nerf-pytorch.git
cd nerf-pytorch
pip install -r requirements.txt
```

<details>
  <summary> Dependencies (click to expand) </summary>
  
  ## Dependencies
  - PyTorch 1.4
  - matplotlib
  - numpy
  - imageio
  - imageio-ffmpeg
  - configargparse
  
The LLFF data loader requires ImageMagick.

You will also need the [LLFF code](http://github.com/fyusion/llff) (and COLMAP) set up to compute poses if you want to run on your own real data.
  
</details>

## How To Run?

### Quick Start

Download data for two example datasets: `lego` and `fern`
```
bash download_example_data.sh
```

To train a low-res `lego` NeRF:
```
python run_nerf.py --config configs/lego.txt
```
After training for 100k iterations (~4 hours on a single 2080 Ti), you can find the following video at `logs/lego_test/lego_test_spiral_100000_rgb.mp4`.

![](https://user-images.githubusercontent.com/7057863/78473103-9353b300-7770-11ea-98ed-6ba2d877b62c.gif)

---

### Your Datasets

#### 1. Creating nerf_lfff_data Format

To prepare your custom dataset in nerf_lfff_data format:

1. Create a new folder at `./data/{yourdata}/images` (replace `{yourdata}` with your dataset name)
2. Place all your images in this folder
3. Run `bash colmap.sh` from the root directory

This will generate:
- Downsampled images (4x and 8x resolution)
- Corresponding camera parameters
- Properly formatted nerf_lfff_data structure

#### 2. Training NeRF on Different Datasets

To train NeRF on various datasets:

```bash
python run_nerf.py --config configs/{DATASET}.txt
```

Replace `{DATASET}` with one of the available options:  
`trex` | `horns` | `flower` | `fortress` | `lego` | etc.

Important Note for 360° Capture Datasets:
If working with spherical/360° capture data, use this modified command:

```bash
python run_nerf.py --config configs/{DATASET}.txt --spherify --no_ndc
```

#### 3. Testing Trained NeRF Models

To render images from a trained NeRF model:

```bash
python run_nerf.py --config configs/{DATASET}.txt --render_only
```

Again, replace `{DATASET}` with your target dataset:  
`trex` | `horns` | `flower` | `fortress` | `lego` | etc.

---

### Pre-trained Models

You can download our data [here](https://drive.google.com/file/d/1VVxPjeyNwFnri1gNtayobPErzAL5exy7/view?usp=sharing), unzip it and place it in `./data/nerf_lfff_data` directory.
You can download our pre-trained models [here](https://drive.google.com/file/d/1ZNPDw_9ZZJfhMC-CZ-xF2voicjOV9Aa7/view?usp=sharing). Unzip and place the downloaded directory in `./logs` in order to test it later. See the following directory structure for an example:

```
├── logs 
│   ├── fern_test
│   ├── flower_test  # downloaded logs
│   ├── trex_test    # downloaded logs
```

### Reproducibility 

Tests that ensure the results of all functions and training loop match the official implentation are contained in a different branch `reproduce`. One can check it out and run the tests:
```
git checkout reproduce
py.test
```

## Method

[NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis](http://tancik.com/nerf)  
 [Ben Mildenhall](https://people.eecs.berkeley.edu/~bmild/)\*<sup>1</sup>,
 [Pratul P. Srinivasan](https://people.eecs.berkeley.edu/~pratul/)\*<sup>1</sup>,
 [Matthew Tancik](http://tancik.com/)\*<sup>1</sup>,
 [Jonathan T. Barron](http://jonbarron.info/)<sup>2</sup>,
 [Ravi Ramamoorthi](http://cseweb.ucsd.edu/~ravir/)<sup>3</sup>,
 [Ren Ng](https://www2.eecs.berkeley.edu/Faculty/Homepages/yirenng.html)<sup>1</sup> <br>
 <sup>1</sup>UC Berkeley, <sup>2</sup>Google Research, <sup>3</sup>UC San Diego  
  \*denotes equal contribution  
  
<img src='imgs/pipeline.jpg'/>

> A neural radiance field is a simple fully connected network (weights are ~5MB) trained to reproduce input views of a single scene using a rendering loss. The network directly maps from spatial location and viewing direction (5D input) to color and opacity (4D output), acting as the "volume" so we can use volume rendering to differentiably render new views

