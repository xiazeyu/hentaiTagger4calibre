# hentaiTagger4calibre
A tag converter for calibre

---


### 注意

我为了提示阅读体验，已经迁移到了 [LANraragi](https://github.com/Difegue/LANraragi). 因此这个repo将不那么频繁地进行维护。

LANraragi的优点:

- Calibre-web 在线阅读时需要 **加载整个cbz文件**, LANraragi 支持 **服务端解压加载，传输单张图片给浏览器**.
- 支持**直接输入 e-hentai 网址** 下载本子, 支持 **自动从 e-hentai 和 n-hentai 下载标签标题信息**.
- 更好的**标签管理**, 尤其适合本子 **有许多标签** 的情形, calibre-web里存在太多标签会使得标签系统失去作用.
- **不更改文件的hash值**, 因此下载的问价你可以直接从 e-hentai 服务器溯源，或是作为种子文件再次上传.

这个脚本的优点:

- 支持嵌入 **eze 的 info.json**, 意味着不想LANraragi将信息单独存放在它自己的数据库中， **所有的** 元信息 **都和本子在一起**.
- 支持检查画廊更新，有时候有些画廊会，每周更新，这个脚本可以方便地将其捞出来.
- **精准地导入元数据**, 当多个汉化组同时汉化一本本子时，LANraragi自带的搜刮器可能会下错翻译组的信息.
- **兼容** 包括 calibre and LANraragi 在内的所有阅读方案.


### Notice

I have migrated to [LANraragi](https://github.com/Difegue/LANraragi) due to its better web reading experience. So this repo is maintained in a less frequent status.

Advantages in LANraragi:

- Calibre-web requires **loading of the whole cbz file**, and LANraragi supports decompress cbz file **at server-side**.
- Support direct download **by inputing the e-hentai url**, and support **automatically scrub the meta info from e-hentai and n-hentai**.
- Better **tag management**, especially designed for commic files with **lots of tags**, in calibre-web, too much tag makes the whole tag system unavailable to use.
- **Not modify the hash of the archive**, means that using that hash, the archive can be found more easily on e-hentai server, or be uploaded as a bittorrent file.

Advantages of this script:

- support embedding **eze info.json**, which means **all** meta infos are **with the cbz file**, not like LANraragi, meta infomation are stored in its seperated database.
- support checking for update. Sometimes some galley will have new images uploaded, this script can help find these out-dated archives.
- **More precise while importing meta**, when importing with LANraragi, some meta may be downloaded from the wrong galley, may caused by multiple translation group are translating the same galley.
- **compatible** with all solutions like calibre and LANraragi

### Introduction

This simple python3 app can convert metadata in archive zip file downloaded from e-hentai or exhentai to a format that calibre can recognize.

### Requirements

- A windows machine, linux not tested
- A plugin called [Embeded Comic metadata](https://github.com/dickloraine/EmbedComicMetadata) should be installed on calibre.

```bash
sudo apt install python p7zip-full # on windows: choco install python 7zip
pip -r requirements.txt
```

### Usage

- Download a zip archive from one of two hentai websites
- Use [this script](https://raw.githubusercontent.com/dnsev-h/x/master/builds/x-gallery-metadata.user.js) to get metadata in a form of info.json (from https://dnsev-h.github.io/x/), and add it into the zip file.
- Delete all intermediate and final outputs like `inf.json`, `ser.json`, `out/`
- Uncompress the zip file, move the output folder into `work/` subfolder.

Work folder should look like this:

```
│  1_info.py
│  2_compress.cmd
│  3_zipNote.py
│
└─work
    ├─commic1
    │      1.png
    │      2.png
    │      info.json
    │
    └─commic2
            1.png
            2.png
            info.json
```

- Make sure all the requirements are satisfied.
- Run `python main.py` in order.

The final cbz files should appear in `out/` subfolder.



### Checker

Specify your cbz path in `checker_custom_path.py`, and run it. It will help you check if your books are up-to-date.

~~The `checker.py` can check whether books recorded in `inf.json` are all visible now. It is useful to use this script to track some ongoing comics since they will be replaced and become invisible. ~~
