1. modify the keyowrds

```python
if __name__ == '__main__':
    # add keyword you want to search here
    keywords = ['python', 'react', 'deep learning']
    for keyword in keywords:
        print(crawl_topic(keyword))
```

2. `python main.py`

3. output will be

```python
[
    [
        {'title': book1_title, 'author': book1_author, 'price': book1_price}, # 天攏書局
        {'title': book1_title, 'author': book1_author, 'price': book1_price}, # 博客來書局
    ],
    [
        {'title': book2_title, 'author': book2_author, 'price': book2_price}, # 天攏書局
        {'title': book2_title, 'author': book2_author, 'price': book2_price}, # 博客來書局
    ],
    [
        {'title': book3_title, 'author': book3_author, 'price': book3_price}, # 天攏書局
        { None }, # not found in 博客來書局
    ],
    
    ...
    
]
```

