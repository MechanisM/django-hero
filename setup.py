from setuptools import setup, find_packages

setup(
    name = "django-hero",
    version = "0.1",
    author = "Sjoerd Arendsen",
    author_email = "s.arendsen@hub.nl",
    description = "Achievements app for Django",
    long_description = open("README.md").read(),
    license = "BSD",
    url = "http://github.com/hub-nl/django-hero",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
