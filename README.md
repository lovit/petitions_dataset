# 청와대 국민청원 데이터셋

청와대 국민청원 게시판으로부터 수집된 데이터를 사용하기 편한 API 의 형태로 제공합니다. 

[청와대 국민청원 스크래퍼][scraper]로부터 매 월 청원 완료된 데이터를 정리하여 업데이트 합니다. 수집된 데이터는 [data archive][archive] 에 저장되어 있습니다.

## Install

설치는 git clone 으로 할 수 있습니다.

```
git clone https://github.com/lovit/petition_dataset.git
```

## Fetch

설치된 패키지는 데이터를 가지고 있지 않습니다. `fetch` 를 이용하여 데이터를 다운로드 받습니다.

```python
from petitions_dataset import fetch

fetch()
```

## Usage

다운로드 받은 데이터 폴더 위치를 `data_dir` 에 입력할 수 있습니다.

```python
from petitions_dataset import Petitions

petitions = Petitions()
petitions = Petitions(data_dir='./tmp')
```

Iteration 시 yield 되는 항목을 설정할 수 있습니다. 설정 가능한 항목은 아래와 같습니다.

```
['category', 'begin', 'end', 'content', 'num_agree', 'petition_idx', 'status', 'title', 'replies']
```

```python
petitions.set_keys('category', 'title')

for petition in petitions:
    # do something
```


[scraper]: https://github.com/lovit/petitions_scraper
[archive]: https://github.com/lovit/petitions_dataset_