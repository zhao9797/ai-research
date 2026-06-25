# 🧞 Genie: Generative Interactive Environments
Source: https://sites.google.com/view/genie-2024/home
🧞 Genie: Generative Interactive Environments

搜索此网站

嵌入的文件

跳至主要内容

调至导航栏

[![](https://lh3.googleusercontent.com/sitesv/AA5AbUCOpTcUIF0Bg1znVw-kQ_4kSnykSTq-yQvmKk66VSJcPmgkMNpz9OMWMGiDF1Hemwx0HlTRWluBJ01AuN34ka8P9LzmYCoWSUhrVrvz3Z7PNWS9z6St_N5eJlntkN5KYEB2EhY_4M-uDjuJNbyB9tgdIX8I8gET0-M-DVjv3GJBz4xFVfWOSkCtWPKi=w16383)🧞 Genie: Generative Interactive Environments](/view/genie-2024/home)

# 🧞 Genie: Generative Interactive Environments

  

Genie Team

  

We introduce Genie, a foundation world model trained from Internet videos that can generate an endless variety of playable (action-controllable) worlds from synthetic images, photographs, and even sketches.

![](https://lh3.googleusercontent.com/sitesv/AA5AbUB6K28dMadFVAx2Kf6C_0pr6PKS8IBFD-Emn8ugHEAcw5mhMNMpZYpYaUcogcUGDMzhBOUh8ttI2t5WKAWFB6Zmwe_pBBpeKSlHcDIAbY_DDm4W0Sd5vv6fWmgEA8jU8Rm-ZZTbsQXnjydXkquk9pAX4CRO0AHd0kU4ftJAoqzwqisTHzTxXgVqd6QbShJHHOe7nn31-fXQBcV4FEciMtWxYn44_T9QhDwa2PIvUvM=w1280)

[Read Paper](https://www.google.com/url?q=https%3A%2F%2Farxiv.org%2Fabs%2F2402.15391&sa=D&sntz=1&usg=AOvVaw0PIgdwpLI7_OGTVwslE43h)

## A Foundation Model for Playable Worlds

The last few years have seen an emergence of generative AI, with models capable of generating novel and creative content via language, images, and even videos. Today, we introduce a new paradigm for generative AI, generative interactive environments (Genie), whereby interactive, playable environments can be generated from a single image prompt. 

  

Genie can be prompted with images it has never seen before, such as real world photographs or sketches, enabling people to interact with their imagined virtual worlds-–essentially acting as a foundation world model. This is possible despite training without any action labels. Instead, Genie is trained from a large dataset of publicly available Internet videos. We focus on videos of 2D platformer games and robotics but our method is general and should work for any type of domain, and is scalable to ever larger Internet datasets.

## Learning to control without action labels

What makes Genie unique is its ability to learn fine-grained controls exclusively from Internet videos. This is a challenge because Internet videos do not typically have labels regarding which action is being performed, or even which part of the image should be controlled. Remarkably, Genie learns not only which parts of an observation are generally controllable, but also infers diverse latent actions that are consistent across the generated environments. Note here how the same latent actions yield similar behaviors across different prompt images.

![](https://lh3.googleusercontent.com/sitesv/AA5AbUAzp1BzVW-9xdNh8PpytcCSdcD6iWRvBAcPhhcolew1f9tYeybXLMHW1zhC8VSDsm5mzPoOyKqRo6sSXHMCycOwndZ8GIsicWhWhua5nXD1z5AjhjHqaFtVqKm0ojjeSfodvbIAiSC2bM5y5RPfEgMX9VMuW1YKWP-7dHM5I9srV1-MaXpYLcJLlfpYpHwjJFf-zlYig16XJ_Epq33ZBG8C5GWEXio7-VYdnxQ6=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUCBFaDKIA46ewTWKn1wFvWl0-rMbyxZw5366PuHc2Pta8K_hh39NN0R3E1eKy4g9xnOOl1nXc8Q9JMX2VyQSQml0A2q70HxFEHUgXVNrPCBtaR7PKLA7pDhKhcEHc10wcEEUvX6Blmh_a4EA3DZ66xmg6gf_4Qr0qa9biyg4FiraAnOwd5p7pVNER2Jnjotf65T0BjiHzRDGPMDDAi-cACHYiWdFKCe7s1TM6tUpY8=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUAqAhxwZOXfp5Ch2OTOG9qe91jdEUkEB25gNnP_cOAYL3x2Oj6GCf_NZzKpOQtcHwAapSDAnC7qD9H7kUkNXAKcrV8mcK9sgfSZqUFPY6t-k3tN1nTaWORcM-i7QWW6otJcLSaSFpm4VpJt5gO53L16h4Pk9EqTovieR-NxTqXxs9pTOfdxL7nuGZu_xee8fcrw5zGMOaGrkueBvd_LsSMgrFknwjXf_A45SEYsNW4=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUB3Mo6HBzZnN39kJQSYqKEsT0uG_YJTgPkzeml5i86x8HPi086vXfgxPC04gqYPi9h9jfAZNDaI57ZHSYa66pzqjvKvfCU7OHb9-f8mWmia0elhwzLoLCmCMs4CHYp5y_sW5sjRqM5qmFh9XdghjaZbnDCzOrOKqSU8MVa4i56zYxpNgs3InDwfcHNgGos5GDlkp1TA_1zudvNmtkH9pEGGtvkMkCUiUU_UnhMC-Os=w1280)

latent actions: 6, 6, 7, 6, 7, 6, 5, 5, 2, 7

![](https://lh3.googleusercontent.com/sitesv/AA5AbUBCful6xDPusGou_DBIccf_erbnrEvIr2iiPip9yQ86A9Y5gdc27nodC7ocxzKxtIULwmz2hsMmUOpYnsU8yMguJoTrxTYUA4WDA222CyQ8d21nXyH2p56NlZuKSgloy4_iDp3PXp5BgpWcO_DlU40IgoXL-B14Hq_MWdLuxTAd695kLIWwPN3sWjMlP4B0c6J98rHVQE0jya69UWIQFNS4pVsST3cH57-k9Jw-huM=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUAgpMPGOQeTqjZtrIqwrPgK3W9bDvZ_0Lrx2IY9rZ5vwe9u80rHD3mHHCPDombQhO0UN9wApnoWkx_Z6QbtLPv6rcR0njcyAIfNqMdpCkrKCgtPNyYg2oZ5P29EY3WCMvXWjk9Qemu0RcJVM_y_cFwtSZQzCDTHajSnPi58FwIne-TcLKrNS7gT-jtzHRIoyEQqPdNDUinmce7O8jLkzDJhPrW0qWyqq7tkMtt8TTQ=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUDf_6s9IOMIb_by4XxWKuB68Q_c1bAr6N7o5SBt87VZ8jaQaJ_gemSTbpKwocSnfLegSuFry0nGnUARg9XIA3-_m-ebEBXG1CdDO-NjcoSKWjAnftz1hMoFD6fTsZ93MLxyFpPpKeM9f-UDGbOFhGriWGuX81Ho7fz01V7PrMJXRnEBH9mTcdg4sdCFkFSv9HXoFcMvykziaxN4Jj_fkRixZIzeCOX3RGAdi5Z7=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUBpRKg0tQ6I31gKF83NpBA3cnrRvi5ovg3cCmLfGtV_R4vbVzoAWM_LtjE2Ea4gBDJ8Yq2avwWX-Yk41IWBowWlPEHg3DN7L4gKOySFVsIITQB7ybi7O_2a_TDFmxOBnfdSJ2I884JB-tSQDxm0hd78P17JB_hchyl3pRfzXdROs-2n0T-vfs8evo2duVeD-S2sQ7fm2gVDThLgBvFHLW8rSBTfgy5rFxhtZ1g_KS8=w1280)

latent actions: 5, 6, 2, 2, 6, 2, 5, 7, 7, 7

## Enabling a new generation of creators

Amazingly, it only takes a single image to create an entire new interactive environment. This opens the door to a variety of new ways to generate and step into virtual worlds, for instance, we can take a state-of-the-art text-to-image generation model and use it to produce starting frames that we can then bring to life with Genie. Here we generate images with [Imagen2](https://deepmind.google/technologies/imagen-2/) and bring them to life with Genie.

![](https://lh3.googleusercontent.com/sitesv/AA5AbUBSl2nOyEW4x6dnm7CNovAhXJ8qU0ssu6Ok9Q-E-QaOyNmD82PbNRqseHJ7aKODxIpl5j_g5MhY6dVsW2nOkF5-cPab18tsSstTsTtUGu21mSHmWzs1c3dLtC8gjYicwiPgDzyUUg6y7fRuXoJKlybwFD-W9mhkUKV1PRbtHMyCvqVJ2buI48nZKeduuac78vvvTLMXMPx69zcB_K5qHEfIeziR6jwAm54fO5kyfro=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUCPARCKmNi-nTUUpQH4LBSw9oDYktQXqHHthHsogKENKgVqXOr-5ei8n8KVHml4NKjzZ3fMJKAHWP08Gw47xTUurJ-smrGTESyqM3atQzNz-Q6K2LLHND7t_xBZLm0J4ApcC_U_xmZptodjcI-RG6UoPaqas2RcK2FkPGV8Q_lLvRMkIbvubEMIye-ZkcGLotSNq9I19h351P0tkN7vXuGt7tYW7WLRkWXHtuMT=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUDFRG0y6BroJZDoHIBSU3gqWu9PQyW_yHJqgI5F8ExFFrD3_uMVyezAyVoZQku5mIw_Uv2yvZ2jEnbQWhXIvTPXCLKJq_IcDjXyTixwC4ZJgGrJUFwwYQT_75yEceODagXndREzoQkn8VzhS-nDxeV0jnET_lEgGJFtJ23pwrSMxWiAQQu8kOGyA1ndYht1LCXCjuYSIIqYCrZ_MPdIinzIdPTBjiP5i_a7_dQ9ZsY=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUDJugngHOlqXnvYqINskKEtbBWRqk0iLoDYSYKwFt5V726XI1rs8ZuC9rIGQ2sGt9XPy13phL1yFrO4j3vOWceMSlZyYZb7BCz01HlWK_i-R9apazG7gxK1jj0tD2JmYj5IcbcSxxsqHhC56ZLGzXLmZaomYPGChukfZnV2Lcfx2iGOW01T3iao1eA8Ol_D-59TAKz39O3Rd0Y6GL1VRKXLlpXaEB5mF62qwjQN=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUAhsmcob6ALYJuD_JMzCAjHFZZbBB0hAznKh_vVujM_033mqbfj9c8tiOGlc3QgySHk_iiezIcAtcoQpe1ExBQ2vUqgUJddt7koL10cr0g1A6Ed7kovaJJfm40V8yKWsR1LQjz6BjhCf_xwjjZZrDWseC6HDM4J0i8ec7LbLrS1pul9W8FlqAFi5AX27BFbvoNAeGbTiszWOwcoGrDu6VG7CbBn7ftek682s_IJpgE=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUBPI5Tl9_urJrrMXD_V2g5XYEUPMnEkYAGTRF80u-IJbyz98PL_XwYXx5YW_4Ty8kdPiT9dzQnKw0OJ4-Yg0zVcXdkIobsfwDHeyHhDAhkxiguVzxUH6X3-AQJlfok880pnkkt5F3RXzonDDJNL6suegy15YeA7KNsFubVe7le9aL1hx-VM0WX5IIdVjYTCRDrGY9XB9-HRa6_gbnMPZ9ysuRFrDgBisvuK6jovQ4A=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUDqH8RcIzDD0bTDSdys6ehXE91GL2bBEIwHQU3enj6kTaT5Q1fwokGDfCZysLz5RVUfsi9dTLWtK8bK8TbH9Zglndzd5UwZyzaEDoTK6LO253pmCQnPUuWpIL2AvAXVuuMzir2TF_SYmPBMXq3Sk1gOkFI6sVnfW8VZbR_MEZ8_x-8PYtuFpSN98D6BO6HaV48YYgvewLFEUi3hmGbfJ9QMzJdX5ZQf2mhj4xhpk80=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUBVikLcxgeHsxZIoGtK1t_hoS4Sj0y0kvnrDpthORQO9oCyqmSLw43sYUYgydKM45MKZqkTiKKDbuqrBiWHrRkDynUZ-XgPbBWjtp6et-0DNbzidPLTlwo7h3je9YQYBC2VOyBixcId07VEbBR3FevsC_8PxH6nV0tnYkFgtFQEZHHgJsCcOOcFPJcxB2Su1Pg10d12VpN1pWWuuoInROO7DDgpt0myCKd9AyC35dE=w1280)

But it doesn’t stop there, we can even step into human designed creations such as sketches! 🧑‍🎨

![](https://lh3.googleusercontent.com/sitesv/AA5AbUBwSgaIRMgEK_67mPQHeMHq2HIGpl-tlnl3ZYVkMsyGSz3txzbBCJwOyNURHwo_LVgXG3P7Hb8maSN6O2pPbShadWKwMiJemVluN7K8I7MwUmnY-v_4CH4PBXVG8Qf1_0rm_rJ93K2NqNVPGLafvV_z8RM5oVm8nfUIuw-WlHTQtG5mh_ZzThfhcbN4gCiypcYEoM6cgOCtlXlRBYJ2fAejTbBV1dnwPHOE4Tf5EaY=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUAyLkXuBo5Cncz3MTEkkWoA76yubhJL9gJPsmiHlmKtanu7IXpE1AdhUb0jQqo9nq3Fkq8pIFnV2-4qYvCEr0i_YQUTrIC4oViB37bFCP0n8sjlSXCyV0cuoUPC8OXJyO9SZX3tf16zPsnJzUiCjWJc1j2uGkybcJ_e_zBy1GPse3SEsX1NE1a5IwiTC4lpeN3bqccSkluoH9e6wtUVal_f5cRnoWCFcshHgx03SFA=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUBZtIybu92mHP98FpvMp35rgwB4orNZM1uBvl2h8vuVK07faUVYJ5NdEWxydQbPR39e9uLTUxeabaf3pnEvtCjn5O0waNiVtGMiY4nedHmJsG9EvjASvXXj4wP6mwQzEfTM0nCetTaT7aKQfn5_g5qRF_15PNh8xP6HJazdq4xKQ12YpXl8dkif_gm3txLk_GooybRsBqql-yDwLeok2xRwVojSu6mcOjOBn9az5B8=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUBVanGXByZDWN7fEyC3KBl4Co2Rr4jqrGJ58ZnA9JJGqTmmXEbHEApRiG56ZzJ8CjKqKEc5D1PAJvPJ6T7wAecR-rK7qhQe5OYHchxQiXLJLerVv39vN_ZYziw8ePQgvTkkDl60efy8212aVf0JxdawmUyngd4hVXDGRy7YBTAroSsNv-xm8rVxCsY5srGQl-puWSICroPUY4IXF2ak7MR5hK10i-BIiVYjIK6hG4o=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUCTZj9dYk_CLAKCN01onQ0JIguWKmbVmSF5WtQcbaJzryj_suiebHYRbX5th59VE6sDOzEudcJR3Z8hWqkuJ61bp9oMzSxpO_77l0WjBzaZDf-b4zSBifzt8c1-hi3bTLpJJ41bsnQF4kk0UvryxniO0Ue3B3yuitk6NEgo9RHBclgpBcdPIRJjnckWUJ3lLCvgJEDgOk0De-Ef90KXZ7_UAx6KJ2MArDNu0QK8qPU=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUCpk-D-aZMFatKp7VorREpMWIqvL6aZxcaNzeOa3pqejDzrXUb7_Ymgi0d1nO0xwGMTamW2O9G4G-0CHObp0tQL1TOXfaH8mX7HXQViYHCG9rSql8YX1wso-aw_X3llJr1qsONEo_fiqVAQiOUGo6yQx4NnaSfJKh9u41MHn50SU1zJvw6Ac2dMQ5o-OA0r8QjZJ01J-hFEBbVyT8LhLX03xlvLc5iPc8R982bCT-s=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUD718Wfreu6H80IHjHRV9JU0YlhGMkze45KuCkTholPWn47PeCjUj1RMvjp30HgQFbcm9TlUaidEChJ2Dhtub0g7MN1ORL4h1s7VTuxrdFAD_Zj1MeDM6TnOJS1PMun--gaqWSJ9yvkMS7A8-hPFWKoMOeffXyVCgErybfH7gdi7jDR0pC_CGSiFRuf-ZDDyaryICRzKV6hzPE1TBcs1-BgBWzoB5u6jL8ZiheQ_oY=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUA2aA2ADTI22UwSH_Xq5-yDAfXdiy5IUbkUtmRNkKaN-LV4yiGIiH6ZVIVgoLqZkA3pIi2JHqceSUVIupKDM6KY_QGvT7yZo2pyrJv86gwkWlEOmRJpGuu5QOYZR9ut2SzY8BGszUKaBuU3PUqwJTTWO_WU_KNJ6BUabEL-LT9qiCnq1HZLGgjSxi4m2VDc5h9s2bJ1S5ITR6_-2bCmMBEDBkhQSjmj4z-7KSz2gxU=w1280)

Or real world images 🤯

![](https://lh3.googleusercontent.com/sitesv/AA5AbUCSBXVuqAtkx_Z4EnWFHv7t1nmrdHL8_zhSP-onJtx0QsBlOrgoK5lW5O9gmmBF3GoU56lA6kRSZ4GEB_UWx1_ctlfRFe4d5S2A2uboaTAX0eYX-NnnyiIbV6ZfNYQ42cGl5WmtaOKVwbu4Oxw9vAv257mYBnAmlJwHwxQtDU2YKp4kPRJDs52AiUSa5c_anluvvgTVCbg3brilSBTjgoJLLsxnFZtkkpQYb5vHbTw=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUC8vrAqOTKyEU1QpTrDBBKADTsaWon_Cm6vfBL549V_NOK9T-9lspuUs-c-i-o0ECL9oCjDaCfB6wN6ZDgqw7zLluhFtiBrYnPN9lvc-gF71dTNiRLhLNvZjETwTgV__JQZvGZPVWCCfOty73duDEWERxuh9j9Z9bn8CcDzXkFUUKDk7fH9Y07g2_Tecp-pDYLmF5Fsurzz_PNRXhUdTy_wiRv2eoC1MSUpnyVi=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUAscvVylA8nUTMjujpUJvvvny13VL8nq_fzQEQvLURNTvESg9RrUMR5s3XBrOfahGxvn6KF62ZByA646cP3uPovlts0G6p6bXBrN2t5biuJvmLGwvKdzDod9UDrQIM3ewY7du8dNexj3U7IqvrCKIoM73jIfWRJJ2ssB8lCR-HkE-K-yXrRzNlEFr21N2TwJpHUOujcVna9ULyhA7hx5UEt67VKdYRaeVMe-bh6plY=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUBvKwvgADvLM8RDMPSMQ6KaSl_p7lX1W4WCdh8pqPw_UqJ3U2xXp0PvR5gpXQuQDXu1SoA-q7V0gLS49lC5bGVRcLhIRS-sWER-QwQQZVFBubiPewSreOxDkjrVxUOlkx4ui66xtVcPKuXG_Yk46SkgLtWzHRDZrR5N1p3K8haa-aeWpG9y-3DEZTEqGfpiiIDTJQkQzZyhqMIgkWPoRuMpYYzwOoBIQpR7k8wXxhc=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUBkWUDroPRqRfLUiQh6iid_qcng79TFOWR4iny5pxUAtWjzSFpWZTcQ0zfwf7dCkCysLxcpN-uFYuZyJQbX6hKKPdkOmbe9i5oh9HD5C3gKPL-9HCvoMmFhm00QZzBwLxT_d6yV6bbuxck0Wg2GEuihCeCLq78js2E86TeuyLXQ77m3vyB03k8Z8k0vIBK6I1xehYz6kekHhAOPfUZKFF0n_1OijOFqtmxYAyMQcf0=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUAg2HkBjrGuoKaeheY4-_NwEa5S9uGYA4LRY7XrpCDl84mbgXNt_TxklBBlTmkwUq3SbtA4YT5BLGFocmjuDD1x7skgEFhVX5h2i0rswXtb3MdgtMmBrrO_FgLXob-X9Vk5-7TgS0sOMIAt4DuiggLKKozmTTzEFUh2-2kigY5QwRVKygiV5DGhkALXgtMIIsEB66CBHWzkDWyArw_Cdj63t43r61JtCApz_bT9Dto=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUBD4oC3wpwhwG0nAjkyDwKWQnErIQ949JtyZaPvALre5vLxV7OehUc98b9iD-RWW1Hn9P6joII92kE0UNFveOf03L75CUsh8z3OUmhi_dBEIlej8a21c7SA8bJ6SxEDUQ4OAqrAlwMTI-rJGENLbJjasf2q0V5D7AHvxTIFke9si1KtLIsj3OBZt-bJnXbViubMorDtrBvuovg7qPV_gnK7HkBYpkB4exSX3GwS=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUDJ_sRxmUQIUpTvyptprRoV-NR26H94UAiCDZlIxIl1bC1L-u80g7AiUFP1WulYVABXfaGwpCHWbtHRdCHBOXS5zxrVVdlPEPmRvMJJRafvaJ3MhSkHbiTr9XefuJaM_zvARPNnJuRfW5My0BsZAZRyzs16oNHrLL7POWOjJS-3BywIzD_RIi6teU6Tqbe0_ZhjMtcE--MIThbNtRl-7xChJqNWDszExubKhR8RDXg=w1280)

## A stepping stone for generalist agents

Genie also has implications for training generalist agents. [Previous works](https://sites.google.com/corp/view/adaptive-agent/) have shown that game environments can be an effective testbed for developing AI agents, but we are often limited by the number of games available. With Genie, our future AI agents can be trained in a never-ending curriculum of new, generated worlds. In our paper we have a proof of concept that the latent actions learned by Genie can transfer to real human-designed environments, but this is just scratching the surface of what may be possible in the future.

## The future of generative virtual worlds

Finally, while we have focused on results from Platformers on this website, Genie is a general method and can be applied to a multitude of domains without requiring any additional domain knowledge. 

We trained a smaller 2.5B model on action-free videos from [RT1](https://arxiv.org/abs/2212.06817). As was the case for Platformers, trajectories with the same latent action sequence typically display similar behaviors. This indicates Genie is able to learn a consistent action space which may be amenable to training embodied generalist agents.

![](https://lh3.googleusercontent.com/sitesv/AA5AbUDk-lrYCjH_IAbR4unBj87Qw_3DBkmyQ5xAxFAj3pq7p2ERqdO2gIWamgoFOY7fE7J1CMqhdICxuN-MW4ImoKK-HlwK-_oLRcYvdOQMSsevBRMIP0XyCfHRaX7WLYZe7ItcxOTSBEdJpjFk8egNPE7LOMHODEUFUclrWTojWz5czioauwEHyx9ZKObhjrCjw4VP-ZU-KypA8bT0xEUDvG5PiTxqe4H7LcaKyg=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUCdSvzpuq__QWNKgu346btJJRnlcl01K1ejyc3ObNZQPfTrDtwjFkpX_Xw8hflR6dh3pfrbD0K9cAfSzeRAcyNFu9ZAStdfDjDq_W79hpzhwkoFQ6XB1FUgujpfTTgRcrRL4itTFT4rqK32FVpotAd06oDZ_Xocclr0ZfCqexyusRDyDYdV6qe7PlgT86NVnQu4plM16Le9ZGEwUBEyAvXBGEC-StWjXtNRsi65=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUBDRk6exq4kT4v5wpbD4JsMLkQ-It1EdlvgZMj5_83C-Zy_cUCcjFZOWdJpeLt9Ei9m0l_G0LrOw8FPh9kW1y10Hm-09d2pCCMg1DKWuaKnrhW4wyA-tUnGyAcOkvY9y1jQBwNp-AJXkHIwF_-f_7Htl_AyprYmd--3rpCuCW9ZQbHuuZ8IY4MQjBYFdN9G7N92aknbbcvQGubA4epNCUZigSohfKAVYnfUmfprIgQ=w1280)

![](https://lh3.googleusercontent.com/sitesv/AA5AbUAIrppurb-2ECa4XKlC-rXDVFKgwX5b-6PA-k6aA2NP21emKkgwZI6_esoNVFuETIw1qjdE00WTnmzMpcaWK1OoxfoOoAXB6r5jkzg70MY4GWJ_XHmTTSD5Ve2hhx5cjG1GcAOFOSRKFwI4uUBRRyQ7SafdqKx2oEVRz3DYTq8u3U75qxKFK-nWIyFQ49xFRNLzs30NIjR0UWRNR0wyI0mjLXDvqWhSJedufpsjdq4=w1280)

latent actions: 0, 0, 1, 2, 6, 1, 1, 4, 0, 0

Genie can also simulate deformable objects 👕, a challenging task for human-designed simulators that can instead be learned from data.

![](https://lh3.googleusercontent.com/sitesv/AA5AbUDOKmY4JbA9dMcVXdWEbc_UIXs9pG0FaAAb3g4Fk0AwrzfXWn14YiwOHT7Gn0EHLzlgPI7Xbdf9AWci1CkAqR6eSvu_6J_j7eQ6wAn0XOF7lHz_5cmPFP_---krUvNsA3UT8vf5az5zu44pW6jJYc-1o0gIe2L_sw2cQ39pnc43Nc5ZxFG41UL1EPBjE98679fE_dU7B5qL77BzNppUdZle-j2939VBQRv6tPaKmw4=w1280)

Genie introduces the era of being able to generate entire interactive worlds from images or text. We also believe it will be a catalyst for training the generalist AI agents of the future. 🤖

## The Genie Team 🫶

Jake Bruce\*, Michael Dennis\*, Ashley Edwards\*, Jack Parker-Holder\*, Yuge (Jimmy) Shi\*, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, Yusuf Aytar, Sarah Bechtle, Feryal Behbahani, Stephanie Chan, Nicolas Heess, Lucy Gonzalez, Simon Osindero, Sherjil Ozair, Scott Reed, Jingwei Zhang, Konrad Zolna, Jeff Clune, Nando de Freitas, Satinder Singh, Tim Rocktäschel\*

\*Equal contribution

Please contact Ashley Edwards ([edwardsashley@google.com](mailto:edwardsashley@google.com)), Jack Parker-Holder ([jparkerholder@google.com](mailto:jparkerholder@google.com)) or Jake Bruce ([jacobbruce@google.com](mailto:jacobbruce@google.com)) for additional questions :)

### More details in the paper!

页面更新时间：

Google 网站

举报不良行为
