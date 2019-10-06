import petitions_dataset
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="petitions_dataset",
    version=petitions_dataset.__version__,
    author=petitions_dataset.__author__,
    author_email='soy.lovit@gmail.com',
    url='https://github.com/lovit/petitions_dataset',
    description="청와대 국민청원 데이터셋",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords = ['petitions', 'korean petitions'],
    packages=find_packages()
)
