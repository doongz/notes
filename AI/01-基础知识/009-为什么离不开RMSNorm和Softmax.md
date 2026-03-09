# 为什么大模型推理离不开 RMSNorm 和 Softmax？

作者：Grassroot
链接：https://zhuanlan.zhihu.com/p/1997621330464511246
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



从数值稳定性，到低精度推理与 [MoE](https://zhida.zhihu.com/search?content_id=269403097&content_type=Article&match_order=1&q=MoE&zhida_source=entity) 的系统视角

很多人第一次看 [Transformer](https://zhida.zhihu.com/search?content_id=269403097&content_type=Article&match_order=1&q=Transformer&zhida_source=entity)，会觉得 [RMSNorm](https://zhida.zhihu.com/search?content_id=269403097&content_type=Article&match_order=1&q=RMSNorm&zhida_source=entity)、Softmax 这些东西有点“多余”：

- Softmax 不就是归一化吗？
- RMSNorm 不就是防止数值太大吗？
- 推理阶段又不反向传播，真的这么重要吗？

**只要你做过大模型推理，尤其是 [INT8](https://zhida.zhihu.com/search?content_id=269403097&content_type=Article&match_order=1&q=INT8&zhida_source=entity) / [FP8](https://zhida.zhihu.com/search?content_id=269403097&content_type=Article&match_order=1&q=FP8&zhida_source=entity) / MoE 推理，就会知道答案是：必须要，而且是系统级必须。**

## 一、先说一个反直觉的结论

> **Transformer 天生是一个“数值尺度放大系统”**

它不是一个简单的线性堆叠网络，而是一个：

- 带指数算子（Softmax）
- 带加法记忆（[Residual](https://zhida.zhihu.com/search?content_id=269403097&content_type=Article&match_order=1&q=Residual&zhida_source=entity)）
- 带动态路由（MoE）

的系统。

在这种结构里，如果你不主动控制尺度，
模型会**自己制造大数、小数、极端分布**。

## 二、Softmax 在 Attention 里到底干了什么？

大多数解释都会说：

> Softmax 把注意力分数变成概率

这句话是对的，但**没有说到关键点**。

Softmax 真正重要的性质只有一个：

> **它是指数函数**

指数函数意味着什么？
意味着**微小差异会被迅速放大**。

来看一个非常真实的数值例子。

假设 attention score 是：

```text
[1.0, 1.2, 1.5]
```

Softmax 后大概是：

```text
[0.23, 0.28, 0.49]
```

现在只改一个数：

```text
[1.0, 1.2, 2.5]
```

Softmax 立刻变成：

```text
[0.05, 0.07, 0.88]
```

注意这个变化：

- score 只多了 1.0
- 权重却从 0.49 → 0.88

这说明什么？

> **Softmax 会把“略微更重要”的 token，迅速变成“几乎唯一重要”的 token**

这正是 Attention 能学会对齐、聚焦、选择的原因。

## 三、为什么 Attention 是“尺度放大器”？

Attention 的输出公式是：

```text
output = Σ αᵢ · vᵢ
```

当 Softmax 非常尖锐时：

```text
α_max ≈ 1
```

那结果就是：

```text
output ≈ 某一个 v
```

也就是说：

> Attention 可以几乎原样复制某个 token 的 value

如果这个 value 本身就比较大，那么：

- 这个“大数”会被完整放到输出
- 下一层看到的，就是一个已经被放大的表示

Attention 本身并不会“平均”数值，
它在极端情况下是**复制器**。

## 四、Residual：真正让问题不可逆的结构

如果只有 Attention，还不至于灾难。

真正危险的是这一行：

```text
x_next = x + Attention(x)
```

Residual 的本意是：

- 保留历史信息
- 稳定梯度

但从数值角度看，它意味着：

- 大值一定会被保留下来
- 小值会被逐渐淹没
- 尺度会一层一层累积

于是 Transformer 变成了：

> 一个“谁大谁活，谁小谁消失”的系统

在 FP32 / FP16 下，这个问题被表示范围掩盖了；
但在 INT8 / FP8 下，它会立刻暴露。

## 五、那能不能只靠输入预处理解决？

很多工程直觉会想：

> 我把模型输入限制在 [-1, 1]，不就安全了吗？

问题在于：

- Attention 会重新组合 token
- Softmax 会指数放大差异
- Residual 会不断叠加历史

也就是说：

> 即使输入是“干净的”，模型内部也会自己制造极端数值

**数值不稳定是结构性问题，不是输入问题。**

## 六、RMSNorm 真正解决的不是“数值爆炸”

很多资料会说：

> RMSNorm 是为了防止数值爆炸

这句话其实不够准确。

RMSNorm 真正解决的是：

> **尺度失控（scale drift）**

它做的事情非常简单：

```text
x ← x / RMS(x)
```

但效果非常关键：

- 不关心均值，只控制能量
- 保证不同 token 在同一尺度空间
- 给 Softmax 一个稳定的输入范围
- 给 Residual 一个“可叠加”的前提

一句话说清楚：

> RMSNorm 是 Transformer 的“电源稳压器”

## 七、为什么低精度推理离不开 RMSNorm？

在 INT8 / FP8 推理里，你面对的是：

- 有限的表示范围
- 饱和风险
- 量化噪声

如果没有 RMSNorm：

- Attention 的极值会直接 saturate
- Softmax 会退化成 0 / 1
- Residual 会把错误永久写进状态

你看到的现象往往不是：

> 精度掉 1%

而是：

> 模型输出行为完全异常

所以在低精度推理中：

> RMSNorm 不是性能优化，而是稳定性前提

## 八、为什么 MoE 比 Dense 更依赖 RMSNorm？

因为 MoE 引入了**不可逆放大路径**：

1. Gate Softmax（指数放大）
2. TopK 选择（离散决策）
3. Combine 加权累加（误差叠加）

MoE 的特点是：

> 一次路由错误，会影响整条计算路径

如果 token 的尺度不可比：

- Gate 会被数值大的 token 主导
- Expert 负载会严重不均
- Combine 会被单一路径垄断

这也是为什么：

> Dense 模型还能“凑合跑”，
> MoE 没有 RMSNorm，基本是必炸。

## 九、总结

- **Softmax**：让 Attention 有选择能力
- **Residual**：让历史不断累积
- **RMSNorm**：让整个系统不会失控

在大模型推理，尤其是：

- INT8 / FP8
- 长上下文
- MoE

的场景下：

> RMSNorm 不是“为了训练”，
> 而是为了让模型在推理时仍然是一个稳定系统。



