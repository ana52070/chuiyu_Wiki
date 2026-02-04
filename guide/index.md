# 学习笔记 📚
这里是我的日常学习碎片。


# Markdown撰写笔记

## 标注框

格式：
```bash
> [!info] 
> > 这是一个标注框 
> > > 它支持 **Markdown 语法**、 [[内部链接|Wikilinks]] 和 [[嵌入文件|embeds]]。
```
![[20260204114532.png]]

```bash
> [!tip] 小技巧 
> > 这个小技巧的标题不是默认的 “Tip”
```
![[20260204114539.png]]


```
> [!question] 标注框可以被嵌套吗？ 
> > > [!success] 当然 
> > > > > > [!example] 第三层嵌套
```
![[20260204114547.png]]


在 `> [!标注]` 后，添加一个加号（`+`）或减号（`-`） 就可以将其设置为折叠标注框，加号是默认展开，减号是默认折叠。

标注类型	别名
Note	
Abstract	summary, tldr
Info	
Todo	
Tip	hint, important
Success	check, done
Question	help, faq
Warning	caution, attention
Failure	fail, missing
Danger	error
Bug	
Example	
Quote	cite