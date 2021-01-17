# hentaiTagger4calibre
A tag converter for calibre

---

### Introduction

This simple python3 app can convert metadata in archive zip file downloaded from e-hentai or exhentai to a format that calibre can recognize. 

### Requirements

- A windows machine
- Simple make some modifications in `2_compress.cmd` and you can make your own linux version xD.
- A plugin called [Embeded Comic metadata](https://github.com/dickloraine/EmbedComicMetadata) should be installed on calibre.

```bash
sudo apt install python p7zip # choco install python 7zip
pip install pycountry 
```



### Usage

- Download a zip archive from one of two hentai websites
- Use [this script](https://raw.githubusercontent.com/dnsev-h/x/master/builds/x-gallery-metadata.user.js) to get metadata in a form of info.json (from https://dnsev-h.github.io/x/), and add it into the zip file.
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
- Run `python 1_info.py`, `2_compress.cmd`, `python 3_zipNote.py` in order.

The final cbz files should appear in `out/` subfolder.
