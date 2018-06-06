# SlideShare2pdf

A Python Script to downloads 



## Requirements

- Pipenv 
- ImageMagick



## Installation

```
$ sudo apt update && sudo apt install -y imagemagick
$ git clone https://github.com/yukke42/SlideShare2pdf.git
$ cd SlideShare2pdf
$ pipenv install
```



## Help

- If you get erros like `cache resources exhausted `, you can resolve it by changing `/etc/ImageMagick-6/policy.xml`
  - https://github.com/ImageMagick/ImageMagick/issues/396