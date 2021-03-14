Photolikes Telegram Bot
---

Tooling:
- Python 3.7
- [poetry](https://python-poetry.org/) for dependency management ([installation](https://python-poetry.org/docs/#installation))
- MongoDB as DBMS
- Docker and Docker Compose for containerized deployment 
- GitHub Actions for CI/CD
- [sentry](http://sentry.io/) for application monitoring and error tracking

Libraries and frameworks:
- tensorflow with Keras API for ML
- [scrapy](https://scrapy.org/) for data scraping
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for Telegram bot frontend implementation  

The repository uses [git flow](https://danielkummer.github.io/git-flow-cheatsheet/) branching model with supplemental scripts: 
- make new release from `develop` branch and bump the version:

    `scripts/release.py {major,minor,patch} <relase_message>`
   
### Software development process
![](https://camo.githubusercontent.com/2e840faa3b8588b30c4098e0545d8fb3a7751cf29242e46dc2873e6e07da5069/68747470733a2f2f63646e2e766f782d63646e2e636f6d2f7468756d626f722f32713937594358634c4f6c6b6f52326a4b4b454d512d776b47396b3d2f3078303a393030783530302f31323030783830302f66696c746572733a666f63616c28333738783137383a35323278333232292f63646e2e766f782d63646e2e636f6d2f75706c6f6164732f63686f7275735f696d6167652f696d6167652f34393439333939332f746869732d69732d66696e652e302e6a7067)
