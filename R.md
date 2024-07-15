#1多因素分析
##1.1二元logist回归分析
###1.1.1装包
```{r}
install.packages("survival")
install.packages('rrtable')
install.packages('magrittr') 
install.packages("ggplot")
install.packages("dplyr")
install.packages("AER")
library("dplyr")
library("AER")
library(openxlsx) 
library(survival) 
library(rrtable)
library(ggplot2)
```

```{r}
# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv")
```

最佳cut-off值的计算
```{r}
# 假设你已经有了包含肿瘤直径和SLNM的数据集 data，其中 "Diameter" 是肿瘤直径，"SLNM" 是淋巴结转移是否

# 加载所需的包
library(pROC)

# 计算ROC曲线
roc_obj <- roc(data$Level.IV.Lymph.Node.Metastasis, data$Ipsilateral.Central.Lymph.Node.Metastases.Number)

# 根据最大Youden指数选择最佳cut-off值
best_cutoff <- coords(roc_obj, "best", ret="threshold")

# 打印最佳cut-off值
print(best_cutoff)
```



###1.1.2 logistic---最开始的那个原
```{r}
A<-fit1<-glm(Ipsilateral.Lateral.Lymph.Node.Metastasis~Age+Sex+Tumor.border+Aspect.ratio+Ingredients+Internal.echo.homogeneous+Calcification+Tumor.Peripheral.blood.flow+Tumor.internal.vascularization+Extrathyroidal.extension+Size+Location+Mulifocality+T.staging+Side.of.position+Ipsilateral.Central.Lymph.Node.Metastasis+Ipsilateral.Central.Lymph.Node.Metastasis.Rate+Ipsilateral.Central.Lymph.Node.Metastases.Number+Prelaryngeal.Lymph.Node.Metastasis+Prelaryngeal.Lymph.Node.Metastasis.Rate+Prelaryngeal.Lymph.Node.Metastases.Number+Pretracheal.Lymph.Node.Metastasis+Pretracheal.Lymph.Node.Metastasis.Rate+Pretracheal.Lymph.Node.Metastases.Number+Paratracheal.Lymph.Node.Metastasis+Paratracheal.Lymph.Node.Metastasis.Rate+Paratracheal.Lymph.Node.Metastases.Number+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Number,data=data,family = binomial())
summary(A)

coefficients(A)
exp(coefficients(A))
exp(confint(A))
coef<-summary(A)$coefficients[,1]
se<-summary(A)$coefficients[,2]
pvalue<-summary(A)$coefficients[,4]

Results<-cbind(exp(coef),exp(coef-1.96*se),exp(coef+1.96*se),pvalue)
dimnames(Results)[[2]]<-c("OR","LL","UL","p value")
Results
Results=Results[,]
View(Results)
table2docx(Results, add.rownames = FALSE)

```



##1.2森林图的绘制原
```{r}
library(ggplot2)
# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv")

# 提取模型的系数
fit1 <- glm(Ipsilateral.Lateral.Lymph.Node.Metastasis~Age+Sex+Tumor.border+Aspect.ratio+Ingredients+Internal.echo.homogeneous+Calcification+Tumor.Peripheral.blood.flow+Tumor.internal.vascularization+Extrathyroidal.extension+Size+Location+Mulifocality+T.staging+Side.of.position+Ipsilateral.Central.Lymph.Node.Metastasis+Ipsilateral.Central.Lymph.Node.Metastasis.Rate+Ipsilateral.Central.Lymph.Node.Metastases.Number+Prelaryngeal.Lymph.Node.Metastasis+Prelaryngeal.Lymph.Node.Metastasis.Rate+Prelaryngeal.Lymph.Node.Metastases.Number+Pretracheal.Lymph.Node.Metastasis+Pretracheal.Lymph.Node.Metastasis.Rate+Pretracheal.Lymph.Node.Metastases.Number+Paratracheal.Lymph.Node.Metastasis+Paratracheal.Lymph.Node.Metastasis.Rate+Paratracheal.Lymph.Node.Metastases.Number+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Number, data = data, family = binomial())

coefficients <- coef(fit1)

# 创建系数数据框
coef_df <- data.frame(
  variable = names(coefficients),
  coefficient = coefficients,
  odds_ratio = exp(coefficients),
  p_value = summary(fit1)$coefficients[, "Pr(>|z|)"],
  ci_lower = exp(confint(fit1)[, 1]),  # 使用指数化的置信区间
  ci_upper = exp(confint(fit1)[, 2])   # 使用指数化的置信区间
)

# 将(Intercept)标签改为Intercept
coef_df$variable[coef_df$variable == "(Intercept)"] <- "Intercept"

# 手动设置变量顺序并反转
variable_order <- c("Intercept","Age","Sex","Tumor.border","Aspect.ratio","Ingredients","Internal.echo.homogeneous","Calcification","Tumor.Peripheral.blood.flow","Tumor.internal.vascularization","Extrathyroidal.extension","Size","Location","Mulifocality","T.staging","Side.of.position","Ipsilateral.Central.Lymph.Node.Metastasis","Ipsilateral.Central.Lymph.Node.Metastasis.Rate","Ipsilateral.Central.Lymph.Node.Metastases.Number","Prelaryngeal.Lymph.Node.Metastasis","Prelaryngeal.Lymph.Node.Metastasis.Rate","Prelaryngeal.Lymph.Node.Metastases.Number","Pretracheal.Lymph.Node.Metastasis","Pretracheal.Lymph.Node.Metastasis.Rate","Pretracheal.Lymph.Node.Metastases.Number","Paratracheal.Lymph.Node.Metastasis","Paratracheal.Lymph.Node.Metastasis.Rate","Paratracheal.Lymph.Node.Metastases.Number","Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis","Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate","Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Number")
coef_df$variable <- factor(coef_df$variable, levels = rev(variable_order))

# 创建森林图
forest_plot <- ggplot(coef_df, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper), height = 0.2, color = "black") +
  geom_point(aes(color = p_value < 0.05), size = 2) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""), x = -20, hjust = -0.1), size = 2.5) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 20, hjust = 1.1), size = 2.5) +
  coord_cartesian(xlim = c(-20, 20)) +
  scale_color_manual(values = c("black", "red"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Ipsilateral Lateral Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal()

# 显示森林图
print(forest_plot)


```


#1.3排序森林图原
```{r}
library(ggplot2)

# 提取模型的系数
fit1 <- glm(II.Level.Lymph.Node.Metastasis~Age+Sex+Tumor.border+Aspect.ratio+Internal.echo.pattern+Internal.echo.homogeneous+Calcification+Tumor.Peripheral.blood.flow+Tumor.internal.vascularization+Extrathyroidal.extension+Size+Location+Mulifocality+T.staging+Ipsilateral.Central.Lymph.Node.Metastasis+Ipsilateral.Central.Lymph.Node.Metastasis.Rate+Ipsilateral.Central.Lymph.Node.Metastases.Number+Prelaryngeal.Lymph.Node.Metastasis+Prelaryngeal.Lymph.Node.Metastasis.Rate+Prelaryngeal.Lymph.Node.Metastases.Number+Pretracheal.Lymph.Node.Metastasis+Pretracheal.Lymph.Node.Metastasis.Rate+Pretracheal.Lymph.Node.Metastases.Number+Paratracheal.Lymph.Node.Metastasis+Paratracheal.Lymph.Node.Metastasis.Rate+Paratracheal.Lymph.Node.Metastases.Number+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Number, data = data, family = binomial())
coefficients <- coef(fit1)

# 创建系数数据框
coef_df <- data.frame(
  variable = names(coefficients),
  coefficient = coefficients,
  odds_ratio = exp(coefficients),
  p_value = summary(fit1)$coefficients[, "Pr(>|z|)"],
  ci_lower = exp(confint(fit1)[, 1]),  # 使用指数化的置信区间
  ci_upper = exp(confint(fit1)[, 2])   # 使用指数化的置信区间
)

# 将数据框按照Odds Ratio值由小到大排序
coef_df <-coef_df[order(-coef_df$odds_ratio), ]
coef_df$variable <- factor(coef_df$variable, levels = coef_df$variable) # 按照排序后的顺序设置变量因子

# 创建森林图
forest_plot <- ggplot(coef_df, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper), height = 0.2, color = "black") +
  geom_point(aes(color = p_value < 0.05), size = 2) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""), x = -20, hjust = -0.1), size = 2.5) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 20, hjust = 1.1), size = 2.5) +
  coord_cartesian(xlim = c(-20, 20)) +
  scale_color_manual(values = c("black", "red"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "II Level Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal()

# 显示森林图
print(forest_plot)

```

#调整尺寸排序森林图和具体的数值之侧区
```{r}
# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv", check.names = FALSE)

# 设置列名
colnames(data) <- c("Age","Sex","Classification of BMI","Tumor border","Aspect ratio","Composition",	
                    "Internal echo pattern","Internal echo homogeneous","Calcification",
                    "Tumor internal vascularization","Tumor Peripheral blood flow","Size","Location",
                    "Mulifocality","Hashimoto","Extrathyroidal extension","Side of position",	
                    "Ipsilateral Central Lymph Node Metastasis","Prelaryngeal Lymph Node Metastasis",
                    "Pretracheal Lymph Node Metastasis","Paratracheal Lymph Node Metastasis",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis","Ipsilateral Lateral Lymph Node Metastasis",
                    "Level II Lymph Node Metastasis","Level III Lymph Node Metastasis","Level IV Lymph Node Metastasis",
                    "T staging","age","size","Ipsilateral Central Lymph Node Metastasis Rate",
                    "Ipsilateral Central Lymph Node Metastases Number","Prelaryngeal Lymph Node Metastasis Rate",
                    "Prelaryngeal Lymph Node Metastases Number","Pretracheal Lymph Node Metastasis Rate",
                    "Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
                    "Paratracheal Lymph Node Metastases Number", "Recurrent Laryngeal Nerve Lymph Node Metastasis Rate",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis Number")



# 构建初始模型
initial_model <- glm(`Ipsilateral Lateral Lymph Node Metastasis` ~Age+Sex+`Tumor border`+`Aspect ratio`+Composition+`Internal echo homogeneous` +Calcification+`Tumor Peripheral blood flow`+`Tumor internal vascularization`+`Extrathyroidal extension`+Size+Location+Mulifocality+`T staging`+`Side of position`+`Ipsilateral Central Lymph Node Metastasis`+`Ipsilateral Central Lymph Node Metastasis Rate` + `Ipsilateral Central Lymph Node Metastases Number` + `Prelaryngeal Lymph Node Metastasis` + `Prelaryngeal Lymph Node Metastasis Rate` + `Prelaryngeal Lymph Node Metastases Number` + `Pretracheal Lymph Node Metastasis` + `Pretracheal Lymph Node Metastasis Rate` + `Pretracheal Lymph Node Metastases Number` + `Paratracheal Lymph Node Metastasis` + `Paratracheal Lymph Node Metastasis Rate` + `Paratracheal Lymph Node Metastases Number` + `Recurrent Laryngeal Nerve Lymph Node Metastasis` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Rate` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Number`, data = data, family = binomial())


# 计算VIF值
vif_values <- vif(initial_model)
print(vif_values)

# 移除高VIF值的变量（假设阈值为5）
selected_vars <- names(vif_values[vif_values < 5])

# 重新构建模型，消除共线性
formula <- as.formula(paste("`Ipsilateral Lateral Lymph Node Metastasis` ~", paste(selected_vars, collapse = " + ")))
final_model <- glm(formula, data = data, family = binomial())

# 提取模型系数
coefficients <- coef(final_model)

# 创建系数数据框
coef_df <- data.frame(
  variable = names(coefficients),
  coefficient = coefficients,
  odds_ratio = exp(coefficients),
  p_value = summary(final_model)$coefficients[, "Pr(>|z|)"],
  ci_lower = exp(confint(final_model)[, 1]),
  ci_upper = exp(confint(final_model)[, 2])
)

# 将(Intercept)标签改为Intercept
coef_df$variable[coef_df$variable == "(Intercept)"] <- "Intercept"

# 手动设置变量顺序并反转
variable_order <- c("Intercept", selected_vars)
coef_df$variable <- factor(coef_df$variable, levels = rev(variable_order))

# 创建初始森林图
forest_plot <- ggplot(coef_df, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper), height = 0.2, color = "black") +
  geom_point(aes(color = p_value < 0.05), size = 2) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""), 
                x = -20, hjust = -0.1), size = 2.5) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1), size = 2.5) +
  coord_cartesian(xlim = c(-20, 20)) +
  scale_color_manual(values = c("black", "goldenrod"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Ipsilateral Lateral Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal()

# 显示初始森林图
#print(forest_plot)
# 保存初始森林图
#ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/1.侧区多因素分析_森林图按输入变量的顺序.png", plot = forest_plot)


# 保存图像函数
save_forest_plot <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果"

# 保存
save_forest_plot(forest_plot, file.path(output_folder, "1.侧区多因素分析_森林图按输入变量的顺序"))

print(forest_plot)



coef_df_sorted <- coef_df[order(coef_df$odds_ratio), ]
coef_df_sorted <- rbind(coef_df_sorted[coef_df_sorted$variable != "Intercept", ], coef_df_sorted[coef_df_sorted$variable == "Intercept", ])
coef_df_sorted$variable <- factor(coef_df_sorted$variable, levels = coef_df_sorted$variable)

forest_plot_sorted <- ggplot(coef_df_sorted, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "goldenrod"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Ipsilateral Lateral Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df_sorted$p_value < 0.05, "goldenrod", "black")))


# 显示排序后的森林图
print(forest_plot_sorted)

# 导出结果到CSV文件并反转顺序
write.csv(coef_df[nrow(coef_df):1, ], "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/1.侧区多因素分析按输入变量的顺序.csv", row.names = FALSE)
write.csv(coef_df_sorted[nrow(coef_df_sorted):1, ], "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/1.侧区多因素分析按OR值的顺序.csv", row.names = FALSE)

# 保存排序后的森林图
#ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/1.侧区多因素分析_森林图_按OR值的顺序.png", plot = forest_plot_sorted)


# 保存图像函数
save_forest_plot_sorted <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果"

# 保存
save_forest_plot_sorted(forest_plot_sorted, file.path(output_folder, "1.侧区多因素分析_森林图_按OR值的顺序"))

print(forest_plot_sorted)



```



##注意！这是为了按输入变量的顺序输出的森林图改尺寸和颜色
```{r}
library(car)
library(ggplot2)


# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv", check.names = FALSE)

# 设置列名
colnames(data) <- c("Age","Sex","Classification of BMI","Tumor border","Aspect ratio","Composition",	
                    "Internal echo pattern","Internal echo homogeneous","Calcification",
                    "Tumor internal vascularization","Tumor Peripheral blood flow","Size","Location",
                    "Mulifocality","Hashimoto","Extrathyroidal extension","Side of position",	
                    "Ipsilateral Central Lymph Node Metastasis","Prelaryngeal Lymph Node Metastasis",
                    "Pretracheal Lymph Node Metastasis","Paratracheal Lymph Node Metastasis",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis","Ipsilateral Lateral Lymph Node Metastasis",
                    "Level II Lymph Node Metastasis","Level III Lymph Node Metastasis","Level IV Lymph Node Metastasis",
                    "T staging","age","size","Ipsilateral Central Lymph Node Metastasis Rate",
                    "Ipsilateral Central Lymph Node Metastases Number","Prelaryngeal Lymph Node Metastasis Rate",
                    "Prelaryngeal Lymph Node Metastases Number","Pretracheal Lymph Node Metastasis Rate",
                    "Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
                    "Paratracheal Lymph Node Metastases Number", "Recurrent Laryngeal Nerve Lymph Node Metastasis Rate",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis Number")



# 构建初始模型
initial_model <- glm(`Ipsilateral Lateral Lymph Node Metastasis` ~Age+Sex+`Tumor border`+`Aspect ratio`+Composition+`Internal echo homogeneous` +Calcification+`Tumor Peripheral blood flow`+`Tumor internal vascularization`+`Extrathyroidal extension`+Size+Location+Mulifocality+`T staging`+`Side of position`+`Ipsilateral Central Lymph Node Metastasis`+`Ipsilateral Central Lymph Node Metastasis Rate` + `Ipsilateral Central Lymph Node Metastases Number` + `Prelaryngeal Lymph Node Metastasis` + `Prelaryngeal Lymph Node Metastasis Rate` + `Prelaryngeal Lymph Node Metastases Number` + `Pretracheal Lymph Node Metastasis` + `Pretracheal Lymph Node Metastasis Rate` + `Pretracheal Lymph Node Metastases Number` + `Paratracheal Lymph Node Metastasis` + `Paratracheal Lymph Node Metastasis Rate` + `Paratracheal Lymph Node Metastases Number` + `Recurrent Laryngeal Nerve Lymph Node Metastasis` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Rate` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Number`, data = data, family = binomial())


# 计算VIF值
vif_values <- vif(initial_model)
print(vif_values)

# 移除高VIF值的变量（假设阈值为5）
selected_vars <- names(vif_values[vif_values < 5])

# 重新构建模型，消除共线性
formula <- as.formula(paste("`Ipsilateral Lateral Lymph Node Metastasis` ~", paste(selected_vars, collapse = " + ")))
final_model <- glm(formula, data = data, family = binomial())

# 提取模型系数
coefficients <- coef(final_model)

# 创建系数数据框
coef_df <- data.frame(
  variable = names(coefficients),
  coefficient = coefficients,
  odds_ratio = exp(coefficients),
  p_value = summary(final_model)$coefficients[, "Pr(>|z|)"],
  ci_lower = exp(confint(final_model)[, 1]),
  ci_upper = exp(confint(final_model)[, 2])
)

# 计算95%置信区间
coef_df$LL <- coef_df$ci_lower
coef_df$UL <- coef_df$ci_upper

# 将(Intercept)标签改为Intercept
coef_df$variable[coef_df$variable == "(Intercept)"] <- "Intercept"

# 手动设置变量顺序并反转
variable_order <- c("Intercept", selected_vars)
coef_df$variable <- factor(coef_df$variable, levels = rev(variable_order))

# 创建初始森林图
forest_plot <- ggplot(coef_df, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "goldenrod"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Ipsilateral Lateral Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df$p_value < 0.05,"goldenrod","black")))

# 显示初始森林图
print(forest_plot)


coef_df_sorted <- coef_df[order(coef_df$variable), ]
coef_df_sorted <- rbind(coef_df_sorted[coef_df_sorted$variable != "Intercept", ], coef_df_sorted[coef_df_sorted$variable == "Intercept", ])
coef_df_sorted$variable <- factor(coef_df_sorted$variable, levels = coef_df_sorted$variable)

forest_plot_sorted <- ggplot(coef_df_sorted, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "goldenrod"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Ipsilateral Lateral Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df_sorted$p_value < 0.05, "goldenrod", "black")))

# 显示排序后的森林图
print(forest_plot_sorted)

# 保存排序后的森林图
#ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/1.侧区多因素分析_森林图按输入变量的顺序.png", plot = forest_plot_sorted)


# 保存图像函数
save_forest_plot_sorted <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果"

# 保存
save_forest_plot_sorted(forest_plot_sorted, file.path(output_folder, "1.侧区多因素分析_森林图按输入变量的顺序"))

print(forest_plot_sorted)


```



#3列线图的绘制

##3.1列线图以及验证曲线的代码
```{r}
#install.packages("foreign")
#install.packages("rms")
library(foreign) 
library(rms)
# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv")

```

##3.2赋值
```{r}
data$Age<-factor(data$Age,levels = c(1,0),labels = c("age≤43","age>43"))
data$Sex<-factor(data$Sex,levels = c(0,1),labels = c("Female","Male"))

data$Tumor.border<-factor(data$Tumor.border,levels = c(0,1,2),labels = c("smooth or borderless","irregular shape or lsharpobed","extrandular invasion"))
data$Aspect.ratio<-factor(data$Aspect.ratio,levels = c(0,1),labels = c("≤1",">1"))
 data$Composition<-factor(data$Composition,levels = c(0,1,2),labels = c("cystic/cavernous","Mixed cystic and solid","solid"))
 data$Internal.echo.pattern<-factor(data$Internal.echo.pattern,levels = c(0,1,2,3),labels = c("echoless","high/isoechoic","hypoechoic","very hypoechoic"))
 data$Internal.echo.homogeneous<-factor(data$Internal.echo.homogeneous,levels = c(0,1),labels = c("Non-uniform","Uniform"))
 data$Calcification<-factor(data$Calcification,levels = c(0,1,2,3),labels = c("no or large comet tail", "coarse calcification","peripheral calcification","Microcalcification"))
data$Tumor.internal.vascularization<-factor(data$Tumor.internal.vascularization,levels = c(0,1),labels = c("Without","Abundant"))
data$Tumor.Peripheral.blood.flow<-factor(data$Tumor.Peripheral.blood.flow,levels = c(0,1),labels = c("Without","Abundant"))
data$Size<-factor(data$Size,levels = c(0,1),labels = c("≤10.5", ">10.5"))
data$Location<-factor(data$Location,levels = c(0,1),labels = c("Non-upper","Upper"))

data$Mulifocality<-factor(data$Mulifocality,levels = c(1,0),labels = c("Abundant", "Without"))
data$Hashimoto<-factor(data$Hashimoto,levels = c(0,1),labels = c("Abundant", "Without"))
data$Extrathyroidal.extension<-factor(data$Extrathyroidal.extension,levels = c(1,0),labels = c("Abundant", "Without"))


data$Side.of.position<-factor(data$Side.of.position,levels = c(0,1,2,3),labels = c("left","right","bilateral" ,"isthmus"))

data$Ipsilateral.Central.Lymph.Node.Metastasis<-factor(data$Ipsilateral.Central.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))
data$Prelaryngeal.Lymph.Node.Metastasis<-factor(data$Prelaryngeal.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))
data$Paratracheal.Lymph.Node.Metastasis<-factor(data$Paratracheal.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))
data$Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis<-factor(data$Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))


```


```{r}
### 4.1.2 整合数据
x <- as.data.frame(data)
dd <- datadist(data)
options(datadist = 'dd')

### 4.2 Logistic回归比GLM好用
fit1 <- lrm(Ipsilateral.Lateral.Lymph.Node.Metastasis ~ Tumor.border + Aspect.ratio + Calcification + Tumor.internal.vascularization + Extrathyroidal.extension + Size + Location + Ipsilateral.Central.Lymph.Node.Metastasis + Prelaryngeal.Lymph.Node.Metastasis + Paratracheal.Lymph.Node.Metastasis + Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis,
            data = data, x = TRUE, y = TRUE)

fit1
summary(fit1) # 可以直接给到一些结果很好

nom1 <- nomogram(fit1, fun = plogis, fun.at = c(.001, .01, .05, seq(.1, .9, by = .1), .95, .99, .999),
                 lp = FALSE, funlabel = "Ipsilateral Lateral Lymph Node Metastasis")
plot(nom1)

### 4.4 验证曲线
cal1 <- calibrate(fit1, method = 'boot', B = 1000)
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))

# 保存列线图为1200 DPI的 .tiff格式
tiff("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/nomogram.tiff", width = 8, height = 6, units = "in", res = 1200, compression = "lzw")
plot(nom1)
dev.off()

# 保存列线图为1200 DPI的 .png格式
png("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/nomogram.png", width = 8, height = 6, units = "in", res = 1200)
plot(nom1)
dev.off()

# 保存列线图为1200 DPI的 .eps格式
postscript("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/nomogram.eps", width = 8, height = 6, horizontal = FALSE, onefile = FALSE, paper = "special")
plot(nom1)
dev.off()

# 保存验证曲线为1200 DPI的 .tiff格式
tiff("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/calibration.tiff", width = 8, height = 6, units = "in", res = 1200, compression = "lzw")
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))
dev.off()

# 保存验证曲线为1200 DPI的 .png格式
png("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/calibration.png", width = 8, height = 6, units = "in", res = 1200)
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))
dev.off()

# 保存验证曲线为1200 DPI的 .eps格式
postscript("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/calibration.eps", width = 8, height = 6, horizontal = FALSE, onefile = FALSE, paper = "special")
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))
dev.off()



```


###4.1.2 调整列线图的图间距和因子名称的大小和间距
```{r}
# 设置绘图参数
par(mar = c(1, 2, 2, 2))  # 调整绘图边距

# 创建 nomogram
nom2 <- nomogram(fit1, fun = plogis, fun.at = c(0.001, 0.01, 0.05, seq(0.1, 0.9, by = 0.1), 0.95, 0.99, 0.999),
                 lp = FALSE, funlabel="Ipsilateral Lateral Lymph Node Metastasis")

# 绘制 nomogram
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)


# 保存列线图为1200 DPI的 .tiff格式
tiff("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/nomogram.tiff", width = 8, height = 6, units = "in", res = 1200, compression = "lzw")
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)
dev.off()

# 保存列线图为1200 DPI的 .png格式
png("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/nomogram.png", width = 8, height = 6, units = "in", res = 1200)
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)
dev.off()

# 保存列线图为1200 DPI的 .eps格式
postscript("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/nomogram.eps", width = 8, height = 6, horizontal = FALSE, onefile = FALSE, paper = "special")
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)
dev.off()







```


##3.2列线图ROC曲线的绘制--单roc

```{r}
# 加载必要的库
library(pROC)
library(ggplot2)

# 读取数据
train_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值矫正后.csv")
test_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/2.验证集编码填补缺失值矫正后.csv")

# 将训练数据按照7:3的比例随机分为训练集和验证集
# 设置随机数种子,以确保结果可复现
set.seed(123)
index <- 1:nrow(train_data)
shuffled_index <- sample(index)
tra_ratio <- 0.7  # 训练集比例
tra_size <- round(tra_ratio * nrow(train_data))
tra_data <- train_data[shuffled_index[1:tra_size], ]
val_data <- train_data[shuffled_index[(tra_size + 1):nrow(train_data)], ]

cat("训练集观测数量:", nrow(tra_data), "\n")
cat("验证集观测数量:", nrow(val_data), "\n")
cat("测试集观测数量:", nrow(test_data), "\n")

# 构建模型
fit1 <- glm(Ipsilateral.Lateral.Lymph.Node.Metastasis ~ Tumor.border + Aspect.ratio + Calcification + Tumor.internal.vascularization + Extrathyroidal.extension + Size + Location +Pretracheal.Lymph.Node.Metastasis+ Prelaryngeal.Lymph.Node.Metastasis+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis,
            data = tra_data, family = binomial())

# 预测概率
train_probs <- predict(fit1, newdata = tra_data, type = "response")
val_probs <- predict(fit1, newdata = val_data, type = "response")
test_probs <- predict(fit1, newdata = test_data, type = "response")

train_response <- tra_data$Ipsilateral.Lateral.Lymph.Node.Metastasis
val_response <- val_data$Ipsilateral.Lateral.Lymph.Node.Metastasis
test_response <- test_data$Ipsilateral.Lateral.Lymph.Node.Metastasis

# 创建ROC对象
train_roc <- roc(train_response, train_probs)
val_roc <- roc(val_response, val_probs)
test_roc <- roc(test_response, test_probs)

# 提取ROC曲线的坐标点
train_roc_data <- coords(train_roc, "all", ret = c("specificity", "sensitivity"))
val_roc_data <- coords(val_roc, "all", ret = c("specificity", "sensitivity"))
test_roc_data <- coords(test_roc, "all", ret = c("specificity", "sensitivity"))

# 转换为数据框
train_roc_data <- as.data.frame(train_roc_data)
val_roc_data <- as.data.frame(val_roc_data)
test_roc_data <- as.data.frame(test_roc_data)

# 绘制ROC曲线
roc_plot <- ggplot() +
  geom_line(data = train_roc_data, aes(x = 1 - specificity, y = sensitivity), color = "goldenrod", size = 0.6) +
  geom_line(data = val_roc_data, aes(x = 1 - specificity, y = sensitivity), color = "orange", size = 0.6) +
  geom_line(data = test_roc_data, aes(x = 1 - specificity, y = sensitivity), color = "gold", size = 0.6) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "black") +
  labs(title = "ROC for Ipsilateral Lateral Lymph Node Metastasis Nomogram Prediction",
       x = "False Positive Rate", y = "True Positive Rate") +
  theme_minimal() +
  theme(legend.position = "none") +
  annotate("text", x = 0.7, y = 0.4, label = paste("Train set AUC =", round(auc(train_roc), 3)), size = 4, color = "goldenrod") +
  annotate("text", x = 0.7, y = 0.3, label = paste("Validation set AUC =", round(auc(val_roc), 3)), size = 4, color = "orange") +
  annotate("text", x = 0.7, y = 0.2, label = paste("Test set AUC =", round(auc(test_roc), 3)), size = 4, color = "gold")

# 保存ROC曲线为.tiff格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/roc_curve.tiff", plot = roc_plot, width = 8, height = 6, units = "in", dpi = 1200, compression = "lzw")

# 保存ROC曲线为.png格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/roc_curve.png", plot = roc_plot, width = 8, height = 6, units = "in", dpi = 1200)

# 保存ROC曲线为.eps格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/roc_curve.eps", plot = roc_plot, width = 8, height = 6, units = "in", dpi = 1200)

```


```{r}
# 加载必要的库
library(pROC)
library(ggplot2)
library(dplyr)

# 读取数据
train_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值矫正后.csv")
test_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/2.验证集编码填补缺失值矫正后.csv")

# 按均值填补缺失值
fill_na_with_mean <- function(df) {
  df %>%
    mutate(across(everything(), ~ ifelse(is.na(.), mean(., na.rm = TRUE), .)))
}

train_data <- fill_na_with_mean(train_data)
test_data <- fill_na_with_mean(test_data)

# 将训练数据按照7:3的比例随机分为训练集和验证集
set.seed(123)
index <- 1:nrow(train_data)
shuffled_index <- sample(index)
tra_ratio <- 0.7  # 训练集比例
tra_size <- round(tra_ratio * nrow(train_data))
tra_data <- train_data[shuffled_index[1:tra_size], ]
val_data <- train_data[shuffled_index[(tra_size + 1):nrow(train_data)], ]

cat("训练集观测数量:", nrow(tra_data), "\n")
cat("验证集观测数量:", nrow(val_data), "\n")
cat("测试集观测数量:", nrow(test_data), "\n")

# 构建模型
fit1 <- glm(Ipsilateral.Lateral.Lymph.Node.Metastasis ~ Tumor.border + Aspect.ratio + Calcification + Tumor.internal.vascularization +Extrathyroidal.extension + Size + Location+Ipsilateral.Central.Lymph.Node.Metastasis +Prelaryngeal.Lymph.Node.Metastasis +Paratracheal.Lymph.Node.Metastasis +Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis,
            data = tra_data, family = binomial())

# 预测概率
train_probs <- predict(fit1, newdata = tra_data, type = "response")
val_probs <- predict(fit1, newdata = val_data, type = "response")
test_probs <- predict(fit1, newdata = test_data, type = "response")

train_response <- tra_data$Ipsilateral.Lateral.Lymph.Node.Metastasis
val_response <- val_data$Ipsilateral.Lateral.Lymph.Node.Metastasis
test_response <- test_data$Ipsilateral.Lateral.Lymph.Node.Metastasis


# 定义净收益计算函数
net_benefit <- function(probs, outcome, threshold) {
  tp <- sum(outcome == 1 & probs >= threshold)
  fp <- sum(outcome == 0 & probs >= threshold)
  total_population <- length(outcome)
  
  if (total_population == 0) {
    return(0)
  }
  
  net_benefit <- (tp / total_population) - ((fp / total_population) * (threshold / (1 - threshold)))
  return(net_benefit)
}

# 计算不同阈值下的净收益
thresholds <- seq(0, 1, by = 0.01)
train_net_benefits <- sapply(thresholds, function(x) net_benefit(train_probs, train_response, x))
val_net_benefits <- sapply(thresholds, function(x) net_benefit(val_probs, val_response, x))
test_net_benefits <- sapply(thresholds, function(x) net_benefit(test_probs, test_response, x))

# 计算所有人都进行干预时的净收益
all_net_benefit <- sapply(thresholds, function(x) net_benefit(rep(1, length(val_response)), val_response, x))

# 计算没有人进行干预时的净收益
none_net_benefit <- rep(0, length(thresholds))

# 找到最大净收益点
train_max_nb <- max(train_net_benefits)
train_max_nb_threshold <- thresholds[which.max(train_net_benefits)]
val_max_nb <- max(val_net_benefits)
val_max_nb_threshold <- thresholds[which.max(val_net_benefits)]
test_max_nb <- max(test_net_benefits)
test_max_nb_threshold <- thresholds[which.max(test_net_benefits)]

# 绘制DCA曲线
dca_data <- data.frame(
  threshold = thresholds,
  train_net_benefit = train_net_benefits,
  val_net_benefit = val_net_benefits,
  test_net_benefit = test_net_benefits,
  all_net_benefit = all_net_benefit,
  none_net_benefit = none_net_benefit
)

dca_plot <- ggplot(dca_data, aes(x = threshold)) +
  geom_line(aes(y = train_net_benefit, color = "Train set"), size = 0.6) +
  geom_line(aes(y = val_net_benefit, color = "Test set"), size = 0.6) +
  geom_line(aes(y = test_net_benefit, color = "Validation set"), size = 0.6) +
  geom_line(aes(y = all_net_benefit, color = "All"), linetype = "dotted", size = 0.6) +
  geom_line(aes(y = none_net_benefit, color = "None"), linetype = "solid", size = 0.6) +
  labs(title = "DCA for Ipsilateral Lateral Lymph Node Metastasis Nomogram Prediction",
       x = "Threshold Probability", y = "Net Benefit") +
  scale_color_manual(values = c("Train set" = "goldenrod", "Test set" = "orange", "Validation set" = "gold", "All" = "grey", "None" = "black")) +
  theme_minimal() +
  theme(legend.position = "right") +
  annotate("text", x = 0.4, y = 0.1, label = "Train set", size = 4, color = "goldenrod") +
  annotate("text", x = 0.4, y = 0.05, label = "Test set", size = 4, color = "orange") +
  annotate("text", x = 0.4, y = 0.01, label = "Validation set", size = 4, color = "gold") +
  annotate("text", x = train_max_nb_threshold, y = train_max_nb, label = sprintf("Max: %.3f", train_max_nb), color = "goldenrod", vjust = -1) +
  annotate("text", x = val_max_nb_threshold, y = val_max_nb, label = sprintf("Max: %.3f", val_max_nb), color = "orange", vjust = -1) +
  annotate("text", x = test_max_nb_threshold, y = test_max_nb, label = sprintf("Max: %.3f", test_max_nb), color = "gold", vjust = -1) +
  coord_cartesian(ylim = c(-0.05, 0.5), xlim = c(0, 0.8))


# 保存ROC曲线为.tiff格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/dca_curve.tiff", plot = dca_plot, width = 8, height = 6, units = "in", dpi = 1200, compression = "lzw")

# 保存ROC曲线为.png格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/dca_curve.png", plot = dca_plot, width = 8, height = 6, units = "in", dpi = 1200)

# 保存ROC曲线为.eps格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/1、侧区的结果/dca_curve.eps", plot = dca_plot, width = 8, height = 6, units = "in", dpi = 1200)

print(dca_plot)

```

```{r}
library(car)
library(ggplot2)

# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv", check.names = FALSE)

# 设置列名
colnames(data) <- c("Age","Sex","Classification of BMI","Tumor border","Aspect ratio","Composition",	
                    "Internal echo pattern","Internal echo homogeneous","Calcification",
                    "Tumor internal vascularization","Tumor Peripheral blood flow","Size","Location",
                    "Mulifocality","Hashimoto","Extrathyroidal extension","Side of position",	
                    "Ipsilateral Central Lymph Node Metastasis","Prelaryngeal Lymph Node Metastasis",
                    "Pretracheal Lymph Node Metastasis","Paratracheal Lymph Node Metastasis",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis","Ipsilateral Lateral Lymph Node Metastasis",
                    "Level II Lymph Node Metastasis","Level III Lymph Node Metastasis","Level IV Lymph Node Metastasis",
                    "T staging","age","size","Ipsilateral Central Lymph Node Metastasis Rate",
                    "Ipsilateral Central Lymph Node Metastases Number","Prelaryngeal Lymph Node Metastasis Rate",
                    "Prelaryngeal Lymph Node Metastases Number","Pretracheal Lymph Node Metastasis Rate",
                    "Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
                    "Paratracheal Lymph Node Metastases Number", "Recurrent Laryngeal Nerve Lymph Node Metastasis Rate",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis Number")



# 构建初始模型
initial_model <- glm(`Level II Lymph Node Metastasis` ~Age+Sex+`Tumor border`+`Aspect ratio`+`Internal echo pattern`+`Internal echo homogeneous` +Calcification+`Tumor Peripheral blood flow`+`Tumor internal vascularization`+`Extrathyroidal extension`+Size+Location+Mulifocality+`T staging`+`Ipsilateral Central Lymph Node Metastasis`+`Ipsilateral Central Lymph Node Metastasis Rate` + `Ipsilateral Central Lymph Node Metastases Number` + `Prelaryngeal Lymph Node Metastasis` + `Prelaryngeal Lymph Node Metastasis Rate` + `Prelaryngeal Lymph Node Metastases Number` + `Pretracheal Lymph Node Metastasis` + `Pretracheal Lymph Node Metastasis Rate` + `Pretracheal Lymph Node Metastases Number` + `Paratracheal Lymph Node Metastasis` + `Paratracheal Lymph Node Metastasis Rate` + `Paratracheal Lymph Node Metastases Number` + `Recurrent Laryngeal Nerve Lymph Node Metastasis` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Rate` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Number`, data = data, family = binomial())

# 计算VIF值
vif_values <- vif(initial_model)
print(vif_values)

# 移除高VIF值的变量（假设阈值为5）
selected_vars <- names(vif_values[vif_values < 5.878])

# 重新构建模型，消除共线性
formula <- as.formula(paste("`Level II Lymph Node Metastasis` ~", paste(selected_vars, collapse = " + ")))
final_model <- glm(formula, data = data, family = binomial())

# 提取模型系数
coefficients <- coef(final_model)

# 创建系数数据框
coef_df <- data.frame(
  variable = names(coefficients),
  coefficient = coefficients,
  odds_ratio = exp(coefficients),
  p_value = summary(final_model)$coefficients[, "Pr(>|z|)"],
  ci_lower = exp(confint(final_model)[, 1]),
  ci_upper = exp(confint(final_model)[, 2])
)

# 将(Intercept)标签改为Intercept
coef_df$variable[coef_df$variable == "(Intercept)"] <- "Intercept"

# 手动设置变量顺序并反转
variable_order <- c("Intercept", selected_vars)
coef_df$variable <- factor(coef_df$variable, levels = rev(variable_order))

# 创建初始森林图
forest_plot <- ggplot(coef_df, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper), height = 0.2, color = "black") +
  geom_point(aes(color = p_value < 0.05), size = 2) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""), 
                x = -20, hjust = -0.1), size = 2.5) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1), size = 2.5) +
  coord_cartesian(xlim = c(-20, 20)) +
  scale_color_manual(values = c("black", "#C71585"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level II Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal()

# 保存图像函数
save_forest_plot <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果"

# 保存
save_forest_plot(forest_plot, file.path(output_folder, "1.2区多因素分析_森林图按输入变量的顺序"))

print(forest_plot)


coef_df_sorted <- coef_df[order(coef_df$odds_ratio), ]
coef_df_sorted <- rbind(coef_df_sorted[coef_df_sorted$variable != "Intercept", ], coef_df_sorted[coef_df_sorted$variable == "Intercept", ])
coef_df_sorted$variable <- factor(coef_df_sorted$variable, levels = coef_df_sorted$variable)

forest_plot_sorted <- ggplot(coef_df_sorted, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "#C71585"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level II Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df_sorted$p_value < 0.05, "#C71585", "black")))


# 显示排序后的森林图
print(forest_plot_sorted)

# 导出结果到CSV文件并反转顺序
write.csv(coef_df[nrow(coef_df):1, ], "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/1.2区多因素分析按输入变量的顺序.csv", row.names = FALSE)
write.csv(coef_df_sorted[nrow(coef_df_sorted):1, ], "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/1.2区多因素分析按OR值的顺序.csv", row.names = FALSE)

# 保存图像函数
save_forest_plot_sorted <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果"

# 保存
save_forest_plot_sorted(forest_plot_sorted, file.path(output_folder, "1.2区多因素分析_森林图_按OR值的顺序"))

print(forest_plot_sorted)



```
```{r}
library(car)
library(ggplot2)

# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv", check.names = FALSE)

# 设置列名
colnames(data) <- c("Age","Sex","Classification of BMI","Tumor border","Aspect ratio","Composition",	
                    "Internal echo pattern","Internal echo homogeneous","Calcification",
                    "Tumor internal vascularization","Tumor Peripheral blood flow","Size","Location",
                    "Mulifocality","Hashimoto","Extrathyroidal extension","Side of position",	
                    "Ipsilateral Central Lymph Node Metastasis","Prelaryngeal Lymph Node Metastasis",
                    "Pretracheal Lymph Node Metastasis","Paratracheal Lymph Node Metastasis",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis","Ipsilateral Lateral Lymph Node Metastasis",
                    "Level II Lymph Node Metastasis","Level III Lymph Node Metastasis","Level IV Lymph Node Metastasis",
                    "T staging","age","size","Ipsilateral Central Lymph Node Metastasis Rate",
                    "Ipsilateral Central Lymph Node Metastases Number","Prelaryngeal Lymph Node Metastasis Rate",
                    "Prelaryngeal Lymph Node Metastases Number","Pretracheal Lymph Node Metastasis Rate",
                    "Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
                    "Paratracheal Lymph Node Metastases Number", "Recurrent Laryngeal Nerve Lymph Node Metastasis Rate",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis Number")



# 构建初始模型
initial_model <- glm(`Level II Lymph Node Metastasis` ~Age+Sex+`Tumor border`+`Aspect ratio`+`Internal echo pattern`+`Internal echo homogeneous` +Calcification+`Tumor Peripheral blood flow`+`Tumor internal vascularization`+`Extrathyroidal extension`+Size+Location+Mulifocality+`T staging`+`Ipsilateral Central Lymph Node Metastasis`+`Ipsilateral Central Lymph Node Metastasis Rate` + `Ipsilateral Central Lymph Node Metastases Number` + `Prelaryngeal Lymph Node Metastasis` + `Prelaryngeal Lymph Node Metastasis Rate` + `Prelaryngeal Lymph Node Metastases Number` + `Pretracheal Lymph Node Metastasis` + `Pretracheal Lymph Node Metastasis Rate` + `Pretracheal Lymph Node Metastases Number` + `Paratracheal Lymph Node Metastasis` + `Paratracheal Lymph Node Metastasis Rate` + `Paratracheal Lymph Node Metastases Number` + `Recurrent Laryngeal Nerve Lymph Node Metastasis` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Rate` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Number`, data = data, family = binomial())

# 计算VIF值
vif_values <- vif(initial_model)
print(vif_values)

# 移除高VIF值的变量（假设阈值为5）
selected_vars <- names(vif_values[vif_values < 5.878])

# 重新构建模型，消除共线性
formula <- as.formula(paste("`Level II Lymph Node Metastasis` ~", paste(selected_vars, collapse = " + ")))
final_model <- glm(formula, data = data, family = binomial())

# 提取模型系数
coefficients <- coef(final_model)

# 创建系数数据框
coef_df <- data.frame(
  variable = names(coefficients),
  coefficient = coefficients,
  odds_ratio = exp(coefficients),
  p_value = summary(final_model)$coefficients[, "Pr(>|z|)"],
  ci_lower = exp(confint(final_model)[, 1]),
  ci_upper = exp(confint(final_model)[, 2])
)

# 计算95%置信区间
coef_df$LL <- coef_df$ci_lower
coef_df$UL <- coef_df$ci_upper

# 将(Intercept)标签改为Intercept
coef_df$variable[coef_df$variable == "(Intercept)"] <- "Intercept"

# 手动设置变量顺序并反转
variable_order <- c("Intercept", selected_vars)
coef_df$variable <- factor(coef_df$variable, levels = rev(variable_order))

# 创建初始森林图
forest_plot <- ggplot(coef_df, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "#C71585"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level II Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df$p_value < 0.05,"#C71585","black")))

# 显示初始森林图
print(forest_plot)


coef_df_sorted <- coef_df[order(coef_df$variable), ]
coef_df_sorted <- rbind(coef_df_sorted[coef_df_sorted$variable != "Intercept", ], coef_df_sorted[coef_df_sorted$variable == "Intercept", ])
coef_df_sorted$variable <- factor(coef_df_sorted$variable, levels = coef_df_sorted$variable)

forest_plot_sorted <- ggplot(coef_df_sorted, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "#C71585"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level II Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df_sorted$p_value < 0.05, "#C71585", "black")))

# 显示排序后的森林图
print(forest_plot_sorted)



# 保存图像函数
save_forest_plot_sorted <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果"

# 保存
save_forest_plot_sorted(forest_plot_sorted, file.path(output_folder, "1.2区多因素分析_森林图按输入变量的顺序"))

print(forest_plot_sorted)

```



```{r}
library(car)
library(ggplot2)

# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv", check.names = FALSE)

# 设置列名
colnames(data) <- c("Age","Sex","Classification of BMI","Tumor border","Aspect ratio","Composition",	
                    "Internal echo pattern","Internal echo homogeneous","Calcification",
                    "Tumor internal vascularization","Tumor Peripheral blood flow","Size","Location",
                    "Mulifocality","Hashimoto","Extrathyroidal extension","Side of position",	
                    "Ipsilateral Central Lymph Node Metastasis","Prelaryngeal Lymph Node Metastasis",
                    "Pretracheal Lymph Node Metastasis","Paratracheal Lymph Node Metastasis",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis","Ipsilateral Lateral Lymph Node Metastasis",
                    "Level II Lymph Node Metastasis","Level III Lymph Node Metastasis","Level IV Lymph Node Metastasis",
                    "T staging","age","size","Ipsilateral Central Lymph Node Metastasis Rate",
                    "Ipsilateral Central Lymph Node Metastases Number","Prelaryngeal Lymph Node Metastasis Rate",
                    "Prelaryngeal Lymph Node Metastases Number","Pretracheal Lymph Node Metastasis Rate",
                    "Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
                    "Paratracheal Lymph Node Metastases Number", "Recurrent Laryngeal Nerve Lymph Node Metastasis Rate",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis Number")



# 构建初始模型
initial_model <- glm(`Level II Lymph Node Metastasis` ~Age+Sex+`Tumor border`+`Aspect ratio`+`Internal echo pattern`+`Internal echo homogeneous` +Calcification+`Tumor Peripheral blood flow`+`Tumor internal vascularization`+`Extrathyroidal extension`+Size+Location+Mulifocality+`T staging`+`Ipsilateral Central Lymph Node Metastasis`+`Ipsilateral Central Lymph Node Metastasis Rate` + `Ipsilateral Central Lymph Node Metastases Number` + `Prelaryngeal Lymph Node Metastasis` + `Prelaryngeal Lymph Node Metastasis Rate` + `Prelaryngeal Lymph Node Metastases Number` + `Pretracheal Lymph Node Metastasis` + `Pretracheal Lymph Node Metastasis Rate` + `Pretracheal Lymph Node Metastases Number` + `Paratracheal Lymph Node Metastasis` + `Paratracheal Lymph Node Metastasis Rate` + `Paratracheal Lymph Node Metastases Number` + `Recurrent Laryngeal Nerve Lymph Node Metastasis` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Rate` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Number`, data = data, family = binomial())


# 计算VIF值
vif_values <- vif(initial_model)
print(vif_values)

# 移除高VIF值的变量（假设阈值为5）
selected_vars <- names(vif_values[vif_values < 5.878])

# 重新构建模型，消除共线性
formula <- as.formula(paste("`Level II Lymph Node Metastasis` ~", paste(selected_vars, collapse = " + ")))
final_model <- glm(formula, data = data, family = binomial())

# 提取模型系数
coefficients <- coef(final_model)

# 创建系数数据框
coef_df <- data.frame(
  variable = names(coefficients),
  coefficient = coefficients,
  odds_ratio = exp(coefficients),
  p_value = summary(final_model)$coefficients[, "Pr(>|z|)"],
  ci_lower = exp(confint(final_model)[, 1]),
  ci_upper = exp(confint(final_model)[, 2])
)

# 计算95%置信区间
coef_df$LL <- coef_df$ci_lower
coef_df$UL <- coef_df$ci_upper

# 将(Intercept)标签改为Intercept
coef_df$variable[coef_df$variable == "(Intercept)"] <- "Intercept"

# 手动设置变量顺序并反转
variable_order <- c("Intercept", selected_vars)
coef_df$variable <- factor(coef_df$variable, levels = rev(variable_order))

# 创建初始森林图
forest_plot <- ggplot(coef_df, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "#C71585"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level II Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df$p_value < 0.05,"#C71585","black")))

# 显示初始森林图
print(forest_plot)


coef_df_sorted <- coef_df[order(coef_df$variable), ]
coef_df_sorted <- rbind(coef_df_sorted[coef_df_sorted$variable != "Intercept", ], coef_df_sorted[coef_df_sorted$variable == "Intercept", ])
coef_df_sorted$variable <- factor(coef_df_sorted$variable, levels = coef_df_sorted$variable)

forest_plot_sorted <- ggplot(coef_df_sorted, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "#C71585"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level II Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df_sorted$p_value < 0.05, "#C71585", "black")))

# 显示排序后的森林图
print(forest_plot_sorted)

# 保存图像函数
save_forest_plot_sorted <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果"

# 保存
save_forest_plot_sorted(forest_plot_sorted, file.path(output_folder, "1.2区多因素分析_森林图按输入变量的顺序"))

print(forest_plot_sorted)

```
```{r}
#install.packages("rms")
library(foreign) 
library(rms)
# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv")

```

##3.2赋值
```{r}
data$Age<-factor(data$Age,levels = c(1,0),labels = c("age≤43","age>43"))
data$Sex<-factor(data$Sex,levels = c(0,1),labels = c("Female","Male"))

data$Tumor.border<-factor(data$Tumor.border,levels = c(0,1,2),labels = c("smooth or borderless","irregular shape or lsharpobed","extrandular invasion"))
data$Aspect.ratio<-factor(data$Aspect.ratio,levels = c(0,1),labels = c("≤1",">1"))
 data$Composition<-factor(data$Composition,levels = c(0,1,2),labels = c("cystic/cavernous","Mixed cystic and solid","solid"))
 data$Internal.echo.pattern<-factor(data$Internal.echo.pattern,levels = c(0,1,2,3),labels = c("echoless","high/isoechoic","hypoechoic","very hypoechoic"))
 data$Internal.echo.homogeneous<-factor(data$Internal.echo.homogeneous,levels = c(0,1),labels = c("Non-uniform","Uniform"))
 data$Calcification<-factor(data$Calcification,levels = c(0,1,2,3),labels = c("no or large comet tail", "coarse calcification","peripheral calcification","Microcalcification"))
data$Tumor.internal.vascularization<-factor(data$Tumor.internal.vascularization,levels = c(0,1),labels = c("Without","Abundant"))
data$Tumor.Peripheral.blood.flow<-factor(data$Tumor.Peripheral.blood.flow,levels = c(0,1),labels = c("Without","Abundant"))
data$Size<-factor(data$Size,levels = c(0,1),labels = c("≤10.5", ">10.5"))
data$Location<-factor(data$Location,levels = c(0,1),labels = c("Non-upper","Upper"))

data$Mulifocality<-factor(data$Mulifocality,levels = c(1,0),labels = c("Abundant", "Without"))
data$Hashimoto<-factor(data$Hashimoto,levels = c(0,1),labels = c("Abundant", "Without"))
data$Extrathyroidal.extension<-factor(data$Extrathyroidal.extension,levels = c(1,0),labels = c("Abundant", "Without"))


data$Side.of.position<-factor(data$Side.of.position,levels = c(0,1,2,3),labels = c("left","right","bilateral" ,"isthmus"))

data$Ipsilateral.Central.Lymph.Node.Metastasis<-factor(data$Ipsilateral.Central.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))
data$Prelaryngeal.Lymph.Node.Metastasis<-factor(data$Prelaryngeal.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))
data$Paratracheal.Lymph.Node.Metastasis<-factor(data$Paratracheal.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))
data$Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis<-factor(data$Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))


```

```{r}
### 4.1.2 整合数据
x <- as.data.frame(data)
dd <- datadist(data)
options(datadist = 'dd')

### 4.2 Logistic回归比GLM好用
fit1 <- lrm(Level.II.Lymph.Node.Metastasis ~Aspect.ratio+Calcification+Size+Location+Mulifocality+Ipsilateral.Central.Lymph.Node.Metastasis+Prelaryngeal.Lymph.Node.Metastasis.Rate,
            data = data, x = TRUE, y = TRUE)

fit1
summary(fit1) # 可以直接给到一些结果很好

nom1 <- nomogram(fit1, fun = plogis, fun.at = c(.001, .01, .05, seq(.1, .9, by = .1), .95, .99, .999),
                 lp = FALSE, funlabel = "Level II Lymph Node Metastasis")
plot(nom1)

### 4.4 验证曲线
cal1 <- calibrate(fit1, method = 'boot', B = 1000)
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))

# 保存列线图为1200 DPI的 .tiff格式
tiff("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/nomogram.tiff", width = 8, height = 6, units = "in", res = 1200, compression = "lzw")
plot(nom1)
dev.off()

# 保存列线图为1200 DPI的 .png格式
png("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/nomogram.png", width = 8, height = 6, units = "in", res = 1200)
plot(nom1)
dev.off()

# 保存列线图为1200 DPI的 .eps格式
postscript("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/nomogram.eps", width = 8, height = 6, horizontal = FALSE, onefile = FALSE, paper = "special")
plot(nom1)
dev.off()

# 保存验证曲线为1200 DPI的 .tiff格式
tiff("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/calibration.tiff", width = 8, height = 6, units = "in", res = 1200, compression = "lzw")
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))
dev.off()

# 保存验证曲线为1200 DPI的 .png格式
png("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/calibration.png", width = 8, height = 6, units = "in", res = 1200)
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))
dev.off()

# 保存验证曲线为1200 DPI的 .eps格式
postscript("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/calibration.eps", width = 8, height = 6, horizontal = FALSE, onefile = FALSE, paper = "special")
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))
dev.off()



```


###4.1.2 调整列线图的图间距和因子名称的大小和间距
```{r}
# 设置绘图参数
par(mar = c(1, 2, 2, 2))  # 调整绘图边距

# 创建 nomogram
nom2 <- nomogram(fit1, fun = plogis, fun.at = c(0.001, 0.01, 0.05, seq(0.1, 0.9, by = 0.1), 0.95, 0.99, 0.999),
                 lp = FALSE, funlabel="Level II Lymph Node Metastasis")

# 绘制 nomogram
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)


# 保存列线图为1200 DPI的 .tiff格式
tiff("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/nomogram.tiff", width = 8, height = 6, units = "in", res = 1200, compression = "lzw")
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)
dev.off()

# 保存列线图为1200 DPI的 .png格式
png("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/nomogram.png", width = 8, height = 6, units = "in", res = 1200)
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)
dev.off()

# 保存列线图为1200 DPI的 .eps格式
postscript("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/nomogram.eps", width = 8, height = 6, horizontal = FALSE, onefile = FALSE, paper = "special")
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)
dev.off()



```


##3.2列线图ROC曲线的绘制--单roc

```{r}
# 加载必要的库
library(pROC)
library(ggplot2)

# 读取数据
train_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值矫正后.csv")
test_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/2.验证集编码填补缺失值矫正后.csv")

# 将训练数据按照7:3的比例随机分为训练集和验证集
# 设置随机数种子,以确保结果可复现
set.seed(123)
index <- 1:nrow(train_data)
shuffled_index <- sample(index)
tra_ratio <- 0.7  # 训练集比例
tra_size <- round(tra_ratio * nrow(train_data))
tra_data <- train_data[shuffled_index[1:tra_size], ]
val_data <- train_data[shuffled_index[(tra_size + 1):nrow(train_data)], ]

cat("训练集观测数量:", nrow(tra_data), "\n")
cat("验证集观测数量:", nrow(val_data), "\n")
cat("测试集观测数量:", nrow(test_data), "\n")

# 构建模型
fit1 <- glm(II.Level.Lymph.Node.Metastasis ~Aspect.ratio+Calcification+Size+Location+Mulifocality+Ipsilateral.Central.Lymph.Node.Metastasis+Prelaryngeal.Lymph.Node.Metastases.Number,
            data = tra_data, family = binomial())

# 预测概率
train_probs <- predict(fit1, newdata = tra_data, type = "response")
val_probs <- predict(fit1, newdata = val_data, type = "response")
test_probs <- predict(fit1, newdata = test_data, type = "response")

train_response <- tra_data$II.Level.Lymph.Node.Metastasis
val_response <- val_data$II.Level.Lymph.Node.Metastasis
test_response <- test_data$II.Level.Lymph.Node.Metastasis

# 创建ROC对象
train_roc <- roc(train_response, train_probs)
val_roc <- roc(val_response, val_probs)
test_roc <- roc(test_response, test_probs)

# 提取ROC曲线的坐标点
train_roc_data <- coords(train_roc, "all", ret = c("specificity", "sensitivity"))
val_roc_data <- coords(val_roc, "all", ret = c("specificity", "sensitivity"))
test_roc_data <- coords(test_roc, "all", ret = c("specificity", "sensitivity"))

# 转换为数据框
train_roc_data <- as.data.frame(train_roc_data)
val_roc_data <- as.data.frame(val_roc_data)
test_roc_data <- as.data.frame(test_roc_data)

# 绘制ROC曲线
roc_plot <- ggplot() +
  geom_line(data = train_roc_data, aes(x = 1 - specificity, y = sensitivity), color = "#C71585", size = 0.6) +
  geom_line(data = val_roc_data, aes(x = 1 - specificity, y = sensitivity), color = "red", size = 0.6) +
  geom_line(data = test_roc_data, aes(x = 1 - specificity, y = sensitivity), color = "pink", size = 0.6) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "black") +
  labs(title = "ROC for Level II Lymph Node Metastasis Nomogram Prediction",
       x = "False Positive Rate", y = "True Positive Rate") +
  theme_minimal() +
  theme(legend.position = "none") +
  annotate("text", x = 0.7, y = 0.4, label = paste("Train set AUC =", round(auc(train_roc), 3)), size = 4, color = "#C71585") +
  annotate("text", x = 0.7, y = 0.3, label = paste("Validation set AUC =", round(auc(val_roc), 3)), size = 4, color = "red") +
  annotate("text", x = 0.7, y = 0.2, label = paste("Test set AUC =", round(auc(test_roc), 3)), size = 4, color = "pink")

# 保存ROC曲线为.tiff格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/roc_curve.tiff", plot = roc_plot, width = 8, height = 6, units = "in", dpi = 1200, compression = "lzw")

# 保存ROC曲线为.png格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/roc_curve.png", plot = roc_plot, width = 8, height = 6, units = "in", dpi = 1200)

# 保存ROC曲线为.eps格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/roc_curve.eps", plot = roc_plot, width = 8, height = 6, units = "in", dpi = 1200)

```


```{r}
# 加载必要的库
library(pROC)
library(ggplot2)
library(dplyr)

# 读取数据
train_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值矫正后.csv")
test_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/2.验证集编码填补缺失值矫正后.csv")

# 按均值填补缺失值
fill_na_with_mean <- function(df) {
  df %>%
    mutate(across(everything(), ~ ifelse(is.na(.), mean(., na.rm = TRUE), .)))
}

train_data <- fill_na_with_mean(train_data)
test_data <- fill_na_with_mean(test_data)

# 将训练数据按照7:3的比例随机分为训练集和验证集
set.seed(123)
index <- 1:nrow(train_data)
shuffled_index <- sample(index)
tra_ratio <- 0.7  # 训练集比例
tra_size <- round(tra_ratio * nrow(train_data))
tra_data <- train_data[shuffled_index[1:tra_size], ]
val_data <- train_data[shuffled_index[(tra_size + 1):nrow(train_data)], ]

cat("训练集观测数量:", nrow(tra_data), "\n")
cat("验证集观测数量:", nrow(val_data), "\n")
cat("测试集观测数量:", nrow(test_data), "\n")

# 构建模型
fit1 <- glm(II.Level.Lymph.Node.Metastasis ~Aspect.ratio+Calcification+Size+Location+Mulifocality+Ipsilateral.Central.Lymph.Node.Metastasis+Prelaryngeal.Lymph.Node.Metastases.Number,
            data = tra_data, family = binomial())

# 预测概率
train_probs <- predict(fit1, newdata = tra_data, type = "response")
val_probs <- predict(fit1, newdata = val_data, type = "response")
test_probs <- predict(fit1, newdata = test_data, type = "response")

train_response <- tra_data$II.Level.Lymph.Node.Metastasis
val_response <- val_data$II.Level.Lymph.Node.Metastasis
test_response <- test_data$II.Level.Lymph.Node.Metastasis


# 定义净收益计算函数
net_benefit <- function(probs, outcome, threshold) {
  tp <- sum(outcome == 1 & probs >= threshold)
  fp <- sum(outcome == 0 & probs >= threshold)
  total_population <- length(outcome)
  
  if (total_population == 0) {
    return(0)
  }
  
  net_benefit <- (tp / total_population) - ((fp / total_population) * (threshold / (1 - threshold)))
  return(net_benefit)
}

# 计算不同阈值下的净收益
thresholds <- seq(0, 1, by = 0.01)
train_net_benefits <- sapply(thresholds, function(x) net_benefit(val_probs, val_response, x))
val_net_benefits <- sapply(thresholds, function(x) net_benefit(train_probs, train_response, x))
test_net_benefits <- sapply(thresholds, function(x) net_benefit(test_probs, test_response, x))

# 计算所有人都进行干预时的净收益
all_net_benefit <- sapply(thresholds, function(x) net_benefit(rep(1, length(val_response)), val_response, x))

# 计算没有人进行干预时的净收益
none_net_benefit <- rep(0, length(thresholds))

# 找到最大净收益点
train_max_nb <- max(train_net_benefits)
train_max_nb_threshold <- thresholds[which.max(train_net_benefits)]
val_max_nb <- max(val_net_benefits)
val_max_nb_threshold <- thresholds[which.max(val_net_benefits)]
test_max_nb <- max(test_net_benefits)
test_max_nb_threshold <- thresholds[which.max(test_net_benefits)]

# 绘制DCA曲线
dca_data <- data.frame(
  threshold = thresholds,
  train_net_benefit = train_net_benefits,
  val_net_benefit = val_net_benefits,
  test_net_benefit = test_net_benefits,
  all_net_benefit = all_net_benefit,
  none_net_benefit = none_net_benefit
)

dca_plot <- ggplot(dca_data, aes(x = threshold)) +
  geom_line(aes(y = train_net_benefit, color = "Train set"), size = 0.6) +
  geom_line(aes(y = val_net_benefit, color = "Test set"), size = 0.6) +
  geom_line(aes(y = test_net_benefit, color = "Validation set"), size = 0.6) +
  geom_line(aes(y = all_net_benefit, color = "All"), linetype = "dotted", size = 0.6) +
  geom_line(aes(y = none_net_benefit, color = "None"), linetype = "solid", size = 0.6) +
  labs(title = "DCA for Level II Lymph Node Metastasis Nomogram Prediction",
       x = "Threshold Probability", y = "Net Benefit") +
  scale_color_manual(values = c("Test set" = "red", "Train set" = "#C71585", "Validation set" = "pink", "All" = "grey", "None" = "black")) +
  theme_minimal() +
  theme(legend.position = "right") +
  annotate("text", x = 0.4, y = 0.075, label = "Train set", size = 4, color = "#C71585") +
  annotate("text", x = 0.4, y = 0.05, label = "Test set", size = 4, color = "red") +
  annotate("text", x = 0.4, y = 0.01, label = "Validation set", size = 4, color = "pink") +
  annotate("text", x = val_max_nb_threshold, y = val_max_nb, label = sprintf("Max: %.3f", val_max_nb), color = "red", vjust = -1)+
  annotate("text", x = train_max_nb_threshold, y = train_max_nb, label = sprintf("Max: %.3f", train_max_nb), color = "#C71585", vjust = -1) +
  annotate("text", x = test_max_nb_threshold, y = test_max_nb, label = sprintf("Max: %.3f", test_max_nb), color = "pink", vjust = -1)+
  coord_cartesian(ylim = c(-0.05, 0.2), xlim = c(0, 0.8))


# 保存ROC曲线为.tiff格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/dca_curve.tiff", plot = dca_plot, width = 8, height = 6, units = "in", dpi = 1200, compression = "lzw")

# 保存ROC曲线为.png格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/dca_curve.png", plot = dca_plot, width = 8, height = 6, units = "in", dpi = 1200)

# 保存ROC曲线为.eps格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/2、二区的结果/dca_curve.eps", plot = dca_plot, width = 8, height = 6, units = "in", dpi = 1200)

print(dca_plot)

```

#调整尺寸排序森林图和具体的数值之侧区
```{r}
library(car)
library(ggplot2)

# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv", check.names = FALSE)

# 设置列名
colnames(data) <- c("Age","Sex","Classification of BMI","Tumor border","Aspect ratio","Composition",	
                    "Internal echo pattern","Internal echo homogeneous","Calcification",
                    "Tumor internal vascularization","Tumor Peripheral blood flow","Size","Location",
                    "Mulifocality","Hashimoto","Extrathyroidal extension","Side of position",	
                    "Ipsilateral Central Lymph Node Metastasis","Prelaryngeal Lymph Node Metastasis",
                    "Pretracheal Lymph Node Metastasis","Paratracheal Lymph Node Metastasis",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis","Ipsilateral Lateral Lymph Node Metastasis",
                    "II Level Lymph Node Metastasis","Level III Lymph Node Metastasis","Level IV Lymph Node Metastasis",
                    "T staging","age","size","Ipsilateral Central Lymph Node Metastasis Rate",
                    "Ipsilateral Central Lymph Node Metastases Number","Prelaryngeal Lymph Node Metastasis Rate",
                    "Prelaryngeal Lymph Node Metastases Number","Pretracheal Lymph Node Metastasis Rate",
                    "Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
                    "Paratracheal Lymph Node Metastases Number", "Recurrent Laryngeal Nerve Lymph Node Metastasis Rate",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis Number")


# 构建初始模型
initial_model <- glm(`Level III Lymph Node Metastasis` ~Age+Sex+`Tumor border`+`Aspect ratio`+`Internal echo homogeneous` +Calcification+`Tumor Peripheral blood flow`+`Tumor internal vascularization`+`Extrathyroidal extension`+Size+Mulifocality+`T staging`+`Side of position`+`Ipsilateral Central Lymph Node Metastasis`+`Ipsilateral Central Lymph Node Metastasis Rate` + `Ipsilateral Central Lymph Node Metastases Number` + `Prelaryngeal Lymph Node Metastasis` + `Prelaryngeal Lymph Node Metastasis Rate` + `Prelaryngeal Lymph Node Metastases Number` + `Pretracheal Lymph Node Metastasis` + `Pretracheal Lymph Node Metastasis Rate` + `Pretracheal Lymph Node Metastases Number` + `Paratracheal Lymph Node Metastasis` + `Paratracheal Lymph Node Metastasis Rate` + `Paratracheal Lymph Node Metastases Number` + `Recurrent Laryngeal Nerve Lymph Node Metastasis` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Rate` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Number`, data = data, family = binomial())

# 计算VIF值
vif_values <- vif(initial_model)
print(vif_values)

# 移除高VIF值的变量（假设阈值为5）
selected_vars <- names(vif_values[vif_values < 5])

# 重新构建模型，消除共线性
formula <- as.formula(paste("`Level III Lymph Node Metastasis` ~", paste(selected_vars, collapse = " + ")))
final_model <- glm(formula, data = data, family = binomial())

# 提取模型系数
coefficients <- coef(final_model)

# 创建系数数据框
coef_df <- data.frame(
  variable = names(coefficients),
  coefficient = coefficients,
  odds_ratio = exp(coefficients),
  p_value = summary(final_model)$coefficients[, "Pr(>|z|)"],
  ci_lower = exp(confint(final_model)[, 1]),
  ci_upper = exp(confint(final_model)[, 2])
)

# 将(Intercept)标签改为Intercept
coef_df$variable[coef_df$variable == "(Intercept)"] <- "Intercept"

# 手动设置变量顺序并反转
variable_order <- c("Intercept", selected_vars)
coef_df$variable <- factor(coef_df$variable, levels = rev(variable_order))

# 创建初始森林图
forest_plot <- ggplot(coef_df, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper), height = 0.2, color = "black") +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""), 
                x = -20, hjust = -0.1), size = 2.5) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1), size = 2.5) +
  coord_cartesian(xlim = c(-20, 20)) +
  scale_color_manual(values = c("black", "goldenrod"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level III Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal()


# 保存图像函数
save_forest_plot <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果"

# 保存
save_forest_plot(forest_plot, file.path(output_folder, "1.3区多因素分析_森林图按输入变量的顺序"))

print(forest_plot)



coef_df_sorted <- coef_df[order(coef_df$odds_ratio), ]
coef_df_sorted <- rbind(coef_df_sorted[coef_df_sorted$variable != "Intercept", ], coef_df_sorted[coef_df_sorted$variable == "Intercept", ])
coef_df_sorted$variable <- factor(coef_df_sorted$variable, levels = coef_df_sorted$variable)

forest_plot_sorted <- ggplot(coef_df_sorted, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "darkblue"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level III Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df_sorted$p_value < 0.05, "darkblue", "black")))


# 显示排序后的森林图
print(forest_plot_sorted)

# 导出结果到CSV文件并反转顺序
write.csv(coef_df[nrow(coef_df):1, ], "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/1.3区多因素分析按输入变量的顺序.csv", row.names = FALSE)
write.csv(coef_df_sorted[nrow(coef_df_sorted):1, ], "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/1.3区多因素分析按OR值的顺序.csv", row.names = FALSE)

# 保存图像函数
save_forest_plot_sorted <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果"

# 保存
save_forest_plot_sorted(forest_plot_sorted, file.path(output_folder, "1.3区多因素分析_森林图_按OR值的顺序"))

print(forest_plot_sorted)



```



##注意！这是为了按输入变量的顺序输出的森林图改尺寸和颜色
```{r}
library(car)
library(ggplot2)

# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv", check.names = FALSE)

# 设置列名
colnames(data) <- c("Age","Sex","Classification of BMI","Tumor border","Aspect ratio","Composition",	
                    "Internal echo pattern","Internal echo homogeneous","Calcification",
                    "Tumor internal vascularization","Tumor Peripheral blood flow","Size","Location",
                    "Mulifocality","Hashimoto","Extrathyroidal extension","Side of position",	
                    "Ipsilateral Central Lymph Node Metastasis","Prelaryngeal Lymph Node Metastasis",
                    "Pretracheal Lymph Node Metastasis","Paratracheal Lymph Node Metastasis",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis","Ipsilateral Lateral Lymph Node Metastasis",
                    "II Level Lymph Node Metastasis","Level III Lymph Node Metastasis","Level IV Lymph Node Metastasis",
                    "T staging","age","size","Ipsilateral Central Lymph Node Metastasis Rate",
                    "Ipsilateral Central Lymph Node Metastases Number","Prelaryngeal Lymph Node Metastasis Rate",
                    "Prelaryngeal Lymph Node Metastases Number","Pretracheal Lymph Node Metastasis Rate",
                    "Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
                    "Paratracheal Lymph Node Metastases Number", "Recurrent Laryngeal Nerve Lymph Node Metastasis Rate",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis Number")


# 构建初始模型
initial_model <- glm(`Level III Lymph Node Metastasis` ~Age+Sex+`Tumor border`+`Aspect ratio`+`Internal echo homogeneous` +Calcification+`Tumor Peripheral blood flow`+`Tumor internal vascularization`+`Extrathyroidal extension`+Size+Mulifocality+`T staging`+`Side of position`+`Ipsilateral Central Lymph Node Metastasis`+`Ipsilateral Central Lymph Node Metastasis Rate` + `Ipsilateral Central Lymph Node Metastases Number` + `Prelaryngeal Lymph Node Metastasis` + `Prelaryngeal Lymph Node Metastasis Rate` + `Prelaryngeal Lymph Node Metastases Number` + `Pretracheal Lymph Node Metastasis` + `Pretracheal Lymph Node Metastasis Rate` + `Pretracheal Lymph Node Metastases Number` + `Paratracheal Lymph Node Metastasis` + `Paratracheal Lymph Node Metastasis Rate` + `Paratracheal Lymph Node Metastases Number` + `Recurrent Laryngeal Nerve Lymph Node Metastasis` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Rate` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Number`, data = data, family = binomial())

# 计算VIF值
vif_values <- vif(initial_model)
print(vif_values)

# 移除高VIF值的变量（假设阈值为5）
selected_vars <- names(vif_values[vif_values < 5])

# 重新构建模型，消除共线性
formula <- as.formula(paste("`Level III Lymph Node Metastasis` ~", paste(selected_vars, collapse = " + ")))
final_model <- glm(formula, data = data, family = binomial())

# 提取模型系数
coefficients <- coef(final_model)

# 创建系数数据框
coef_df <- data.frame(
  variable = names(coefficients),
  coefficient = coefficients,
  odds_ratio = exp(coefficients),
  p_value = summary(final_model)$coefficients[, "Pr(>|z|)"],
  ci_lower = exp(confint(final_model)[, 1]),
  ci_upper = exp(confint(final_model)[, 2])
)

# 计算95%置信区间
coef_df$LL <- coef_df$ci_lower
coef_df$UL <- coef_df$ci_upper

# 将(Intercept)标签改为Intercept
coef_df$variable[coef_df$variable == "(Intercept)"] <- "Intercept"

# 手动设置变量顺序并反转
variable_order <- c("Intercept", selected_vars)
coef_df$variable <- factor(coef_df$variable, levels = rev(variable_order))

# 创建初始森林图
forest_plot <- ggplot(coef_df, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "darkblue"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level III Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df$p_value < 0.05,"darkblue","black")))

# 显示初始森林图
print(forest_plot)


coef_df_sorted <- coef_df[order(coef_df$variable), ]
coef_df_sorted <- rbind(coef_df_sorted[coef_df_sorted$variable != "Intercept", ], coef_df_sorted[coef_df_sorted$variable == "Intercept", ])
coef_df_sorted$variable <- factor(coef_df_sorted$variable, levels = coef_df_sorted$variable)

forest_plot_sorted <- ggplot(coef_df_sorted, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "darkblue"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level III Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df_sorted$p_value < 0.05, "darkblue", "black")))

# 显示排序后的森林图
print(forest_plot_sorted)


# 保存图像函数
save_forest_plot_sorted <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果"

# 保存
save_forest_plot_sorted(forest_plot_sorted, file.path(output_folder, "1.3区多因素分析_森林图按输入变量的顺序"))

print(forest_plot_sorted)


```



#3列线图的绘制

##3.1列线图以及验证曲线的代码
```{r}
#install.packages("foreign")
#install.packages("rms")
library(foreign) 
library(rms)
# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv")
```

##3.2赋值
```{r}
data$Age<-factor(data$Age,levels = c(1,0),labels = c("age≤43","age>43"))
data$Sex<-factor(data$Sex,levels = c(0,1),labels = c("Female","Male"))

data$Tumor.border<-factor(data$Tumor.border,levels = c(0,1,2),labels = c("smooth or borderless","irregular shape or lsharpobed","extrandular invasion"))
data$Aspect.ratio<-factor(data$Aspect.ratio,levels = c(0,1),labels = c("≤1",">1"))
 data$Composition<-factor(data$Composition,levels = c(0,1,2),labels = c("cystic/cavernous","Mixed cystic and solid","solid"))
 data$Internal.echo.pattern<-factor(data$Internal.echo.pattern,levels = c(0,1,2,3),labels = c("echoless","high/isoechoic","hypoechoic","very hypoechoic"))
 data$Internal.echo.homogeneous<-factor(data$Internal.echo.homogeneous,levels = c(0,1),labels = c("Non-uniform","Uniform"))
 data$Calcification<-factor(data$Calcification,levels = c(0,1,2,3),labels = c("no or large comet tail", "coarse calcification","peripheral calcification","Microcalcification"))
data$Tumor.internal.vascularization<-factor(data$Tumor.internal.vascularization,levels = c(0,1),labels = c("Without","Abundant"))
data$Tumor.Peripheral.blood.flow<-factor(data$Tumor.Peripheral.blood.flow,levels = c(0,1),labels = c("Without","Abundant"))
data$Size<-factor(data$Size,levels = c(0,1),labels = c("≤10.5", ">10.5"))
data$Location<-factor(data$Location,levels = c(0,1),labels = c("Non-upper","Upper"))

data$Mulifocality<-factor(data$Mulifocality,levels = c(1,0),labels = c("Abundant", "Without"))
data$Hashimoto<-factor(data$Hashimoto,levels = c(0,1),labels = c("Abundant", "Without"))
data$Extrathyroidal.extension<-factor(data$Extrathyroidal.extension,levels = c(1,0),labels = c("Abundant", "Without"))


data$Side.of.position<-factor(data$Side.of.position,levels = c(0,1,2,3),labels = c("left","right","bilateral" ,"isthmus"))

data$Ipsilateral.Central.Lymph.Node.Metastasis<-factor(data$Ipsilateral.Central.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))
data$Prelaryngeal.Lymph.Node.Metastasis<-factor(data$Prelaryngeal.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))
data$Paratracheal.Lymph.Node.Metastasis<-factor(data$Paratracheal.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))
data$Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis<-factor(data$Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))


```


```{r}
### 4.1.2 整合数据
x <- as.data.frame(data)
dd <- datadist(data)
options(datadist = 'dd')

### 4.2 Logistic回归比GLM好用
fit1 <- lrm(Level.III.Lymph.Node.Metastasis ~Age+Tumor.border+Calcification+Tumor.internal.vascularization+Extrathyroidal.extension+Size+Ipsilateral.Central.Lymph.Node.Metastasis+Pretracheal.Lymph.Node.Metastasis.Rate+Paratracheal.Lymph.Node.Metastasis.Rate+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate,
            data = data, x = TRUE, y = TRUE)

fit1
summary(fit1) # 可以直接给到一些结果很好

nom1 <- nomogram(fit1, fun = plogis, fun.at = c(.001, .01, .05, seq(.1, .9, by = .1), .95, .99, .999),
                 lp = FALSE, funlabel = "Level III Lymph Node Metastasis")
plot(nom1)

### 4.4 验证曲线
cal1 <- calibrate(fit1, method = 'boot', B = 1000)
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))

# 保存列线图为1200 DPI的 .tiff格式
tiff("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/nomogram.tiff", width = 8, height = 6, units = "in", res = 1200, compression = "lzw")
plot(nom1)
dev.off()

# 保存列线图为1200 DPI的 .png格式
png("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/nomogram.png", width = 8, height = 6, units = "in", res = 1200)
plot(nom1)
dev.off()

# 保存列线图为1200 DPI的 .eps格式
postscript("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/nomogram.eps", width = 8, height = 6, horizontal = FALSE, onefile = FALSE, paper = "special")
plot(nom1)
dev.off()

# 保存验证曲线为1200 DPI的 .tiff格式
tiff("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/calibration.tiff", width = 8, height = 6, units = "in", res = 1200, compression = "lzw")
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))
dev.off()

# 保存验证曲线为1200 DPI的 .png格式
png("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/calibration.png", width = 8, height = 6, units = "in", res = 1200)
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))
dev.off()

# 保存验证曲线为1200 DPI的 .eps格式
postscript("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/calibration.eps", width = 8, height = 6, horizontal = FALSE, onefile = FALSE, paper = "special")
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))
dev.off()



```


###4.1.2 调整列线图的图间距和因子名称的大小和间距
```{r}
# 设置绘图参数
par(mar = c(1, 2, 2, 2))  # 调整绘图边距

# 创建 nomogram
nom2 <- nomogram(fit1, fun = plogis, fun.at = c(0.001, 0.01, 0.05, seq(0.1, 0.9, by = 0.1), 0.95, 0.99, 0.999),
                 lp = FALSE, funlabel="Level III Lymph Node Metastasis")

# 绘制 nomogram
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)


# 保存列线图为1200 DPI的 .tiff格式
tiff("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/nomogram.tiff", width = 8, height = 6, units = "in", res = 1200, compression = "lzw")
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)
dev.off()

# 保存列线图为1200 DPI的 .png格式
png("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/nomogram.png", width = 8, height = 6, units = "in", res = 1200)
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)
dev.off()

# 保存列线图为1200 DPI的 .eps格式
postscript("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/nomogram.eps", width = 8, height = 6, horizontal = FALSE, onefile = FALSE, paper = "special")
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)
dev.off()







```


##3.2列线图ROC曲线的绘制--单roc

```{r}
# 加载必要的库
library(pROC)
library(ggplot2)

# 读取数据
train_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值矫正后.csv")
test_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/2.验证集编码填补缺失值矫正后.csv")

# 将训练数据按照7:3的比例随机分为训练集和验证集
# 设置随机数种子,以确保结果可复现
set.seed(123)
index <- 1:nrow(train_data)
shuffled_index <- sample(index)
tra_ratio <- 0.7  # 训练集比例
tra_size <- round(tra_ratio * nrow(train_data))
tra_data <- train_data[shuffled_index[1:tra_size], ]
val_data <- train_data[shuffled_index[(tra_size + 1):nrow(train_data)], ]

cat("训练集观测数量:", nrow(tra_data), "\n")
cat("验证集观测数量:", nrow(val_data), "\n")
cat("测试集观测数量:", nrow(test_data), "\n")

# 构建模型
fit1 <- glm(III.Level.Lymph.Node.Metastasis ~Age+Tumor.border+Calcification+Tumor.internal.vascularization+Extrathyroidal.extension+Size+Ipsilateral.Central.Lymph.Node.Metastasis+Pretracheal.Lymph.Node.Metastasis.Rate+Paratracheal.Lymph.Node.Metastasis.Rate+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate,
            data = tra_data, family = binomial())

# 预测概率
train_probs <- predict(fit1, newdata = tra_data, type = "response")
val_probs <- predict(fit1, newdata = val_data, type = "response")
test_probs <- predict(fit1, newdata = test_data, type = "response")

train_response <- tra_data$III.Level.Lymph.Node.Metastasis
val_response <- val_data$III.Level.Lymph.Node.Metastasis
test_response <- test_data$III.Level.Lymph.Node.Metastasis

# 创建ROC对象
train_roc <- roc(train_response, train_probs)
val_roc <- roc(val_response, val_probs)
test_roc <- roc(test_response, test_probs)

# 提取ROC曲线的坐标点
train_roc_data <- coords(train_roc, "all", ret = c("specificity", "sensitivity"))
val_roc_data <- coords(val_roc, "all", ret = c("specificity", "sensitivity"))
test_roc_data <- coords(test_roc, "all", ret = c("specificity", "sensitivity"))

# 转换为数据框
train_roc_data <- as.data.frame(train_roc_data)
val_roc_data <- as.data.frame(val_roc_data)
test_roc_data <- as.data.frame(test_roc_data)

# 绘制ROC曲线
roc_plot <- ggplot() +
  geom_line(data = train_roc_data, aes(x = 1 - specificity, y = sensitivity), color = "darkblue", size = 0.6) +
  geom_line(data = val_roc_data, aes(x = 1 - specificity, y = sensitivity), color = "blue", size = 0.6) +
  geom_line(data = test_roc_data, aes(x = 1 - specificity, y = sensitivity), color = "skyblue", size = 0.6) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "black") +
  labs(title = "ROC for Level III Lymph Node Metastasis Nomogram Prediction",
       x = "False Positive Rate", y = "True Positive Rate") +
  theme_minimal() +
  theme(legend.position = "none") +
  annotate("text", x = 0.7, y = 0.4, label = paste("Train set AUC =", round(auc(train_roc), 3)), size = 4, color = "darkblue") +
  annotate("text", x = 0.7, y = 0.3, label = paste("Validation set AUC =", round(auc(val_roc), 3)), size = 4, color = "blue") +
  annotate("text", x = 0.7, y = 0.2, label = paste("Test set AUC =", round(auc(test_roc), 3)), size = 4, color = "skyblue")

# 保存ROC曲线为.tiff格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/roc_curve.tiff", plot = roc_plot, width = 8, height = 6, units = "in", dpi = 1200, compression = "lzw")

# 保存ROC曲线为.png格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/roc_curve.png", plot = roc_plot, width = 8, height = 6, units = "in", dpi = 1200)

# 保存ROC曲线为.eps格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/roc_curve.eps", plot = roc_plot, width = 8, height = 6, units = "in", dpi = 1200)

```


```{r}
# 加载必要的库
library(pROC)
library(ggplot2)
library(dplyr)

# 读取数据
train_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值矫正后.csv")
test_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/2.验证集编码填补缺失值矫正后.csv")

# 按均值填补缺失值
fill_na_with_mean <- function(df) {
  df %>%
    mutate(across(everything(), ~ ifelse(is.na(.), mean(., na.rm = TRUE), .)))
}

train_data <- fill_na_with_mean(train_data)
test_data <- fill_na_with_mean(test_data)

# 将训练数据按照7:3的比例随机分为训练集和验证集
set.seed(123)
index <- 1:nrow(train_data)
shuffled_index <- sample(index)
tra_ratio <- 0.7  # 训练集比例
tra_size <- round(tra_ratio * nrow(train_data))
tra_data <- train_data[shuffled_index[1:tra_size], ]
val_data <- train_data[shuffled_index[(tra_size + 1):nrow(train_data)], ]

cat("训练集观测数量:", nrow(tra_data), "\n")
cat("验证集观测数量:", nrow(val_data), "\n")
cat("测试集观测数量:", nrow(test_data), "\n")

# 构建模型
fit1 <- glm(III.Level.Lymph.Node.Metastasis ~Age+Tumor.border+Calcification+Tumor.internal.vascularization+Extrathyroidal.extension+Size+Ipsilateral.Central.Lymph.Node.Metastasis+Pretracheal.Lymph.Node.Metastasis.Rate+Paratracheal.Lymph.Node.Metastasis.Rate+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate,
            data = tra_data, family = binomial())

# 预测概率
train_probs <- predict(fit1, newdata = tra_data, type = "response")
val_probs <- predict(fit1, newdata = val_data, type = "response")
test_probs <- predict(fit1, newdata = test_data, type = "response")

train_response <- tra_data$III.Level.Lymph.Node.Metastasis
val_response <- val_data$III.Level.Lymph.Node.Metastasis
test_response <- test_data$III.Level.Lymph.Node.Metastasis


# 定义净收益计算函数
net_benefit <- function(probs, outcome, threshold) {
  tp <- sum(outcome == 1 & probs >= threshold)
  fp <- sum(outcome == 0 & probs >= threshold)
  total_population <- length(outcome)
  
  if (total_population == 0) {
    return(0)
  }
  
  net_benefit <- (tp / total_population) - ((fp / total_population) * (threshold / (1 - threshold)))
  return(net_benefit)
}

# 计算不同阈值下的净收益
thresholds <- seq(0, 1, by = 0.01)
train_net_benefits <- sapply(thresholds, function(x) net_benefit(train_probs, train_response, x))
val_net_benefits <- sapply(thresholds, function(x) net_benefit(val_probs, val_response, x))
test_net_benefits <- sapply(thresholds, function(x) net_benefit(test_probs, test_response, x))

# 计算所有人都进行干预时的净收益
all_net_benefit <- sapply(thresholds, function(x) net_benefit(rep(1, length(val_response)), val_response, x))

# 计算没有人进行干预时的净收益
none_net_benefit <- rep(0, length(thresholds))

# 找到最大净收益点
train_max_nb <- max(train_net_benefits)
train_max_nb_threshold <- thresholds[which.max(train_net_benefits)]
val_max_nb <- max(val_net_benefits)
val_max_nb_threshold <- thresholds[which.max(val_net_benefits)]
test_max_nb <- max(test_net_benefits)
test_max_nb_threshold <- thresholds[which.max(test_net_benefits)]

# 绘制DCA曲线
dca_data <- data.frame(
  threshold = thresholds,
  train_net_benefit = train_net_benefits,
  val_net_benefit = val_net_benefits,
  test_net_benefit = test_net_benefits,
  all_net_benefit = all_net_benefit,
  none_net_benefit = none_net_benefit
)

dca_plot <- ggplot(dca_data, aes(x = threshold)) +
  geom_line(aes(y = train_net_benefit, color = "Train set"), size = 0.6) +
  geom_line(aes(y = val_net_benefit, color = "Test set"), size = 0.6) +
  geom_line(aes(y = test_net_benefit, color = "Validation set"), size = 0.6) +
  geom_line(aes(y = all_net_benefit, color = "All"), linetype = "dotted", size = 0.6) +
  geom_line(aes(y = none_net_benefit, color = "None"), linetype = "solid", size = 0.6) +
  labs(title = "DCA for Level III Lymph Node Metastasis Nomogram Prediction",
       x = "Threshold Probability", y = "Net Benefit") +
  scale_color_manual(values = c("Train set" = "darkblue", "Test set" = "blue", "Validation set" = "skyblue", "All" = "grey", "None" = "black")) +
  theme_minimal() +
  theme(legend.position = "right") +
  annotate("text", x = 0.4, y = 0.1, label = "Train set", size = 4, color = "darkblue") +
  annotate("text", x = 0.4, y = 0.05, label = "Test set", size = 4, color = "blue") +
  annotate("text", x = 0.4, y = 0.01, label = "Validation set", size = 4, color = "skyblue") +
  annotate("text", x = train_max_nb_threshold, y = train_max_nb, label = sprintf("Max: %.3f", train_max_nb), color = "darkblue", vjust = -1) +
  annotate("text", x = val_max_nb_threshold, y = val_max_nb, label = sprintf("Max: %.3f", val_max_nb), color = "blue", vjust = -1) +
  annotate("text", x = test_max_nb_threshold, y = test_max_nb, label = sprintf("Max: %.3f", test_max_nb), color = "skyblue", vjust = -1) +
  coord_cartesian(ylim = c(-0.05, 0.35), xlim = c(0, 0.8))


# 保存ROC曲线为.tiff格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/dca_curve.tiff", plot = dca_plot, width = 8, height = 6, units = "in", dpi = 1200, compression = "lzw")

# 保存ROC曲线为.png格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/dca_curve.png", plot = dca_plot, width = 8, height = 6, units = "in", dpi = 1200)

# 保存ROC曲线为.eps格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/3、三区的结果/dca_curve.eps", plot = dca_plot, width = 8, height = 6, units = "in", dpi = 1200)

print(dca_plot)

```
#调整尺寸排序森林图和具体的数值之侧区
```{r}
library(car)
library(ggplot2)

# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv", check.names = FALSE)

# 设置列名
colnames(data) <- c("Age","Sex","Classification of BMI","Tumor border","Aspect ratio","Composition",	
                    "Internal echo pattern","Internal echo homogeneous","Calcification",
                    "Tumor internal vascularization","Tumor Peripheral blood flow","Size","Location",
                    "Mulifocality","Hashimoto","Extrathyroidal extension","Side of position",	
                    "Ipsilateral Central Lymph Node Metastasis","Prelaryngeal Lymph Node Metastasis",
                    "Pretracheal Lymph Node Metastasis","Paratracheal Lymph Node Metastasis",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis","Ipsilateral Lateral Lymph Node Metastasis",
                    "II Level Lymph Node Metastasis","III Level Lymph Node Metastasis","Level IV Lymph Node Metastasis",
                    "T staging","age","size","Ipsilateral Central Lymph Node Metastasis Rate",
                    "Ipsilateral Central Lymph Node Metastases Number","Prelaryngeal Lymph Node Metastasis Rate",
                    "Prelaryngeal Lymph Node Metastases Number","Pretracheal Lymph Node Metastasis Rate",
                    "Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
                    "Paratracheal Lymph Node Metastases Number", "Recurrent Laryngeal Nerve Lymph Node Metastasis Rate",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis Number")

# 构建初始模型
initial_model <- glm(`Level IV Lymph Node Metastasis` ~`Age` + `Tumor border` + `Aspect ratio` + `Composition` + `Internal echo homogeneous` + `Calcification` + `Tumor Peripheral blood flow` + `Tumor internal vascularization` + `Extrathyroidal extension` + `Size` + `Location` + `Mulifocality` + `T staging` + `Side of position` + `Ipsilateral Central Lymph Node Metastasis` + `Ipsilateral Central Lymph Node Metastasis Rate` + `Ipsilateral Central Lymph Node Metastases Number` + `Prelaryngeal Lymph Node Metastasis` + `Prelaryngeal Lymph Node Metastasis Rate` + `Prelaryngeal Lymph Node Metastases Number` + `Pretracheal Lymph Node Metastasis` + `Pretracheal Lymph Node Metastasis Rate` + `Pretracheal Lymph Node Metastases Number` + `Paratracheal Lymph Node Metastasis` + `Paratracheal Lymph Node Metastasis Rate` + `Paratracheal Lymph Node Metastases Number` + `Recurrent Laryngeal Nerve Lymph Node Metastasis` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Rate` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Number`, data = data, family = binomial())



# 计算VIF值
vif_values <- vif(initial_model)
print(vif_values)

# 移除高VIF值的变量（假设阈值为5）
selected_vars <- names(vif_values[vif_values < 5])


# 重新构建模型，消除共线性
formula <- as.formula(paste("`Level IV Lymph Node Metastasis` ~", paste(selected_vars, collapse = " + ")))
final_model <- glm(formula, data = data, family = binomial())

# 提取模型系数
coefficients <- coef(final_model)
print(coefficients)
# 创建系数数据框
coef_df <- data.frame(
  variable = names(coefficients),
  coefficient = coefficients,
  odds_ratio = exp(coefficients),
  p_value = summary(final_model)$coefficients[, "Pr(>|z|)"],
  ci_lower = exp(confint(final_model)[, 1]),
  ci_upper = exp(confint(final_model)[, 2])
)

# 将(Intercept)标签改为Intercept
coef_df$variable[coef_df$variable == "(Intercept)"] <- "Intercept"

# 手动设置变量顺序并反转
variable_order <- c("Intercept", selected_vars)
coef_df$variable <- factor(coef_df$variable, levels = rev(variable_order))

# 创建初始森林图
forest_plot <- ggplot(coef_df, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper), height = 0.2, color = "black") +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""), 
                x = -20, hjust = -0.1), size = 2.5) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1), size = 2.5) +
  coord_cartesian(xlim = c(-20, 20)) +
  scale_color_manual(values = c("black", "goldenrod"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level IV Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal()


# 保存图像函数
save_forest_plot <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果"

# 保存
save_forest_plot(forest_plot, file.path(output_folder, "1.4区多因素分析_森林图按输入变量的顺序"))

print(forest_plot)



coef_df_sorted <- coef_df[order(coef_df$odds_ratio), ]
coef_df_sorted <- rbind(coef_df_sorted[coef_df_sorted$variable != "Intercept", ], coef_df_sorted[coef_df_sorted$variable == "Intercept", ])
coef_df_sorted$variable <- factor(coef_df_sorted$variable, levels = coef_df_sorted$variable)

forest_plot_sorted <- ggplot(coef_df_sorted, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "darkgreen"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level IV Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df_sorted$p_value < 0.05, "darkgreen", "black")))


# 显示排序后的森林图
print(forest_plot_sorted)

# 导出结果到CSV文件并反转顺序
write.csv(coef_df[nrow(coef_df):1, ], "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/1.4区多因素分析按输入变量的顺序.csv", row.names = FALSE)
write.csv(coef_df_sorted[nrow(coef_df_sorted):1, ], "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/1.4区多因素分析按OR值的顺序.csv", row.names = FALSE)

# 保存图像函数
save_forest_plot_sorted <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果"

# 保存
save_forest_plot_sorted(forest_plot_sorted, file.path(output_folder, "1.4区多因素分析_森林图_按OR值的顺序"))

print(forest_plot_sorted)



```
##注意！这是为了按输入变量的顺序输出的森林图改尺寸和颜色
```{r}
library(car)
library(ggplot2)
library(dplyr)
library(car)  # 用于计算VIF值

# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv", check.names = FALSE)

# 设置列名
colnames(data) <- c("Age","Sex","Classification of BMI","Tumor border","Aspect ratio","Composition",	
                    "Internal echo pattern","Internal echo homogeneous","Calcification",
                    "Tumor internal vascularization","Tumor Peripheral blood flow","Size","Location",
                    "Mulifocality","Hashimoto","Extrathyroidal extension","Side of position",	
                    "Ipsilateral Central Lymph Node Metastasis","Prelaryngeal Lymph Node Metastasis",
                    "Pretracheal Lymph Node Metastasis","Paratracheal Lymph Node Metastasis",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis","Ipsilateral Lateral Lymph Node Metastasis",
                    "II Level Lymph Node Metastasis","III Level Lymph Node Metastasis","Level IV Lymph Node Metastasis",
                    "T staging","age","size","Ipsilateral Central Lymph Node Metastasis Rate",
                    "Ipsilateral Central Lymph Node Metastases Number","Prelaryngeal Lymph Node Metastasis Rate",
                    "Prelaryngeal Lymph Node Metastases Number","Pretracheal Lymph Node Metastasis Rate",
                    "Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
                    "Paratracheal Lymph Node Metastases Number", "Recurrent Laryngeal Nerve Lymph Node Metastasis Rate",
                    "Recurrent Laryngeal Nerve Lymph Node Metastasis Number")

# 构建初始模型
initial_model <- glm(`Level IV Lymph Node Metastasis` ~`Age` + `Tumor border` + `Aspect ratio` + `Composition` + `Internal echo homogeneous` + `Calcification` + `Tumor Peripheral blood flow` + `Tumor internal vascularization` + `Extrathyroidal extension` + `Size` + `Location` + `Mulifocality` + `T staging` + `Side of position` + `Ipsilateral Central Lymph Node Metastasis` + `Ipsilateral Central Lymph Node Metastasis Rate` + `Ipsilateral Central Lymph Node Metastases Number` + `Prelaryngeal Lymph Node Metastasis` + `Prelaryngeal Lymph Node Metastasis Rate` + `Prelaryngeal Lymph Node Metastases Number` + `Pretracheal Lymph Node Metastasis` + `Pretracheal Lymph Node Metastasis Rate` + `Pretracheal Lymph Node Metastases Number` + `Paratracheal Lymph Node Metastasis` + `Paratracheal Lymph Node Metastasis Rate` + `Paratracheal Lymph Node Metastases Number` + `Recurrent Laryngeal Nerve Lymph Node Metastasis` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Rate` + `Recurrent Laryngeal Nerve Lymph Node Metastasis Number`, data = data, family = binomial())



# 计算VIF值
vif_values <- vif(initial_model)
print(vif_values)

# 移除高VIF值的变量（假设阈值为5）
selected_vars <- names(vif_values[vif_values < 5])


# 重新构建模型，消除共线性
formula <- as.formula(paste("`Level IV Lymph Node Metastasis` ~", paste(selected_vars, collapse = " + ")))
final_model <- glm(formula, data = data, family = binomial())

# 提取模型系数
coefficients <- coef(final_model)
print(coefficients)
# 创建系数数据框
coef_df <- data.frame(
  variable = names(coefficients),
  coefficient = coefficients,
  odds_ratio = exp(coefficients),
  p_value = summary(final_model)$coefficients[, "Pr(>|z|)"],
  ci_lower = exp(confint(final_model)[, 1]),
  ci_upper = exp(confint(final_model)[, 2])
)

# 计算95%置信区间
coef_df$LL <- coef_df$ci_lower
coef_df$UL <- coef_df$ci_upper

# 将(Intercept)标签改为Intercept
coef_df$variable[coef_df$variable == "(Intercept)"] <- "Intercept"

# 手动设置变量顺序并反转
variable_order <- c("Intercept", selected_vars)
coef_df$variable <- factor(coef_df$variable, levels = rev(variable_order))

# 创建初始森林图
forest_plot <- ggplot(coef_df, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "darkgreen"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level IV Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df$p_value < 0.05,"darkgreen","black")))

# 显示初始森林图
print(forest_plot)


coef_df_sorted <- coef_df[order(coef_df$variable), ]
coef_df_sorted <- rbind(coef_df_sorted[coef_df_sorted$variable != "Intercept", ], coef_df_sorted[coef_df_sorted$variable == "Intercept", ])
coef_df_sorted$variable <- factor(coef_df_sorted$variable, levels = coef_df_sorted$variable)

forest_plot_sorted <- ggplot(coef_df_sorted, aes(x = odds_ratio, y = variable)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper, color = p_value < 0.05), height = 0.2) +
  geom_point(aes(color = p_value < 0.05), size = 1) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray") +
  geom_text(aes(label = paste(round(odds_ratio, 3), " (", round(ci_lower, 3), " - ", round(ci_upper, 3), ")", sep = ""),
                x = -5, hjust = -0.1, color = p_value < 0.05), size = 2.2) +
  geom_text(aes(label = paste("p =", round(p_value, 3)), x = 9, hjust = 1.1, color = p_value < 0.05), size = 2.2) +
  coord_cartesian(xlim = c(-5, 9)) +
  scale_color_manual(values = c("black", "darkgreen"), labels = c("p >= 0.05", "p < 0.05")) +
  labs(x = "Level IV Lymph Node Metastasis Odds Ratio", y = "Variable") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6, hjust = 0.5, color = ifelse(coef_df_sorted$p_value < 0.05, "darkgreen", "black")))

# 显示排序后的森林图
print(forest_plot_sorted)


# 保存图像函数
save_forest_plot_sorted <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果"

# 保存
save_forest_plot_sorted(forest_plot_sorted, file.path(output_folder, "1.4区多因素分析_森林图按输入变量的顺序"))

print(forest_plot_sorted)


```



#3列线图的绘制

##3.1列线图以及验证曲线的代码
```{r}
#install.packages("foreign")
#install.packages("rms")
library(foreign) 
library(rms)
# 读取数据
data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值后.csv")


```

##3.2赋值
```{r}
data$Age<-factor(data$Age,levels = c(1,0),labels = c("age≤43","age>43"))
data$Sex<-factor(data$Sex,levels = c(0,1),labels = c("Female","Male"))

data$Tumor.border<-factor(data$Tumor.border,levels = c(0,1,2),labels = c("smooth or borderless","irregular shape or lsharpobed","extrandular invasion"))
data$Aspect.ratio<-factor(data$Aspect.ratio,levels = c(0,1),labels = c("≤1",">1"))
 data$Composition<-factor(data$Composition,levels = c(0,1,2),labels = c("cystic/cavernous","Mixed cystic and solid","solid"))
 data$Internal.echo.pattern<-factor(data$Internal.echo.pattern,levels = c(0,1,2,3),labels = c("echoless","high/isoechoic","hypoechoic","very hypoechoic"))
 data$Internal.echo.homogeneous<-factor(data$Internal.echo.homogeneous,levels = c(0,1),labels = c("Non-uniform","Uniform"))
 data$Calcification<-factor(data$Calcification,levels = c(0,1,2,3),labels = c("no or large comet tail", "coarse calcification","peripheral calcification","Microcalcification"))
data$Tumor.internal.vascularization<-factor(data$Tumor.internal.vascularization,levels = c(0,1),labels = c("Without","Abundant"))
data$Tumor.Peripheral.blood.flow<-factor(data$Tumor.Peripheral.blood.flow,levels = c(0,1),labels = c("Without","Abundant"))
data$Size<-factor(data$Size,levels = c(0,1),labels = c("≤10.5", ">10.5"))
data$Location<-factor(data$Location,levels = c(0,1),labels = c("Non-upper","Upper"))

data$Mulifocality<-factor(data$Mulifocality,levels = c(1,0),labels = c("Abundant", "Without"))
data$Hashimoto<-factor(data$Hashimoto,levels = c(0,1),labels = c("Abundant", "Without"))
data$Extrathyroidal.extension<-factor(data$Extrathyroidal.extension,levels = c(1,0),labels = c("Abundant", "Without"))


data$Side.of.position<-factor(data$Side.of.position,levels = c(0,1,2,3),labels = c("left","right","bilateral" ,"isthmus"))

data$Ipsilateral.Central.Lymph.Node.Metastasis<-factor(data$Ipsilateral.Central.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))
data$Prelaryngeal.Lymph.Node.Metastasis<-factor(data$Prelaryngeal.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))
data$Paratracheal.Lymph.Node.Metastasis<-factor(data$Paratracheal.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))
data$Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis<-factor(data$Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis,levels = c(0,1),labels = c("No", "Yes"))

```


```{r}

### 4.1.2 整合数据
x <- as.data.frame(data)
dd <- datadist(data)
options(datadist = 'dd')
data
### 4.2 Logistic回归比GLM好用
fit1 <- lrm(Level.IV.Lymph.Node.Metastasis ~Aspect.ratio+Calcification+Tumor.internal.vascularization+Size+Ipsilateral.Central.Lymph.Node.Metastasis+Paratracheal.Lymph.Node.Metastasis.Rate+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate,
            data = x , x = TRUE, y = TRUE)

fit1
summary(fit1) # 可以直接给到一些结果很好

nom1 <- nomogram(fit1, fun = plogis, fun.at = c(.001, .01, .05, seq(.1, .9, by = .1), .95, .99, .999),
                 lp = FALSE, funlabel = "Level IV Lymph Node Metastasis")
plot(nom1)

### 4.4 验证曲线
cal1 <- calibrate(fit1, method = 'boot', B = 1000)
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))

# 保存列线图为1200 DPI的 .tiff格式
tiff("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/nomogram.tiff", width = 8, height = 6, units = "in", res = 1200, compression = "lzw")
plot(nom1)
dev.off()

# 保存列线图为1200 DPI的 .png格式
png("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/nomogram.png", width = 8, height = 6, units = "in", res = 1200)
plot(nom1)
dev.off()

# 保存列线图为1200 DPI的 .eps格式
postscript("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/nomogram.eps", width = 8, height = 6, horizontal = FALSE, onefile = FALSE, paper = "special")
plot(nom1)
dev.off()

# 保存验证曲线为1200 DPI的 .tiff格式
tiff("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/calibration.tiff", width = 8, height = 6, units = "in", res = 1200, compression = "lzw")
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))
dev.off()

# 保存验证曲线为1200 DPI的 .png格式
png("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/calibration.png", width = 8, height = 6, units = "in", res = 1200)
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))
dev.off()

# 保存验证曲线为1200 DPI的 .eps格式
postscript("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/calibration.eps", width = 8, height = 6, horizontal = FALSE, onefile = FALSE, paper = "special")
plot(cal1, xlim = c(0, 1.0), ylim = c(0, 1.0))
dev.off()



```


###4.1.2 调整列线图的图间距和因子名称的大小和间距
```{r}
# 设置绘图参数
par(mar = c(1, 2, 2, 2))  # 调整绘图边距

# 创建 nomogram
nom2 <- nomogram(fit1, fun = plogis, fun.at = c(0.001, 0.01, 0.05, seq(0.1, 0.9, by = 0.1), 0.95, 0.99, 0.999),
                 lp = FALSE, funlabel="Level IV Lymph Node Metastasis")

# 绘制 nomogram
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.45, varname.dist = 2000)


# 保存列线图为1200 DPI的 .tiff格式
tiff("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/nomogram.tiff", width = 8, height = 6, units = "in", res = 1200, compression = "lzw")
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)
dev.off()

# 保存列线图为1200 DPI的 .png格式
png("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/nomogram.png", width = 8, height = 6, units = "in", res = 1200)
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.5, varname.dist = 2000)
dev.off()

# 保存列线图为1200 DPI的 .eps格式
postscript("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/nomogram.eps", width = 8, height = 6, horizontal = FALSE, onefile = FALSE, paper = "special")
plot(nom2, abbreviate = FALSE, col.lines = "blue", col.points = "blue", cex.names = 0.1, cex.axis = 0.5,#这是列线图的线的字的大小
     cex.lab = 20, lwd.lines = 20, lwd.funnel = 20, cex.var = 0.55, varname.dist = 2000)
dev.off()







```


##3.2列线图ROC曲线的绘制--单roc

```{r}
# 加载必要的库
library(pROC)
library(ggplot2)

# 读取数据
train_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值矫正后.csv")
test_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/2.验证集编码填补缺失值矫正后.csv")

# 将训练数据按照7:3的比例随机分为训练集和验证集
# 设置随机数种子,以确保结果可复现
set.seed(123)
index <- 1:nrow(train_data)
shuffled_index <- sample(index)
tra_ratio <- 0.7  # 训练集比例
tra_size <- round(tra_ratio * nrow(train_data))
tra_data <- train_data[shuffled_index[1:tra_size], ]
val_data <- train_data[shuffled_index[(tra_size + 1):nrow(train_data)], ]

cat("训练集观测数量:", nrow(tra_data), "\n")
cat("验证集观测数量:", nrow(val_data), "\n")
cat("测试集观测数量:", nrow(test_data), "\n")

# 构建模型
fit1 <- glm(IV.Level.Lymph.Node.Metastasis ~Aspect.ratio+Calcification+Tumor.internal.vascularization+Size+Ipsilateral.Central.Lymph.Node.Metastasis+Paratracheal.Lymph.Node.Metastasis.Rate+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate,
            data = tra_data, family = binomial())

# 预测概率
train_probs <- predict(fit1, newdata = tra_data, type = "response")
val_probs <- predict(fit1, newdata = val_data, type = "response")
test_probs <- predict(fit1, newdata = test_data, type = "response")

train_response <- tra_data$IV.Level.Lymph.Node.Metastasis
val_response <- val_data$IV.Level.Lymph.Node.Metastasis
test_response <- test_data$IV.Level.Lymph.Node.Metastasis

# 创建ROC对象
train_roc <- roc(train_response, train_probs)
val_roc <- roc(val_response, val_probs)
test_roc <- roc(test_response, test_probs)

# 提取ROC曲线的坐标点
train_roc_data <- coords(train_roc, "all", ret = c("specificity", "sensitivity"))
val_roc_data <- coords(val_roc, "all", ret = c("specificity", "sensitivity"))
test_roc_data <- coords(test_roc, "all", ret = c("specificity", "sensitivity"))

# 转换为数据框
train_roc_data <- as.data.frame(train_roc_data)
val_roc_data <- as.data.frame(val_roc_data)
test_roc_data <- as.data.frame(test_roc_data)

# 绘制ROC曲线
roc_plot <- ggplot() +
  geom_line(data = train_roc_data, aes(x = 1 - specificity, y = sensitivity), color = "darkgreen", size = 0.6) +
  geom_line(data = val_roc_data, aes(x = 1 - specificity, y = sensitivity), color = "green", size = 0.6) +
  geom_line(data = test_roc_data, aes(x = 1 - specificity, y = sensitivity), color = "lightgreen", size = 0.6) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "black") +
  labs(title = "ROC for Level IV Lymph Node Metastasis Nomogram Prediction",
       x = "False Positive Rate", y = "True Positive Rate") +
  theme_minimal() +
  theme(legend.position = "none") +
  annotate("text", x = 0.7, y = 0.4, label = paste("Train set AUC =", round(auc(train_roc), 3)), size = 4, color = "darkgreen") +
  annotate("text", x = 0.7, y = 0.3, label = paste("Validation set AUC =", round(auc(val_roc), 3)), size = 4, color = "green") +
  annotate("text", x = 0.7, y = 0.2, label = paste("Test set AUC =", round(auc(test_roc), 3)), size = 4, color = "lightgreen")

# 保存ROC曲线为.tiff格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/roc_curve.tiff", plot = roc_plot, width = 8, height = 6, units = "in", dpi = 1200, compression = "lzw")

# 保存ROC曲线为.png格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/roc_curve.png", plot = roc_plot, width = 8, height = 6, units = "in", dpi = 1200)

# 保存ROC曲线为.eps格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/roc_curve.eps", plot = roc_plot, width = 8, height = 6, units = "in", dpi = 1200)

```


```{r}
# 加载必要的库
library(pROC)
library(ggplot2)
library(dplyr)

# 读取数据
train_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值矫正后.csv")
test_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/2.验证集编码填补缺失值矫正后.csv")

# 按均值填补缺失值
fill_na_with_mean <- function(df) {
  df %>%
    mutate(across(everything(), ~ ifelse(is.na(.), mean(., na.rm = TRUE), .)))
}

train_data <- fill_na_with_mean(train_data)
test_data <- fill_na_with_mean(test_data)

# 将训练数据按照7:3的比例随机分为训练集和验证集
set.seed(123)
index <- 1:nrow(train_data)
shuffled_index <- sample(index)
tra_ratio <- 0.7  # 训练集比例
tra_size <- round(tra_ratio * nrow(train_data))
tra_data <- train_data[shuffled_index[1:tra_size], ]
val_data <- train_data[shuffled_index[(tra_size + 1):nrow(train_data)], ]

cat("训练集观测数量:", nrow(tra_data), "\n")
cat("验证集观测数量:", nrow(val_data), "\n")
cat("测试集观测数量:", nrow(test_data), "\n")

# 构建模型
fit1 <- glm(IV.Level.Lymph.Node.Metastasis ~Aspect.ratio+Calcification+Tumor.internal.vascularization+Size+Ipsilateral.Central.Lymph.Node.Metastasis+Paratracheal.Lymph.Node.Metastasis.Rate+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate,
            data = tra_data, family = binomial())

# 预测概率
train_probs <- predict(fit1, newdata = tra_data, type = "response")
val_probs <- predict(fit1, newdata = val_data, type = "response")
test_probs <- predict(fit1, newdata = test_data, type = "response")

train_response <- tra_data$IV.Level.Lymph.Node.Metastasis
val_response <- val_data$IV.Level.Lymph.Node.Metastasis
test_response <- test_data$IV.Level.Lymph.Node.Metastasis


# 定义净收益计算函数
net_benefit <- function(probs, outcome, threshold) {
  tp <- sum(outcome == 1 & probs >= threshold)
  fp <- sum(outcome == 0 & probs >= threshold)
  total_population <- length(outcome)
  
  if (total_population == 0) {
    return(0)
  }
  
  net_benefit <- (tp / total_population) - ((fp / total_population) * (threshold / (1 - threshold)))
  return(net_benefit)
}

# 计算不同阈值下的净收益
thresholds <- seq(0, 1, by = 0.01)
train_net_benefits <- sapply(thresholds, function(x) net_benefit(train_probs, train_response, x))
val_net_benefits <- sapply(thresholds, function(x) net_benefit(val_probs, val_response, x))
test_net_benefits <- sapply(thresholds, function(x) net_benefit(test_probs, test_response, x))

# 计算所有人都进行干预时的净收益
all_net_benefit <- sapply(thresholds, function(x) net_benefit(rep(1, length(val_response)), val_response, x))

# 计算没有人进行干预时的净收益
none_net_benefit <- rep(0, length(thresholds))

# 找到最大净收益点
train_max_nb <- max(train_net_benefits)
train_max_nb_threshold <- thresholds[which.max(train_net_benefits)]
val_max_nb <- max(val_net_benefits)
val_max_nb_threshold <- thresholds[which.max(val_net_benefits)]
test_max_nb <- max(test_net_benefits)
test_max_nb_threshold <- thresholds[which.max(test_net_benefits)]

# 绘制DCA曲线
dca_data <- data.frame(
  threshold = thresholds,
  train_net_benefit = train_net_benefits,
  val_net_benefit = val_net_benefits,
  test_net_benefit = test_net_benefits,
  all_net_benefit = all_net_benefit,
  none_net_benefit = none_net_benefit
)

dca_plot <- ggplot(dca_data, aes(x = threshold)) +
  geom_line(aes(y = train_net_benefit, color = "Train set"), size = 0.6) +
  geom_line(aes(y = val_net_benefit, color = "Test set"), size = 0.6) +
  geom_line(aes(y = test_net_benefit, color = "Validation set"), size = 0.6) +
  geom_line(aes(y = all_net_benefit, color = "All"), linetype = "dotted", size = 0.6) +
  geom_line(aes(y = none_net_benefit, color = "None"), linetype = "solid", size = 0.6) +
  labs(title = "DCA for Level IV Lymph Node Metastasis Nomogram Prediction",
       x = "Threshold Probability", y = "Net Benefit") +
  scale_color_manual(values = c("Train set" = "darkgreen", "Test set" = "green", "Validation set" = "lightgreen", "All" = "grey", "None" = "black")) +
  theme_minimal() +
  theme(legend.position = "right") +
  annotate("text", x = 0.4, y = 0.1, label = "Train set", size = 4, color = "darkgreen") +
  annotate("text", x = 0.4, y = 0.05, label = "Test set", size = 4, color = "green") +
  annotate("text", x = 0.4, y = 0.01, label = "Validation set", size = 4, color = "lightgreen") +
  annotate("text", x = train_max_nb_threshold, y = train_max_nb, label = sprintf("Max: %.3f", train_max_nb), color = "darkgreen", vjust = -1) +
  annotate("text", x = val_max_nb_threshold, y = val_max_nb, label = sprintf("Max: %.3f", val_max_nb), color = "green", vjust = -1) +
  annotate("text", x = test_max_nb_threshold, y = test_max_nb, label = sprintf("Max: %.3f", test_max_nb), color = "lightgreen", vjust = -1) +
  coord_cartesian(ylim = c(-0.05, 0.3), xlim = c(0, 0.6))


# 保存ROC曲线为.tiff格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/dca_curve.tiff", plot = dca_plot, width = 8, height = 6, units = "in", dpi = 1200, compression = "lzw")

# 保存ROC曲线为.png格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/dca_curve.png", plot = dca_plot, width = 8, height = 6, units = "in", dpi = 1200)

# 保存ROC曲线为.eps格式
ggsave("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/4、四区的结果/dca_curve.eps", plot = dca_plot, width = 8, height = 6, units = "in", dpi = 1200)

print(dca_plot)

```

#总的rOC曲线
```{r}
# 加载必要的库
library(pROC)
library(ggplot2)

# 读取数据
train_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值矫正后.csv")
test_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/2.验证集编码填补缺失值矫正后.csv")


# 将训练数据按照7:3的比例随机分为训练集和验证集
set.seed(123)
index <- 1:nrow(train_data)
shuffled_index <- sample(index)
tra_ratio <- 0.7  # 训练集比例
tra_size <- round(tra_ratio * nrow(train_data))
tra_data <- train_data[shuffled_index[1:tra_size], ]
val_data <- train_data[shuffled_index[(tra_size + 1):nrow(train_data)], ]

cat("训练集观测数量:", nrow(tra_data), "\n")
cat("验证集观测数量:", nrow(val_data), "\n")
cat("测试集观测数量:", nrow(test_data), "\n")
```


```{r}
# 侧区模型
fit1 <- glm(Ipsilateral.Lateral.Lymph.Node.Metastasis ~ Tumor.border + Aspect.ratio + Calcification + Tumor.internal.vascularization + Extrathyroidal.extension + Size + Location +Pretracheal.Lymph.Node.Metastasis+ Prelaryngeal.Lymph.Node.Metastasis+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis,
           data = tra_data, family = binomial())
train_probs1 <- predict(fit1, newdata = tra_data, type = "response")
val_probs1 <- predict(fit1, newdata = val_data, type = "response")
test_probs1 <- predict(fit1, newdata = test_data, type = "response")
train_response1 <- tra_data$Ipsilateral.Lateral.Lymph.Node.Metastasis
val_response1 <- val_data$Ipsilateral.Lateral.Lymph.Node.Metastasis
test_response1 <- test_data$Ipsilateral.Lateral.Lymph.Node.Metastasis
train_roc1 <- roc(train_response1, train_probs1)
val_roc1 <- roc(val_response1, val_probs1)
test_roc1 <- roc(test_response1, test_probs1)

# II区模型
fit2 <- glm(II.Level.Lymph.Node.Metastasis ~ Aspect.ratio + Calcification + Size + Location + Mulifocality + Ipsilateral.Central.Lymph.Node.Metastasis + Prelaryngeal.Lymph.Node.Metastases.Number,
           data = tra_data, family = binomial())
train_probs2 <- predict(fit2, newdata = tra_data, type = "response")
val_probs2 <- predict(fit2, newdata = val_data, type = "response")
test_probs2 <- predict(fit2, newdata = test_data, type = "response")
train_response2 <- tra_data$II.Level.Lymph.Node.Metastasis
val_response2 <- val_data$II.Level.Lymph.Node.Metastasis
test_response2 <- test_data$II.Level.Lymph.Node.Metastasis
train_roc2 <- roc(train_response2, train_probs2)
val_roc2 <- roc(val_response2, val_probs2)
test_roc2 <- roc(test_response2, test_probs2)

# III区模型
fit3 <- glm(III.Level.Lymph.Node.Metastasis ~ Age + Tumor.border + Calcification + Tumor.internal.vascularization + Extrathyroidal.extension + Size + Ipsilateral.Central.Lymph.Node.Metastasis + Pretracheal.Lymph.Node.Metastasis.Rate + Paratracheal.Lymph.Node.Metastasis.Rate + Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate,
           data = tra_data, family = binomial())
train_probs3 <- predict(fit3, newdata = tra_data, type = "response")
val_probs3 <- predict(fit3, newdata = val_data, type = "response")
test_probs3 <- predict(fit3, newdata = test_data, type = "response")
train_response3 <- tra_data$III.Level.Lymph.Node.Metastasis
val_response3 <- val_data$III.Level.Lymph.Node.Metastasis
test_response3 <- test_data$III.Level.Lymph.Node.Metastasis
train_roc3 <- roc(train_response3, train_probs3)
val_roc3 <- roc(val_response3, val_probs3)
test_roc3 <- roc(test_response3, test_probs3)

# IV区模型
fit4 <- glm(IV.Level.Lymph.Node.Metastasis ~Aspect.ratio+Calcification+Tumor.internal.vascularization+Size+Ipsilateral.Central.Lymph.Node.Metastasis+Paratracheal.Lymph.Node.Metastasis.Rate+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate,
           data = tra_data, family = binomial())
train_probs4 <- predict(fit4, newdata = tra_data, type = "response")
val_probs4 <- predict(fit4, newdata = val_data, type = "response")
test_probs4 <- predict(fit4, newdata = test_data, type = "response")
train_response4 <- tra_data$IV.Level.Lymph.Node.Metastasis
val_response4 <- val_data$IV.Level.Lymph.Node.Metastasis
test_response4 <- test_data$IV.Level.Lymph.Node.Metastasis
train_roc4 <- roc(train_response4, train_probs4)
val_roc4 <- roc(val_response4, val_probs4)
test_roc4 <- roc(test_response4, test_probs4)

# 提取ROC曲线的坐标点
# 提取ROC曲线的坐标点
train_roc_data1 <- data.frame(coords(train_roc1, "all"))
train_roc_data2 <- data.frame(coords(train_roc2, "all"))
train_roc_data3 <- data.frame(coords(train_roc3, "all"))
train_roc_data4 <- data.frame(coords(train_roc4, "all"))

val_roc_data1 <- data.frame(coords(val_roc1, "all"))
val_roc_data2 <- data.frame(coords(val_roc2, "all"))
val_roc_data3 <- data.frame(coords(val_roc3, "all"))
val_roc_data4 <- data.frame(coords(val_roc4, "all"))
test_roc_data2 <- data.frame(coords(test_roc2, "all"))
test_roc_data1 <- data.frame(coords(test_roc1, "all"))


test_roc_data3 <- data.frame(coords(test_roc3, "all"))



test_roc_data4 <- data.frame(coords(test_roc4, "all"))
```















##这是在计算评价指标
```{r}
# 安装必要的包
install.packages("pROC")
install.packages("caret")
install.packages("Metrics")

# 加载包
library(pROC)
library(caret)
library(Metrics)

```
```{r}



# 定义函数来计算所有指标
compute_metrics <- function(response, probs, threshold = 0.5) {
  predicted <- ifelse(probs >= threshold, 1, 0)
  
  confusion <- confusionMatrix(factor(predicted), factor(response))
  
  accuracy <- confusion$overall['Accuracy']
  specificity <- confusion$byClass['Specificity']
  sensitivity <- confusion$byClass['Sensitivity']
  npv <- confusion$byClass['Neg Pred Value']
  ppv <- confusion$byClass['Pos Pred Value']
  f1 <- 2 * (ppv * sensitivity) / (ppv + sensitivity)
  auc <- roc(response, probs)$auc
  false_positive_rate <- 1 - specificity
  brier_score <- mean((probs - response)^2)
  kappa <- confusion$overall['Kappa']
  rmse_value <- rmse(response, probs)
  r2_value <- R2(response, probs)
  mae_value <- mae(response, probs)
  lift <- (sum(predicted) / length(predicted)) / (sum(response) / length(response))
  
  cat("Accuracy:", accuracy, "\n")
  cat("AUC:", auc, "\n")
  cat("Specificity:", specificity, "\n")
  cat("Sensitivity:", sensitivity, "\n")
  cat("NPV:", npv, "\n")
  cat("PPV:", ppv, "\n")
  cat("F1 Score:", f1, "\n")
  cat("False Positive Rate:", false_positive_rate, "\n")
  cat("Brier Score:", brier_score, "\n")
  cat("Kappa:", kappa, "\n")
  cat("RMSE:", rmse_value, "\n")
  cat("R2:", r2_value, "\n")
  cat("MAE:", mae_value, "\n")
  cat("Lift:", lift, "\n")
  
  return(c(accuracy, auc, specificity, sensitivity, npv, ppv, f1, false_positive_rate, lift, brier_score, kappa, rmse_value, r2_value, mae_value))
}

# 计算所有数据集上的指标
metrics_names <- c("Accuracy", "AUC", "Specificity", "Sensitivity/Recall", "Negative Predictive Value", 
                   "Positive Predictive Value/Precision", "F1 Score", "False Positive Rate", "Lift", 
                   "Brier Score", "Kappa", "RMSE", "R2", "MAE")

results <- data.frame(matrix(nrow = 12, ncol = 14))
colnames(results) <- metrics_names

# 训练集
results[1, ] <- compute_metrics(tra_data$Ipsilateral.Lateral.Lymph.Node.Metastasis, train_probs1)
results[2, ] <- compute_metrics(tra_data$II.Level.Lymph.Node.Metastasis, train_probs2)
results[3, ] <- compute_metrics(tra_data$III.Level.Lymph.Node.Metastasis, train_probs3)
results[4, ] <- compute_metrics(tra_data$IV.Level.Lymph.Node.Metastasis, train_probs4)

# 验证集
results[5, ] <- compute_metrics(val_data$Ipsilateral.Lateral.Lymph.Node.Metastasis, val_probs1)
results[6, ] <- compute_metrics(val_data$II.Level.Lymph.Node.Metastasis, val_probs2)
results[7, ] <- compute_metrics(val_data$III.Level.Lymph.Node.Metastasis, val_probs3)
results[8, ] <- compute_metrics(val_data$IV.Level.Lymph.Node.Metastasis, val_probs4)

# 测试集
results[9, ] <- compute_metrics(test_data$Ipsilateral.Lateral.Lymph.Node.Metastasis, test_probs1)
results[10, ] <- compute_metrics(test_data$II.Level.Lymph.Node.Metastasis, test_probs2)
results[11, ] <- compute_metrics(test_data$III.Level.Lymph.Node.Metastasis, test_probs3)
results[12, ] <- compute_metrics(test_data$IV.Level.Lymph.Node.Metastasis, test_probs4)

# 设置行名
row.names(results) <- c("同侧侧区_训练集", "II区_训练集", "III区_训练集", "IV区_训练集", 
                        "同侧侧区_验证集", "II区_验证集", "III区_验证集", "IV区_验证集", 
                        "同侧侧区_测试集", "II区_测试集", "III区_测试集", "IV区_测试集")

# 导出到CSV文件
write.csv(results, "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/0.评价指标1.csv", row.names = TRUE)


```

###这是在绘制ROC曲线
```{r}
plot1 <- ggplot() +
  geom_line(data = train_roc_data1, aes(x = 1 - specificity, y = sensitivity), color = "goldenrod", size = 0.6) +
  geom_line(data = val_roc_data1, aes(x = 1 - specificity, y = sensitivity), color = "orange", size = 0.6) +
  geom_line(data = test_roc_data1, aes(x = 1 - specificity, y = sensitivity), color = "gold", size = 0.6) +
  geom_line(data = train_roc_data2, aes(x = 1 - specificity, y = sensitivity), color = "#C71585", size = 0.6) +
  geom_line(data = val_roc_data2, aes(x = 1 - specificity, y = sensitivity), color = "red", size = 0.6) +
  geom_line(data = test_roc_data2, aes(x = 1 - specificity, y = sensitivity), color = "pink", size = 0.6) +
  geom_line(data = train_roc_data3, aes(x = 1 - specificity, y = sensitivity), color = "darkblue", size = 0.6) +
  geom_line(data = val_roc_data3, aes(x = 1 - specificity, y = sensitivity), color = "blue", size = 0.6) +
  geom_line(data = test_roc_data3, aes(x = 1 - specificity, y = sensitivity), color = "skyblue", size = 0.6) +
  geom_line(data = train_roc_data4, aes(x = 1 - specificity, y = sensitivity), color = "darkgreen", size = 0.6) +
  geom_line(data = val_roc_data4, aes(x = 1 - specificity, y = sensitivity), color = "green", size = 0.6) +
  geom_line(data = test_roc_data4, aes(x = 1 - specificity, y = sensitivity), color = "lightgreen", size = 0.6) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "black") +
  labs(title = "ROC Curves for Lymph Node Metastasis Nomogram Prediction (All Sets)", size = 3,
       x = "False Positive Rate", y = "True Positive Rate") +
  theme_minimal() +
  theme(legend.position = "none") +
  annotate("text", x = 0.7, y = 0.56, label = paste("Ipsilateral lateral Lymph Node Metastasis Train  AUC =", round(auc(train_roc1), 3)), size = 3, color = "goldenrod") +
  annotate("text", x = 0.7, y = 0.51, label = paste("Ipsilateral lateral Lymph Node Metastasis Test AUC =", round(auc(val_roc1), 3)), size = 3, color = "orange") +
  annotate("text", x = 0.7, y = 0.46, label = paste("Ipsilateral lateral Lymph Node Metastasis Validation AUC =", round(auc(test_roc1), 3)), size = 3, color = "gold") +
  annotate("text", x = 0.7, y = 0.41, label = paste("Level II Lymph Node Metastasis Train  AUC =", round(auc(train_roc2), 3)), size = 3, color = "#C71585") +
  annotate("text", x = 0.7, y = 0.36, label = paste("Level II Lymph Node Metastasis Test AUC =", round(auc(val_roc2), 3)), size = 3, color = "red") +
  annotate("text", x = 0.7, y = 0.31, label = paste("Level II Lymph Node Metastasis Validation AUC =", round(auc(test_roc2), 3)), size = 3, color = "pink") +
  annotate("text", x = 0.7, y = 0.26, label = paste("Level III Lymph Node Metastasis Train AUC =", round(auc(train_roc3), 3)), size = 3, color = "darkblue") +
  annotate("text", x = 0.7, y = 0.21, label = paste("Level III Lymph Node Metastasis Test AUC =", round(auc(val_roc3), 3)), size = 3, color = "blue") +
  annotate("text", x = 0.7, y = 0.16, label = paste("Level III Lymph Node Metastasis Validation AUC =", round(auc(test_roc3), 3)), size = 3, color = "skyblue") + 
  annotate("text", x = 0.7, y = 0.11, label = paste("Level IV Lymph Node Metastasis Train AUC =", round(auc(train_roc4), 3)), size = 3, color = "darkgreen") +
  annotate("text", x = 0.7, y = 0.06, label = paste("Level IV Lymph Node Metastasis Validation AUC =", round(auc(val_roc4), 3)), size = 3, color = "green") + 
  annotate("text", x = 0.7, y = 0.01, label = paste("Level IV Lymph Node Metastasis Validation AUC =", round(auc(test_roc4), 3)), size = 3, color = "lightgreen")
print(plot1)


plot2 <- ggplot() +
  geom_line(data = train_roc_data1, aes(x = 1 - specificity, y = sensitivity), color = "goldenrod", size = 0.6) +
  geom_line(data = train_roc_data2, aes(x = 1 - specificity, y = sensitivity), color = "#C71585", size = 0.6) +
  geom_line(data = train_roc_data3, aes(x = 1 - specificity, y = sensitivity), color = "darkblue", size = 0.6) +
  geom_line(data = train_roc_data4, aes(x = 1 - specificity, y = sensitivity), color = "darkgreen", size = 0.6) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "black") +
  labs(title = "ROC Curves for Lymph Node Metastasis Nomogram Prediction (Train Set)", 
       x = "False Positive Rate", y = "True Positive Rate") +
  theme_minimal() +
  theme(legend.position = "none") +
  annotate("text", x = 0.7, y = 0.16, label = paste("Ipsilateral lateral Lymph Node Metastasis Train AUC =", round(auc(train_roc1), 3)), size = 3.5, color = "goldenrod") +
  annotate("text", x = 0.7, y = 0.11, label = paste("Level II Lymph Node Metastasis Train AUC =", round(auc(train_roc2), 3)), size = 3.5, color = "#C71585") +
  annotate("text", x = 0.7, y = 0.06, label = paste("Level III Lymph Node Metastasis Train AUC =", round(auc(train_roc3), 3)), size = 3.5, color = "darkblue") +
  annotate("text", x = 0.7, y = 0.01, label = paste("Level IV Lymph Node Metastasis Train AUC =", round(auc(train_roc4), 3)), size = 3.5, color = "darkgreen")
print(plot2)

plot3 <- ggplot() +
  geom_line(data = val_roc_data1, aes(x = 1 - specificity, y = sensitivity), color = "orange", size = 0.6) +
  geom_line(data = val_roc_data2, aes(x = 1 - specificity, y = sensitivity), color = "red", size = 0.6) +
  geom_line(data = val_roc_data3, aes(x = 1 - specificity, y = sensitivity), color = "blue", size = 0.6) +
  geom_line(data = val_roc_data4, aes(x = 1 - specificity, y = sensitivity), color = "green", size = 0.6) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "black") +
  labs(title = "ROC Curves for Lymph Node Metastasis Nomogram Prediction (Test Set)", 
       x = "False Positive Rate", y = "True Positive Rate") +
  theme_minimal() +
  theme(legend.position = "none") +
  annotate("text", x = 0.7, y = 0.16, label = paste("Ipsilateral lateral Lymph Node Metastasis Test AUC =", round(auc(val_roc1), 3)), size = 3.5, color = "orange") +
  annotate("text", x = 0.7, y = 0.11, label = paste("Level II Lymph Node Metastasis Test AUC =", round(auc(val_roc2), 3)), size = 3.5, color = "red") +
  annotate("text", x = 0.7, y = 0.06, label = paste("Level III Lymph Node Metastasis Test AUC =", round(auc(val_roc3), 3)), size = 3.5, color = "blue") +
  annotate("text", x = 0.7, y = 0.01, label = paste("Level IV Lymph Node Metastasis Test AUC =", round(auc(val_roc4), 3)), size = 3.5, color = "green")
print(plot3)

plot4 <- ggplot() +
  geom_line(data = test_roc_data1, aes(x = 1 - specificity, y = sensitivity), color = "gold", size = 0.6) +
  geom_line(data = test_roc_data2, aes(x = 1 - specificity, y = sensitivity), color = "pink", size = 0.6) +
  geom_line(data = test_roc_data3, aes(x = 1 - specificity, y = sensitivity), color = "skyblue", size = 0.6) +
  geom_line(data = test_roc_data4, aes(x = 1 - specificity, y = sensitivity), color = "lightgreen", size = 0.6) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "black") +
  labs(title = "ROC Curves for Lymph Node Metastasis Nomogram Prediction (Validation Set)", 
       x = "False Positive Rate", y = "True Positive Rate") +
  theme_minimal() +
  theme(legend.position = "none") +
  annotate("text", x = 0.7, y = 0.16, label = paste("Ipsilateral lateral Lymph Node Metastasis Validation AUC =", round(auc(test_roc1), 3)), size = 3.5, color = "gold") +
  annotate("text", x = 0.7, y = 0.11, label = paste("Level II Lymph Node Metastasis Validation AUC =", round(auc(test_roc2), 3)), size = 3.5, color = "pink") +
  annotate("text", x = 0.7, y = 0.06, label = paste("Level III Lymph Node Metastasis Validation AUC =", round(auc(test_roc3), 3)), size = 3.5, color = "skyblue") +
  annotate("text", x = 0.7, y = 0.01, label = paste("Level IV Lymph Node Metastasis Validation AUC =", round(auc(test_roc4), 3)), size = 3.5, color = "lightgreen")
print(plot4)
#install.packages("ggplot2")
#install.packages("gplots")

# 保存图像函数
save_roc_plot <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/0.总曲线"

# 保存每个图
save_roc_plot(plot1, file.path(output_folder, "ROC_Curves_All_Sets"))
save_roc_plot(plot2, file.path(output_folder, "ROC_Curves_Train_Set"))
save_roc_plot(plot3, file.path(output_folder, "ROC_Curves_Test_Set"))
save_roc_plot(plot4, file.path(output_folder, "ROC_Curves_Validation_Set"))



```
```{r}
# 提取ROC曲线的坐标点
train_roc_data1 <- data.frame(coords(train_roc1, "all"))
val_roc_data1 <- data.frame(coords(val_roc1, "all"))
test_roc_data1 <- data.frame(coords(test_roc1, "all"))

train_roc_data2 <- data.frame(coords(train_roc2, "all"))
val_roc_data2 <- data.frame(coords(val_roc2, "all"))
test_roc_data2 <- data.frame(coords(test_roc2, "all"))

train_roc_data3 <- data.frame(coords(train_roc3, "all"))
val_roc_data3 <- data.frame(coords(val_roc3, "all"))
test_roc_data3 <- data.frame(coords(test_roc3, "all"))

train_roc_data4 <- data.frame(coords(train_roc4, "all"))
val_roc_data4 <- data.frame(coords(val_roc4, "all"))
test_roc_data4 <- data.frame(coords(test_roc4, "all"))

```




```{r}
plot2 <- ggplot() +
  geom_line(data = train_roc_data1, aes(x = 1 - specificity, y = sensitivity), color = "goldenrod", size = 0.6) +
  geom_line(data = train_roc_data2, aes(x = 1 - specificity, y = sensitivity), color = "#C71585", size = 0.6)  +
  geom_line(data = train_roc_data3, aes(x = 1 - specificity, y = sensitivity), color = "darkblue", size = 0.6) +
  geom_line(data = train_roc_data4, aes(x = 1 - specificity, y = sensitivity), color = "darkgreen", size = 0.6) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "black") +
  labs(title = "ROC Curves for Lymph Node Metastasis Nomogram Prediction (Train Set)", 
       x = "False Positive Rate", y = "True Positive Rate") +
  theme_minimal() +
  theme(legend.position = "none") +
  annotate("text", x = 0.7, y = 0.16, label = paste("Ipsilateral lateral Lymph Node Metastasis Train AUC =", round(auc(train_roc1), 3)), size = 3.5, color = "goldenrod") +
  annotate("text", x = 0.7, y = 0.11, label = paste("Level II Lymph Node Metastasis Train AUC =", round(auc(train_roc2), 3)), size = 3.5, color = "#C71585") +
  annotate("text", x = 0.7, y = 0.06, label = paste("Level III Lymph Node Metastasis Train AUC =", round(auc(train_roc3), 3)), size = 3.5, color = "darkblue") +
  annotate("text", x = 0.7, y = 0.01, label = paste("Level IV Lymph Node Metastasis Train AUC =", round(auc(train_roc4), 3)), size = 3.5, color = "darkgreen")
print(plot2)


```


```{r}
plot3 <- ggplot() +
  geom_line(data = val_roc_data1, aes(x = 1 - specificity, y = sensitivity), color = "orange", size = 0.6) +
  geom_line(data = val_roc_data2, aes(x = 1 - specificity, y = sensitivity), color = "red", size = 0.6) +
  geom_line(data = val_roc_data3, aes(x = 1 - specificity, y = sensitivity), color = "blue", size = 0.6) +
  geom_line(data = val_roc_data4, aes(x = 1 - specificity, y = sensitivity), color = "green", size = 0.6) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "black") +
  labs(title = "ROC Curves for Lymph Node Metastasis Nomogram Prediction (Test Set)", 
       x = "False Positive Rate", y = "True Positive Rate") +
  theme_minimal() +
  theme(legend.position = "none") +
  annotate("text", x = 0.7, y = 0.16, label = paste("Ipsilateral lateral Lymph Node Metastasis Test AUC =", round(auc(val_roc1), 3)), size = 3.5, color = "orange") +
  annotate("text", x = 0.7, y = 0.11, label = paste("Level II Lymph Node Metastasis Test AUC =", round(auc(val_roc2), 3)), size = 3.5, color = "red") +
  annotate("text", x = 0.7, y = 0.06, label = paste("Level III Lymph Node Metastasis Test AUC =", round(auc(val_roc3), 3)), size = 3.5, color = "blue") +
  annotate("text", x = 0.7, y = 0.01, label = paste("Level IV Lymph Node Metastasis Test AUC =", round(auc(val_roc4), 3)), size = 3.5, color = "green")
print(plot3)

```


```{r}
plot4 <- ggplot() +
  geom_line(data = test_roc_data1, aes(x = 1 - specificity, y = sensitivity), color = "gold", size = 0.6) +
  geom_line(data = test_roc_data2, aes(x = 1 - specificity, y = sensitivity), color = "pink", size = 0.6) +
  geom_line(data = test_roc_data3, aes(x = 1 - specificity, y = sensitivity), color = "skyblue", size = 0.6) +
  geom_line(data = test_roc_data4, aes(x = 1 - specificity, y = sensitivity), color = "lightgreen", size = 0.6) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "black") +
  labs(title = "ROC Curves for Lymph Node Metastasis Nomogram Prediction (Validation Set)", 
       x = "False Positive Rate", y = "True Positive Rate") +
  theme_minimal() +
  theme(legend.position = "none") +
  annotate("text", x = 0.7, y = 0.16, label = paste("Ipsilateral lateral Lymph Node Metastasis Validation AUC =", round(auc(test_roc1), 3)), size = 3.5, color = "gold") +
  annotate("text", x = 0.7, y = 0.11, label = paste("Level II Lymph Node Metastasis Validation AUC =", round(auc(test_roc2), 3)), size = 3.5, color = "pink") +
  annotate("text", x = 0.7, y = 0.06, label = paste("Level III Lymph Node Metastasis Validation AUC =", round(auc(test_roc3), 3)), size = 3.5, color = "skyblue") +
  annotate("text", x = 0.7, y = 0.01, label = paste("Level IV Lymph Node Metastasis Validation AUC =", round(auc(test_roc4), 3)), size = 3.5, color = "lightgreen")
print(plot4)

```

```{r}
# 加载必要的库
library(pROC)
library(ggplot2)
library(dplyr)

# 读取数据
train_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值矫正后.csv")
test_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/2.验证集编码填补缺失值矫正后.csv")

# 按均值填补缺失值
fill_na_with_mean <- function(df) {
  df %>%
    mutate(across(everything(), ~ ifelse(is.na(.), mean(., na.rm = TRUE), .)))
}

train_data <- fill_na_with_mean(train_data)
test_data <- fill_na_with_mean(test_data)

# 将训练数据按照7:3的比例随机分为训练集和验证集
set.seed(123)
index <- 1:nrow(train_data)
shuffled_index <- sample(index)
tra_ratio <- 0.7  # 训练集比例
tra_size <- round(tra_ratio * nrow(train_data))
tra_data <- train_data[shuffled_index[1:tra_size], ]
val_data <- train_data[shuffled_index[(tra_size + 1):nrow(train_data)], ]

cat("训练集观测数量:", nrow(tra_data), "\n")
cat("验证集观测数量:", nrow(val_data), "\n")
cat("测试集观测数量:", nrow(test_data), "\n")

# 构建模型
fit4 <- glm(IV.Level.Lymph.Node.Metastasis ~ Aspect.ratio + Calcification + Tumor.internal.vascularization + Size + Ipsilateral.Central.Lymph.Node.Metastasis + Paratracheal.Lymph.Node.Metastasis.Rate + Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate, data = tra_data, family = binomial())
fit2 <- glm(II.Level.Lymph.Node.Metastasis ~ Aspect.ratio + Calcification + Tumor.internal.vascularization + Size + Ipsilateral.Central.Lymph.Node.Metastasis + Paratracheal.Lymph.Node.Metastasis.Rate + Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate, data = tra_data, family = binomial())
fit3 <- glm(III.Level.Lymph.Node.Metastasis ~ Aspect.ratio + Calcification + Tumor.internal.vascularization + Size + Ipsilateral.Central.Lymph.Node.Metastasis + Paratracheal.Lymph.Node.Metastasis.Rate + Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate, data = tra_data, family = binomial())
fit1 <- glm(Ipsilateral.Lateral.Lymph.Node.Metastasis ~ Tumor.border + Aspect.ratio + Calcification + Tumor.internal.vascularization + Extrathyroidal.extension + Size + Location +Pretracheal.Lymph.Node.Metastasis+ Prelaryngeal.Lymph.Node.Metastasis+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis, data = tra_data, family = binomial())

# 预测概率
train_probs4 <- predict(fit4, newdata = tra_data, type = "response")
train_probs2 <- predict(fit2, newdata = tra_data, type = "response")
train_probs3 <- predict(fit3, newdata = tra_data, type = "response")
train_probs1 <- predict(fit1, newdata = tra_data, type = "response")

train_response4 <- tra_data$IV.Level.Lymph.Node.Metastasis
train_response2 <- tra_data$II.Level.Lymph.Node.Metastasis
train_response3 <- tra_data$III.Level.Lymph.Node.Metastasis
train_response1 <- tra_data$Ipsilateral.Lateral.Lymph.Node.Metastasis

# 定义净收益计算函数
net_benefit <- function(probs, outcome, threshold) {
  tp <- sum(outcome == 1 & probs >= threshold)
  fp <- sum(outcome == 0 & probs >= threshold)
  total_population <- length(outcome)
  
  if (total_population == 0) {
    return(0)
  }
  
  net_benefit <- (tp / total_population) - ((fp / total_population) * (threshold / (1 - threshold)))
  return(net_benefit)
}

# 计算不同阈值下的净收益
thresholds <- seq(0, 1, by = 0.01)
train_net_benefits1 <- sapply(thresholds, function(x) net_benefit(train_probs1, train_response1, x))
train_net_benefits2 <- sapply(thresholds, function(x) net_benefit(train_probs2, train_response2, x))
train_net_benefits3 <- sapply(thresholds, function(x) net_benefit(train_probs3, train_response3, x))
train_net_benefits4 <- sapply(thresholds, function(x) net_benefit(train_probs4, train_response4, x))

# 计算所有人都进行干预时的净收益
all_net_benefit <- sapply(thresholds, function(x) net_benefit(rep(1, length(train_response2)), train_response2, x))


# 计算没有人进行干预时的净收益
none_net_benefit <- rep(0, length(thresholds))

# 绘制DCA曲线
dca_data_train <- data.frame(
  threshold = thresholds,
  train_net_benefit1 = train_net_benefits1,
  train_net_benefit2 = train_net_benefits2,
  train_net_benefit3 = train_net_benefits3,
  train_net_benefit4 = train_net_benefits4,
  all_net_benefit = all_net_benefit,
  none_net_benefit = none_net_benefit
)

dca_plot <- ggplot(dca_data_train, aes(x = threshold)) + 
  geom_line(aes(y = train_net_benefit1, color = "Ipsilateral lateral Lymph Node Metastasis"), size = 0.6)+
  geom_line(aes(y = train_net_benefit2, color = "Level II Lymph Node Metastasis"), size = 0.6) +
  geom_line(aes(y = train_net_benefit3, color = "Level III Lymph Node Metastasis"), size = 0.6) +
  geom_line(aes(y = train_net_benefit4, color = "Level IV Lymph Node Metastasis"), size = 0.6) +
  geom_line(aes(y = all_net_benefit, color = "All"), linetype = "dotted", size = 0.6) +
  geom_line(aes(y = none_net_benefit, color = "None"), linetype = "solid", size = 0.6) +
  labs(title = "DCA for Lymph Node Metastasis Nomogram Prediction (Train Set)",
       x = "Threshold Probability", y = "Net Benefit") +
  scale_color_manual(values = c("Ipsilateral lateral Lymph Node Metastasis" = "goldenrod", "Level II Lymph Node Metastasis" = "#C71585", "Level III Lymph Node Metastasis" = "darkblue", "Level IV Lymph Node Metastasis" = "darkgreen", "All" = "grey", "None" = "black")) +
  theme_minimal() +
  theme(legend.position = "right") +
  coord_cartesian(ylim = c(-0.05, 0.45), xlim = c(0, 0.8))



# 保存图像函数
save_dca_plot <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/0.总曲线"

# 保存DCA曲线图
save_dca_plot(dca_plot, file.path(output_folder, "DCA_Lymph_Node_Metastasis_Train_Set"))

print(dca_plot)



```

```{r}
## 预测测试集概率
test_probs1 <- predict(fit1, newdata = test_data, type = "response")
test_probs2 <- predict(fit2, newdata = test_data, type = "response")
test_probs3 <- predict(fit3, newdata = test_data, type = "response")
test_probs4 <- predict(fit4, newdata = test_data, type = "response")

test_response1 <- test_data$Ipsilateral.Lateral.Lymph.Node.Metastasis
test_response2 <- test_data$II.Level.Lymph.Node.Metastasis
test_response3 <- test_data$III.Level.Lymph.Node.Metastasis
test_response4 <- test_data$IV.Level.Lymph.Node.Metastasis

# 计算不同阈值下的净收益
test_net_benefits1 <- sapply(thresholds, function(x) net_benefit(test_probs1, test_response1, x))
test_net_benefits2 <- sapply(thresholds, function(x) net_benefit(test_probs2, test_response2, x))
test_net_benefits3 <- sapply(thresholds, function(x) net_benefit(test_probs3, test_response3, x))
test_net_benefits4 <- sapply(thresholds, function(x) net_benefit(test_probs4, test_response4, x))

# 计算所有人都进行干预时的净收益
all_net_benefit_test <- sapply(thresholds, function(x) net_benefit(rep(1, length(test_response2)), test_response2, x))

# 绘制DCA曲线
dca_data_test <- data.frame(
  threshold = thresholds,
  test_net_benefit1 = test_net_benefits1,
  test_net_benefit2 = test_net_benefits2,
  test_net_benefit3 = test_net_benefits3,
  test_net_benefit4 = test_net_benefits4,
  all_net_benefit = all_net_benefit_test,
  none_net_benefit = none_net_benefit
)

dca_plot2 <- ggplot(dca_data_test, aes(x = threshold)) +
  geom_line(aes(y = test_net_benefit1, color = "Ipsilateral lateral Lymph Node Metastasis"), size = 0.6) +
  geom_line(aes(y = test_net_benefit2, color = "Level II Lymph Node Metastasis"), size = 0.6) +
  geom_line(aes(y = test_net_benefit3, color = "Level III Lymph Node Metastasis"), size = 0.6) +
  geom_line(aes(y = test_net_benefit4, color = "Level IV Lymph Node Metastasis"), size = 0.6) +
  geom_line(aes(y = all_net_benefit, color = "All"), linetype = "dotted", size = 0.6) +
  geom_line(aes(y = none_net_benefit, color = "None"), linetype = "solid", size = 0.6) +
  labs(title = "DCA for Lymph Node Metastasis Nomogram Prediction (Validation Set)",
       x = "Threshold Probability", y = "Net Benefit") +
  scale_color_manual(values = c("Ipsilateral lateral Lymph Node Metastasis" = "gold", "Level II Lymph Node Metastasis" = "pink", "Level III Lymph Node Metastasis" = "skyblue", "Level IV Lymph Node Metastasis" = "lightgreen", "All" = "grey", "None" = "black")) +
  theme_minimal() +
  theme(legend.position = "right") +
  coord_cartesian(ylim = c(-0.05, 0.5), xlim = c(0, 0.8))



# 保存图像函数
save_dca_plot2 <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/0.总曲线"

# 保存DCA曲线图
save_dca_plot2(dca_plot2, file.path(output_folder, "DCA_Lymph_Node_Metastasis_val_Set"))

print(dca_plot2)


```


```{r}
# 预测验证集概率
val_probs1 <- predict(fit1, newdata = val_data, type = "response")
val_probs2 <- predict(fit2, newdata = val_data, type = "response")
val_probs3 <- predict(fit3, newdata = val_data, type = "response")
val_probs4 <- predict(fit4, newdata = val_data, type = "response")

val_response1 <- val_data$Ipsilateral.Lateral.Lymph.Node.Metastasis
val_response2 <- val_data$II.Level.Lymph.Node.Metastasis
val_response3 <- val_data$III.Level.Lymph.Node.Metastasis
val_response4 <- val_data$IV.Level.Lymph.Node.Metastasis

# 计算不同阈值下的净收益
val_net_benefits1 <- sapply(thresholds, function(x) net_benefit(val_probs1, val_response1, x))
val_net_benefits2 <- sapply(thresholds, function(x) net_benefit(val_probs2, val_response2, x))
val_net_benefits3 <- sapply(thresholds, function(x) net_benefit(val_probs3, val_response3, x))
val_net_benefits4 <- sapply(thresholds, function(x) net_benefit(val_probs4, val_response4, x))

# 计算所有人都进行干预时的净收益
all_net_benefit_val <- sapply(thresholds, function(x) net_benefit(rep(1, length(val_response2)), val_response2, x))

# 绘制DCA曲线
dca_data_val <- data.frame(
  threshold = thresholds,
  val_net_benefit1 = val_net_benefits1,
  val_net_benefit2 = val_net_benefits2,
  val_net_benefit3 = val_net_benefits3,
  val_net_benefit4 = val_net_benefits4,
  all_net_benefit = all_net_benefit_val,
  none_net_benefit = none_net_benefit
)

dca_plot3 <- ggplot(dca_data_val, aes(x = threshold)) +
  geom_line(aes(y = val_net_benefit1, color = "Ipsilateral lateral Lymph Node Metastasis"), size = 0.6) +
  geom_line(aes(y = val_net_benefit2, color = "Level II Lymph Node Metastasis"), size = 0.6) +
  geom_line(aes(y = val_net_benefit3, color = "Level III Lymph Node Metastasis"), size = 0.6) +
  geom_line(aes(y = val_net_benefit4, color = "Level IV Lymph Node Metastasis"), size = 0.6) +
  geom_line(aes(y = all_net_benefit, color = "All"), linetype = "dotted", size = 0.6) +
  geom_line(aes(y = none_net_benefit, color = "None"), linetype = "solid", size = 0.6) +
  labs(title = "DCA for Lymph Node Metastasis Nomogram Prediction (Test Set)",
       x = "Threshold Probability", y = "Net Benefit") +
  scale_color_manual(values = c("Ipsilateral lateral Lymph Node Metastasis" = "orange", "Level II Lymph Node Metastasis" = "red", "Level III Lymph Node Metastasis" = "blue", "Level IV Lymph Node Metastasis" = "green", "All" = "grey", "None" = "black")) +
  theme_minimal() +
  theme(legend.position = "right") +
  coord_cartesian(ylim = c(-0.05, 0.45), xlim = c(0, 0.8))

# 保存图像函数
save_dca_plot3 <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/0.总曲线"

# 保存DCA曲线图
save_dca_plot3(dca_plot3, file.path(output_folder, "DCA_Lymph_Node_Metastasis_test_Set"))

print(dca_plot3)


```

```{r}
# 绘制所有线的DCA曲线
dca_plot4 <- ggplot() +
  geom_line(data = dca_data_train, aes(x = threshold, y = train_net_benefit1, color = "Ipsilateral lateral Lymph Node Metastasis (Train)"), size = 0.6) +
  geom_line(data = dca_data_test, aes(x = threshold, y = test_net_benefit1, color = "Ipsilateral lateral Lymph Node Metastasis (Test)"), linetype = "solid", size = 0.6) +
  geom_line(data = dca_data_val, aes(x = threshold, y = val_net_benefit1, color = "Ipsilateral lateral Lymph Node Metastasis (Validation)"), linetype = "solid", size = 0.6) +
  geom_line(data = dca_data_train, aes(x = threshold, y = train_net_benefit2, color = "Level II Lymph Node Metastasis (Train)"), size = 0.6) +
  geom_line(data = dca_data_test, aes(x = threshold, y = test_net_benefit2, color = "Level II Lymph Node Metastasis (Test)"), linetype = "solid", size = 0.6) +
  geom_line(data = dca_data_val, aes(x = threshold, y = val_net_benefit2, color = "Level II Lymph Node Metastasis (Validation)"), linetype = "solid", size = 0.6) +
  geom_line(data = dca_data_train, aes(x = threshold, y = train_net_benefit3, color = "Level III Lymph Node Metastasis (Train)"), size = 0.6) +
  geom_line(data = dca_data_test, aes(x = threshold, y = test_net_benefit3, color = "Level III Lymph Node Metastasis (Test)"), linetype = "solid", size = 0.6) +
  geom_line(data = dca_data_val, aes(x = threshold, y = val_net_benefit3, color = "Level III Lymph Node Metastasis (Validation)"), linetype = "solid", size = 0.6) +
  geom_line(data = dca_data_train, aes(x = threshold, y = train_net_benefit4, color = "Level IV Lymph Node Metastasis (Train)"), size = 0.6) +
  geom_line(data = dca_data_test, aes(x = threshold, y = test_net_benefit4, color = "Level IV Lymph Node Metastasis (Test)"), linetype = "solid", size = 0.6) + 
  geom_line(data = dca_data_val, aes(x = threshold, y = val_net_benefit4, color = "Level IV Lymph Node Metastasis (Validation)"), linetype = "solid", size = 0.6) +
  geom_line(data = dca_data_train, aes(x = threshold, y = all_net_benefit, color = "All (Train)"), linetype = "dashed", size = 0.6) +
  geom_line(data = dca_data_test, aes(x = threshold, y = all_net_benefit, color = "All (Test)"),
linetype = "dashed", size = 0.6) +
  geom_line(data = dca_data_val, aes(x = threshold, y = all_net_benefit, color = "All (Validation)"), linetype = "dashed", size = 0.6) +
  geom_line(data = dca_data_train, aes(x = threshold, y = none_net_benefit, color = "None"), linetype = "solid", size = 0.6) +
  labs(title = "DCA for Lymph Node Metastasis Nomogram Prediction (All Sets)",
       x = "Threshold Probability", y = "Net Benefit") +
  scale_color_manual(values = c(
     "Ipsilateral lateral Lymph Node Metastasis (Train)" = "goldenrod",
    "Ipsilateral lateral Lymph Node Metastasis (Test)" = "orange",
    "Ipsilateral lateral Lymph Node Metastasis (Validation)" = "gold",
    "Level II Lymph Node Metastasis (Train)" = "#C71585",
    "Level II Lymph Node Metastasis (Test)" = "red",
    "Level II Lymph Node Metastasis (Validation)" = "pink",
    "Level III Lymph Node Metastasis (Train)" = "darkblue", 
    "Level III Lymph Node Metastasis (Test)" = "blue", 
    "Level III Lymph Node Metastasis (Validation)" = "skyblue",
    "Level IV Lymph Node Metastasis (Train)" = "darkgreen",
    "Level IV Lymph Node Metastasis (Test)" = "green",
    "Level IV Lymph Node Metastasis (Validation)" = "lightgreen",
    "All (Train)" = "grey",
    "All (Test)" = "grey",
    "All (Validation)" = "grey",
    "None" = "black"
  )) +
  theme_minimal() +
  theme(legend.position = "right") +
  coord_cartesian(ylim = c(-0.05, 0.4), xlim = c(0, 0.8))
# 保存图像函数
save_dca_plot4 <- function(plot, filename_prefix) {
  # Save as TIFF at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.tiff"), plot, dpi = 300)
  # Save as TIFF at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.tiff"), plot, dpi = 1200)
  # Save as PNG at 300 DPI
  ggsave(paste0(filename_prefix, "_300dpi.png"), plot, dpi = 300)
  # Save as PNG at 1200 DPI
  ggsave(paste0(filename_prefix, "_1200dpi.png"), plot, dpi = 1200)
  # Save as EPS
  ggsave(paste0(filename_prefix, ".eps"), plot, device = "eps")
}

# 文件夹路径
output_folder <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/0.总曲线"

# 保存DCA曲线图
save_dca_plot4(dca_plot4, file.path(output_folder, "DCA_Lymph_Node_Metastasis_all_Set"))

print(dca_plot4)
```
#总的rOC曲线
```{r}
# 加载必要的库

library(dplyr)

# 读取数据
train_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值矫正后.csv")
test_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/2.验证集编码填补缺失值矫正后.csv")
# 按均值填补缺失值
fill_na_with_mean <- function(df) {
  df %>%
    mutate(across(everything(), ~ ifelse(is.na(.), mean(., na.rm = TRUE), .)))
}

train_data <- fill_na_with_mean(train_data)
test_data <- fill_na_with_mean(test_data)


# 将训练数据按照7:3的比例随机分为训练集和验证集
set.seed(123)
index <- 1:nrow(train_data)
shuffled_index <- sample(index)
tra_ratio <- 0.7  # 训练集比例
tra_size <- round(tra_ratio * nrow(train_data))
tra_data <- train_data[shuffled_index[1:tra_size], ]
val_data <- train_data[shuffled_index[(tra_size + 1):nrow(train_data)], ]

cat("训练集观测数量:", nrow(tra_data), "\n")
cat("验证集观测数量:", nrow(val_data), "\n")
cat("测试集观测数量:", nrow(test_data), "\n")
```


```{r}
# 侧区模型
fit1 <- glm(Ipsilateral.Lateral.Lymph.Node.Metastasis ~ Tumor.border + Aspect.ratio + Calcification + Tumor.internal.vascularization + Extrathyroidal.extension + Size + Location +Pretracheal.Lymph.Node.Metastasis+ Prelaryngeal.Lymph.Node.Metastasis+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis,
           data = tra_data, family = binomial())
train_probs1 <- predict(fit1, newdata = tra_data, type = "response")
val_probs1 <- predict(fit1, newdata = val_data, type = "response")
test_probs1 <- predict(fit1, newdata = test_data, type = "response")
train_response1 <- tra_data$Ipsilateral.Lateral.Lymph.Node.Metastasis
val_response1 <- val_data$Ipsilateral.Lateral.Lymph.Node.Metastasis
test_response1 <- test_data$Ipsilateral.Lateral.Lymph.Node.Metastasis
train_roc1 <- roc(train_response1, train_probs1)
val_roc1 <- roc(val_response1, val_probs1)
test_roc1 <- roc(test_response1, test_probs1)

# II区模型
fit2 <- glm(II.Level.Lymph.Node.Metastasis ~ Aspect.ratio + Calcification + Size + Location + Mulifocality + Ipsilateral.Central.Lymph.Node.Metastasis + Prelaryngeal.Lymph.Node.Metastases.Number,
           data = tra_data, family = binomial())
train_probs2 <- predict(fit2, newdata = tra_data, type = "response")
val_probs2 <- predict(fit2, newdata = val_data, type = "response")
test_probs2 <- predict(fit2, newdata = test_data, type = "response")
train_response2 <- tra_data$II.Level.Lymph.Node.Metastasis
val_response2 <- val_data$II.Level.Lymph.Node.Metastasis
test_response2 <- test_data$II.Level.Lymph.Node.Metastasis
train_roc2 <- roc(train_response2, train_probs2)
val_roc2 <- roc(val_response2, val_probs2)
test_roc2 <- roc(test_response2, test_probs2)

# III区模型
fit3 <- glm(III.Level.Lymph.Node.Metastasis ~ Age + Tumor.border + Calcification + Tumor.internal.vascularization + Extrathyroidal.extension + Size + Ipsilateral.Central.Lymph.Node.Metastasis + Pretracheal.Lymph.Node.Metastasis.Rate + Paratracheal.Lymph.Node.Metastasis.Rate + Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate,
           data = tra_data, family = binomial())
train_probs3 <- predict(fit3, newdata = tra_data, type = "response")
val_probs3 <- predict(fit3, newdata = val_data, type = "response")
test_probs3 <- predict(fit3, newdata = test_data, type = "response")
train_response3 <- tra_data$III.Level.Lymph.Node.Metastasis
val_response3 <- val_data$III.Level.Lymph.Node.Metastasis
test_response3 <- test_data$III.Level.Lymph.Node.Metastasis
train_roc3 <- roc(train_response3, train_probs3)
val_roc3 <- roc(val_response3, val_probs3)
test_roc3 <- roc(test_response3, test_probs3)

# IV区模型
fit4 <- glm(IV.Level.Lymph.Node.Metastasis ~Aspect.ratio+Calcification+Tumor.internal.vascularization+Size+Ipsilateral.Central.Lymph.Node.Metastasis+Paratracheal.Lymph.Node.Metastasis.Rate+Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate,
           data = tra_data, family = binomial())
train_probs4 <- predict(fit4, newdata = tra_data, type = "response")
val_probs4 <- predict(fit4, newdata = val_data, type = "response")
test_probs4 <- predict(fit4, newdata = test_data, type = "response")
train_response4 <- tra_data$IV.Level.Lymph.Node.Metastasis
val_response4 <- val_data$IV.Level.Lymph.Node.Metastasis
test_response4 <- test_data$IV.Level.Lymph.Node.Metastasis
train_roc4 <- roc(train_response4, train_probs4)
val_roc4 <- roc(val_response4, val_probs4)
test_roc4 <- roc(test_response4, test_probs4)

# 提取ROC曲线的坐标点
# 提取ROC曲线的坐标点
train_roc_data1 <- data.frame(coords(train_roc1, "all"))
train_roc_data2 <- data.frame(coords(train_roc2, "all"))
train_roc_data3 <- data.frame(coords(train_roc3, "all"))
train_roc_data4 <- data.frame(coords(train_roc4, "all"))

val_roc_data1 <- data.frame(coords(val_roc1, "all"))
val_roc_data2 <- data.frame(coords(val_roc2, "all"))
val_roc_data3 <- data.frame(coords(val_roc3, "all"))
val_roc_data4 <- data.frame(coords(val_roc4, "all"))
test_roc_data2 <- data.frame(coords(test_roc2, "all"))
test_roc_data1 <- data.frame(coords(test_roc1, "all"))


test_roc_data3 <- data.frame(coords(test_roc3, "all"))



test_roc_data4 <- data.frame(coords(test_roc4, "all"))
```




```{r}


# 加载包
library(pROC)
library(caret)
library(Metrics)

```

```{r}



# 定义函数来计算所有指标
compute_metrics <- function(response, probs, threshold = 0.5) {
  predicted <- ifelse(probs >= threshold, 1, 0)
  
  confusion <- confusionMatrix(factor(predicted), factor(response))
  
  accuracy <- confusion$overall['Accuracy']
  specificity <- confusion$byClass['Specificity']
  sensitivity <- confusion$byClass['Sensitivity']
  npv <- confusion$byClass['Neg Pred Value']
  ppv <- confusion$byClass['Pos Pred Value']
  f1 <- 2 * (ppv * sensitivity) / (ppv + sensitivity)
  auc <- roc(response, probs)$auc
  false_positive_rate <- 1 - specificity
  brier_score <- mean((probs - response)^2)
  kappa <- confusion$overall['Kappa']
  rmse_value <- rmse(response, probs)
  r2_value <- R2(response, probs)
  mae_value <- mae(response, probs)
  lift <- (sum(predicted) / length(predicted)) / (sum(response) / length(response))
  
  cat("Accuracy:", accuracy, "\n")
  cat("AUC:", auc, "\n")
  cat("Specificity:", specificity, "\n")
  cat("Sensitivity:", sensitivity, "\n")
  cat("NPV:", npv, "\n")
  cat("PPV:", ppv, "\n")
  cat("F1 Score:", f1, "\n")
  cat("False Positive Rate:", false_positive_rate, "\n")
  cat("Brier Score:", brier_score, "\n")
  cat("Kappa:", kappa, "\n")
  cat("RMSE:", rmse_value, "\n")
  cat("R2:", r2_value, "\n")
  cat("MAE:", mae_value, "\n")
  cat("Lift:", lift, "\n")
  
  return(c(accuracy, auc, specificity, sensitivity, npv, ppv, f1, false_positive_rate, lift, brier_score, kappa, rmse_value, r2_value, mae_value))
}

# 计算所有数据集上的指标
metrics_names <- c("Accuracy", "AUC", "Specificity", "Sensitivity/Recall", "Negative Predictive Value", 
                   "Positive Predictive Value/Precision", "F1 Score", "False Positive Rate", "Lift", 
                   "Brier Score", "Kappa", "RMSE", "R2", "MAE")

results <- data.frame(matrix(nrow = 12, ncol = 14))
colnames(results) <- metrics_names

# 训练集
results[1, ] <- compute_metrics(tra_data$Ipsilateral.Lateral.Lymph.Node.Metastasis, train_probs1)
results[2, ] <- compute_metrics(tra_data$II.Level.Lymph.Node.Metastasis, train_probs2)
results[3, ] <- compute_metrics(tra_data$III.Level.Lymph.Node.Metastasis, train_probs3)
results[4, ] <- compute_metrics(tra_data$IV.Level.Lymph.Node.Metastasis, train_probs4)

# 验证集
results[5, ] <- compute_metrics(val_data$Ipsilateral.Lateral.Lymph.Node.Metastasis, val_probs1)
results[6, ] <- compute_metrics(val_data$II.Level.Lymph.Node.Metastasis, val_probs2)
results[7, ] <- compute_metrics(val_data$III.Level.Lymph.Node.Metastasis, val_probs3)
results[8, ] <- compute_metrics(val_data$IV.Level.Lymph.Node.Metastasis, val_probs4)

# 测试集
results[9, ] <- compute_metrics(test_data$Ipsilateral.Lateral.Lymph.Node.Metastasis, test_probs1)
results[10, ] <- compute_metrics(test_data$II.Level.Lymph.Node.Metastasis, test_probs2)
results[11, ] <- compute_metrics(test_data$III.Level.Lymph.Node.Metastasis, test_probs3)
results[12, ] <- compute_metrics(test_data$IV.Level.Lymph.Node.Metastasis, test_probs4)

# 设置行名
row.names(results) <- c("同侧侧区_训练集", "II区_训练集", "III区_训练集", "IV区_训练集", 
                        "同侧侧区_验证集", "II区_验证集", "III区_验证集", "IV区_验证集", 
                        "同侧侧区_测试集", "II区_测试集", "III区_测试集", "IV区_测试集")

# 导出到CSV文件
write.csv(results, "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/0.评价指标2.csv", row.names = TRUE)


```


```{r}
# 加载必要的库
library(pROC)
library(ggplot2)
library(dplyr)

# 读取数据
train_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/1.总编码填补缺失值矫正后.csv")
test_data <- read.csv("/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/0.数据/2.验证集编码填补缺失值矫正后.csv")

# 将训练数据按照7:3的比例随机分为训练集和验证集
set.seed(123)
index <- 1:nrow(train_data)
shuffled_index <- sample(index)
tra_ratio <- 0.7  # 训练集比例
tra_size <- round(tra_ratio * nrow(train_data))
tra_data <- train_data[shuffled_index[1:tra_size], ]
val_data <- train_data[shuffled_index[(tra_size + 1):nrow(train_data)], ]

cat("训练集观测数量:", nrow(tra_data), "\n")
cat("验证集观测数量:", nrow(val_data), "\n")
cat("测试集观测数量:", nrow(test_data), "\n")

# 定义训练和评估函数
train_and_evaluate <- function(train_data, val_data, test_data, formula) {
  # 不同样本量进行训练
  sample_sizes <- seq(100, nrow(train_data), by = 100)
  results <- data.frame()
  
  for (size in sample_sizes) {
    subset_train_data <- train_data[1:size, ]
    
    # 训练模型
    model <- glm(formula, data = subset_train_data, family = binomial())
    
    # 预测概率
    train_probs <- predict(model, newdata = subset_train_data, type = "response")
    val_probs <- predict(model, newdata = val_data, type = "response")
    test_probs <- predict(model, newdata = test_data, type = "response")
    
    # 计算AUC
    train_roc <- roc(subset_train_data[[as.character(formula[[2]])]], train_probs)
    val_roc <- roc(val_data[[as.character(formula[[2]])]], val_probs)
    test_roc <- roc(test_data[[as.character(formula[[2]])]], test_probs)
    
    train_auc <- auc(train_roc)
    val_auc <- auc(val_roc)
    test_auc <- auc(test_roc)
    
    train_ci <- ci.auc(train_roc)
    val_ci <- ci.auc(val_roc)
    test_ci <- ci.auc(test_roc)
    
    # 将结果保存到数据框中
    results <- rbind(results, data.frame(
      Sample_Size = size,
      AUC = c(train_auc, val_auc, test_auc),
      CI_Lower = c(train_ci[1], val_ci[1], test_ci[1]),
      CI_Upper = c(train_ci[3], val_ci[3], test_ci[3]),
      Dataset = factor(c("Train", "Validation", "Test"), levels = c("Train", "Validation", "Test"))
    ))
  }
  
  return(results)
}

# 配置模型公式
formulas <- list(
  Ipsilateral.Lateral.Lymph.Node.Metastasis ~ Tumor.border + Aspect.ratio + Calcification + Tumor.internal.vascularization + Extrathyroidal.extension + Size + Location + Pretracheal.Lymph.Node.Metastasis + Prelaryngeal.Lymph.Node.Metastasis + Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis,
  II.Level.Lymph.Node.Metastasis ~ Aspect.ratio + Calcification + Size + Location + Mulifocality + Ipsilateral.Central.Lymph.Node.Metastasis + Prelaryngeal.Lymph.Node.Metastases.Number,
  III.Level.Lymph.Node.Metastasis ~ Age + Tumor.border + Calcification + Tumor.internal.vascularization + Extrathyroidal.extension + Size + Ipsilateral.Central.Lymph.Node.Metastasis + Pretracheal.Lymph.Node.Metastasis.Rate + Paratracheal.Lymph.Node.Metastasis.Rate + Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate,
  IV.Level.Lymph.Node.Metastasis ~ Aspect.ratio + Calcification + Tumor.internal.vascularization + Size + Ipsilateral.Central.Lymph.Node.Metastasis + Paratracheal.Lymph.Node.Metastasis.Rate + Recurrent.Laryngeal.Nerve.Lymph.Node.Metastasis.Rate
)

# 计算所有模型的AUC
results <- lapply(formulas, function(formula) {
  train_and_evaluate(tra_data, val_data, test_data, formula)
})

# 绘制学习曲线
plot_learning_curve <- function(data, title, save_path) {
  # 计算平均AUC值
  avg_aucs <- data %>%
    group_by(Dataset) %>%
    summarize(Avg_AUC = mean(AUC))
  
  # 创建新的标签
  new_labels <- setNames(paste(levels(data$Dataset), "(mean AUC =", round(avg_aucs$Avg_AUC, 3), ")"), levels(data$Dataset))
  
  p <- ggplot(data, aes(x = Sample_Size, y = AUC, color = Dataset, fill = Dataset)) +
    geom_line() +
    geom_point() +
    geom_ribbon(aes(ymin = CI_Lower, ymax = CI_Upper), alpha = 0.2) +
    labs(title = title, x = "Training Examples", y = "AUC Score") +
    theme_minimal() +
    theme(plot.title = element_text(hjust = 0.5)) +
    scale_color_manual(values = c("Train" = "red", "Validation" = "green", "Test" = "blue"), labels = new_labels, name = "Dataset") +
    scale_fill_manual(values = c("Train" = "pink", "Validation" = "lightgreen", "Test" = "skyblue"), labels = new_labels, name = "Dataset")
  
  # 在每个点标注AUC值
  p <- p + geom_text(aes(label = round(AUC, 3)), hjust = 1.5, vjust = -0.5, size = 2.5)
  
  # 保存图片
  ggsave(filename = paste0(save_path, title, ".tiff"), plot = p, dpi = 600, width = 10, height = 8)
  ggsave(filename = paste0(save_path, title, "_high_res.tiff"), plot = p, dpi = 1200, width = 10, height = 8)
}

# 保存图片
save_path <- "/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/1.R语言的结果/0.总曲线/"

plot_learning_curve(results[[1]], "Learning curve for Ipsilateral Lateral Lymph Node Metastasis:Nomogram Prediction", save_path)
plot_learning_curve(results[[2]], "Learning curve for Level II Lymph Node Metastasis:Nomogram Prediction", save_path)
plot_learning_curve(results[[3]], "Learning curve for Level III Lymph Node Metastasis:Nomogram Prediction", save_path)
plot_learning_curve(results[[4]], "Learning curve for Level IV Lymph Node Metastasis:Nomogram Prediction", save_path)

```
