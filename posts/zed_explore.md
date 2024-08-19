# zed 的使用体验

最近 zed 发布了 linux 的版本之后一直想尝试一下，开坑新项目的时候直接上手使用了两天，说一下感受吧，由于项目是 python，所以只说 python

登陆 GitHub 账户授权后可以同步配置，包括设置插件和主题，这属于基本功能了

内置了 GitHub Copilot，前面登陆账户后便可直接使用提示，与 vscode 代码提示部分体验无差，sublime text 这个功能是包装的 neovim 体验稍差，但也仅有这个功能，如果需要使用 copilot chat，需要单打开一个 vscode 当作聊天窗口使用

代码编辑体验，我的主力编辑器是 sublime text，官方比对 zed 快一些，但实际使用体验不到这么点渲染差距，但就论跟手程度，都比 vscode 要好，这也是我为什么长期只用 vscode 做一些边角料工作的原因，不够丝滑，在这一点 zed 和 sublime text 都很好

编辑器内置了 lsp，也就是写什么语言编辑器就会提示安装什么 lsp，python 是 pyright，根据提示安装好便可，同时扩展市场内有 ruff，安装后配置好便可有提示，这点体验与 sublime text 一样，功劳都是 lsp，有了这两个写 python 体验就已经很好了，但目前 zed 的 lsp 功能至少在 python 上面没有 goto definition，这一点非常影响体验，看到 issues 里面已经有很多提交，应该不久就会解决

扩展市场不够丰富，由于是新玩意，这一点跟进的不太足，大部分主流一点的扩展基本还好，但说一个小众需求，我需要一个快捷键选中当前括号内所有内容，编辑器没有内置这个快捷按钮，需要通过插件实现，sublime text 和 vscode 都有，还有主题我经常使用的 monokai pro 这种小众但还算主流的配色也还没有 zed 版本，只能等后续完善了

总的来说，这款编辑器的成熟程度已经无限逼近 sublime text，作为 sublime text 党已经感受到岌岌可危了，毕竟万物皆 rust 的加持下这款编辑器活跃程度只会暴涨，而 vscode 作为万能钥匙一样的存在，再加上 copilot 各种原生体验的加持，目前还不可能撼动
