### 离散时间代数黎卡提方程

该问题为在满足系统状态约束（1）的情况下，寻求最优控制，最小化性能指标$\mathcal{J}$

对于系统
$$
\pmb{x}(k+1)=\pmb{x}(k)+\pmb{B\triangle g}(k) \tag{1}
$$

性能指标
$$
\mathcal{J}(\pmb{\triangle g})=\frac{1}{2}\sum_{k=0}^{\infty}(||\pmb{x}(k)||_{\pmb{Q}}^2+||\pmb{\triangle g}(k)||_{\pmb{R}}^2) \tag{2}
$$

求得$\pmb{\triangle g}(k)=-(\pmb{B}^T\pmb{P}(k)\pmb{B}+\pmb{R})^{-1}(\pmb{B}^T\pmb{P}(k))\pmb{x}(k)$

因此，在系统运行至第$k+1$个周期初始时刻时，$LQ$策略需要根据第$k$个周期的车流情况去调节第$k+1$个周期的信号配时$\pmb{g}(k+1)=\pmb{g}(k)+\pmb{\triangle g}(k)=\pmb{g}(k)-(\pmb{B}^T\pmb{P}(k)\pmb{B}+\pmb{R})^{-1}(\pmb{B}^T\pmb{P}(k))\pmb{x}(k)$。其中，$\pmb{g}(0)=\pmb{g}^N$

其中，$\pmb{P}(k)$需由$\pmb{P}(k-1)=\pmb{Q}+\pmb{P}(k)-\pmb{P}(k)\pmb{B}(\pmb{B}^T\pmb{P}(k)\pmb{B}+\pmb{R})^{-1}\pmb{B}^T\pmb{P}(k)$计算，令$\pmb{P}(T)=\pmb{Q}$

**求解黎卡提方程**

set $P_N:=Q$

for $k=N,\cdots,1$

​	$\pmb{P}(k-1)=\pmb{Q}+\pmb{P}(k)-\pmb{P}(k)\pmb{B}(\pmb{B}^T\pmb{P}(k)\pmb{B}+\pmb{R})^{-1}\pmb{B}^T\pmb{P}(k)$



其中，$\pmb{Q}=I_{4\times 4},\pmb{R}=r\pmb{I}_{4\times 4},\pmb{B}=-\pmb{I}_{4\times 4}$



**来源文献：A multivariable regulator approach to traffiffiffic-responsive network wide signal control的第三部分（The TUC strategy）**

\[相关链接][(10条消息) 【数理知识】Riccati 黎卡提 system_Zhao-Jichao的博客-CSDN博客_黎卡提方程](https://blog.csdn.net/weixin_36815313/article/details/111773535)

[(10条消息) 迭代法求黎卡提（Riccati）方程的解_肥嘟嘟的左卫门的博客-CSDN博客_riccati方程](https://blog.csdn.net/ChenGuiGan/article/details/116495061)

#### 注意：

- (2)的形式与链接资料中有差异：区间为无穷和有限/两项或三项，为此，进行了推算(LQ策略推导.pdf)。
- 无限时间和有限时间的黎卡提方程求解不知道是否一样，在这暂时使用有限时间的方法求解。
