<a id="readme-top"></a>
<div align="center">
<h3 align="center">apodify</h3>

  <p align="center">
    Enhance APOD by adding extra properties for better organization and filtering.
    <br />
    <a href="#getting-started"><strong>Getting Started »</strong></a>
    <br />
    <a href="https://github.com/paulinek13/apodify/issues">Report Bug</a>
    ·
    <a href="https://github.com/paulinek13/apodify/issues">Request Feature</a>
  </p>
</div>

---

⚠️ **Please Note**: This project is currently in active development and has not yet reached its first full release. There are some features that are still in progress or not yet implemented, and the documentation may be missing information.

---

<br />

![GitHub](https://img.shields.io/github/license/paulinek13/apodify?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/paulinek13/apodify?style=for-the-badge)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/paulinek13/apodify?style=for-the-badge)
![GitHub all releases](https://img.shields.io/github/downloads/paulinek13/apodify/total?style=for-the-badge)

![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![.ENV Badge](https://img.shields.io/badge/.ENV-ECD53F?logo=dotenv&logoColor=000&style=for-the-badge)
![YAML Badge](https://img.shields.io/badge/YAML-CB171E?logo=yaml&logoColor=fff&style=for-the-badge)

<br />

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-apodify">About `apodify`</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#features">Features</a></li>
  </ol>
</details>

<br />

## About `apodify`

The goal of this project is to **enhance APODs** (Astronomy Picture of the Day), with a primary focus on tailoring these enhancements specifically for the needs of [neso](https://github.com/paulinek13/neso). This includes features such as adding more detailed information to APOD entries and implementing advanced functionality like color-based searching and filtering. The project has recently shifted direction to prioritize integration and customization for [neso](https://github.com/paulinek13/neso), ensuring that all new features align closely with its specific requirements.

[Here](/docs/README.md) you can read the documentation and find more detailed information about the project.

<p align="right"><a href="#readme-top">ᴛᴏᴘ⇈</a></p>

## Getting Started

### Prerequisites

- **Python** (>=3.12) - [python.org/downloads](https://www.python.org/downloads/)
- **pip** - [pip.pypa.io/en/stable/installation](https://pip.pypa.io/en/stable/installation/)
- **NASA API Key** (optional) - [api.nasa.gov](https://api.nasa.gov/)

While not mandatory, having a NASA API key allows for increased usage limits. The project's functionality remains the same, but with an API key, you can make more requests to the APOD API and thus use this tool more effectively.

### Installation

1. Clone the repo

    ```sh
    git clone https://github.com/paulinek13/apodify.git
    ```
2. Change directory
    ```sh
    cd apodify
    ```
3. Create virtual environment using `venv`
    ```sh
    py -m venv env
    ```
4. Activate your virtual environment
    ```sh
    call env\Scripts\activate
    ```
5. Install all the dependencies
    ```sh
    pip install -r requirements.txt
    ```
6. Rename `.env.example` to `.env`
7. Optionally change `DEMO_KEY` to your NASA API key
8. Change the config file `config.yml` to your preferences and needs
9. Run the program
    ```sh
    py main.py
    ```

<p align="right"><a href="#readme-top">ᴛᴏᴘ⇈</a></p>

## Acknowledgments

- Thanks to NASA for providing [APOD API](https://github.com/nasa/apod-api)
- Special thanks to the open-source community for valuable libraries and tools used in this project:
  - **colorama** ([GitHub](https://github.com/tartley/colorama), [PyPI](https://pypi.org/project/colorama/)), **extcolors** ([GitHub](https://github.com/CairX/extract-colors-py), [PyPI](https://pypi.org/project/extcolors/)), **Pillow** ([GitHub](https://github.com/python-pillow/Pillow), [PyPI](https://pypi.org/project/Pillow/)), **python-dotenv** ([GitHub](https://github.com/theskumar/python-dotenv), [PyPI](https://pypi.org/project/python-dotenv/)), **PyYAML** ([GitHub](https://github.com/yaml/pyyaml), [PyPI](https://pypi.org/project/PyYAML/)), **requests** ([GitHub](https://github.com/psf/requests), [PyPI](https://pypi.org/project/requests/)), **urllib3** ([GitHub](https://github.com/urllib3/urllib3), [PyPI](https://pypi.org/project/urllib3/)), _and more ..._
  - _For a comprehensive list of project dependencies, please refer to the `requirements.txt` file._

<p align="right"><a href="#readme-top">ᴛᴏᴘ⇈</a></p>

## Features

- Extract color palettes from APOD images.
- Create a list of filterable colors for easy reference.

<p align="right"><a href="#readme-top">ᴛᴏᴘ⇈</a></p>

---

![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/m/paulinek13/apodify/master?style=for-the-badge)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/paulinek13/apodify?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/paulinek13/apodify?style=for-the-badge)
