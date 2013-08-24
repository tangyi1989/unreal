# *_* coding=utf8 *_*

"""
描述：Unreal Proxy 安装脚本。
作者：Tang Wanwan
"""

import setuptools

setuptools.setup(
    requirements = ["eventlet, tornado"],
    name="unreal",
    version="2013.8",
    author="Tang",
    description="Tang Wanwan's Unreal proxy for bad things.",
    packages=setuptools.find_packages(exclude=['tests', 'bin']),
    scripts=['bin/unreal-server'],
)
