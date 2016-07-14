from setuptools import setup

setup(
    name='kanjivg-2-animation',
    version='0.1',
    description=(
        "Convert kanjiVG's SVG files into animations that reveal the stroke "
        "order of different kanji. All animations are done in accordance to "
        "the SVG animation standard."
    ),
    license='CC BY-SA 3.0',
    scripts=[
        'kanjivg2animation.py',
    ],
    install_requires=[
        'svg.path',
    ],
    zip_safe=False,
)
