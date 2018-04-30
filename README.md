# Extract Keyword

## Running Locally
Make sure you have Python [installed properly](http://install.python-guide.org). 

```sh
$ git clone https://github.com/henrywang1/django_extract_keyword.git
$ cd final-cw

$ pipenv install
$ python manage.py migrate
$ python manage.py collectstatic
$ python manage.py run server
```

## 批次處理文章
```sh
$ python batch_process.py

```
### 輸入
- 檔案名稱: input.csv
- 需求欄位: title, content

### 輸出
- 檔案名稱: output.csv
- 增加欄位: predict_tags


## 功能說明
1. 關鍵字擷取
2. 查詢 Google Trend 列出相關字及趨勢
3. 提供方便使用的網站及後台，
4. 使用者可自訂關鍵字及停用字
5. 標題產生的功能，因為還在實驗階段，暫時移除


