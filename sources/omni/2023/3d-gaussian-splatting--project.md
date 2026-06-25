# 3D Gaussian Splatting for Real-Time Radiance Field Rendering
Source: https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/
3D Gaussian Splatting for Real-Time Radiance Field Rendering




More Research

[Fungraph Publications](https://project.inria.fr/fungraph/publications/)

# 3D Gaussian Splatting for Real-Time Radiance Field Rendering

# SIGGRAPH 2023 (ACM Transactions on Graphics)

[Bernhard Kerbl](https://scholar.google.at/citations?user=jeasMB0AAAAJ&hl=en)\* 1,2     

[Georgios Kopanas](https://grgkopanas.github.io/)\* 1,2     
[Thomas Leimkühler](https://people.mpi-inf.mpg.de/~tleimkue/)3     

[George Drettakis](http://www-sop.inria.fr/members/George.Drettakis/)1,2

\* Denotes equal contribution

1Inria     
2Université Côte d'Azur     
3MPI Informatik

1 [![](content/images/inria_logo.png)](https://www.inria.fr/) 
2 [![](content/images/uca_logo.png)](https://univ-cotedazur.eu/) 
3 [![](content/images/mpi_logo-01-01.jpg)](https://www.mpi-inf.mpg.de)

[Paper - 115MB](3d_gaussian_splatting_high.pdf)

[Paper - 25MB](3d_gaussian_splatting_low.pdf)
  

[Code](https://github.com/graphdeco-inria/gaussian-splatting)

[Scenes - 650MB](datasets/input/tandt_db.zip)

[Results - 7GB](evaluation/images.zip)

[Group Publ. Page](https://www-sop.inria.fr/reves/Basilic/2023/KKLD23/)

[![](content/images/graphdeco_logo.png)](https://team.inria.fr/graphdeco/)

[

](content/videos/bicycle.mp4)

[

](content/videos/stump.mp4)

[

](content/videos/garden.mp4)

[

](content/videos/playroom.mp4)

[

](content/videos/bicycle.mp4)

[

](content/videos/stump.mp4)

[

](content/videos/garden.mp4)

[

](content/videos/playroom.mp4)

[

](content/videos/bicycle.mp4)

[

](content/videos/stump.mp4)

[

](content/videos/garden.mp4)

[

](content/videos/playroom.mp4)

[

](content/videos/bicycle.mp4)

[

](content/videos/stump.mp4)

[

](content/videos/garden.mp4)

## Abstract

Radiance Field methods have recently revolutionized novel-view synthesis
of scenes captured with multiple photos or videos. However, achieving high
visual quality still requires neural networks that are costly to train and render,
while recent faster methods inevitably trade off speed for quality. For
**unbounded and complete scenes** (rather than isolated objects) and **1080p**
resolution rendering, no current method can achieve real-time display rates.

We introduce three key elements that allow us to achieve state-of-the-art
visual quality while maintaining competitive training times and importantly
allow **high-quality real-time** (≥ 100 fps) novel-view synthesis at **1080p** resolution.

First, starting from sparse points produced during camera calibration,
we represent the scene with *3D Gaussians* that preserve desirable properties
of continuous volumetric radiance fields for scene optimization while
avoiding unnecessary computation in empty space; Second, we perform
interleaved optimization/density control of the 3D Gaussians, notably optimizing
anisotropic covariance to achieve an accurate representation of the
scene; Third, we develop a fast visibility-aware rendering algorithm that
supports anisotropic splatting and both accelerates training and allows realtime
rendering. We demonstrate state-of-the-art visual quality and real-time
rendering on several established datasets.

## Video

## Evaluation

We tested our algorithm on a total of 13 real scenes taken from previously published datasets and the synthetic Blender dataset.
In particular, we tested our approach on the full set of scenes presented in Mip-Nerf360 [Barron 2022], which is the current state of the art in NeRF rendering quality,
two scenes from the Tanks and Temples dataset [Knapitsch 2017] and two scenes provided by Deep Blending [Hedman 2018].
For the full evaluation please check the paper and the supplemental.

![Graph for quality evaluation](content/images/Artboard 19.png)



![Graph for perfomance evaluation](content/images/Artboard 22.png)

## Visual Comparisons

![](content/images/comparisons/ours_bicycle.png)

Ours

![](content/images/comparisons/mipnerf_bicycle.png)

Mip-NeRF360 [Barron 2022]

![](content/images/comparisons/ours_stump.png)

Ours

![](content/images/comparisons/plenoxels_stump.png)

Plenoxels [Fridovich-Keil and Yu 2022]



![](content/images/comparisons/ours_garden.png)

Ours

![](content/images/comparisons/ingp_garden.JPG)

Instant-NGP [Müller 2022]

![](content/images/comparisons/ours_truck.png)

Ours

![](content/images/comparisons/gt_truck.png)

Ground Truth

## BibTeX

```
@Article{kerbl3Dgaussians,
      author       = {Kerbl, Bernhard and Kopanas, Georgios and Leimk{\"u}hler, Thomas and Drettakis, George},
      title        = {3D Gaussian Splatting for Real-Time Radiance Field Rendering},
      journal      = {ACM Transactions on Graphics},
      number       = {4},
      volume       = {42},
      month        = {July},
      year         = {2023},
      url          = {https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/}
}
```

## Acknowledgments and Funding

![](content/images/erc.jpg)

This research was funded by the ERC Advanced grant [FUNGRAPH](http://fungraph.inria.fr) No 788065. The authors are grateful to Adobe for generous donations, the OPAL infrastructure from Université Côte d’Azur and for the HPC resources from GENCI–IDRIS (Grant 2022-AD011013409). The authors thank the anonymous reviewers for their valuable feedback, P. Hedman and A. Tewari for proofreading earlier drafts also T. Müller, A. Yu and S. Fridovich-Keil for helping with the comparisons.

## References

[Müller 2022] Müller, T., Evans, A., Schied, C. and Keller, A., 2022. Instant neural graphics primitives with a multiresolution hash encoding

[Hedman 2018] Hedman, P., Philip, J., Price, T., Frahm, J.M., Drettakis, G. and Brostow, G., 2018. Deep blending for free-viewpoint image-based rendering. ACM Transactions on Graphics (TOG), 37(6), pp.1-15.

[Barron 2022] Barron, Jonathan T., et al. "Mip-nerf 360: Unbounded anti-aliased neural radiance fields." Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2022.

[Fridovich-Keil and Yu 2022] Fridovich-Keil, Sara, et al. "Plenoxels: Radiance fields without neural networks." Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2022.

[Knapitsch 2017] Knapitsch, Arno, et al. "Tanks and temples: Benchmarking large-scale scene reconstruction." ACM Transactions on Graphics (ToG) 36.4 (2017): 1-13.

We thank the authors of [Nerfies](https://nerfies.github.io/) that kindly open sourced the template of this website.
