---
title: Sherpa-Onnx 语音实时识别 /RK3588部署
date: 最新推荐文章于 2026-01-01
tags: [CSDN搬运]
---

# Sherpa-Onnx 语音实时识别 /RK3588部署

> 原文链接：[Sherpa-Onnx 语音实时识别 /RK3588部署](https://blog.csdn.net/chui_yu666/article/details/147338735)

## 环境

LubanCat4 RK3588S

ubuntu22.04 LTS

Python3.10

相关来源链接：

[预训练模型 — sherpa 1.3 文档](<https://k2-fsa.github.io/sherpa/onnx/rknn/models.html#sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16>)

[111\. 新一代Kaldi + RK NPU: 本地实时语音识别之rk3588_哔哩哔哩_bilibili](<https://www.bilibili.com/video/BV1TqXWYnEJd/?spm_id_from=333.1007.top_right_bar_window_default_collection.content.click>)

[野火]嵌入式AI应用开发实战指南—基于LubanCat-RK系列板卡 文档](<https://doc.embedfire.com/linux/rk356x/Ai/zh/latest/lubancat_ai/env/toolkit_lite2.html#id2>)

## 安装

首先安装Python环境，这里使用venv示例，可以使用conda
    
    
    python3 -m venv kaldi
    

然后激活环境
    
    
    source /kaldi/bin/activate
    

然后安装Sherpa-onnx
    
    
    pip install sherpa-onnx -f https://k2-fsa.github.io/sherpa/onnx/rk-npu-cn.html
    

检查是否具有rknn支持
    
    
    ldd $(which sherpa-onnx)
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/da8895b02d97434e9e5e220e0d483c52.png)

具体检查是否具有librknnrt.so

如果找不到 ，则表示您未能安装支持 rknn 的librknnrt.so，请手动安装

安装链接：

https://github.com/airockchip/rknn-toolkit2/blob/v2.2.0/rknpu2/runtime/Linux/librknn_api/aarch64/librknnrt.so

将librknnrt.so下载到开发板（下载过程省略）

然后将其移动到/usr/bin/目录
    
    
    sudo cp librknnrt.so /usr/lib/librknnrt.so
    

再次使用查看
    
    
    ldd $(which sherpa-onnx)
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/00a79c190c714683a64c6c07a4ee88c6.png)

如果正确显示librknnrt.so，则表示成功，如果还是未显示可以尝试重新安装sherpa-onnx库再试

## 下载
    
    
    cd ~/
    
    wget https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16.tar.bz2
    
    tar xvf sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16.tar.bz2
    
    rm sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16.tar.bz2
    

## 运行

#### 例程

测试例程：
    
    
    sherpa-onnx \
      --provider=rknn \
      --encoder=./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/encoder.rknn \
      --decoder=./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/decoder.rknn \
      --joiner=./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/joiner.rknn \
      --tokens=./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/tokens.txt \
      ./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/test_wavs/4.wav
    

输出如下：
    
    
    OnlineRecognizerConfig(feat_config=FeatureExtractorConfig(sampling_rate=16000, feature_dim=80, low_freq=20, high_freq=-400, dither=0, normalize_samples=True, snip_edges=False), model_config=OnlineModelConfig(transducer=OnlineTransducerModelConfig(encoder="./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/encoder.rknn", decoder="./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/decoder.rknn", joiner="./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/joiner.rknn"), paraformer=OnlineParaformerModelConfig(encoder="", decoder=""), wenet_ctc=OnlineWenetCtcModelConfig(model="", chunk_size=16, num_left_chunks=4), zipformer2_ctc=OnlineZipformer2CtcModelConfig(model=""), nemo_ctc=OnlineNeMoCtcModelConfig(model=""), provider_config=ProviderConfig(device=0, provider="rknn", cuda_config=CudaConfig(cudnn_conv_algo_search=1), trt_config=TensorrtConfig(trt_max_workspace_size=2147483647, trt_max_partition_iterations=10, trt_min_subgraph_size=5, trt_fp16_enable="True", trt_detailed_build_log="False", trt_engine_cache_enable="True", trt_engine_cache_path=".", trt_timing_cache_enable="True", trt_timing_cache_path=".",trt_dump_subgraphs="False" )), tokens="./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/tokens.txt", num_threads=1, warm_up=0, debug=False, model_type="", modeling_unit="cjkchar", bpe_vocab=""), lm_config=OnlineLMConfig(model="", scale=0.5, shallow_fusion=True), endpoint_config=EndpointConfig(rule1=EndpointRule(must_contain_nonsilence=False, min_trailing_silence=2.4, min_utterance_length=0), rule2=EndpointRule(must_contain_nonsilence=True, min_trailing_silence=1.2, min_utterance_length=0), rule3=EndpointRule(must_contain_nonsilence=False, min_trailing_silence=0, min_utterance_length=20)), ctc_fst_decoder_config=OnlineCtcFstDecoderConfig(graph="", max_active=3000), enable_endpoint=True, max_active_paths=4, hotwords_score=1.5, hotwords_file="", decoding_method="greedy_search", blank_penalty=0, temperature_scale=2, rule_fsts="", rule_fars="")
    ./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/test_wavs/4.wav
    Number of threads: 1, Elapsed seconds: 3.5, Audio duration (s): 18, Real time factor (RTF) = 3.5/18 = 0.2
    嗯 ON TIME比较准时 IN TIME是及时叫他总是准时教他的作业那用一般现在时是没有什么感情色彩的陈述一个事实下一句话为什么要用现在进行时它的意思并不是说说他现在正在教他的
    { "text": "嗯 ON TIME比较准时 IN TIME是及时叫他总是准时教他的作业那用一般现在时是没有什么感情色彩的陈述一个事实下一句话为什么要用现在进行时它的意思并不是说说他现在正在教他的", "tokens": ["嗯", " ON", " TIME", "比", "较", "准", "时", " IN", " TIME", "是", "及", "时", "叫", "他", "总", "是", "准", "时", "教", "他", "的", "作", "业", "那", "用", "一", "般", "现", "在", "时", "是", "没", "有", "什", "么", "感", "情", "色", "彩", "的", "陈", "述", "一", "个", "事", "实", "下", "一", "句", "话", "为", "什", "么", "要", "用", "现", "在", "进", "行", "时", "它", "的", "意", "思", "并", "不", "是", "说", "说", "他", "现", "在", "正", "在", "教", "他", "的"], "timestamps": [0.00, 0.64, 0.80, 1.12, 1.16, 1.36, 1.64, 2.00, 2.16, 2.52, 2.80, 2.92, 3.28, 3.64, 3.92, 4.16, 4.48, 4.60, 4.84, 5.12, 5.28, 5.52, 5.72, 6.20, 6.52, 6.80, 7.04, 7.28, 7.52, 7.72, 7.84, 8.08, 8.24, 8.40, 8.44, 8.68, 8.92, 9.00, 9.24, 9.48, 9.80, 9.92, 10.16, 10.32, 10.56, 10.80, 11.52, 11.60, 11.80, 11.96, 12.20, 12.32, 12.40, 12.56, 12.80, 13.12, 13.32, 13.56, 13.76, 13.92, 14.24, 14.36, 14.52, 14.68, 14.92, 15.04, 15.16, 15.32, 15.72, 16.12, 16.36, 16.48, 16.68, 16.88, 17.08, 17.24, 17.84], "ys_probs": [], "lm_probs": [], "context_scores": [], "segment": 0, "words": [], "start_time": 0.00, "is_final": false}
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ed393fda1599479199eba88ae38d8097.png)

#### 麦克风实时识别

首先，我们需要获取板上麦克风的名称：
    
    
    arecord -l
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9502e2e054164b37910df99c12b35806.png)

我们将使用 ，因此名称为 。`card 2``device 0``plughw:2,0`
    
    
    sherpa-onnx-alsa \
      --provider=rknn \
      --encoder=./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/encoder.rknn \
      --decoder=./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/decoder.rknn \
      --joiner=./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/joiner.rknn \
      --tokens=./sherpa-onnx-rk3588-streaming-zipformer-small-bilingual-zh-en-2023-02-16/tokens.txt \
      plughw:2,0
    

运行后，就可以直接使用麦克风实时流式识别了：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/4366904004084e2ba031825b7eb73b1c.png)

