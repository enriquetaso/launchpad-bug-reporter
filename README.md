# Launchpad Bug Report 

:tea: This is a simple script that generates a list of bugs from today minus 7 days. However, you can easily change this. 

## Sample

```
(.env)$ python main.py 
cinder
---
- Bug #1971483
 Date 2022-05-03 19:33:33.877298+00:00
 Link https://bugs.launchpad.net/cinder/+bug/1971483

os-brick
---
No bugs from 2022-04-30 to 2022-05-10

cinderlib
---
No bugs from 2022-04-30 to 2022-05-10

cinder-tempest-plugin
---
No bugs from 2022-04-30 to 2022-05-10
```


## Getting Started

### Installation
```
python3 -m venv myenv
pip install -r requirements.txt
python main.py
```

### Usage
The Launchpad client requires UTC time. So if you want to generate a report from a different date, you can do so like this:

```
utc_start_date = datetime(2022, 4, 27).astimezone(tz.UTC)
```

## Contributing
Contributions are what make the open source community such a great place for learning, inspiration and creativity. Any contribution you make is greatly appreciated.

## Acknowledgments
- I found the following articles very interesting, maybe they are interesting for you too. [Stop using utcnow and utcfromtimestamp](https://blog.ganssle.io/articles/2019/11/utcnow.html) 

- I would like to thank Schwuk. [Simple script to slurp bugs from a Launchpad project into Pivotal Tracker stories.](https://gist.github.com/schwuk/517279/a26dcbb59fb151e3ef00d84f2977a6c2355363d2)

- [Launchpad Api Doc](https://launchpad.net/+apidoc/1.0.html)
