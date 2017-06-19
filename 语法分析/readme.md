### 	text1的分析结果所生成的抽象语法树使用python中的第三方库pygrapgviz绘制成了.jpg格式的图，详见Threadx(x=1,2,3,4,5,6).jpg，text3的报错在test3_syntaxOut.txt中显示
### 	本程序使用python2.7编写，SyntaxExcute.py为语法分析主程序，LexicalAnalysis.py与LexicalExcute.py为生成输入的词法分析程序，运行的话请安装python2.7环境以及第三方库pygraphviz



对文法进行了相应的变形和改写，改写的结果如下：

Thread --> **thread ** **identifier** \[**features** feature\] \[ **flows **flow_spec \] \[**properties** association**; **\] **end ** **identifier**  **;**

feature--> **none** **; **

feature-->  **identifier ** **:** IOtype port_spec|Parameter

port_spec --> port_type [ **{** { association } **}**] **;**

port_type -->**data port** [ reference ] | **event data port**[ reference ]| **event port**

Parameter --> **parameter** \[reference \][ **{** { association } **}** ] **;**

IOtype--> **in** | **out** | **in out** 

flow_spec --> **identifier ** **:** **flow **flow_source_spec| flow_sink_spec| flow_path_spec| **none** **;**

flow_source_spec --> **source** **identifier**[ **{** { association } **}** ] **;**

flow_sink_spec --> **sink** **identifier**[ **{ **{ association } **}**] **;**

flow_path_spec --> **path** **identifier** **-> ** **identifier** **;**

association -->[ **identifier** **::** ] **identifier** splitter [ **constant**] **access** **decimal** |**none**

splitter--> **=>** | **+=>** 

reference --> { **identifier ::** }  **identifier** (**id :: id ::id :: ………..**)

相应的抽象语法树如下：

![Thread](.\SyntaxTree\Thread.png)

![association](.\SyntaxTree\association.png)

![feature](.\SyntaxTree\feature.png)

![flow_path_spec](.\SyntaxTree\flow_path_spec.png)

![flow_sink_spec](.\SyntaxTree\flow_sink_spec.png)

![flow_source_spec](.\SyntaxTree\flow_source_spec.png)

![flow_spec](.\SyntaxTree\flow_spec.png)

![IOtype](.\SyntaxTree\IOtype.png)

![flow_path_spec](.\SyntaxTree\flow_path_spec.png)

![Parameter](.\SyntaxTree\Parameter.png)

![port_spec](.\SyntaxTree\port_spec.png)

![port_type](.\SyntaxTree\port_type.png)

![reference](.\SyntaxTree\reference.png)

![splitter](.\SyntaxTree\splitter.png)

